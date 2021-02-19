
positions = {
    'Goalkeeper' : 1,
    'Right Back' : 2,
    'Right Center Back' : 3,
    'Center Back' : 3.5,
    'Left Center Back' : 4,
    'Left Back' : 5,
    'Right Wing Back' : 12,
    'Left Wing Back' : 13,
    'Right Defensive Midfielder' : 6,
    'Center Defensive Midfielder' : 6.1, 
    'Left Defensive Midfielder' : 6.2,
    'Right Center Midfield' : 8.1,
    'Left Center Midfield' : 8.2,
    'Left Midfield' : 8.5,
    'Right Midfield' : 8.6,
    'Right Attacking Midfield' : 8.8,
    'Left Attacking Midfield' : 8.9,
    'Right Wing' : 7.1,
    'Center Forward' : 7.2,
    'Left Wing' : 7.3,
    'Left Center Forward' : 9.1,
    'Right Center Forward' : 9.2,
    'Striker' : 7.4
}

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
        home_formation = self.events[0]['tactics']['formation']
        away_formation = self.events[1]['tactics']['formation']