__all__ = ["Tournament", "Team", "Match", "Game"]

from collections import abc
from abc import abstractmethod
from copy import deepcopy
from typing import List
import json

class BaseItem(abc.MappingView):
    def __init__(self, **kwargs):
        '''
        Makes all keys in kwargs an attribute of the object with its respective value in kwargs
        '''
        for key, val in kwargs.items():
            self.__setattr__(key, val)
    
    def json(self, whitelist=None):
        '''
        Convert object into JSON serializable string
        '''
        if whitelist is None:
            return json.dumps({k: v for k, v in self.__dict__.items() 
                                    if not callable(v)})
        else:
            return json.dumps({k: v for k, v in self.__dict__.items()
                                    if not callable(v)
                                    and k in whitelist})

    def patch_fields(self):
        return []

    def __contains__(self, key):
        return key in self.__dict__

    def __getitem__(self, key):
        return self.__getattribute__(key)

    def __len__(self):
        return self.__dict__.__len__()
    
    def __repr__(self):
        return f'{self.__class__} (id={id(self)})'

    def __str__(self):
        return self.__repr__()

    
class Tournament(BaseItem):
    # These attributes are guarenteed - as dictated by the requirements set at
    # https://developer.toornament.com/v2/doc/organizer_tournaments#post:tournaments
    name: str
    timezone: str
    size: int
    discipline: str
    participant_type: str
    platforms: List[str]

    def __init__(self, **kwargs):
        self.name = None
        self.timezone = None
        self.size = None
        self.discipline = None
        self.participant_type = 'team' # Currently this use-case for this API wrapper is to 
                                       # work for team-based tournaments as this guarentees
                                       # a 'lineup' attribute in the Team object
        self.platforms = []

        self.__dict__.update(kwargs)
        super().__init__(**self.__dict__)

    def patch_fields(self):
        # As dictated by 
        # https://developer.toornament.com/v2/doc/organizer_tournaments#patch:tournaments:id
        return ['name', 'full_name', 'scheduled_date_start', 
                'scheduled_date_end', 'timezone', 'public', 'size', 'online',
                'location', 'country', 'logo', 'registration_enabled', 
                'registration_opening_datetime', 'registration_closing_datetime', 
                'organization', 'contact', 'discord', 'website', 'description', 
                'rules', 'prize', 'match_report_enabled', 
                'registration_request_message', 'check_in_enabled', 
                'check_in_participant_enabled', 
                'check_in_participant_start_datetime', 
                'check_in_participant_end_datetime', 'archived', 
                'registration_acceptance_message', 'registration_refusal_message', 
                'registration_terms_enabled', 'registration_terms_url', 'team_min_size', 
                'team_max_size']

    def __repr__(self):
        return f"{self.name}: {self.discipline} tournament for {', '.join(self.platforms)}"




class Team(BaseItem):
    # These attributes are guarenteed - as dictated by the requirements set at
    # https://developer.toornament.com/v2/doc/organizer_participants#post:tournaments:tournament_id:participants
    name: str
    lineup: List[dict]

    def __init__(self, **kwargs):
        self.name = None
        self.lineup = []
        self.__dict__.update(**kwargs)
        super().__init__(**self.__dict__)

    def patch_fields(self):
        # As dictated by
        # https://developer.toornament.com/v2/doc/organizer_participants#patch:tournaments:tournament_id:participants:id
        return ['name', 'email', 'custom_user_identifier', 'checked_in',
                'custom_fields', 'lineup']

    def __repr__(self):
        return f"Team {self.name} (Members: {', '.join([l['name'] for l in self.lineup])})"


class Match(BaseItem):
    # A match cannot be POST-ed
    # https://developer.toornament.com/v2/doc/organizer_matches
    number: int
    opponents: List[dict]

    def __init__(self, **kwargs):
        self.number = None
        self.opponents = []
        self.__dict__.update(**kwargs)
        super().__init__(**self.__dict__)

    def summary(self, top_n = 3):
        sorted_list = [team for team in self.opponents if team['score'] is not None]
        sorted_list.sort(key=lambda team: team['score'], reverse = True)

        top_n = max(0, min(top_n, len(sorted_list)))
        return ', '.join([f"{team['participant']['name']}: {team['score']}" for team in sorted_list[:top_n]])
    
    def patch_fields(self):
        # As dictated by
        # https://developer.toornament.com/v2/doc/organizer_matches#patch:tournaments:tournament_id:matches:id
        return ['scheduled_datetime', 'public_note', 'private_note', 'opponents']

    def __repr__(self):
        return f"Match {self.number}: {self.summary()}"


class Game(BaseItem):
    # A game cannot be POST-ed
    # https://developer.toornament.com/v2/doc/organizer_match_games
    status: str
    opponents: List[dict]
    number: int
    properties: dict

    def __init__(self, **kwargs):
        self.status = None
        self.opponents = []
        self.number = None
        self.properties = dict()
        self.__dict__.update(**kwargs)
        super().__init__(**self.__dict__)

    def patch_fields(self):
        # As dictated by 
        # https://developer.toornament.com/v2/doc/organizer_match_games#patch:tournaments:tournament_id:matches:match_id:games:number
        return ['status', 'opponents', 'properties']

    def __repr__(self):
        return f"Scores: {', '.join([str(team['score']) for team in self.opponents if team['score'] is not None])}"