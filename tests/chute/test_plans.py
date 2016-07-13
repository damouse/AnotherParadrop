
from mock import patch, MagicMock

from paradrop.chute import plans, plangraph
from paradrop.config import osconfig, configservice, firewall
from paradrop.config import osconfig, configservice, dhcp, dockerconfig


@patch('paradrop.chute.plans.log')
def test_generatePlansName(mockOutput):
    """
    Test that the generatePlans function does it's job.
    """
    # Test that we get a warning if there is one
    update = MagicMock()
    update.old.warning = "TEST WARNING"
    plans.Name.generatePlans(update)
    update.pkg.request.write.assert_called_once_with(update.old.warning + "\n")


@patch('paradrop.chute.plans.log')
def test_generatePlansTraffic(mockOutput):
    """
    Test that the generatePlans function does it's job.
    """
    update = MagicMock()
    update.plans.addPlans.side_effect = [Exception('e'), None, Exception('e'), None, None, None]
    todoPlan = (configservice.reloadAll,)

    abtPlan = [(osconfig.revertConfig, "dhcp"),
               (osconfig.revertConfig, "firewall"),
               (osconfig.revertConfig, "network"),
               (osconfig.revertConfig, "wireless"),
               (configservice.reloadAll, )]

    def c1():
        update.plans.addPlans.assert_called_with(plangraph.TRAFFIC_GET_OS_FIREWALL, (firewall.getOSFirewallRules, ))

    def c2():
        update.plans.addPlans.assert_called_with(plangraph.TRAFFIC_GET_DEVELOPER_FIREWALL, (firewall.getDeveloperFirewallRules, ))

    def c3():
        todoPlan = (firewall.setOSFirewallRules, )
        abtPlan = (osconfig.revertConfig, "firewall")
        update.plans.addPlans.assert_called_with(plangraph.TRAFFIC_SET_OS_FIREWALL, todoPlan, abtPlan)
    for call in [c1, c2, c3]:
        try:
            plans.Traffic.generatePlans(update)
        except Exception as e:
            pass
        call()


@patch('paradrop.chute.plans.log')
def test_generatePlansRuntime(mockOutput):
    """
    Test that the generatePlans function does it's job.
    """
    update = MagicMock()
    update.plans.addPlans.side_effect = [Exception('e'), None, Exception('e'), None, None, Exception('e'), None, None, None, None]
    todoPlan = (configservice.reloadAll, )

    abtPlan = [(osconfig.revertConfig, "dhcp"),
               (osconfig.revertConfig, "firewall"),
               (osconfig.revertConfig, "network"),
               (osconfig.revertConfig, "wireless"),
               (configservice.reloadAll, )]

    def c1():
        update.plans.addPlans.assert_called_with(plangraph.RUNTIME_GET_VIRT_PREAMBLE, (dockerconfig.getVirtPreamble, ))

    def c2():
        update.plans.addPlans.assert_called_with(plangraph.RUNTIME_GET_VIRT_DHCP, (dhcp.getVirtDHCPSettings, ))

    def c3():
        update.plans.addPlans.assert_called_with(plangraph.RUNTIME_SET_VIRT_DHCP, (dhcp.setVirtDHCPSettings, ))

    def c4():
        update.plans.addPlans.assert_called_with(plangraph.RUNTIME_RELOAD_CONFIG, todoPlan, abtPlan)
    for call in [c1, c2, c3, c4]:
        try:
            plans.Runtime.generatePlans(update)
        except Exception as e:
            pass
        call()


@patch('paradrop.chute.plans.log')
def test_generatePlansResource(mockOutput):
    """
    Test that the generatePlans function does it's job.
    """
    # Test that we get a out.header call
    update = MagicMock()
    plans.Resource.generatePlans(update)
    mockOutput.header.assert_called_once_with("%r\n" % (update))


@patch('paradrop.chute.plans.log')
def test_generatePlansFiles(mockOutput):
    """
    Test that the generatePlans function does it's job.
    """
    # Test that we get a out.header call
    update = MagicMock()
    plans.Files.generatePlans(update)
    mockOutput.header.assert_called_once_with("%r\n" % (update))
