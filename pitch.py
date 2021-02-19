import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Arc, Circle, ConnectionPatch, Rectangle

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

    """

    def __init__(self, length : float, width : float):
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
        axes.axis('off')  # this hides the x and y ticks
        plt.ylim(-2, self.width + 2)
        plt.xlim(-2, self.length + 2)
        # for i in shapes:
        #     axes.add_artist(i)

        self.axes = axes
        self.figure = figure

    def __pitch_components(traditional = False):
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
        else:
            pitch_color = 'white'
            line_color = 'black'
            
        return [
            Rectangle((0, 0), width=self.width, length=self.length,
                        fill=False, color='grey'),  # pitch
            Rectangle([0, 22.3], width=14.6, length=35.3,
                        fill=False),  # left penalty area
            Rectangle([105.4, 22.3], width=14.6, length=35.3,
                        fill=False),  # right penalty area
            ConnectionPatch([60, 0], [60, 80], "data", "data"),
            Rectangle([0, 32], width=4.9, length=16, fill=False),
            Rectangle([115.1, 32], width=4.9, length=16, fill=False),
            plt.Circle((60, 40), 9.1, color="black", fill=False),
            plt.Circle((60, 40), 0.33, color="black"),
            plt.Circle((9.7, 40), 0.33, color="black"),
            plt.Circle((110.3, 40), 0.33, color="black"),
            Arc((9.7, 40), length=16.2, width=16.2, angle=0,
                theta1=310, theta2=50, color="black"),
            Arc((110.3, 40), length=16.2, width=16.2, angle=0,
                theta1=130, theta2=230, color="black")
        ]



