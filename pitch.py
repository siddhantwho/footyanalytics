import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Arc, Circle, ConnectionPatch, Rectangle, Wedge
from matplotlib.lines import Line2D

positions = {
    'Goalkeeper' : (7.5,40),

    'Right Back' : (20, 12),
    'Right Center Back' : (17.5,32),
    'Center Back' : (20, 40),
    'Left Center Back' : (17.5,48),
    'Left Back' : (20,68),
    'Right Wing Back' : (25,10),
    'Left Wing Back' : (25,70),

    'Right Defensive Midfield' : (30, 20),
    'Center Defensive Midfield' : (30, 40), 
    'Left Defensive Midfield' : (30,60),
    'Right Center Midfield' : (35,20),
    'Center Midfield' : (35, 40),
    'Left Center Midfield' : (35, 60),
    'Left Midfield' : (35,70),
    'Right Midfield' : (35,10),
    'Right Attacking Midfield' : (42.5,20),
    'Center Attacking Midfield' : (42.5, 40),
    'Left Attacking Midfield' : (42.5,60),

    'Right Wing' : (50,10),
    'Center Forward' : (52.5, 40),
    'Left Wing' : (50,70),
    'Left Center Forward' : (52.5, 55),
    'Right Center Forward' : (52.5,25),
    'Secondary Striker' : (50,40)
}

def jersey(x:float,y:float, home: bool, traditional: bool, **kwargs) -> list:
    """
    Returns a list of matplotlib objects that form the shape of a jersey
    ...

    Parameters
    x : float
        x position of the jersey
    y : float
        y position of the jersey
    home : bool
        Whether its a home or away team jersey
    traditional : bool
        traditional colours are green and white, else white and black.
    """
    a = 2.5 #scale factor
    pitch_color = 'green' if traditional else 'white'
    if kwargs:
        if kwargs['full']:
            a = 3.25
     
    if home:   
        return [
            
            Rectangle([x-1.5*a,y-1*a], width=2.5*a, height=2.5*a, fill=True, ec = "red", fc ="red"),
            Rectangle([x+1*a,y-1.75*a], width=1*a, height=4*a, fill=True, ec = "red", fc ="red"),
            Wedge((x+2.25*a,y+0.25*a),r=0.8*a, theta1=90, theta2=270, ec=pitch_color,
            fill = True, fc = pitch_color),
            Circle((x,y+0.5),2.5, fill=False, ec = "black")

        ]

    else:
        return [
            Rectangle([x-1*a,y-1*a], width=2.5*a, height=2.5*a, fill=True, ec = "blue", fc ="blue"),
            Rectangle([x-2*a,y-1.75*a], width=1*a, height=4*a, fill=True, ec = "blue", fc ="blue"),
            Wedge((x-2.25*a,y+0.25*a),r=0.8*a, theta1=270, theta2=90, ec=pitch_color,
            fill = True, fc = pitch_color),
            Circle((x,y+0.5),2.5, fill=False, ec = "white")

        ]

def manager_handles(managers):
    handle_home_manager = Line2D([],[], color="black", marker = '2',
                linestyle='None', markersize = 10,label= f'{managers[0]}')
    handle_away_manager = Line2D([],[], color="black", marker = '2',
                linestyle='None', markersize = 10,label= f'{managers[1]}')

    legend_home_manager = plt.legend(handles=[handle_home_manager], fontsize = 8, bbox_to_anchor=(-0.1, 0.95),
                        loc='center left', ncol=1)         
    legend_away_manager = plt.legend(handles=[handle_away_manager], fontsize = 8, bbox_to_anchor=(1.065, 0.95),
                        loc='center right', ncol=1)
    return (legend_home_manager, legend_away_manager)



class Pitch:
    """
    A class used to represent a football pitch
    ...

    Attributes
    ----------
    length : float
        The desired length of the pitch in metres
    width: float
        The desired width of the pitch in metres
    ...

    Parameters
    ----------
    length : float (default = 120)
        The desired length of the pitch in metres
    width: float (default = 80)
        The desired width of the pitch in metres

    Methods
    -------
    show() - plots the pitch 
    """

    def __init__(self, length: float = 120, width : float = 80, traditional: bool = True):
        """
        Initialises the pitch object with length, width and the basic outlines.
        ...

        Parameters
        ----------
        length (optional) : float 
            The desired length of the pitch in metres
        width (optional): float 
            The desired width of the pitch in metres
        traditional (optional) : bool
            Whether to use traditional colors (green and white) or modern (white and black)
        """
        self.length = length
        self.width = width
        self.traditional = traditional

        figure, axes = plt.subplots(figsize = (self.length/10 + 5,self.width/10))
        axes.axis('off')  # this hides the x and y ticks
        plt.ylim(-2, self.width+2)
        plt.xlim(-2 - 25, self.length+2 + 25)
        components = self.__pitch_components()
        for shape in components: #draw pitch using individual shapes
            axes.add_artist(shape)

        self.axes = axes
        self.figure = figure

    def __pitch_components(self):
        """
        creates matolotlib objects representing shapes on the football pitch
        ...
        Parameters
        ----------
        traditional : bool
            traditional colours are green and white, else white and black.

        Returns
        -------
        List of matplotlib objects of pitch components
        """
        if self.traditional:
            pitch_color = 'green'
            line_color = 'white'
            fill_color = True
        else:
            fill_color = False
            line_color = 'black'

        return [
            Rectangle((0, 0), width=self.length, height=self.width, fc = 'green',
                fill=fill_color, color="black"),  # pitch
            Rectangle([0, 22.3], width=14.6, height=35.3, color = line_color,
                fill=False),  # left penalty area
            Rectangle([105.4, 22.3], width=14.6, height=35.3, color = line_color,
                fill=False),  # right penalty area
            ConnectionPatch([60, 0], [60, 80], "data", "data", color = line_color),
            Rectangle([0, 32], width=4.9, height=16, fill=False, color = line_color),
            Rectangle([115.1, 32], width=4.9, height=16, fill=False, color = line_color),
            Circle((60, 40), 9.1, color=line_color, fill=False),
            Circle((60, 40), 0.33, color=line_color),
            Circle((9.7, 40), 0.33, color=line_color),
            Circle((110.3, 40), 0.33, color=line_color),
            Arc((9.7, 40), height=16.2, width=16.2, angle=0,
                theta1=310, theta2=50, color=line_color),
            Arc((110.3, 40), height=16.2, width=16.2, angle=0,
                theta1=130, theta2=230, color=line_color)
        ]

    def buildLineUp(self, lineup: list, managers, home: bool, both: bool = True):
        """
        Builds a visual representation of the lineup on the pitch object
        ...
        Parameters
        ----------
        lineup : list
            List of players participating in the game found in the event data
        managers : list or tuple
            strings of the managers names
        home : bool
            Home or away team
        both : bool
            Whether to plot the lineups of both teams
        """
        lineup_list = []
        for player in lineup:
            lineup_list.append([player['player']['name'], player['position']['name'],player['jersey_number']])
        
        reflector_x = 0 if home else 120 #reflects positions to right side of pitch
        reflector_y = 0 if home else 80
        scale = 1 if both else 2
        full_field = False if both else True

        num_color = 'black' if home else 'white'
        home_handles = []
        away_handles = []

        for player in lineup_list:

            pos_x = abs(reflector_x - positions[player[1]][0]*scale)
            pos_y = abs(reflector_y - positions[player[1]][1])

            #jersey icons on pitch
            icon = jersey(pos_x, pos_y, home, self.traditional, full = full_field)
            for parts in icon:
                self.axes.add_artist(parts)
            
            #jersey numbers
            if player[2]<10:
                self.axes.text(pos_x-1,pos_y-0.5, player[2], fontsize = 15, color = num_color)
            elif player[2]<20:
                self.axes.text(pos_x-1.85,pos_y-0.5, player[2], fontsize = 15, color = num_color)
            else:
                self.axes.text(pos_x-1.5,pos_y-0.5, player[2], fontsize = 15, color = num_color)
            
            #lineup lists
            if positions[player[1]][0] >= 50:
                legend_color = 'red'
                legend_marker = '>'
            elif positions[player[1]][0] >= 30:
                legend_color = 'blue'
                legend_marker = 'o'
            elif positions[player[1]][0] >= 10:
                legend_color = 'green'
                legend_marker = '<'
            else:
                legend_color = 'yellow'
                legend_marker = 'x'
             
            if home:
                home_handles.append(Line2D([],[], color=legend_color, marker = legend_marker,
                linestyle='None', markersize = 10,label= f'{player[2]} : {player[0]} \n'))
            else:
                away_handles.append(Line2D([],[], color=legend_color, marker = legend_marker,
                linestyle='None', markersize = 8,label= f'{player[2]} : {player[0]} \n'))

        legend_home = plt.legend(handles=home_handles, fontsize = 8, bbox_to_anchor=(-0.1, 0.5),
                        loc='center left', ncol=1)
        legend_away = plt.legend(handles=away_handles, fontsize = 8, bbox_to_anchor=(1.065, 0.5),
                        loc='center right', ncol=1)
        legend_home_manager = manager_handles(managers)[0]
        legend_away_manager = manager_handles(managers)[1]

        if both: #plotting both teams on the same pitch

            self.axes.add_artist(legend_home)
            self.axes.add_artist(legend_home_manager)
            self.axes.add_artist(legend_away)
            self.axes.add_artist(legend_away_manager)

        else: #plotting just one team
            if home:
                self.axes.add_artist(legend_home)
                self.axes.add_artist(legend_home_manager)
            else:
                self.axes.add_artist(legend_away)
                self.axes.add_artist(legend_away_manager)

    
    def show(self):
        self.figure.show()
        plt.show()

if __name__ == "__main__":

    newpitch = Pitch()
    #newpitch.show()
    plt.show()



