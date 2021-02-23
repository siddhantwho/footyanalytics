import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Arc, Circle, ConnectionPatch, Rectangle, Wedge

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
    pitch_color = 'green' if traditional else 'white'

    if home:
        return [
  
            Rectangle([x-1.5,y-1], width=2.5, height=2.5, fill=True, ec = "red", fc ="red"),
            Rectangle([x+1,y-1.75], width=1, height=4, fill=True, ec = "red", fc ="red"),
            Wedge((x+2.25,y+0.25),r=0.8, theta1=90, theta2=270, ec=pitch_color,
            fill = True, fc = pitch_color)

        ]
    else:
        return [
            Rectangle([x-1,y-1], width=2.5, height=2.5, fill=True, ec = "blue", fc ="blue"),
            Rectangle([x-2,y-1.75], width=1, height=4, fill=True, ec = "blue", fc ="blue"),
            Wedge((x-2.25,y+0.25),r=0.8, theta1=270, theta2=90, ec=pitch_color,
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

    def __init__(self, length: float = 120, width : float = 80):
        """
        Initialises the pitch object with length, width and the basic outlines.
        ...

        Parameters
        ----------
        length : float (default = 120)
            The desired length of the pitch in metres
        width: float (default = 80)
            The desired width of the pitch in metres

        """
        self.length = length
        self.width = width

        figure, axes = plt.subplots(figsize = (self.length/10,self.width/10))
        axes.axis('on')  # this hides the x and y ticks
        plt.ylim(-2, self.width + 2)
        plt.xlim(-2, self.length + 2)
        components = self.__pitch_components()
        for shape in components: #draw pitch using individual shapes
            axes.add_artist(shape)

        self.axes = axes
        self.figure = figure

    def __pitch_components(self, traditional: bool = True):
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
        if traditional:
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
    
    def show(self):
        self.figure.show()
        plt.show()

if __name__ == "__main__":
    pass
    newpitch = Pitch()
    newpitch.show()
    plt.show()



