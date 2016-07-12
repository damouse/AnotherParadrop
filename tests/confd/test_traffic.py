# from paradrop.chute.plans import Traffic
# from mock import patch, MagicMock
# from paradrop.config import osconfig, configservice, firewall
# from paradrop.chute import plangraph


# @patch('paradrop.chute.plans.log')
# def test_generatePlans(mockOutput):
#     """
#     Test that the generatePlans function does it's job.
#     """
#     update = MagicMock()
#     update.plans.addPlans.side_effect = [Exception('e'), None, Exception('e'), None, None, None]
#     todoPlan = (configservice.reloadAll, )

#     abtPlan = [(osconfig.revertConfig, "dhcp"),
#                (osconfig.revertConfig, "firewall"),
#                (osconfig.revertConfig, "network"),
#                (osconfig.revertConfig, "wireless"),
#                (configservice.reloadAll, )]

#     def c1():
#         update.plans.addPlans.assert_called_with(plangraph.TRAFFIC_GET_OS_FIREWALL, (firewall.getOSFirewallRules, ))

#     def c2():
#         update.plans.addPlans.assert_called_with(plangraph.TRAFFIC_GET_DEVELOPER_FIREWALL, (firewall.getDeveloperFirewallRules, ))

#     def c3():
#         todoPlan = (firewall.setOSFirewallRules, )
#         abtPlan = (osconfig.revertConfig, "firewall")
#         update.plans.addPlans.assert_called_with(plangraph.TRAFFIC_SET_OS_FIREWALL, todoPlan, abtPlan)
#     for call in [c1, c2, c3]:
#         try:
#             Traffic().generatePlans(update)
#         except Exception as e:
#             pass
#         call()
