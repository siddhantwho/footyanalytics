import requests

base_url = "https://raw.githubusercontent.com/statsbomb/open-data/master/data/"
match_url = base_url + "matches/{}/{}.json"
event_url = base_url + "events/{}.json"
comp_url = base_url + "competitions.json"
lineup_url = base_url + "lineups/{}.json"

def get_match(match_id, comp_id, season_id):

    competition = requests.get(url=match_url.format(comp_id,season_id)).json()
    match = requests.get(url=event_url.format(match_id)).json()
    lineup =  requests.get(url=lineup_url.format(match_id)).json()

    return (match,competition,match_id,lineup)

def get_data():
    comp_id = 43
    season_id = 3
    competition = requests.get(url=match_url.format(comp_id,season_id)).json()
    wcdf = pd.DataFrame(competition)
    wcmatchids = list(wcdf.match_id)

    wcfeatures = pd.DataFrame()
    wclabels = pd.DataFrame()

    for i in (wcmatchids):

        match_id = i
        
        match = requests.get(url=event_url.format(match_id)).json()

        lineup =  requests.get(url=lineup_url.format(match_id)).json()
        
        wcmatch = Match(match,competition, match_id, lineup)
        
        tempfeats,templabels = wcmatch.train_XY()
        
        wcfeatures = wcfeatures.append(tempfeats,sort = False)
        wclabels = wclabels.append(templabels, sort = False)
        
    return wcfeatures, wclabels
