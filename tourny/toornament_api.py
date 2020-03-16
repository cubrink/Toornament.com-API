import json
import requests
from urllib.parse import quote_plus

from .TournamentItems import Tournament, Team, Match, Game
from ._get import GET
from ._post import POST
from ._patch import PATCH

# Types of scopes available for the API,
# https://developer.toornament.com/v2/security/scopes
scopes = [ "participant:manage_registrations",
           "participant:manage_participations",
           "user:info",
           "organizer:view",
           "organizer:admin",
           "organizer:result",
           "organizer:participant",
           "organizer:registration",
           "organizer:permission",
           "organizer:delete" ]

class API:
    def __init__(self, filepath='apidata.json'):
        # TODO
        # Lets pretend these are encrypted for now.
        self.__key = None
        self.__client_id = None
        self.__client_secret = None
        self.auth_tokens = dict()
        for scope in scopes:
            self.auth_tokens[scope] = None
        
        self.session = requests.Session()
        self.get = GET(self)
        self.post = POST(self)
        self.patch = PATCH(self)

        try:
            with open(filepath) as loadfile:
                api_data = json.load(loadfile)
                
            self.set_key(api_data['api_key'])
            self.set_client_id(api_data['client_id'])
            self.set_client_secret(api_data['client_secret'])
        except FileNotFoundError:
            raise UserWarning(f"File for API information not found ({filepath}), please manually add API info")


    #####################################
    #                                   #
    #              API SETUP            #
    #                                   #
    #####################################

    def set_key(self, key):
        self.__key = key
        self.session.headers.update({'X-Api-Key': self.__key})


    def set_client_id(self, client_id):
        self.__client_id = client_id


    def set_client_secret(self, client_secret):
        self.__client_secret = client_secret


    # Gets the appropriate authentication token from the server
    def get_auth_token(self, scope):
        if scope not in scopes:
            # Maybe raise error? for now pass
            # TODO
            pass
        else:
            url = "https://api.toornament.com/oauth/v2/token"

            payload = f"grant_type=client_credentials&client_id={self.__client_id}&client_secret={self.__client_secret}&scope={quote_plus(scope)}"
            
            headers = {
                'content-type': "application/x-www-form-urlencoded",
                }

            response = self.session.request("POST", url, data=payload, headers=headers)
            
            if response.status_code == 200:
                data = json.loads(response.text)
                self.auth_tokens[data['scope']] = data['access_token']
            
            return response.status_code

        














