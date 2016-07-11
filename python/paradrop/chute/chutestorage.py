###################################################################
# Copyright 2013-2014 All Rights Reserved
# Authors: The Paradrop Team
###################################################################

import sys
import copy
import pickle

from paradrop.shared.output import out
from paradrop.shared import pdos
from paradrop.shared import settings


class PDStorage(object):

    """
        ParaDropStorage class.

        This class is designed to be implemented by other classes.
        Its purpose is to make whatever data is considered important persistant to disk.

        This is done by providing a reactor so a "LoopingCall" can be utilized to save to disk.

        The implementer can override functions in order to implement this class:
            getAttr() : Get the attr we need to save to disk
            setAttr() : Set the attr we got from disk
            importAttr(): Takes a payload and returns the properly formatted data
            exportAttr(): Takes the data and returns a payload
            attrSaveable(): Returns True if we should save this attr
    """

    def __init__(self, filename, reactor, saveTimer):
        self.filename = filename
        self.reactor = reactor
        self.saveTimer = saveTimer

        # Setup looping call to keep chute list perisistant only if reactor present
        if(self.reactor):
            self.repeater = self.reactor.LoopingCall(self.saveToDisk)
            self.repeater.start(self.saveTimer)

    def loadFromDisk(self):
        """Attempts to load the data from disk.
            Returns True if success, False otherwise."""

        if(pdos.exists(self.filename)):
            deleteFile = False
            log.info('Loading from disk\n')
            data = ""
            try:
                pyld = pickle.load(pdos.open(self.filename, 'rb'))
                self.setAttr(self.importAttr(pyld))
                return True
            except Exception as e:
                log.err('Error loading from disk: %s\n' % (str(e)))
                deleteFile = True

            # Delete the file
            if(deleteFile):
                try:
                    pdos.unlink(self.filename)
                except Exception as e:
                    log.err('Error unlinking %s\n' % (self.filename))

        return False

    def saveToDisk(self):
        """Saves the data to disk."""
        log.info('Saving to disk (%s)\n' % (self.filename))

        # Make sure they want to save
        if(not self.attrSaveable()):
            return

        # Get whatever the data is
        pyld = self.exportAttr(self.getAttr())

        # Write the file to disk, truncate if it exists
        try:
            pickle.dump(pyld, pdos.open(self.filename, 'wb'))
            pdos.syncFS()

        except Exception as e:
            log.err('Error writing to disk %s\n' % (str(e)))

    def attrSaveable(self):
        """THIS SHOULD BE OVERRIDEN BY THE IMPLEMENTER."""
        return False

    def importAttr(self, pyld):
        """By default do nothing, but expect that this function could be overwritten"""
        return pyld

    def exportAttr(self, data):
        """By default do nothing, but expect that this function could be overwritten"""
        return data


class ChuteStorage(PDStorage):

    """
        ChuteStorage class.

        This class holds onto the list of Chutes on this AP.

        It implements the PDStorage class which allows us to save the chuteList to disk transparently
    """
    # Class variable of chute list so all instances see the same thing
    chuteList = dict()

    def __init__(self, filename=None, reactor=None):
        if(not filename):
            filename = settings.FC_CHUTESTORAGE_SAVE_PATH
        PDStorage.__init__(self, filename, reactor, settings.FC_CHUTESTORAGE_SAVE_TIMER)

        # Has it been loaded?
        if(len(ChuteStorage.chuteList) == 0):
            log.verbose('Loading chutes from disk: %s\n' % (filename))
            self.loadFromDisk()

    def setAttr(self, attr):
        """Save our attr however we want (as class variable for all to see)"""
        ChuteStorage.chuteList = attr

    def getAttr(self):
        """Get our attr (as class variable for all to see)"""
        return ChuteStorage.chuteList

    def getChuteList(self):
        """Return a list of the names of the chutes we know of."""
        return ChuteStorage.chuteList.values()

    def getChute(self, name):
        """Returns a reference to a chute we have in our cache, or None."""
        return ChuteStorage.chuteList.get(name, None)

    def deleteChute(self, ch):
        """Deletes a chute from the chute storage. Can be sent the chute object, or the chute name."""
        if (isinstance(ch, Chute)):
            del ChuteStorage.chuteList[ch.name]
        else:
            del ChuteStorage.chuteList[ch]
        self.saveToDisk()

    def saveChute(self, ch):
        """
            Saves the chute provided in our internal chuteList.
            Also since we just received a new chute to hold onto we should save our ChuteList to disk.
        """
        # check if there is a version of the chute already
        oldch = ChuteStorage.chuteList.get(ch.name, None)
        if(oldch != None):
            newch = copy.deepcopy(oldch)
            # we should merge these chutes so we don't lose any data
            oldch.__dict__.update(ch.__dict__)
            # TODO: do we need to deal with cache separate? Old code we did
        else:
            ChuteStorage.chuteList[ch.name] = ch

        self.saveToDisk()

    def clearChuteStorage(self):
        ChuteStorage.chuteList = {}
        pdos.remove(settings.FC_CHUTESTORAGE_SAVE_PATH)

    #
    # Functions we override to implement PDStorage Properly
    #
    def attrSaveable(self):
        """Returns True if we should save the ChuteList, otherwise False."""
        return (type(ChuteStorage.chuteList) == dict)


if(__name__ == '__main__'):  # pragma: no cover
    def usage():
        print('Usage: $0 -ls : print chute storage details')
        exit(0)

    try:
        if(sys.argv[1] != '-ls'):
            usage()
    except Exception as e:
        print(e)
        usage()

    cs = ChuteStorage()

    chutes = cs.getChuteList()
    for ch in chutes:
        print(ch)
