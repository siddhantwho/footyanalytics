# footyanalytics
An analysis tool for football (soccer) match event data- creates ratings and visualisation for match events. This project uses the open source Statsbomb play-by-play (event) data (https://github.com/statsbomb/open-data) and the Match object is compatible for reading, processing and viewing Statsbomb event data files.

Implementation of a classifier to predict the odds that a given action in a football match will lead to a goal being scored. The algorithm is trained on the initial and final location of the actions, the type of action, its location with respect to the goal and the pattern of play (free kicks, throw-ins etc.). The classifier then learns whether the action leads to a goal (scored or conceded) in the next *x* match events and then values that action. This is then converted into an action rating as outlined in "Actions Speak Louder Than Goals: Valuing Player Actions in Soccer - https://dl.acm.org/doi/10.1145/3292500.3330758 ."

Scores of current version:
1. Goal scored = (ROC: 92.95%), (Brier: 82.00 %)
2. Goal conceded = (ROC: 96.28), (Brier: 86.96 %)


The components of this projects are displayed below:

A series of actions can be viewed by the plotting function or the events_viz method in the Match object, the visualisation tool then plots such a series of actions, using a colourmap to scale the offensive values of the action and different markers to designate the different key actions.:

![Gerrard's goal against AC Milan in 2005](gerrard.png)

The colour scale is based off the offensive rating of the action

A Match object that contains all the information associated with the football match including events, lineups and match details. The details are available to view:

![Match Information](matchinfo.png)

Coming soon:

1. A more sophisticated classifier to designate action ratings- football is not just about goals.
2. Visualisation tools to view lineups and tactical shifts.
3. Improving scores by training on a larger dataset/ tweaking features.





