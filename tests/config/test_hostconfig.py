import tempfile

from mock import MagicMock, patch
from nose.tools import assert_raises


def test_generateHostConfig():
    """
    Test paradrop.config.hostconfig.generateHostConfig
    """
    from paradrop.config.hostconfig import generateHostConfig

    devices = dict()
    devices['wan'] = [{'name': 'eth0'}]
    devices['lan'] = [{'name': 'eth1'}]
    devices['wifi'] = [{'name': 'wlan0'}]

    config = generateHostConfig(devices)
    assert config['wan']['interface'] == "eth0"
    assert config['lan']['interfaces'] == ["eth1"]
    assert config['wifi'][0]['interface'] == "wlan0"


@patch("paradrop.config.devices.detectSystemDevices")
@patch("paradrop.config.hostconfig.settings")
def test_prepareHostConfig(settings, detectSystemDevices):
    """
    Test paradrop.config.hostconfig.prepareHostConfig
    """
    from paradrop.config.hostconfig import prepareHostConfig

    devices = {
        'wan': [{'name': 'eth0'}],
        'lan': list(),
        'wifi': list()
    }
    detectSystemDevices.return_value = devices

    source = tempfile.NamedTemporaryFile(delete=True)
    source.write("{test: value}")
    source.flush()

    settings.HOST_CONFIG_PATH = source.name

    config = prepareHostConfig()
    assert config['test'] == 'value'

    with patch("paradrop.config.hostconfig.yaml") as yaml:
        yaml.safe_load.side_effect = IOError()
        yaml.safe_dump.return_value = "{test: value}"

        config = prepareHostConfig()
        assert config['wan']['interface'] == 'eth0'

        # Now simulate failure to write to file.
        yaml.safe_dump.side_effect = IOError()
        assert_raises(Exception, prepareHostConfig)


@patch("paradrop.config.hostconfig.prepareHostConfig")
def test_getHostconfig(prepareHostConfig):
    """
    Test paradrop.config.hostconfig.getHostConfig
    """
    from paradrop.config.hostconfig import getHostConfig

    update = MagicMock()
    getHostConfig(update)
    assert update.new.setCache.called
