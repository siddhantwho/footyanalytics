from pitch import Pitch
import requests

class Match:
    """
    A class used to represent a football Match captured by event (play by play) data
    The event data used to create this project is provided by Statsbomb
    ...

    Attributes
    ----------
    match : DataFrame
        An object containing information about each event in the football match in tabular format
    competition: DataFrame
        An object containing information about all the matches in the competition
    match_id : int
        The Statsbomb match ID for the match being loaded
    lineup : DataFrame
        An object containing Statsbomb lineup information for the match in a table

    Methods
    -------


    """
    def __init__(self, events : list, competition : list, match_id : int, lineup : list):
        """
        Parameters
        ----------
        events : list
            A list of json objects representing the events in a football game
        competition : list
            A list of json objects representing all the match information in the competition of interest
        match_id : int
            The Statsbomb match ID for the match being loaded
        lineup : list
            A list of json objects representing the lineup information for the match
        """
        self.events = events
        self.competition = competition
        self.match_id = match_id
        self.lineup = lineup
    
    def Lineups(self):
        """
        Shows a matplotlib visual representation of the starting lineups of both teams
        """
        newpitch = Pitch()
        newpitch.buildLineUp(self.events[0]['tactics']['lineup'], home = True, both = True)
        newpitch.buildLineUp(self.events[1]['tactics']['lineup'], home = False, both = True)
        newpitch.show()
        
    def Formation(self, home_team: bool):
        newpitch = Pitch()
        team_index = 0 if home_team else 1
        newpitch.buildLineUp(self.events[team_index]['tactics']['lineup'], home = home_team,
                            both = False)
        newpitch.show()


if __name__ == "__main__":

    base_url = "https://raw.githubusercontent.com/statsbomb/open-data/master/data/"
    match_url = base_url + "matches/{}/{}.json"
    event_url = base_url + "events/{}.json"
    comp_url = base_url + "competitions.json"
    lineup_url = base_url + "lineups/{}.json"


    match_id = 8650
    #match_id = 7586
    comp_id = 43
    season_id = 3

    bel_bra = requests.get(event_url.format(match_id)).json()
    fifawc = requests.get(match_url.format(comp_id,season_id)).json()
    lineup = requests.get(lineup_url.format(match_id)).json()

    testmatch = Match(bel_bra, fifawc, match_id, lineup)
    testmatch.Lineups()
            