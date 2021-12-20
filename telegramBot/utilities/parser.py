from utilities import global_vars


def parseVotings(response):
    res = []
    for r in response:
        v = {'id': r['id'], 'name': r['name'], 'desc': r['desc'], 'end_date': r['end_date'],
             'start_date': r['start_date'], 'question': r['question'], 'pub_key': r['pub_key']}
        if v['start_date'] is not None and v['end_date'] is None:
            res.append(v)

    return res


def parseVoting():
    voting = {}
    for v in global_vars.user_votings:
        id_voting = v['id']
        if str(id_voting) == global_vars.voting_selected:
            voting = v
            global_vars.pub_key=v['pub_key']
    return voting


def createKeybVoting(votings):
    res = [[]]

    for v in votings:
        votingName = []
        votingName.append(str(v['id'])+"-"+v['name'])
        res.append(votingName)
    return res


def createKeyOption(options):
    res = [[]]

    for o in options:
        optionName = []
        optionName.append(str(o['number'])+"-"+o['option'])
        res.append(optionName)
    return res
