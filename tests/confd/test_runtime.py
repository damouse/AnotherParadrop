
# from mock import patch, MagicMock

# from paradrop.config import osconfig, configservice, dhcp, dockerconfig
# from paradrop.chute import plangraph
# from paradrop.chute.plans import Runtime


# @patch('paradrop.chute.plans.log')
# def test_generatePlans(mockOutput):
#     """
#     Test that the generatePlans function does it's job.
#     """
#     update = MagicMock()
#     update.plans.addPlans.side_effect = [Exception('e'), None, Exception('e'), None, None, Exception('e'), None, None, None, None]
#     todoPlan = (configservice.reloadAll, )

#     abtPlan = [(osconfig.revertConfig, "dhcp"),
#                (osconfig.revertConfig, "firewall"),
#                (osconfig.revertConfig, "network"),
#                (osconfig.revertConfig, "wireless"),
#                (configservice.reloadAll, )]

#     def c1():
#         update.plans.addPlans.assert_called_with(plangraph.RUNTIME_GET_VIRT_PREAMBLE, (dockerconfig.getVirtPreamble, ))

#     def c2():
#         update.plans.addPlans.assert_called_with(plangraph.RUNTIME_GET_VIRT_DHCP, (dhcp.getVirtDHCPSettings, ))

#     def c3():
#         update.plans.addPlans.assert_called_with(plangraph.RUNTIME_SET_VIRT_DHCP, (dhcp.setVirtDHCPSettings, ))

#     def c4():
#         update.plans.addPlans.assert_called_with(plangraph.RUNTIME_RELOAD_CONFIG, todoPlan, abtPlan)
#     for call in [c1, c2, c3, c4]:
#         try:
#             Runtime().generatePlans(update)
#         except Exception as e:
#             pass
#         call()
