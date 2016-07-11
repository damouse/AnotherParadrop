###################################################################
# Copyright 2013-2014 All Rights Reserved
# Authors: The Paradrop Team
###################################################################

import os

from paradrop.shared import settings
from paradrop.shared import pdos
from paradrop.shared.output import out


def getSystemConfigDir():
    base = settings.UCI_CONFIG_DIR
    pdos.makedirs_quiet(base)
    return base


def getSystemPath(filename):
    """
    Get the path to the system configuration file.

    This function also attempts to create the configuration directory if it
    does not exist.

    Typical filenames: network, wireless, qos, firewall, dhcp, etc.
    """
    base = getSystemConfigDir()
    return os.path.join(base, filename)


def stringify(a):
    b = {}
    #print("%s\n" % a)
    if (type(a) == str):
        return a
    for k, v in a.iteritems():
        if type(v) is dict:
            b[k] = stringify(v)
        elif type(v) is list:
            b[k] = [stringify(v1) for v1 in v]
        else:
            b[k] = str(v)
    return b


def getLineParts(line):
    """
    Split the UCI line into its whitespace-separated parts.

    Returns a list of strings, with apostrophes removed.
    """
    parts = line.split(" ")
    # Attempt to remove single quotes from the value if it exists
    #print("l: %s" % l)

    if len(parts) < 3:
        return parts

    if parts[1].startswith("'") and parts[1].endswidth("'"):
        parts[1] = parts[1][1:-1]

    try:
        if (parts[2].startswith("'") and not parts[2].endswith("'")):
            # strip off first quotation
            parts[2] = parts[2][1:]
            addStr = parts[2]

            i = 3

            # Iterate over the rest of the words until we find a second quotation
            while True:
                if (parts[i].endswith("'")):
                    addStr = "%s %s" % (addStr, parts[i][:-1])

                    a = [parts[0], parts[1]]
                    a.append(addStr)
                    if (len(parts) > i + 1):
                        a.extend(parts[i + 1:])
                    break
                else:
                    addStr = "%s %s" % (addStr, parts[i])
                i += 1

            parts = a
        else:
            parts[2] = parts[2].replace("'", "")
            parts[2] = parts[2].replace('"', '')
    except:
        pass

    return parts


def chuteConfigsMatch(chutePre, chutePost):
    """ Takes two lists of objects, and returns whether or not they are identical."""
    # TODO - currently using a naive implementation by searching over the old configs and the new configs.
    # Could improve if slow by keep track of matched configs on both sides, deleting from search space
    # If any objects remain at the end
    # loop through all old configs, check if they each have a match in the new configs
    for c1 in chutePre:

        for c2 in chutePost:
            if (singleConfigMatches(c1, c2)):
                break
        else:
            # We got through the loop without finding a match, so return false
            return False

    for c2 in chutePost:
        for c1 in chutePre:
            if (singleConfigMatches(c1, c2)):
                break
        else:
            return False

    return True


def isMatch(a, b):
    a = stringify(a)
    b = stringify(b)
    return (a == b)


def isMatchIgnoreComments(a, b):
    import copy
    a1 = copy.deepcopy(a)
    b1 = copy.deepcopy(b)

    a1.pop('comment', None)
    b1.pop('comment', None)
    a1 = stringify(a1)
    b1 = stringify(b1)
    return (a1 == b1)


def singleConfigMatches(a, b):
    (c1, o1) = a
    (c2, o2) = b
    return isMatch(c1, c2) and isMatch(o1, o2)


class UCIConfig:
    """
        Wrapper around the UCI configuration files.
            These files are found under /etc/config/*, and are used by OpenWrt to keep track of
            configuration for modules typically found in /etc/init.d/*

            The modules of interest and with current support are:
                - firewall
                - network
                - wireless
                - qos

            * This class should work with any UCI module but ALL others are UNTESTED!

        New configuration settings can be added to the UCI file via addConfig().

        Each UCI config file is expected to contain the following syntax:

            config keyA [valueA]
                option key1 value1
                ...
                list key2 value1
                list key2 value2
                ...
                list key3 value1
                list key3 value2

        Based on the UCI file above, the config syntax would look like the following:
            config is a list of tuples, containing 2 dict objects in each tuple:

                - tuple[0] describes the first line (config keyA [valueA])
                    {'type': keyA, 'name': valueA}
                    The value parameter is optional and if missing, then the 'name' key is also missing (rather than set to None).

                - tuple[1] describes the options associated with the settings (both 'option' and 'list' lines)
                    {'key1': 'value1', ...}

                    If a list is present, it looks like the following:
                        {
                            ..., 
                            'list': {
                                'key2': [value1, value2, ...],
                                'key3': [value1, value2, ...]
                                }
                        }

                So for the example above, the full config definition would look like:
                    C = {'type': 'keyA', 'name': 'valueA'}
                    O = {'key1': 'value1', 'list': {'key2': ['value1', 'value2'], 'key3': ['value1', 'value2']}}
                    config = [(C, O)]
    """

    def __init__(self, filepath):
        self.filepath = filepath
        self.myname = os.path.basename(self.filepath)
        if (not os.path.isfile(self.filepath)):
            open(self.filepath, 'a').close()

        self.config = self.readConfig()

    def __eq__(self, o):
        if(self.filepath != o.filepath):
            return False
        if(self.myname != o.myname):
            return False

        # before parsing through each one, do simple check to make sure the number of configs is the same
        if(len(self.config) != len(o.config)):
            return False

        # Parse through config finding any differences
        oc = o.config
        for cfg in self.config:
            c, o = cfg
            # This is stupid slow, but easy, just look through all values for a match
            for cfg1 in oc:
                c1, o1 = cfg1
                if(c1 == c and o1 == o):
                    break
            else:
                # Found no match so we return None
                return False

        return True

    def __ne__(self, o):
        """Override the not equals operator between 2 Config objects
            This is required because the config attribute contains a list of tuples which Python doesn't
            seem to like to do comparisons directly on, for instance cfg1.config != cfg2.config fails to 
            say they are the same even though they are."""
        if(self.filepath != o.filepath):
            return True
        if(self.myname != o.myname):
            return True

        # before parsing through each one, do simple check to make sure the number of configs is the same
        if(len(self.config) != len(o.config)):
            return True

        # Parse through config finding any differences
        oc = o.config
        for cfg in self.config:
            c, o = cfg
            # This is stupid slow, but easy, just look through all values for a match
            for cfg1 in oc:
                c1, o1 = cfg1
                if(c1 == c and o1 == o):
                    break
            else:
                # Found no match so we return None
                return True

        return False

    def getConfig(self, config):
        """ Returns a list of call configs with the given title """
        matches = []
        # Search through the config array for matches
        config = stringify(config)
        for e in self.config:
            c, o = e
            if(c == config):
                matches.append((c, o))

        return matches

    def getConfigIgnoreComments(self, config):
        """ Returns a list of call configs with the given title.
            Comments are ignored.
         """
        matches = []
        # Search through the config array for matches
        for e in self.config:
            c, o = e
            if(isMatchIgnoreComments(c, config)):
                matches.append((c, o))

        return matches

    def existsConfig(self, config, options):
        """Tests if the (config, options) is in the current config file."""
        # Search through the config array for matches
        config = stringify(config)
        options = stringify(options)
        for e in self.config:
            c, o = e
            if(c == config and o == options):
                return True
        return False

    def addConfigs(self, configs):
        """ Adds a list of tuples to our config """
        for e in configs:
            c, o = e
            self.addConfig(c, o)

    def delConfigs(self, configs):
        """ Adds a list of tuples to our config """
        for e in configs:
            c, o = e
            self.delConfig(c, o)

    def addConfig(self, config, options):
        """Adds the tuple to our config."""
        if (not self.existsConfig(config, options)):
            self.config.append((config, options))

    def delConfig(self, config, options):
        """Finds a match to the config input and removes it from the internal config data structure."""
        config = stringify(config)
        options = stringify(options)

        # Search through the config array for matches
        for i, e in enumerate(self.config):
            c, o = e
            if(c == config and o == options):
                break
        else:
            # Getting here means we didn't break so no match
            log.verbose('No match to delete, config: %r\n' % (config))
            return

        del(self.config[i])

    def backup(self, backupToken):
        """
            Puts a backup of this config to the location specified in @backupPath.
        """
        backupPath = '/tmp/%s-%s' % (self.myname, backupToken)
        pdos.copy(self.filepath, backupPath)

    def restore(self, backupToken, saveBackup=True):
        """
            Replaces real file (at /etc/config/*) with backup copy from /tmp/*-@backupToken location.

            Arguments:
                backupToken: The backup token appended at the end of the backup path
                saveBackup : A flag to keep a backup copy or delete it (default is keep backup)
        """
        # Make sure it exists!
        backupPath = '/tmp/%s-%s' % (self.myname, backupToken)
        if(pdos.exists(backupPath)):
            if(saveBackup):
                pdos.copy(backupPath, self.filepath)
            else:
                pdos.move(backupPath, self.filepath)
        else:
            # This might be ok if they didn't actually make any changes
            log.warn('Cannot restore, %s missing backup (might be OK if no changes made)\n' % (self.myname))

    def getChuteConfigs(self, internalid):
        chuteConfigs = []
        for e in self.config:
            c, o = e
            if (c.get('comment', '') == internalid):
                chuteConfigs.append((c, o))
        return chuteConfigs

    def save(self, backupToken=None, internalid=None):
        """
            Saves out the file in the proper format.

            Arguments:
                [backupPath] : Save a backup copy of the UCI file to the path provided.
                                Should be a token name like 'backup', it gets appended with a hyphen.
        """
        # Save original copy
        if(backupToken):
            self.backup(backupToken)

        output = ""
        # Now generate what the file would look like
        for c, o in self.config:
            #print("c: %s\n" % c.keys())
            line = "config %s" % c['type']
            # Check for optional name
            if('name' in c.keys()):
                line += " %s" % c['name']
            if('comment' in c.keys()):
                line += " #%s" % c['comment']
            output += "%s\n" % line

            # Get options
            # check for lists first, if they exist remove them first
            if('list' in o.keys()):
                theLists = o['list']
            else:
                theLists = None

            # Now process everything else quick
            for k, v in o.iteritems():
                # Make sure we skip the lists key
                if(k != 'list'):
                    line = "\toption %s '%s'\n" % (k, v)
                    output += line

            # Now process the list
            if(theLists):
                # theLists is a dict where the key is each list name
                # and the value is a list of the options we need to include
                for k, v in theLists.iteritems():
                    # so @v here is a list
                    for vals in v:
                        # Now append a list set to the config
                        line = "\tlist %s '%s'\n" % (k, vals)
                        output += line

            # Now add one extra newline before the next set
            output += "\n"

        # Now write to disk
        try:
            log.info('Saving %s to disk\n' % (self.filepath))
            fd = pdos.open(self.filepath, 'w')
            fd.write(output)

            # Guarantee that its written to disk before we close
            fd.flush()
            os.fsync(fd.fileno())
            fd.close()
        except Exception as e:
            log.err('Unable to save new config %s, %s\n' % (self.filepath, str(e)))
            log.err('Config may be corrupted, backup exists at /tmp/%s\n' % (self.myname))

    def readConfig(self):
        """Reads in the config file."""
        def correctStr(line):
            return " ".join(line.split())

        lines = []
        try:

            fd = pdos.open(self.filepath, 'r')

            while(True):
                line = fd.readline()
                if(not line):
                    break
                lines.append(line)
            fd.close()
        except Exception as e:
            log.err('Error reading file %s: %s\n' % (self.filepath, str(e)))
            raise e

        cfg = None
        opt = None
        data = []

        # Now we have the data, deal with it
        for line in lines:
            line = line.rstrip()
            # If comment ignore
            if(line.startswith('#')):
                continue

            # First make all lines have correct whitespace
            # FIXME: if there is a space WITHIN quotes this kills it!
            # this could come up as a key in an encryption key
            line = correctStr(line)
            l = getLineParts(line)

            #
            # Config
            #
            #print("l: %s" % l)
            if(l[0] == 'config'):
                # Save last config we had
                if(cfg and opt):
                    data.append((cfg, opt))

                # start a new config
                cfg = {'type': l[1]}

                # Third element can be comment or name
                if(len(l) == 3):
                    if (l[2].startswith('#')):
                        cfg['comment'] = l[2][1:]
                    else:
                        cfg['name'] = l[2]
                elif (len(l) == 4):
                    # Four elements, so third is name and 4th is comment
                    cfg['name'] = l[2]
                    cfg['comment'] = l[3][1:]
                opt = {}

            #
            # Options
            #
            elif(l[0] == 'option'):
                opt[l[1]] = l[2]

            #
            # List
            #
            elif(l[0] == 'list'):
                # Make sure there is a list key
                if('list' not in opt.keys()):
                    opt['list'] = {}
                if(l[1] in opt['list'].keys()):
                    opt['list'][l[1]].append(l[2])
                else:
                    opt['list'][l[1]] = [l[2]]
        else:
            # Also at the end of the loop, save the final config we were making
            # Make sure cfg,opt aren't None
            if(None not in (cfg, opt)):
                data.append((cfg, opt))
        return data
