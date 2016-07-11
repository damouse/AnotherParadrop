
from paradrop.shared import log
from io import BytesIO

"""
    dockerconfig module:
        This module contains all of the knowledge of how to take internal pdfcd
        representation of configurations of chutes and translate them into specifically
        what docker needs to function properly, whether that be in the form of dockerfiles
        or the HostConfig JSON object known at init time of the chute.
"""


def getVirtPreamble(update):
    log.warn('TODO implement me\n')
    if update.updateType == 'create':
        if not hasattr(update, 'dockerfile'):
            return
        if update.dockerfile is None:
            return
        else:
            log.info('Using prexisting dockerfile.\n')
            update.dockerfile = BytesIO(update.dockerfile.encode('utf-8'))
