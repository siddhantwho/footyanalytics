import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Arc, Circle, ConnectionPatch, Rectangle, Wedge

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

        figure, axes = plt.subplots(figsize = (self.length/10,self.width/10))
        axes.axis('off')  # this hides the x and y ticks
        plt.ylim(-2, self.width+2)
        plt.xlim(-2, self.length+2)
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

    def buildLineUp(self, lineup: list, home: bool, both: bool = True):
        """
        Builds a visual representation of the lineup on the pitch object
        ...
        Parameters
        ----------
        lineup : list
            List of players participating in the game found in the event data
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
        player_list = [[x[0],x[2]] for x in lineup_list]
        for player in lineup_list:

            pos_x = abs(reflector_x - positions[player[1]][0])*scale
            pos_y = abs(reflector_y - positions[player[1]][1])

            icon = jersey(pos_x, pos_y, home, self.traditional, full = full_field)
            for parts in icon:
                self.axes.add_artist(parts)

            if player[2]<10:
                self.axes.text(pos_x-1,pos_y-0.5, player[2], fontsize = 15, color = num_color)
            elif player[2]<20:
                self.axes.text(pos_x-1.85,pos_y-0.5, player[2], fontsize = 15, color = num_color)
            else:
                self.axes.text(pos_x-1.5,pos_y-0.5, player[2], fontsize = 15, color = num_color)
    
    def show(self):
        self.figure.show()
        plt.show()

if __name__ == "__main__":


    #pass
    argentina = [{'player': {'id': 6312, 'name': 'Franco Armani'},
  'position': {'id': 1, 'name': 'Goalkeeper'},
  'jersey_number': 12},
 {'player': {'id': 5742, 'name': 'Gabriel Iván Mercado'},
  'position': {'id': 2, 'name': 'Right Back'},
  'jersey_number': 2},
 {'player': {'id': 3090, 'name': 'Nicolás Hernán Otamendi'},
  'position': {'id': 3, 'name': 'Right Center Back'},
  'jersey_number': 17},
 {'player': {'id': 3602, 'name': 'Faustino Marcos Alberto Rojo'},
  'position': {'id': 5, 'name': 'Left Center Back'},
  'jersey_number': 16},
 {'player': {'id': 5507, 'name': 'Nicolás Alejandro Tagliafico'},
  'position': {'id': 6, 'name': 'Left Back'},
  'jersey_number': 3},
 {'player': {'id': 5506, 'name': 'Javier Alejandro Mascherano'},
  'position': {'id': 10, 'name': 'Center Defensive Midfield'},
  'jersey_number': 14},
 {'player': {'id': 5741, 'name': 'Enzo Nicolás Pérez'},
  'position': {'id': 13, 'name': 'Right Center Midfield'},
  'jersey_number': 15},
 {'player': {'id': 5504, 'name': 'Éver Maximiliano David Banega'},
  'position': {'id': 15, 'name': 'Left Center Midfield'},
  'jersey_number': 7},
 {'player': {'id': 2995, 'name': 'Ángel Fabián Di María Hernández'},
  'position': {'id': 17, 'name': 'Right Wing'},
  'jersey_number': 11},
 {'player': {'id': 5496, 'name': 'Cristian David Pavón'},
  'position': {'id': 21, 'name': 'Left Wing'},
  'jersey_number': 22},
 {'player': {'id': 5503, 'name': 'Lionel Andrés Messi Cuccittini'},
  'position': {'id': 23, 'name': 'Center Forward'},
  'jersey_number': 10}]

    newpitch = Pitch()
    newpitch.buildLineUp(argentina, False)
    newpitch.show()
    plt.show()



