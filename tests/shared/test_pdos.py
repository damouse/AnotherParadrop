from paradrop.shared import pdos
from paradrop.shared import pdos
from mock import patch


@patch('paradrop.shared.pdos.os')
def test_pdos(mOs):
    pdos.listdir('test')
    mOs.listdir.assert_called_once_with('test')


@patch('paradrop.shared.pdos.os')
def test_pdoqs(mOs):
    assert pdos.makedirs_quiet('test')
    mOs.makedirs.assert_called_once_with('test')
