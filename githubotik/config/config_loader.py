import os
import json

class ConfigLoader():

    CONFIG_FILE = 'config.json'

    def config(self):
        config_file = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            self.CONFIG_FILE)
        if not hasattr(self, '_parsed_config'):
            self._parsed_config = self.load(config_file)
        return self._parsed_config

    def load(self, config_file):
        with open(config_file) as f:
            self._parsed_config = json.load(f)
        return self._parsed_config
