###################################################################
# Copyright 2013-2014 All Rights Reserved
# Authors: The Paradrop Team
###################################################################

import os
import errno
import subprocess
import shutil

from distutils import dir_util

# We have to import this for the decorator
from paradrop.shared import log

# protect the original open function
__open = open

# Since we overwrite everything else, do the same to basename
basename = lambda x: os.path.basename(x)


def getMountCmd():
    return "mount"


def isMount(mnt):
    """This function checks if @mnt is actually mounted."""
    # TODO - need to check if partition and mount match the expected??
    return os.path.ismount(mnt)


def oscall(cmd, get=False):
    """
    This function performs a OS subprocess call.
    All output is thrown away unless an error has occured or if @get is True
    Arguments:
        @cmd: the string command to run
        [get] : True means return (stdout, stderr)
    Returns:
        None if not @get and no error
        (stdout, retcode, stderr) if @get or yes error
    """
    # Since we are already in a deferred chain, use subprocess to block and make the call to mount right HERE AND NOW
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, errors = proc.communicate()
    if(proc.returncode or get):
        return (output, proc.returncode, errors)
    else:
        if(output and output != ""):
            log.verbose('"%s" stdout: "%s"\n' % (cmd, output.rstrip()))
        if(errors and errors != ""):
            log.verbose('"%s" stderr: "%s"\n' % (cmd, errors.rstrip()))
        return None


def syncFS():
    oscall('sync')


def getFileType(f):
    if not exists(f):
        return None
    r = oscall('file "%s"' % f, True)
    if(r is not None and isinstance(r, tuple)):
        return r[0]
    else:  # pragma: no cover
        return None


def exists(p):
    return os.path.exists(p)


def listdir(p):
    return os.listdir(p)


def unlink(p):
    return os.unlink(p)


def mkdir(p):
    return os.mkdir(p)


def symlink(a, b):
    return os.symlink(a, b)


def ismount(p):
    return os.path.ismount(p)


def fixpath(p):
    """This function is required because if we need to pass a path to something like tarfile,
        we cannot overwrite the function to fix the path, so we need to expose it somehow."""
    return p


def copy(a, b):
    return shutil.copy(a, b)


def move(a, b):
    return shutil.move(a, b)


def remove(a):
    if (isdir(a)):
        return shutil.rmtree(a)
    else:
        return os.remove(a)


def isdir(a):
    return os.path.isdir(a)


def isfile(a):
    return os.path.isfile(a)


def copytree(a, b):
    """shutil's copytree is dumb so use distutils."""
    return dir_util.copy_tree(a, b)


def open(p, mode):
    return __open(p, mode)


def writeFile(filename, line, mode="a"):
    """Adds the following cfg (either str or list(str)) to this Chute's current
        config file (just stored locally, not written to file."""
    try:
        if(type(line) is list):
            data = "\n".join(line) + "\n"
        elif(type(line) is str):
            data = "%s\n" % line
        else:
            log.err("Bad line provided for %s\n" % filename)
            return
        fd = open(filename, mode)
        fd.write(data)
        fd.flush()
        fd.close()

    except Exception as e:
        log.err('Unable to write file: %s\n' % (str(e)))


def write(filename, data, mode="w"):
    """ Writes out a config file to the specified location.
    """
    try:
        fd = open(filename, mode)
        fd.write(data)
        fd.flush()
        fd.close()
    except Exception as e:
        log.err('Unable to write to file: %s\n' % str(e))


def readFile(filename, array=True, delimiter="\n"):
    """
        Reads in a file, the contents is NOT expected to be binary.
        Arguments:
            @filename: absolute path to file
            @array : optional: return as array if true, return as string if False
            @delimiter: optional: if returning as a string, this str specifies what to use to join the lines

        Returns:
            A list of strings, separated by newlines
            None: if the file doesn't exist
    """
    if(not exists(filename)):
        return None

    lines = []
    with open(filename, 'r') as fd:
        while(True):
            line = fd.readline()
            if(not line):
                break
            lines.append(line.rstrip())
    if(array is True):
        return lines
    else:
        return delimiter.join(lines)

"""
Quiet pdos module.
Implements utility OS operations without relying on the output module.
Therefore, this module can be used by output without circular dependency.
"""


def makedirs_quiet(p):
    """
    Recursive directory creation (like mkdir -p).
    Returns True if the path is successfully created, False if it existed
    already, and raises an OSError on other error conditions.
    """
    try:
        os.makedirs(p)
        return True
    except OSError as e:
        # EEXIST is fine (directory already existed).  Anything else would be
        # problematic.
        if e.errno != errno.EEXIST:
            raise e
    return False