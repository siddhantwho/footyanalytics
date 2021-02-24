from pitch import Pitch

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
        newpitch.buildLineUp(self.events[0]['tactics']['lineup'], home = True)
        newpitch.buildLineUp(self.events[1]['tactics']['lineup'], home = False)
        newpitch.show()
        


        