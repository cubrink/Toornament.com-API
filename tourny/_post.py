import json
from .TournamentItems import Tournament, Team, Match, Game

class POST():
    """
    Handle API POST requests for the toornament.com API
    """
    def __init__(self, api):
        self._api = api

    def tournament(self, tournament):
        """
        Posts in a tournament object
        """
        scope = 'organizer:admin'
        url = "https://api.toornament.com/organizer/v2/tournaments"
        url_kwargs = {}
        return self.__post(tournament.json(), scope, url, **url_kwargs)

    def team(self, tournament, team):
        """
        Posts in a team object
        """
        scope = 'organizer:participant'
        url = "https://api.toornament.com/organizer/v2/tournaments/{tournament_id}/participants"
        url_kwargs = {'tournament_id': tournament.id}
        return self.__post(team.json(), scope, url, **url_kwargs)


    def __post(self, data, scope, url, **url_kwargs):
        """
        Generalized function for sending POST requests
        """
        headers = {
            'authorization': "{0}".format(self._api.auth_tokens[scope])
        }

        response = self._api.session.request("POST", 
                                             url.format(**url_kwargs),
                                             headers=headers,
                                             data=data)

        if response.status_code == 401:
            self._api.get_auth_token(scope)
            headers['authorization'] = "{0}".format(self._api.auth_tokens[scope])
            response = self._api.session.request("POST", 
                                                 url.format(**url_kwargs),
                                                 headers=headers,
                                                 data=data)

        return response                                