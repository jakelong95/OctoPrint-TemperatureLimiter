# coding=utf-8
from __future__ import absolute_import
import time

import octoprint.plugin
from octoprint.util import RepeatedTimer

class TemperaturelimiterPlugin(octoprint.plugin.StartupPlugin,
                               octoprint.plugin.ShutdownPlugin):

    def __init__(self):
        self.updateTimer = None

    def startTimer(self):
        self._logger.info(u"Starting timer")
        self.updateTimer = RepeatedTimer(1, self.timerCheck)
        self.updateTimer.start()

    def timerCheck(self):
        self._logger.info(u"Timer triggered")


    ##~~ StartupPlugin hook

    def on_after_startup(self):
        self._logger.info(u"Starting up Temperature Limiter")
        self.startTimer()

    ##~~ ShutdownPlugin hook

    def on_shutdown(self):
        self._logger.info(u"Shutting down Temerature Limiter")

    ##~~ Softwareupdate hook

    def get_update_information(self):
        # Define the configuration for your plugin to use with the Software Update
        # Plugin here. See https://docs.octoprint.org/en/master/bundledplugins/softwareupdate.html
        # for details.
        return {
            "TemperatureLimiter": {
                "displayName": "Temperaturelimiter Plugin",
                "displayVersion": self._plugin_version,

                # version check: github repository
                "type": "github_release",
                "user": "jakelong95",
                "repo": "OctoPrint-Temperaturelimiter",
                "current": self._plugin_version,

                # update method: pip
                "pip": "https://github.com/jakelong95/OctoPrint-Temperaturelimiter/archive/{target_version}.zip",
            }
        }

__plugin_name__ = "Temperature Limiter Plugin"
__plugin_pythoncompat__ = ">=3,<4" # only python 3

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = TemperaturelimiterPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }
