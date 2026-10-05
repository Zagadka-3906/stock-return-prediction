"""Preserve historical layer parameters when reconstructing later frozen schemes.

The flat last-round configuration cannot represent every earlier retention
floor.  This graph instead reads each selected round's own configuration.
"""
from copy import deepcopy

ROLES=('membership','top','rest')
EARLY_GROUPS=('diverse_augmentation','secondary_augmentation','final_augmentation','linear_augmentation')
LATE_GROUPS=('regularization','stacking','neural_tuning','catboost_tuning',
             'expanded_stacking','additive_ridge','fourier_ridge',
             'nonlinear_stacking','fourier_tuning')
ROLE_ROUNDS={31+2*index:group for index,group in enumerate(LATE_GROUPS)}
PURE_ROUNDS=tuple(number+1 for number in ROLE_ROUNDS)
SHIFT_FIELDS=('final_limit_delta','linear_limit_delta')+tuple(group+'_limit_delta' for group in LATE_GROUPS)


def prior_delta(configuration,group):
    delta=configuration['limit_up_delta']
    stop=SHIFT_FIELDS.index(group+'_limit_delta')
    # Match historical left-associative additions exactly, including rounding.
    for key in SHIFT_FIELDS[:stop]:
        delta=delta+configuration.get(key,0.)
    return delta


def compile_graph(configurations,through=49):
    assert 30<=through<=49
    assert all(number in configurations for number in range(30,through+1))
    root={'kind':'complete_r30','round':30,'configuration':deepcopy(configurations[30])}
    layers=[];discarded=[];temporal=None
    for number in range(31,through+1):
        cfg=configurations[number]
        if number in ROLE_ROUNDS:
            group=ROLE_ROUNDS[number]
            layers.append({'name':group,'round':number,'group':group+'_augmentation',
                'specs':deepcopy(cfg[group+'_augmentation']),
                'retention':cfg['retention'],'original_delta':prior_delta(cfg,group),
                'additional_delta':cfg[group+'_limit_delta']})
        elif number in PURE_ROUNDS:
            if cfg['standalone_replacement']:
                assert cfg['standalone'] is not None
                discarded.append({'replacement_round':number,'previous_root_round':root['round'],
                                  'discarded_layer_rounds':[layer['round'] for layer in layers]})
                root={'kind':'standalone','round':number,'configuration':deepcopy(cfg)}
                layers=[]
        elif number==49:
            temporal=deepcopy(cfg['temporal_postprocessing'])
        else:
            raise AssertionError(number)
    axes=[]
    if root['kind']=='complete_r30':
        base=root['configuration']
        for group in EARLY_GROUPS:
            if base.get('standalone') and group in EARLY_GROUPS[:2]:
                continue
            for role,spec in base[group].items():
                if spec['weight']>0:
                    axes.append({'round':30,'group':group,'role':role,'model':spec['model'],'anchor':spec['weight']})
    for layer in layers:
        for role,spec in layer['specs'].items():
            if spec['weight']>0:
                axes.append({'round':layer['round'],'group':layer['group'],'role':role,
                             'model':spec['model'],'anchor':spec['weight']})
    return {'through_round':through,'root':root,'layers':layers,'temporal_postprocessing':temporal,
            'discarded_branches':discarded,'active_weight_axes':axes,
            'each_layer_uses_its_own_historical_retention':True}


def with_weight_overrides(graph,overrides):
    result=deepcopy(graph)
    allowed={(axis['round'],axis['group'],axis['role']) for axis in graph['active_weight_axes']}
    assert set(overrides).issubset(allowed)
    for (number,group,role),weight in overrides.items():
        assert 0.<=weight<=.8
        if number==30:
            result['root']['configuration'][group][role]['weight']=weight
        else:
            layer=next(item for item in result['layers'] if item['round']==number)
            assert layer['group']==group
            layer['specs'][role]['weight']=weight
    return result
