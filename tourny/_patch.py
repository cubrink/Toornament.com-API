import json
from .TournamentItems import Tournament, Team, Match, Game

class PATCH():
    """
    Handle API PATCH requests for the toornament.com API
    """
    def __init__(self, api):
        self._api = api


    def tournament(self, tournament):
        """
        Patches in a tournament object
        """
        scope = 'organizer:admin'
        url = "https://api.toornament.com/organizer/v2/tournaments/{id}"
        url_kwargs = {'id': tournament.id}
        data = tournament.json(whitelist=tournament.patch_fields())
        return self.__patch(data, scope, url, **url_kwargs)


    def team(self, tournament, team):
        """
        Patches in a team object
        """
        scope = 'organizer:participant'
        url = 'https://api.toornament.com/organizer/v2/tournaments/{tournament_id}/participants/{id}'
        url_kwargs = {'tournament_id': tournament.id,
                      'id': team.id}
        data = team.json(whitelist=team.patch_fields())
        return self.__patch(data, scope, url, **url_kwargs)


    def match(self, tournament, match):
        """
        Patches in a match object
        """
        scope = 'organizer:result'
        url = 'https://api.toornament.com/organizer/v2/tournaments/{tournament_id}/matches/{id}'
        url_kwargs = {'tournament_id': tournament.id,
                      'id': match.id}
        data = match.json(whitelist=match.patch_fields())
        return self.__patch(data, scope, url, **url_kwargs)


    def game(self, tournament, match, game):
        """
        Patches in a game object
        """
        scope = 'organizer:result'
        url = 'https://api.toornament.com/organizer/v2/tournaments/{tournament_id}/matches/{match_id}/games/{number}'
        url_kwargs = {'tournament_id': tournament.id,
                      'match_id': match.id,
                      'number': game.number}
        data = game.json(whitelist=game.patch_fields())
        return self.__patch(data, scope, url, **url_kwargs)


    def __patch(self, data, scope, url, **url_kwargs):
        """
        Generalized function for sending PATCH requests
        """
        headers = {
            'authorization': "{0}".format(self._api.auth_tokens[scope])
        }

        response = self._api.session.request("PATCH", 
                                             url.format(**url_kwargs),
                                             headers=headers,
                                             data=data)

        if response.status_code == 401:
            self._api.get_auth_token(scope)
            headers['authorization'] = "{0}".format(self._api.auth_tokens[scope])
            response = self._api.session.request("PATCH", 
                                                 url.format(**url_kwargs),
                                                 headers=headers,
                                                 data=data)
        return response 