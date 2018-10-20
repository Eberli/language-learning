# language-learning/src/grammar_inducer.py                              81012
from copy import deepcopy
from .category_learner import cats2list
from .widgets import display, html_table
from .utl import UTC

def induce_grammar(categories, links, verbose='none'):      # 81012
    # categories: {'cluster': [], 'words': [], ...}
    # links: pd.DataFrame (legacy)
    if verbose in ['max','debug']:
        print(UTC(),':: induce_grammar: categories.keys():', categories.keys())
    rules = deepcopy(categories)

    clusters = [i for i,x in enumerate(rules['cluster']) if i>0 and x is not None]
    word_clusters = dict()
    for i in clusters:
        for word in rules['words'][i]:
            word_clusters[word] = i

    if verbose in ['max','debug']:
        print('induce_grammar: rules.keys():', rules.keys())
        print('induce_grammar: clusters:', clusters)
        print('induce_grammar: word_clusters:', word_clusters)
        print('induce_grammar: rules ~ categories:')

    for cluster in clusters:
        djs = []
        for rule in categories['disjuncts'][cluster]:  #FIXME: categories ⇒ rules 80621
            # 'a- & was-' ⇒ (-9,-26)
            #+TODO? (-x,-y,z) ⇒ (-x,z), (-y,z) ?
            if type(rule) is str:
                x = rule.split()
                lefts = []
                rights = []
                for y in x:
                    if (y not in ['&', ' ', '']) and (y[:-1] in word_clusters):
                        if y[-1] == '+':
                            rights.append(word_clusters[y[:-1]])
                        elif y[-1] == '-':
                            lefts.append(-1 * word_clusters[y[:-1]])
                        else:
                            print('no sign?', y, 'in', x)  #TODO:ERROR?
                lefts.reverse()
                dj = lefts + rights
                if len(dj) > 0:
                    djs.append(tuple(dj))
                if verbose == 'debug':
                    print('induce_gramma: cluster', cluster, '::', rule, '⇒', tuple(dj))
            #TODO? +elif type(rule) is tuple? connectors - tuples?
        rules['disjuncts'][cluster] = set(djs)
        if verbose == 'debug':
            print('induce_grammar: rules["disjuncts"]['+str(cluster)+']', rules['disjuncts'][cluster])
    #rules['djs'] = copy.deepcopy(rules['disjuncts'])  #TODO: check jaccard with tuples else replace with numbers

    if verbose == 'debug':
        print('induce_grammar: updated disjuncts:')
        display(html_table([['Code','Parent','Id','Quality','Words', 'Disjuncts', 'djs','Relevance','Children']] \
            + [x for i,x in enumerate(cats2list(rules)) if i < 32]))

    return rules, {'learned_rules': \
                    len([x for i,x in enumerate(rules['parent']) if x==0 and i>0]), \
                   'total_clusters': len(rules['cluster']) - 1}


#Notes:

#80802 poc05.py restructured: induce_grammar ⇒ grammar_inducer.py v~80625
