import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Arc, Circle, ConnectionPatch, Rectangle, Wedge

positions = {
    'Goalkeeper' : (7.5,40),
    'Right Back' : (20, 16),
    'Right Center Back' : (20,32),
    'Center Back' : (22.5, 40),
    'Left Center Back' : (20,48),
    'Left Back' : (20,64),
    'Right Wing Back' : (25,10),
    'Left Wing Back' : (25,70),
    'Right Defensive Midfield' : (30, 20),
    'Center Defensive Midfield' : (30, 40), 
    'Left Defensive Midfield' : (30,60),
    'Right Center Midfield' : (40,32),
    'Left Center Midfield' : (40, 48),
    'Left Midfield' : (40,70),
    'Right Midfield' : (40,10),
    'Right Attacking Midfield' : (45,20),
    'Left Attacking Midfield' : (45,60),
    'Right Wing' : (52.5,10),
    'Center Forward' : (52.5, 40),
    'Left Wing' : (52.5,70),
    'Left Center Forward' : (52.5, 55),
    'Right Center Forward' : (52.5,25),
    'Striker' : (60,60)
}

def jersey(x:float,y:float, home: bool, traditional: bool) -> list:
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
    pitch_color = 'green' if traditional else 'white'
    a = 2.75 #scale factor
    if home:
        return [
  
            Rectangle([x-1.5*a,y-1*a], width=2.5*a, height=2.5*a, fill=True, ec = "red", fc ="red"),
            Rectangle([x+1*a,y-1.75*a], width=1*a, height=4*a, fill=True, ec = "red", fc ="red"),
            Wedge((x+2.25*a,y+0.25*a),r=0.8*a, theta1=90, theta2=270, ec=pitch_color,
            fill = True, fc = pitch_color)

        ]
    else:
        return [
            Rectangle([x-1*a,y-1*a], width=2.5*a, height=2.5*a, fill=True, ec = "blue", fc ="blue"),
            Rectangle([x-2*a,y-1.75*a], width=1*a, height=4*a, fill=True, ec = "blue", fc ="blue"),
            Wedge((x-2.25*a,y+0.25*a),r=0.8*a, theta1=270, theta2=90, ec=pitch_color,
            fill = True, fc = pitch_color)

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
        traditional : bool
            Whether to use traditional colors (green and white) or modern (white and black)
        """
        self.length = length
        self.width = width
        self.traditional = traditional

        figure, axes = plt.subplots(figsize = (self.length/10,self.width/10))
        axes.axis('off')  # this hides the x and y ticks
        plt.ylim(-2, self.width + 2)
        plt.xlim(-2, self.length + 2)
        components = self.__pitch_components()
        for shape in components: #draw pitch using individual shapes
            axes.add_artist(shape)
        
        # for pos in positions.keys():
        #     jerz = jersey(positions[pos][0],positions[pos][1],True,True,scale=2)
        #     for i in jerz:
        #         axes.add_artist(i)

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

    def buildLineUp(self, lineup, home, traditional):
        for player in lineup:
            icon = jersey(positions[player[1]][0],positions[player[1]][1], home, traditional)
            for parts in icon:
                self.axes.add_artist(parts)
    
    def show(self):
        self.figure.show()
        plt.show()

if __name__ == "__main__":


    #pass
    argentina = [['Franco Armani', 'Goalkeeper', 12],
        ['Gabriel Iván Mercado', 'Right Back', 2],
        ['Nicolás Hernán Otamendi', 'Right Center Back', 17],
        ['Faustino Marcos Alberto Rojo', 'Left Center Back', 16],
        ['Nicolás Alejandro Tagliafico', 'Left Back', 3],
        ['Javier Alejandro Mascherano', 'Center Defensive Midfield', 14],
        ['Enzo Nicolás Pérez', 'Right Center Midfield', 15],
        ['Éver Maximiliano David Banega', 'Left Center Midfield', 7],
        ['Ángel Fabián Di María Hernández', 'Right Wing', 11],
        ['Cristian David Pavón', 'Left Wing', 22],
        ['Lionel Andrés Messi Cuccittini', 'Center Forward', 10]]

    newpitch = Pitch()
    newpitch.buildLineUp(argentina, True,True)
    newpitch.show()
    plt.show()



