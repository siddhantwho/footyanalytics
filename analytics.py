from match import Match
from pitch import Pitch

class Analytics:
    """
    A class used to perform analytical operations on event data from football games
    
    Attributes
    ----------
    events: list
        list of match events in json format
    lineups : list
        player lineups for the match

    Parameters
    ----------
    match : Match
        A match.Match object containing all the event information

    Methods
    -------

    """
    
    def __init__(self,Match):
        """
        Parameters
        ----------
        match : Match
        A match.Match object containing all the event information
        """
        
        self.events = Match.events
        self.lineup = Match.lineup



    