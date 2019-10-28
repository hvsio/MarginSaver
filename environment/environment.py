from configparser import ConfigParser
import os


class Config:
    """Interact with configuration variables."""

    configParser = ConfigParser()
    configFilePath = (os.path.join(os.getcwd(), 'environment/config.ini'))
    # for running the application outside a container, so we dont have to initialize a PYTHONPATH in local.
    if not os.path.exists(configFilePath):
        configFilePath = (os.path.join(os.getcwd(), 'environment/config.ini'))
    print(configFilePath)
    if os.path.isfile(configFilePath):
        print("we got a file")

    @classmethod
    def initialize(cls):
        """Start config by reading config.ini."""
        print("initializing")
        cls.configParser.read(cls.configFilePath, encoding='utf-8')

    @classmethod
    def cloud(cls, key):
        """Get prod values from config.ini."""
        return cls.configParser.get('CLOUD', key)

    @classmethod
    def dev(cls, key):
        """Get dev values from config.ini."""
        return cls.configParser.get('DEV', key)
