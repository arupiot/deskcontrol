import os
import json
from config import FIREBASE_AUTH

from a00_command import Commander
from navigation import StateModule


def say(message):
    print message


class CommanderModule(StateModule):

    always_tick = True

    def __init__(self, controller):
        super(CommanderModule, self).__init__(controller)

        # read in the credentials from file
        with open(FIREBASE_AUTH["credentials_path"]) as f:
            creds = json.loads(f.read())

        # make one
        self.commander = Commander(creds,
                              FIREBASE_AUTH["google_api_key"],
                              FIREBASE_AUTH["custom_token_url"],
                              FIREBASE_AUTH["auth_domain"],
                              FIREBASE_AUTH["db_url"])


        # add a function to be called by the commander
        self.commander.add_function("say", say)

        self.commander.start()


    def __del__(self):
        # stop it
        self.commander.stop()

    def tick(self):
        self.commander.tick()

