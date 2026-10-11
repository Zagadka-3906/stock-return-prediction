"""Replay complete fixed-consensus graph roles and independent standalone outputs."""
from copy import deepcopy
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
from whole_scheme_replay_runtime_20261004 import ValidationContext,raw_sources
from whole_scheme_future_runtime_20261004 import graph_native_models,candidate_models
from types import SimpleNamespace
import classifier_consensus_model_sources_20261005 as router
import build_classifier_consensus_bank_20261005 as native
bank=SimpleNamespace(ROOT=ROOT,OUT=native.OUT,CONFIGS=router.NEW_CONFIGS,all_configs=router.CONFIGS,
    engine=native.engine,YEARS=native.YEARS,SOURCE=native.SOURCE,native=native,
    read=native.read,dump=native.dump,sha=native.sha,log=native.log)

ROLES=('membership','top','rest')


def empty_roles():return {role:{'model':'none','weight':0.} for role in ROLES}


def cumulative_delta(graph):
    root=graph['root'];cfg=root['configuration'];value=cfg['limit_up_delta']
    if root['kind']=='complete_r30':
        value=value+cfg.get('final_limit_delta',0.)
        value=value+cfg.get('linear_limit_delta',0.)
    for node in graph['layers']:value=value+node['additional_delta']
    return value


def append_role_layer(graph,number=89):
    result=deepcopy(graph)
    assert not any(node['round']==number for node in result['layers'])
    result['layers'].append({'name':'classifier_consensus','round':number,'group':'classifier_consensus_augmentation',
        'specs':empty_roles(),'retention':.98,'original_delta':cumulative_delta(graph),'additional_delta':0.})
    result['through_round']=number
    return result


def standalone_graph(graph,name,postprocessing,retention=.98,delta=.075,number=90):
    result=deepcopy(graph);cfg=deepcopy(graph['root']['configuration'])
    for key in cfg:
        if key.endswith('_augmentation'):cfg[key]=empty_roles()
        elif key.endswith('_limit_delta'):cfg[key]=0.
    cfg.update(standalone={'model':name,'postprocessing':deepcopy(postprocessing)},
        standalone_replacement=True,retention=retention,limit_up_delta=delta)
    result['discarded_branches']=[*result.get('discarded_branches',[]),
        {'replacement_round':number,'previous_root_round':graph['root']['round'],
         'discarded_layer_rounds':[node['round'] for node in graph['layers']]}]
    result.update(root={'kind':'standalone','round':number,'configuration':cfg},layers=[],
        active_weight_axes=[],through_round=number)
    return result


def native_sources(graph,candidate_overrides=None):
    overrides=candidate_overrides or {};result={}
    for name,number in graph_native_models(graph).items():
        if name in bank.CONFIGS:
            info=bank.read(router.source_dir(name)/'info_2025.json')
            source=ROOT/f'analysis/classifier_consensus_future_qa_20261005/{name}.joblib'
            assert info['status']=='passed' and bank.sha(source)==info['model_sha256']
            result[name]={'path':str(source),'sha256':info['model_sha256'],'training_info':info,
                'configuration':deepcopy(bank.CONFIGS[name]),'source_bank':str(router.source_dir(name))}
        else:
            candidate=Path(overrides.get(number,ROOT/f'candidates/optimization_20261003_r{number}'))
            matches=[item for key,item in candidate_models(candidate).items()
                if key.endswith('_'+name) and Path(item['path']).suffix=='.joblib']
            assert matches and len({item['sha256'] for item in matches})==1,(name,number)
            result[name]=deepcopy(matches[0])
    return result


def prepare_raw(output,names=None):
    import numpy as np
    import polars as pl
    names=tuple(bank.CONFIGS) if names is None else tuple(names)
    folder=Path(output)/'raw';folder.mkdir(exist_ok=True)
    keys=pl.read_parquet(ROOT/'analysis/connected_validation_20261002/combined_fold_frame.parquet',columns=bank.engine.KEYS)
    for name in names:
        path=folder/f'{name}.npy'
        if path.exists():continue
        parts=[]
        for year in bank.YEARS:
            directory=router.source_dir(name)
            info=bank.read(directory/f'info_{year}.json');source=directory/f'raw_{year}.parquet'
            assert info['status']=='passed' and info['model_reload_bit_identical'] and bank.sha(source)==info['prediction_sha256']
            meta=info['training_meta'];assert meta['last']<meta['cutoff_exclusive'] and meta['last_label_end']<=meta['cutoff_exclusive']<year*10000+101
            frame=pl.read_parquet(source);assert frame.select(bank.engine.KEYS).equals(keys.filter(pl.col('trade_date')//10000==year))
            parts.append(frame['pred_raw'].to_numpy())
        raw=np.concatenate(parts);assert len(raw)==5635800 and np.isfinite(raw).all();np.save(path,raw)
    return {name:folder/f'{name}.npy' for name in names}


class AdaptiveGraphContext(ValidationContext):
    def weights_for(self,spec):
        from agreement_gated_weights_20261005 import context_weight
        return context_weight(self,spec,super().weights_for(spec))
    def __init__(self,graph,scoring,paths):
        self._basis_all_paths=deepcopy(paths)
        super().__init__(graph,scoring=scoring,paths=paths)
    def configure(self,configuration):
        graph=configuration['whole_scheme_graph']
        if hasattr(self,'_whole_base') and (
                graph['root']['kind']!=self._whole_graph['root']['kind'] or
                graph['root']['round']!=self._whole_graph['root']['round']):
            paths=self._basis_all_paths;scoring=self.scoring
            fresh=ValidationContext(graph,scoring=scoring,paths=paths)
            self.__dict__.clear();self.__dict__.update(fresh.__dict__);self._basis_all_paths=paths
        else:super().configure(configuration)


def all_paths(graph,output):
    paths={name:items[0] for name,items in raw_sources(graph).items()}
    paths.update({name:Path(output)/f'raw/{name}.npy' for name in bank.CONFIGS})
    return paths
