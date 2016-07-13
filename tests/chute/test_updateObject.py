
from paradrop.chute import updateObject

from mock import patch, MagicMock


# @patch('paradrop.chute.updateObject.log')
# @patch('paradrop.chute.updateObject.plangraph')
# @patch('paradrop.chute.updateObject.chutestorage')
# @patch('paradrop.chute.updateObject.executionplan')
# def test_updateObject(mOut, mExc, mStore, mExcPlan):
#     func = MagicMock()
#     store = MagicMock()

#     mStore.ChuteStorage.return_value = store
#     update = dict(updateClass='CHUTE', updateType='create', name='test', tok=111111, pkg=None, func=func)

#     update = updateObject.parse(update)

#     mExcPlan.generatePlans.return_value = False
#     mExcPlan.executePlans.return_value = False

#     update.execute()

#     mExcPlan.generatePlans.assert_called_once_with(update)
#     mExcPlan.aggregatePlans.assert_called_once_with(update)
#     mExcPlan.executePlans.assert_called_once_with(update)

#     store.saveChute.assert_called_once_with(update.new)

#     assert mOut.usage.call_count == 1
#     func.assert_called_once_with(update)
