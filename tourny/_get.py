import json
from .TournamentItems import Tournament, Team, Match, Game

class GET():
    """
    Handle API GET requests for the toornament.com API
    """
    def __init__(self, api):
        self._api = api


    #####################################
    #                                   #
    #             GET BY ID             #
    #                                   #
    #####################################

# ^(?:    )#([^#]+?)\n.+(def.+\n)
# ^(?:    )# (.+?)\n.+(def.+)\n

    def tournament_by_id(self, tournament_id):
        """
        Get a tournament by a known id
        """
        scope = 'organizer:view'
        url = "https://api.toornament.com/organizer/v2/tournaments/{tournament_id}"
        url_kwargs = {'tournament_id': id}
        _, data = self.__get_by_id(scope, url, **url_kwargs)
        if data is not None:
            return None
        return Tournament(**data)
        

    def team_by_id(self, tournament_id, team_id):
        """
        Get a team by a known id
        """
        scope = 'organizer:participant'
        url = "https://api.toornament.com/organizer/v2/tournaments/{tournament_id}/participants/{team_id}"
        url_kwargs = {'tournament_id': tournament_id,
                      'team_id': team_id}
        _, data = self.__get_by_id(scope, url, **url_kwargs)
        if data is None:
            return None
        return Team(**data)


    def match_by_id(self, tournament_id, match_id):
        """
        Get a match by a known id
        """
        scope = 'organizer:result'
        url = 'https://api.toornament.com/organizer/v2/tournaments/{tournament_id}/matches/{match_id}'
        url_kwargs = {'tournament_id': tournament_id,
                      'match_id': match_id}
        _, data = self.__get_by_id(scope, url, **url_kwargs)
        if data is None:
            return None
        return Match(**data)


    def game_by_id(self, tournament_id, match_id, game_number):
        """
        Get a game by a known id
        """
        scope = 'organizer:result'
        url = 'https://api.toornament.com/organizer/v2/tournaments/{tournament_id}/matches/{match_id}/games/{game_number}'
        url_kwargs = {'tournament_id': tournament_id,
                      'match_id': match_id,
                      'game_number': game_number}
        _, data = self.__get_by_id(scope, url, **url_kwargs)
        if data is None:
            return None
        return Game(**data)



    #####################################
    #                                   #
    #           GET BY RANGE            #
    #                                   #
    #####################################

    
    def tournaments(self, range_values = (0, 49), params=dict()):
        """
        Gets a list of tournaments connected to the account
        """
        scope = 'organizer:view'
        range_unit = 'tournaments'
        url = "https://api.toornament.com/organizer/v2/tournaments"
        url_kwargs = dict()
        
        _, data = self.__get_by_range(range_values, range_unit, scope, url, params=params, **url_kwargs)
        if data is None:
            return None
        return [Tournament(**t) for t in data]


    def matches(self, tournament, range_values = (0, 99), params=dict()):
        """
        Gets a list of matches for a specified tournament
        """
        scope = 'organizer:result'
        range_unit = 'matches'
        url = "https://api.toornament.com/organizer/v2/tournaments/{tournament_id}/matches"
        url_kwargs = {'tournament_id': tournament.id}

        _, data = self.__get_by_range(range_values, range_unit, scope, url, params=params, **url_kwargs)
        if data is None:
            return None
        return [Match(**m) for m in data]


    def games(self, tournament, match, range_values = (0, 49), params=dict()):
        """
        Get a list of games belonging to the specified match in the specified tournament
        """
        scope = 'organizer:result'
        range_unit = 'games'
        url = 'https://api.toornament.com/organizer/v2/tournaments/{tournament_id}/matches/{match_id}/games'
        url_kwargs = {'tournament_id': tournament.id,
                      'match_id': match.id}

        _, data = self.__get_by_range(range_values, range_unit, scope, url, params=params, **url_kwargs)
        if data is None:
            return None
        return [Game(**g) for g in data]
        

    def teams(self, tournament, range_values = (0, 49), params=dict()):
        """
        Gets a list of participants
        """
        scope = 'organizer:participant'
        range_unit = 'participants'
        url = "https://api.toornament.com/organizer/v2/tournaments/{tournament_id}/participants"
        url_kwargs = {'tournament_id': tournament.id}

        _, data = self.__get_by_range(range_values, range_unit, scope, url, params=params, **url_kwargs)
        if data is None:
            return None
        return [Team(**t) for t in data]



    #####################################
    #                                   #
    #              GET ALL              #
    #                                   #
    #####################################

    def all_tournaments(self, params=dict()):
        """
        Returns a list of all tournaments
        """
        return self.__get_all(self.tournaments, params=params)

    def all_matches(self, tournament, params=dict()):
        """
        Returns a list of all matches for a given tournament
        """
        return self.__get_all(self.matches, tournament, params=params)

    def all_games(self, tournament, match, params=dict()):
        """
        Returns a list of all games for a match in a given tournament
        """
        return self.__get_all(self.games, tournament, match, params=params())

    def all_teams(self, tournament, params=dict()):
        """
        Returns a list of all participants in a given tournament.
        """
        return self.__get_all(self.teams, tournament, params=params)


    #####################################
    #                                   #
    #          CLASS UTILITIES          #
    #                                   #
    #####################################


    def __get_by_id(self, scope, url, params=dict(), **url_kwargs):
        """
        Generalized function for getting specified objects by their id
        """
        data = None
        
        if self._api.auth_tokens[scope] is None:
            self._api.get_auth_token(scope)

        headers = {
            'authorization': "{0}".format(self._api.auth_tokens[scope])
        }
        response = self._api.session.request("GET", url.format(**url_kwargs), data="", headers=headers, params=params)

        if response.status_code in (200, 206, 416):
            data = json.loads(response.text)

        return response.status_code, data


    def __get_by_range(self, range_values, range_unit, scope, url, params=dict(), **url_kwargs):
        """
        Generalized function for getting a collection of specified objects.
        """
        data = None

        if self._api.auth_tokens[scope] is None:
            self._api.get_auth_token(scope)

        headers = {
            'range': f"{range_unit}={range_values[0]}-{range_values[1]}",
            'authorization': f"{self._api.auth_tokens[scope]}"
        }

        response = self._api.session.request("GET", url.format(**url_kwargs), data="", headers=headers, params=params)

        if response.status_code == 401:
            self._api.get_auth_token(scope)
            headers['authorization'] = "{0}".format(self._api.auth_tokens[scope])
            response = self._api.session.request("GET", url.format(**url_kwargs), data="", headers=headers, params=params)

        if response.status_code in (200, 206):
            data = json.loads(response.text)

        return response.status_code, data

    def __get_all(self, func, *func_args, params=dict()):
        """
        Generalized function for getting all instances of specified objects.
        """
        MAX_PAGE_LENGTH = 50
        current_range = (0, MAX_PAGE_LENGTH - 1)

        data = []

        response_data = func(*func_args, current_range, params=params)
        
        while response_data is not None:
            data += response_data
            current_range = tuple((v+MAX_PAGE_LENGTH for v in current_range))
            response_data = func(*func_args, current_range, params=params)
        
        return data