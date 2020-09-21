import requests
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder

def flatten_id(d):
    newd = {}
    extra = {}
    for k, v in d.items():
        if isinstance(v, dict):
            if len(v) == 2 and "id" in v and "name" in v:
                newd[k + "_id"] = v["id"]
                newd[k + "_name"] = v["name"]
            else:
                extra[k] = v
        else:
            newd[k] = v
    newd["extra"] = extra
    return newd

def angle(x,y):
    goalx = 120 + 0.1
    goaly = 40 + 0.1
    
    dx = goalx - x
    dy = goaly - y
    
    angle = np.arctan(dy/dx)
    return angle

def goaldist(x,y):
    
    goalx = 120 + 0.1
    goaly = 40 + 0.1
    
    dx = goalx - x
    dy = goaly - y
    
    distance = np.sqrt(dx**2 + dy**2)
    return distance

class Match:
    
    def __init__(self, match, competition, match_id, lineup):
        self.match = match
        self.competition = competition
        self.match_id = match_id
        self.lineup = lineup
        
    def info(self):
        matchinfo = pd.DataFrame(competition)
        matchinfo = matchinfo.loc[matchinfo.match_id == match_id]
        
        finalinfo = {'home_team_name': list(matchinfo.get('home_team'))[0]['home_team_name'],
              'home_team_id': list(matchinfo.get('home_team'))[0]['home_team_id'],
              'away_team_name': list(matchinfo.get('away_team'))[0]['away_team_name'],
              'away_team_id': list(matchinfo.get('away_team'))[0]['away_team_id'],
              'match_id' : list(matchinfo.get('match_id'))[0],
              'match_date': list(matchinfo.get('match_date'))[0],
              'kick_off_time' : list(matchinfo.get('kick_off'))[0],
              'home_score' : list(matchinfo.get('home_score'))[0],
              'away_score' : list(matchinfo.get('away_score'))[0],
              'competition_id' : list(matchinfo.get('competition'))[0]['competition_id'],
              'competition_name' : list(matchinfo.get('competition'))[0]['competition_name']}
        
        if ('managers' in list(list(matchinfo.get('home_team'))[0].keys())):
            finalinfo['home_manager'] = list(matchinfo.get('home_team'))[0]['managers'][0]['name']
            finalinfo['away_manager'] = list(matchinfo.get('away_team'))[0]['managers'][0]['name']
            finalinfo['home_manager_id'] = list(matchinfo.get('home_team'))[0]['managers'][0]['id']
            finalinfo['away_manager_id'] = list(matchinfo.get('away_team'))[0]['managers'][0]['id']
            
        
        if ('stadium' in list(matchinfo.columns)):
            
            if (len(list(matchinfo.get('stadium'))) > 1):
                
                finalinfo['stadium_id'] = list(matchinfo.get('stadium'))[0]['id']
                finalinfo['stadium_name'] = list(matchinfo.get('stadium'))[0]['name']
            else:
                finalinfo['stadium'] = list(matchinfo.get('stadium'))
                
        if ('referee' in list(matchinfo.columns)):
            
            if (len(list(matchinfo.get('referee'))) > 1):
                finalinfo['referee_id'] = list(matchinfo.get('referee'))[0]['id']
                finalinfo['referee_name'] = list(matchinfo.get('referee'))[0]['name']
            else:
                finalinfo['referee'] = list(matchinfo.get('referee'))

        if ('competition_stage' in list(matchinfo.columns)):
            finalinfo['stage_id'] = list(matchinfo.get('competition_stage'))[0]['id']
            finalinfo['stage_name'] = list(matchinfo.get('competition_stage'))[0]['name']
        
        return finalinfo
    
    def players(self):
        return pd.DataFrame(flatten_id(p)
            for l in self.lineup
            for p in l["lineup"]
            )
    
    def fullevents(self):
        
        finalinfo = self.info()
        finalt = pd.DataFrame(self.match).fillna(425895)
        playerinfo = self.players()
        
        #time ----------------------------------------------------------------------------------------------------------

        timestr = [0]*len(finalt)
        minstr = [str(i) for i in list(finalt['minute'])]
        secstr = [str(i) for i in list(finalt['second'])]

        for i in range(len(minstr)):
            if len(secstr[i])==1:
                secstr[i] = '0'+secstr[i]
            timestr[i] = minstr[i] + ':' + secstr[i]
            
        #events info from the match file --------------------------------------------------------------------------------
        
        pass_ = finalt['pass'].apply(pd.Series)
        shot_ = finalt['shot'].apply(pd.Series)
        type_ = finalt['type'].apply(pd.Series)
        possession_team_ = finalt['possession_team'].apply(pd.Series)
        play_pattern_ = finalt['play_pattern'].apply(pd.Series)
        team_ = finalt['team'].apply(pd.Series)
        player_ = finalt['player'].apply(pd.Series).iloc[:,1:3]
        position_ = finalt['position'].apply(pd.Series).iloc[:,1:3]
        carry_ = pd.DataFrame(finalt['carry'].apply(pd.Series).iloc[:,1])
        ball_receipt_ = pd.DataFrame(finalt['ball_receipt'].apply(pd.Series).iloc[:,1])
        
        if ('clearance' in finalt.columns):
            clearance_ = finalt['clearance'].apply(pd.Series)
        foul_won_ = finalt['foul_won'].apply(pd.Series)
        duel_ = finalt['duel'].apply(pd.Series)
        dribble_ = finalt['dribble'].apply(pd.Series)
        goalkeeper_ = finalt['goalkeeper'].apply(pd.Series)
        interception_ = finalt['interception'].apply(pd.Series)
        foul_committed_ = finalt['foul_committed'].apply(pd.Series)
        
        #----------------------------------------------------------------------------------------------------------------
        events = pd.DataFrame()
        
        events = events.assign(action = type_['name'])
        events = events.assign(action_id = type_['id'])
        
        events = events.assign(player_id = player_['id'].fillna(425895).loc[player_['id']!=425895].apply(int))
        events = events.merge(playerinfo,'left')
        events["player"] = events[['player_nickname','player_name']].apply(lambda x: x[0] if x[0] else x[1],axis=1)
        events = events.drop(columns=['player_nickname','player_name'])
        
        events = events.assign(team = team_['name'])
        events = events.assign(team_id = team_['id'])
        events = events.assign(home_team_bool = events['team_id'].apply(lambda x: x == finalinfo['home_team_id']))
        
        events = events.assign(possession_number = finalt['possession'])
        events = events.assign(possession_team = possession_team_['name'])
        events = events.assign(timestamp = finalt['timestamp'])
        
        events = events.assign(time = timestr)
        events = events.assign(period = finalt['period'])
        events = events.assign(play_pattern = play_pattern_['name'])
        events = events.assign(play_pattern_id = play_pattern_['id'])
        

        events = events.assign(player_position = position_['name'])
        events = events.assign(player_position_id = position_['id'])
        
        events = events.assign(match_id = finalinfo['match_id'])
        
        
        #derived and specific info ---------------------------------------------------------------------------------------
        
        posoutcomes = ['Complete','Success','Cleared','Foul','Won','Saved','Success In Play','In Play Safe','Success Out',
              'In Play Danger','No Touch','Touched Out','Punched out','Touched In','Block','Foul Won','Ball Recovered',
               'Goal','Collected Twice']
        negoutcomes = ['Incomplete','Failure','Lost In Play','Pass Offside','Out','Off T','Lost','Unknown','Post','Miscontrol',
                      'Dispossessed','Blocked','Lost Out','Error','Offside','Concede']
        
        start_xs = [0]*len(finalt)
        start_ys = [0]*len(finalt)

        end_x = [0]*len(finalt)
        end_y = [0]*len(finalt)

        result = ['None']*len(finalt)
        technique = ['Normal']*len(finalt)
        body_part = ['Foot']*len(finalt)
        outcome = ['None']*len(finalt)


        #dataframe main loop
        for index, row in finalt.iterrows():
            if (row['location']!= 425895):
                start_xs[index] = row['location'][0]
                start_ys[index] = row['location'][1]

            if (row['counterpress'] != 425895):
                technique[index] = 'Counter Pressure'

        #events loop      
        for index, row in events.iterrows():

            end_x[index] = start_xs[index]
            end_y[index] = start_ys[index]

            if (row['action']== 'Pass'):
                result[index] = 'Complete'

            if (row['action'] == 'Goal Keeper'):
                result[index] = 'Saved'
                body_part[index] = 'Hands'

            if (row['action'] == 'Clearance'):
                result[index] = 'Cleared'
                technique[index] = 'Normal'

            if (row['action'] == 'Dribble'):
                technique[index] = 'Run Past'

            if (row['action'] == 'Ball Receipt*'):
                result[index] = 'Complete'

            if (row['action'] == 'Carry'):
                result[index] = 'Complete' 

            if (row['action'] == 'Dribbled Past'):
                result[index] = 'Failure'
                body_part[index] = 'Body'

            if (row['action'] == 'Ball Recovery'):
                result[index] = 'Ball Recovered'

            if (row['action'] == 'Foul Won'):
                result[index] = 'Foul Won'
                body_part[index] = 'Body'

            if (row['action'] == 'Dispossessed'):
                result[index] = 'Dispossessed'

            if row['action']=='Pressure':
                body_part[index] = 'Body'
                if (start_xs[index] > 60):
                    result[index] = 'Offensive Pressure'
                else:
                    result[index] = 'Defensive Pressure'

            if (row['action'] == 'Block'):
                result[index] = 'Block'

            if (row['action'] == 'Miscontrol'):
                result[index] = 'Miscontrol'

            if (row['action'] == 'Foul Committed'):
                result[index] = 'Foul'

            if (row['action'] == 'Offside'):
                result[index] = 'Offside'

            if (row['action'] == 'Error'):
                result[index] = 'Error'
            
            if (row['action'] == 'Own Goal For'):
                result[index] = 'Goal'
            
            if (row['action'] == 'Own Goal Against'):
                result[index] = 'Concede'

            if row['action']=='Duel':
                if (list(events['team'])[index]==list(events['team'])[index+1]
                   and result[index+1] in posoutcomes):
                    result[index] = 'Won'
                elif (list(events['team'])[index]!=list(events['team'])[index+1]
                   and result[index+1] in negoutcomes ):
                    result[index] = 'Won'
                else:
                    result[index] = 'Lost'

            if row['action']=='Pressure':
                if (list(events['team'])[index]==list(events['team'])[index+1]
                   and result[index+1] in posoutcomes ):
                    outcome[index] = 'Success'
                elif (list(events['team'])[index]!=list(events['team'])[index+1]
                   and result[index+1] in negoutcomes ):
                    outcome[index] = 'Success'
                else:
                    outcome[index] = 'Failure'


        #passing loop     
        for index, row in pass_.fillna(425895).iterrows():
            if (row['end_location']!= 425895):
                end_x[index] = row['end_location'][0]
                end_y[index] = row['end_location'][1]
            if (row['outcome']!= 425895):
                result[index] = row['outcome']['name']
            if (row['height']!= 425895):
                technique[index] = row['height']['name']
            if (row['body_part']!= 425895):
                body_part[index] = row['body_part']['name']


        #shots loop
        for index, row in shot_.fillna(425895).iterrows():
            if (row['end_location']!= 425895):
                end_x[index] = row['end_location'][0]
                end_y[index] = row['end_location'][1]
            if (row['outcome']!= 425895):
                result[index] = row['outcome']['name']
            if (row['technique']!= 425895):
                technique[index] = row['technique']['name']
            if (row['body_part']!= 425895):
                body_part[index] = row['body_part']['name']

        #carry loop
        for index, row in carry_.fillna(425895).iterrows():
            if (row['end_location']!= 425895):
                end_x[index] = row['end_location'][0]
                end_y[index] = row['end_location'][1]


        #goalkeeper loop
        for index, row in goalkeeper_.fillna(425895).iterrows():
            if (row['end_location']!= 425895):
                end_x[index] = row['end_location'][0]
                end_y[index] = row['end_location'][1]

            if (row['outcome']!= 425895):
                result[index] = row['outcome']['name']
            if (row['technique']!= 425895):
                technique[index] = row['technique']['name']
            if (row['body_part']!= 425895):
                body_part[index] = row['body_part']['name']

        #clearance loop
        if ('clearance' in finalt.columns):
            for index, row in clearance_.fillna(425895).iterrows():
                if ('body part' in list(clearance_.columns)):
                    if (row['body_part'] != 425895):
                        body_part[index] = row['body_part']['name']
                if (row['aerial_won'] != 425895):
                    technique[index] = 'Aerial'

        #dribble loop
        for index, row in dribble_.fillna(425895).iterrows():
            if (row['outcome']!= 425895):
                result[index] = row['outcome']['name']
            if ('nutmeg' in list(dribble_.columns)):
                if (row['nutmeg']!= 425895):
                    technique[index] = 'Nutmeg'

        #ball receipt loop
        for index, row in ball_receipt_.fillna(425895).iterrows():
            if (row['outcome']!= 425895):
                result[index] = row['outcome']['name']

        #interception loop
        for index, row in interception_.fillna(425895).iterrows():
            if (row['outcome']!= 425895):
                result[index] = row['outcome']['name']


        for i in range(len(result)):
            if (result[i] in posoutcomes):
                outcome[i] = 'Success'
            if (result[i] in negoutcomes):
                outcome[i] = 'Failure'

        #fix away team locations
        
        max_x = max(start_xs)
        max_y = max(start_ys)
        
        
        #reflect x and y for the away team

        for index, row in events.iterrows():
            if (row['team'] == finalinfo['away_team_name']):
                end_x[index] = max_x - end_x[index]
                end_y[index] = max_y - end_y[index]
                start_xs[index] = max_x - start_xs[index]
                start_ys[index] = max_y - start_ys[index]

        
        events = events.assign(start_x_noscale = start_xs)
        events = events.assign(start_y_noscale = start_ys)
        events = events.assign(start_x = events.start_x_noscale * 120 / max_x)
        events = events.assign(start_y = events.start_y_noscale * 80 / max_y)
        
        events = events.assign(end_x_noscale = end_x)
        events = events.assign(end_y_noscale = end_y)
        events = events.assign(end_x = events.end_x_noscale * 120 / max_x)
        events = events.assign(end_y = events.end_y_noscale * 80 / max_y)
        
        events = events.assign(result = result)
        events = events.assign(technique = technique)
        events = events.assign(body_part = body_part)
        events = events.assign(outcome = outcome)
        
        return events
    #-------------------------------------------------------------------------------------------------------------------
    
    def events_viz(self):
        full = self.fullevents()
        
        return full[['team','time','player','action','start_x','start_y','end_x','end_y','result','play_pattern']]
    
    def train_XY(self, prev_actions = 10):
        
        events = self.fullevents()[['match_id','action','start_x','start_y','end_x','end_y','outcome','play_pattern',
                       'home_team_bool', 'result','team','team_id']]
        
        N = len(events)
        traininfo = self.info()
        
        #Calculating X for the training data
        
        start_x_train = [0]*N
        end_x_train = [0]*N
        start_y_train = [0]*N
        end_y_train = [0]*N
        
        home_goal_count = 0
        home_score = [0]*N
        away_goal_count = 0
        away_score = [0]*N
        goal_diff = [0]*N

        
        for index, row in events.iterrows():
            #reflect positions back to left-right play for feature consistency
            if (row.home_team_bool):

                start_x_train[index] = row.start_x
                end_x_train[index] = row.end_x
                start_y_train[index] = row.start_y
                end_y_train[index] = row.end_y

            else:

                start_x_train[index] = 120 - row.start_x
                end_x_train[index] = 120 - row.end_x
                start_y_train[index] = 80 - row.start_y
                end_y_train[index] = 80 - row.end_y
                
            #keeping track of the live game score    
            if (row.result== 'Goal'):        
                if (row.home_team_bool):
                    home_goal_count = home_goal_count + 1
                else:
                    away_goal_count = away_goal_count + 1

            home_score[index] = home_goal_count
            away_score[index] = away_goal_count
            goal_diff[index] = home_goal_count - away_goal_count
        
        
        trainday = events.assign(start_x = start_x_train, start_y = start_y_train,
                                end_x = end_x_train, end_y = end_y_train,
                                home_score = home_score, away_score = away_score, goal_diff = goal_diff)
        
        trainday = trainday.assign(deltax = trainday.end_x - trainday.start_x, deltay = trainday.end_y - trainday.start_y)
        trainday = trainday.assign(movement = np.sqrt(trainday.deltax**2 + trainday.deltay**2))

        trainday = trainday.assign(start_angle = angle(trainday.start_x,trainday.start_y),
                                   end_angle = angle(trainday.end_x,trainday.end_y),
                                  start_goald = goaldist(trainday.start_x,trainday.start_y),
                                  end_goald = goaldist(trainday.end_x,trainday.end_y)
                                  )
        
        #preparing the X labels from the X data
        
        features = trainday.assign(index = list(trainday.index))
        trainfeats = features[['index','start_x','start_y','end_x','end_y','home_team_bool','home_score',
                     'away_score','goal_diff','deltax','deltay','movement','start_angle','end_angle',
                     'start_goald',
                     'end_goald']]

        trainhot = features[['action','play_pattern','outcome']]
        
        hottie = OneHotEncoder(sparse = False)
        trainenc = hottie.fit_transform(trainhot)
        cats = hottie.categories_
        
        catlist = []
        for i in cats:
            for j in i:
                catlist.append(j)
        
        hotlabels = pd.DataFrame()
        for i in range(len(catlist)):
            kwargs = {catlist[i] : trainenc[:,i]}
            hotlabels = hotlabels.assign(**kwargs)

        hotlabels = hotlabels.assign(index = list(hotlabels.index))
        Xfeatures = trainfeats.merge(hotlabels,how='outer')
        
        dropcols = ['Camera On','Camera off','Bad Behavior','Half End','Half Start','Injury Stoppage','Player Off',
                    'Player On','Starting XI','Substitution','Tactical Shift','All Out Attack','index','Bad Behaviour',
                   'Own Goal For','Own Goal Against','Referee Ball-Drop']
        
        for i in dropcols:
            if (i in list(Xfeatures.columns)):
                Xfeatures = Xfeatures.drop(columns = [i])


        # Caluclating labels ie Y for the training data
        
        homegoalindex = trainday.loc[(trainday.result == 'Goal')]
        homegoalindex = list(homegoalindex[homegoalindex.home_team_bool].index)

        awaygoalindex = trainday.loc[(trainday.result == 'Goal')]
        awaygoalindex = list(awaygoalindex[awaygoalindex.home_team_bool == False].index)
        
        scoresinthefuture = [0]*N
        for i in homegoalindex:
            for j in range(10):
                scoresinthefuture[i-j] = 1
        for i in awaygoalindex:
            for j in range(10):
                scoresinthefuture[i-j] = 2
        
        traindayscores = trainday.assign(scoresinthefuture = scoresinthefuture)
        
        scoreslabel = [False]*len(trainday)
        concedeslabel = [False]*len(trainday)
        goalfromshot = [False]*len(trainday)

        for index, row in traindayscores.iterrows():
            if (row.scoresinthefuture == 1):

                if (row.home_team_bool == True):
                    scoreslabel[index] = True
                if (row.home_team_bool == False):
                    concedeslabel[index] = True

            if (row.scoresinthefuture == 2):

                if (row.home_team_bool == True):
                    concedeslabel[index] = True
                if (row.home_team_bool == False):
                    scoreslabel[index] = True

            if ((row.action == 'Shot') and (row.result=='Goal')):
                goalfromshot[index] = True
        
        Ylabels = pd.DataFrame()
        Ylabels = Ylabels.assign(scores = scoreslabel,
                                concedes = concedeslabel,
                                goal_from_shot = goalfromshot)
        
        
        return Xfeatures, Ylabels

