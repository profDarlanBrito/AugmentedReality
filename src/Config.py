# Module used to read the configuration file
import os
import yaml


class Settings:
    _instance = None

    @classmethod
    def get(self):
        if self._instance is None:
            self._instance = parse_settings_file("../config.yaml")
        return self._instance


def parse_settings_file(filename):

    if not os.path.exists(filename):
        print("File does not exist:", filename)
        quit()

    print("Using for calibration settings: ", filename)

    with open(filename) as f:
        settings = yaml.safe_load(f)

    if not settings["is_ok"]:
        print("Configuration file is incorrect")
        quit()

    return settings


if __name__ == "__main__":
    sett = parse_settings_file("../config.yaml")
    print(sett["checkerboard size"])
