# In The Name Of Allah
# Ali Salimi

import copy


def forwardCreator(node_dict, root):
    extensive_form = node_dict[root]
    edges = extensive_form['edges']
    i = 0
    if edges:
        for e in edges:
            extensive_form['edges'][i]['to'] = forwardCreator(node_dict, e['to'])
            i += 1
    return extensive_form


def gameCreator(file_path):
    file = open(file_path, 'r')
    #
    # creating players
    players = dict()
    line = file.readline()
    line = line.replace('\n', '')
    line = line.replace('(', '').replace(')', '').split(',')
    for i in range(0, len(line)):
        players[i] = {'name': str(line[i])}
    #
    # creating extensive form
    node_dict = dict()
    for line in file:
        line = line.replace('\n', '').split(' ')
        id = int(line[0])
        is_terminal = None
        player = None
        value = None
        edges = None
        #
        if line[1].startswith('('):
            is_terminal = True
            value = line[1].replace('(', '').replace(')', '').split(',')
            value = tuple(map(int, value))
        else:
            is_terminal = False
            player = int(line[1])
            edges = list()
            for i in range(2, len(line)):
                l = line[i].split('-')
                e = {
                    'label': str(l[0]),
                    'to': int(l[1]),
                    'is_active': False
                }
                edges.append(e)
        #
        node_dict[id] = {
            'is_terminal': is_terminal,
            'player': player,
            'value': value,
            'edges': edges
        }
    extensive_form = forwardCreator(node_dict, 0)
    #
    game = {
        'players': players,
        'extensive_form': extensive_form
    }
    return game


def backwardInduction(extensive_form):
    extensive_form = copy.deepcopy(extensive_form)
    #
    extensive_form_list = list()
    extensive_form_list.append(extensive_form)
    values_list = list()
    values_list.append(list())
    for i in range(0, len(extensive_form['edges'])):
        v = extensive_form['edges'][i]['to']['value']
        if v:
            for j in range(0, len(values_list)):
                values_list[j].append(v)
        else:
            efs = backwardInduction(extensive_form['edges'][i]['to'])
            temp = list()
            for ef_out in efs:
                for ef_in in extensive_form_list:
                    new_ef_in = copy.deepcopy(ef_in)
                    new_ef_in['edges'][i]['to'] = ef_out
                    temp.append(new_ef_in)
            extensive_form_list = temp
            temp = list()
            for ef in extensive_form_list:
                for values in values_list:
                    new_values = copy.deepcopy(values)
                    new_values.append(ef['edges'][i]['to']['value'])
                    temp.append(new_values)
            values_list = temp
    #
    temp = list()
    for i in range(0, len(extensive_form_list)):
        ef = extensive_form_list[i]
        vs = values_list[i]
        max = vs[0][ef['player']]
        for j in range(1, len(vs)):
            v = vs[j]
            if v[ef['player']] > max:
                max = v[ef['player']]
        for j in range(0, len(ef['edges'])):
            v = vs[j]
            if v[ef['player']] == max:
                new_ef = copy.deepcopy(ef)
                new_ef['value'] = v
                new_ef['edges'][j]['is_active'] = True
                temp.append(new_ef)
    extensive_form_list = temp
    return extensive_form_list


def getNETuple(solved_extensive_form, ne_tuple):
    ne_tuple = copy.deepcopy(ne_tuple)
    if solved_extensive_form['edges']:
        for edge in solved_extensive_form['edges']:
            if edge['is_active']:
                ne_tuple[solved_extensive_form['player']] += edge['label']
            ne_tuple = getNETuple(edge['to'], ne_tuple)
    return ne_tuple


def gameSolver(game):
    game = copy.deepcopy(game)
    #
    players = game['players']
    solved_extensive_form_list = backwardInduction(game['extensive_form'])
    #
    ne_tuple = list()
    for p in players:
        ne_tuple.append('')
    #
    ne_list = list()
    for sef in solved_extensive_form_list:
        ne_list.append(tuple(getNETuple(sef, ne_tuple)))
    #
    solved_game = {
        'players': players,
        'solved_extensive_form_list': solved_extensive_form_list,
        'ne_list': ne_list
    }
    return solved_game


print()

print('price war game NE(s):')
game = gameCreator('price_war.txt')
solved_game = gameSolver(game)
for i in range(0, len(solved_game['ne_list'])):
    print(solved_game['ne_list'][i], ':', solved_game['solved_extensive_form_list'][i]['value'])

print()

print('3voter game NE(s):')
game = gameCreator('3voter.txt')
solved_game = gameSolver(game)
for i in range(0, len(solved_game['ne_list'])):
    print(solved_game['ne_list'][i], ':', solved_game['solved_extensive_form_list'][i]['value'])

print()

print('Another Game\'s game NE(s):')
game = gameCreator('another_game.txt')
solved_game = gameSolver(game)
for i in range(0, len(solved_game['ne_list'])):
    print(solved_game['ne_list'][i], ':', solved_game['solved_extensive_form_list'][i]['value'])

print()
