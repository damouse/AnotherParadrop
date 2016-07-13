###################################################################
# Copyright 2013-2014 All Rights Reserved
# Authors: The Paradrop Team
###################################################################

from paradrop import config
from paradrop.shared import settings, log
from paradrop.chute import dockerapi as virt

from . import plangraph, chute


class Name:

    @classmethod
    def generatePlans(klass, update):
        """
            This function looks at a diff of the current Chute (in @chuteStor) and the @newChute,
            then adds Plan() calls to make the Chute match the @newChute.

            Returns:
                True: abort the plan generation process
        """
        log.verbose("%r\n" % (update))

        # print any warnings from previous update if they exist
        if hasattr(update, 'pkg') and update.old != None and update.old.warning != None:
            update.pkg.request.write(update.old.warning + '\n')

        # TODO: Create a directory for the chute for us to hold onto things (dockerfile, OS config stuff)

        return None


class Traffic:

    @classmethod
    def generatePlans(klass, update):
        """
            This function looks at a diff of the current Chute (in @chuteStor) and the @newChute,
            then adds Plan() calls to make the Chute match the @newChute.

            Returns:
                True: abort the plan generation process
        """
        log.header("%r\n" % (update))

        # Make sure we need to create this chute (does it already exist)
        # TODO
        #    chutePlan.addPlans(new, plangraph.TRAFFIC_SECURITY_CHECK, (security.checkTraffic, (chuteStor, new)))

        # First time, so generate the basic firewall rules in cache (key: 'osFirewallConfig')
        update.plans.addPlans(plangraph.TRAFFIC_GET_OS_FIREWALL, (config.firewall.getOSFirewallRules, ))

        # Get developer firewall rules (key: 'developerFirewallRules')
        update.plans.addPlans(plangraph.TRAFFIC_GET_DEVELOPER_FIREWALL, (config.firewall.getDeveloperFirewallRules, ))

        # Combine rules from above two fucntions, save to file
        todoPlan = (config.firewall.setOSFirewallRules, )
        abtPlan = (config.osconfig.revertConfig, "firewall")
        update.plans.addPlans(plangraph.TRAFFIC_SET_OS_FIREWALL, todoPlan, abtPlan)

        return None


class Struct:

    @classmethod
    def generatePlans(klass, update):
        """
            This function looks at a diff of the current Chute (in @chuteStor) and the @newChute,
            then adds Plan() calls to make the Chute match the @newChute.

            Returns:
                True: abort the plan generation process
        """
        log.verbose("%r\n" % (update))

        # Detect system devices and set up basic configuration for them (WAN
        # interface, wireless devices).  These steps do not need to be reverted on
        # abort.
        #
        # abortNetworkConfig is added as an abort command here so that it runs when
        # config.network.getNetworkConfig or just about anything else fails.
        #
        # reloadAll is added as an abort command here so that it runs when any of
        # the set* plans fail and back log.
        update.plans.addPlans(plangraph.STRUCT_GET_SYSTEM_DEVICES,
                              (config.devices.getSystemDevices, ),
                              (config.network.abortNetworkConfig, ))
        update.plans.addPlans(plangraph.STRUCT_SET_SYSTEM_DEVICES,
                              (config.devices.setSystemDevices, ),
                              (config.configservice.reloadAll, ))

        update.plans.addPlans(plangraph.STRUCT_GET_HOST_CONFIG,
                              (config.hostconfig.getHostConfig, ))

        # Save current network configuration into chute cache (key: 'networkInterfaces')
        update.plans.addPlans(plangraph.STRUCT_GET_INT_NETWORK,
                              (config.network.getNetworkConfig, ))

        # Setup changes to push into OS config files (key: 'osNetworkConfig')
        update.plans.addPlans(plangraph.STRUCT_GET_OS_NETWORK, (config.network.getOSNetworkConfig, ))

        # Setup changes to push into OS config files (key: 'osWirelessConfig')
        update.plans.addPlans(plangraph.STRUCT_GET_OS_WIRELESS, (config.wifi.getOSWirelessConfig, ))

        # Setup changes into virt configuration file (key: 'virtNetworkConfig')
        update.plans.addPlans(plangraph.STRUCT_GET_VIRT_NETWORK, (config.network.getVirtNetworkConfig, ))

        # Changes for networking
        todoPlan = (config.network.setOSNetworkConfig, )
        abtPlan = (config.osconfig.revertConfig, 'network')
        update.plans.addPlans(plangraph.STRUCT_SET_OS_NETWORK, todoPlan, abtPlan)

        # Changes for wifi
        todoPlan = (config.wifi.setOSWirelessConfig, )
        abtPlan = (config.osconfig.revertConfig, 'wireless')
        update.plans.addPlans(plangraph.STRUCT_SET_OS_WIRELESS, todoPlan, abtPlan)

        return None


class Runtime:

    @classmethod
    def generatePlans(klass, update):
        """
            This function looks at a diff of the current Chute (in @chuteStor) and the @newChute,
            then adds Plan() calls to make the Chute match the @newChute.

            Returns:
                True: abort the plan generation process
        """
        log.verbose("%r\n" % (update))

        # Generate virt start script, stored in cache (key: 'virtPreamble')
        update.plans.addPlans(plangraph.RUNTIME_GET_VIRT_PREAMBLE, (config.dockerconfig.getVirtPreamble, ))

        # If the user specifies DHCP then we need to generate the config and store it to disk
        update.plans.addPlans(plangraph.RUNTIME_GET_VIRT_DHCP, (config.dhcp.getVirtDHCPSettings, ))
        update.plans.addPlans(plangraph.RUNTIME_SET_VIRT_DHCP, (config.dhcp.setVirtDHCPSettings, ))

        # Reload configuration files
        todoPlan = (config.configservice.reloadAll, )
        abtPlan = [(config.osconfig.revertConfig, "dhcp"),
                   (config.osconfig.revertConfig, "firewall"),
                   (config.osconfig.revertConfig, "network"),
                   (config.osconfig.revertConfig, "wireless"),
                   (config.configservice.reloadAll, )]
        update.plans.addPlans(plangraph.RUNTIME_RELOAD_CONFIG, todoPlan, abtPlan)

        return None


class State:

    @classmethod
    def generatePlans(klass, update):
        """
            This function looks at a diff of the current Chute (in @chuteStor) and the @newChute,
            then adds Plan() calls to make the Chute match the @newChute.

            Returns:
                True: abort the plan generation process
        """
        log.verbose("%r\n" % (update))

        # If this chute is new (no old version)
        if(update.old is None):
            log.verbose('new chute\n')

            # If it's a stop, start, delete, or restart command go ahead and fail right now since we don't have a record of it
            if update.updateType in ['stop', 'start', 'delete', 'restart']:
                update.failure = "No chute found with id: " + update.name
                return True
            # If we are now running then everything has to be setup for the first time
            if(update.new.state == chute.STATE_RUNNING):
                update.plans.addPlans(plangraph.STATE_CALL_START, (virt.startChute,))

            # Check if the state is invalid, we should return bad things in this case (don't do anything)
            elif(update.new.state == chute.STATE_INVALID):
                if(settings.DEBUG_MODE):
                    update.responses.append('Chute state is invalid')
                return True

        # Not a new chute
        else:
            if update.updateType == 'start':
                if update.old.state == chute.STATE_RUNNING:
                    update.failure = update.name + " already running."
                    return True
                update.plans.addPlans(plangraph.STATE_CALL_START, (virt.restartChute,))
            elif update.updateType == 'restart':
                update.plans.addPlans(plangraph.STATE_CALL_START, (virt.restartChute,))
            elif update.updateType == 'create':
                update.failure = update.name + " already exists on this device."
                return True
            elif update.new.state == chute.STATE_STOPPED:
                if update.updateType == 'delete':
                    update.plans.addPlans(plangraph.STATE_CALL_STOP, (virt.removeChute,))
                if update.updateType == 'stop':
                    if update.old.state == chute.STATE_STOPPED:
                        update.failure = update.name + " already stopped."
                        return True
                    update.plans.addPlans(plangraph.STATE_CALL_STOP, (virt.stopChute,))

        return None


class Resource:

    @classmethod
    def generatePlans(klass, update):
        """
            This function looks at a diff of the current Chute (in @chuteStor) and the @newChute,
            then adds Plan() calls to make the Chute match the @newChute.

            Returns:
                True: abort the plan generation process
        """
        log.header("%r\n" % (update))

        # Make sure we need to create this chute (does it already exist)
        # TODO

        #   # Check if the chute is new
        #   # if(not old):
        #   # convert cpu cgroups and add to lxcconfig (cached, key: 'cpuConfig')
        #   chutePlan.addPlans(new, plangraph.RESOURCE_GET_VIRT_CPU, (new.getCpuConfigString, None))
        #
        #   # convert mem cgroups and add to lxcconfig (cached, key: 'memConfig')
        #   chutePlan.addPlans(new, plangraph.RESOURCE_GET_VIRT_MEM, (new.getMemConfigString, None))

        #   # Generate a config file for wshaper, put in cache (key: 'osResourceConfig')
        #   chutePlan.addPlans(new, plangraph.RESOURCE_GET_OS_CONFIG, (new.getOSResourceConfig, None))

        #   # Make calls to configure the wshaper UCI file
        #   todoPlan = (new.setOSResourceConfig, old)
        #   abtPlan = (new.resetOSResourceConfig, None)
        #   chutePlan.addPlans(new, plangraph.RESOURCE_SET_VIRT_QOS, todoPlan, abtPlan)
        #
        #   # Once all changes are made into UCI system, reload the wshaper daemon
        #   todoPlan = (osenv.reloadQos, (chuteStor, new, True))
        #   abtPlan = [(new.resetOSResourceConfig, None), (osenv.reloadQos, (chuteStor, new, False))]
        #   chutePlan.addPlans(new, plangraph.RESOURCE_RELOAD_QOS, todoPlan, abtPlan)

        return None


class Files:

    @classmethod
    def generatePlans(klass, update):
        """
            This function looks at a diff of the current Chute (in @chuteStor) and the @newChute,
            then adds Plan() calls to make the Chute match the @newChute.

            Returns:
                True: abort the plan generation process
        """
        log.header("%r\n" % (update))

        # Make sure we need to create this chute (does it already exist)
        # TODO

        #   new = newChute
        #   old = chuteStor.getChute(newChute.guid)
        #   log.header("Generating Files Plan: %r\n" % (new))
        #
        #   tok = new.getCache('updateToken')
        #   if(tok and tok == 'STARTINGUP'):
        #       starting = True
        #   else:
        #       starting = False

        #   # The Chute uses libraries borrowed from the host, copy them
        #   if(not old or starting):
        #       chutePlan.addPlans(new, plangraph.FILES_COPY_FROM_OS, (new.copyEssentials, None))

        #   # There are a few files (lxc_start.sh) that need to be copied from the /root/cXXXX/ dir into the mounted partition
        #   if(not old or starting):
        #       chutePlan.addPlans(new, plangraph.FILES_COPY_TO_MNT, (new.copyFilesToMount, None))
        #
        #   # See if there is a change between the old.files and new.files
        #   if(old and old.files == new.files and not starting):
        #       return None

        #   # Are there any files?
        #   if(len(new.files) == 0):
        #       return None
        #
        #   # Otherwise, we have files to download, so check for proper format first
        #   chutePlan.addPlans(new, plangraph.FILES_SECURITY_CHECK, (security.checkFiles, new))
        #
        #   # Add plan to fetch the files
        #   chutePlan.addPlans(new, plangraph.FILES_FETCH, (new.fetchFiles, None))
        #   # Add plan to fetch the files
        #   chutePlan.addPlans(new, plangraph.FILES_COPY_USER, (new.copyFiles, None))
        #

        #   ##################
        #   # This part is semi-complicated
        #   # If a chute was running/frozen and then some files in the chute are updated, we need to restart the chute as the new binaries/files won't be currently used.
        #   # This function will call the necessary lxc-start/stop commands
        #   # NOTE: we only need to do this when an old chute exists and the state is running/frozen.
        #   # Otherwise, the next lxc-start command will properly load the new binaries/data.
        #   # If fetchFiles does not make any changes, it will skip this function

        #   if (old and (new.state == chute.STATE_RUNNING or new.state == chute.STATE_FROZEN)):
        #       currChuteState = stats.getLxcState(new.getInternalName())
        #       # We only want to reload when the chute is actually running
        #       # Could be power cycled and chutes would be stopped
        #       # In that case exc/state.py will handle that possibility, and start the chute
        #       if (currChuteState == chute.STATE_RUNNING or currChuteState == chute.STATE_FROZEN):
        #           chutePlan.addPlans(new, plangraph.STATE_FILES_STOP, (virt.fileStop, new))
        #           chutePlan.addPlans(new, plangraph.STATE_FILES_START, (virt.fileStart, new))

        return None
