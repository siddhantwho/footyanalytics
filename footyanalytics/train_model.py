import requests
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
import xgboost
from sklearn.metrics import brier_score_loss, roc_auc_score, log_loss
from tqdm import tqdm
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.lines as mlines

import Match.py

def offence_value(events, scores, concedes, Y):
    
    prev_events = events.shift(1).fillna(0)
    same_team = prev_events.team_id == events.team_id

    prevlabels = Y.shift(1).fillna(0)

    sameteam = (prev_events.team_id == events.team_id)
    goalevent = ((prev_events.action == 'Shot') & (prev_events.result == 'Success'))
    
    prev_scores = prevlabels.scores * sameteam + prevlabels.concedes * (~sameteam)
    #prev_scores[goalevent] = 0
    
    offscore = list(scores - prev_scores)
    maxoff = max(offscore)
    minoff = min(offscore)
    
    for i in range(len(offscore)):
        offscore[i] = (offscore[i] - minoff)/(maxoff-minoff)*100
    return offscore

def defence_value(events, scores, concedes, Y):
    
    prev_events = events.shift(1).fillna(0)
    same_team = prev_events.team_id == events.team_id

    prevlabels = Y.shift(1).fillna(0)

    sameteam = (prev_events.team_id == events.team_id)
    goalevent = ((prev_events.action == 'Shot') & (prev_events.result == 'Success'))
    
    prev_concedes = prevlabels.concedes * sameteam + prevlabels.scores * (~sameteam)
    #prev_concedes[goalevent] = 0
    
    defscore = list(concedes - prev_concedes)
    maxdef = max(defscore)
    mindef = min(defscore)
    
    for i in range(len(defscore)):
        defscore[i] = (defscore[i] - mindef)/(maxdef-mindef)*100
    
    return defscore

def label_match(training_data, matchfeats, model, events_full):
    missing = []
    for i in list(training_data.columns):
        if i not in list(matchfeats.columns):
            kwargs = {i:0}
            matchfeats = matchfeats.assign(**kwargs)
            
    matchfeats = matchfeats[list(training_data.columns)]
            
    Y_new = pd.DataFrame()
    for col in Y.columns:
        Y_new[col] = [p[1] for p in model[col].predict_proba(matchfeats)]
    
    events_full = events_full.assign(offence_value = offence_value(events_full,Y_new.scores,Y_new.concedes,Y_new))
    events_full = events_full.assign(defence_value = defence_value(events_full,Y_new.scores,Y_new.concedes,Y_new))
    
    #events_full = events_full[['team','time','player','action','start_x','start_y','end_x','end_y','result',
         #                      'play_pattern','offence_value','defence_value']]
    
    return events_full

def evaluate(y,y_hat):
    """Evaluates the model using 3 different scores """
    
    p = sum(y)/len(y)
    base = [p] * len(y)
    brier = brier_score_loss(y,y_hat)
    print(f"  Brier score: %.5f (%.5f)" % (brier,brier/brier_score_loss(y,base)))
    ll = log_loss(y,y_hat)
    print(f"  log loss score: %.5f (%.5f)" % (ll,ll/log_loss(y,base)))
    print(f"  ROC AUC: %.5f" % roc_auc_score(y,y_hat))


def train_model(features, labels):
    X = features.fillna(0)
    Y = labels
        
    Y_hat = pd.DataFrame()
    models = {}
    for col in list(Y.columns):
        model = xgboost.XGBClassifier(n_estimators=50,max_depth=3,n_jobs=-3,verbosity=0)
        model.fit(X,Y[col])
        models[col] = model
        
    testX,testY = X,Y

    for col in testY.columns:
        Y_hat[col] = [p[1] for p in models[col].predict_proba(testX)]
        print(f"### Y: {col} ###")
        evaluate(testY[col],Y_hat[col])
