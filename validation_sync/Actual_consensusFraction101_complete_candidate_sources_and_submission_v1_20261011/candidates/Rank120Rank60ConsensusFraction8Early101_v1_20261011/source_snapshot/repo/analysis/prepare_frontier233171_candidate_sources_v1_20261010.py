"""Prepare fresh selected233 candidate sources without dispatching future inference."""
from pathlib import Path
import ast,sys
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import create,sha

def replace(text,before,after,count=1):
    assert text.count(before)==count,(before,text.count(before),count)
    return text.replace(before,after)

def common(text):
    for before,after in [('Cross120170','Frontier233171'),('cross120170_storage','frontier233171_storage'),('第170轮','第171轮'),('selected_anchor132','selected_anchor233'),('actual132_selected','actual233_selected'),('pilot132','pilot233')]:text=text.replace(before,after)
    return text

def main():
    from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
    assert allowed();originals=[];outputs=[]
    source=A/'cross120170_storage_v1_20261010.py';originals.append(source)
    text=common(source.read_text(encoding='utf8')).replace('_r170','_r171').replace('round170','round171').replace('qa_v81','qa_v82').replace("'QA81'","'QA82'")
    text=replace(text,'assert number == 169','assert number == 171')
    # All large registration artifacts also reside on E; registry admits this exact empty junction.
    text=replace(text,"OUTPUTS = {","OUTPUTS = {ROOT/'analysis/optimization_20261003_r171':EBASE/'registered_release',")
    def emit(name,text):
        target=A/name;assert not target.exists(),target;ast.parse(text);target.write_text(text,encoding='utf8');outputs.append(target)
    emit('frontier233171_storage_v1_20261010.py',text)
    source=A/'prepare_cross120170_selected_candidate_v4_20261010.py';originals.append(source);text=common(source.read_text(encoding='utf8'))
    text=text.replace('qualify_cross120_two_target132_selected_native14_v3','qualify_frontier233_selected_native_stage_v2').replace('Cross120170_selected_native14_v3','Frontier233_selected_native_stage_v2')
    # common() changes service prefix before the replacement above.
    text=text.replace('Frontier233171_selected_native14_v3','Frontier233_selected_native_stage_v2')
    text=text.replace("GRAPH_KEY='cross120_after_complete169_native_v1_20261010'","GRAPH_KEY='frontier233_after_complete_qualified_parent_v1_20261010'")
    text=text.replace('import cross120_after_complete169_native_stage_v2_20261010 as native_stage','import frontier233_after_complete_parent_native_stage_v1_20261010 as native_stage')
    text=text.replace('predict_cross120170_complete169_scheme_v1','predict_frontier233_complete_parent_scheme_v1').replace('prepare_cross120170_selected_candidate','prepare_frontier233171_selected_candidate').replace('seal_cross120170_selected_candidate','seal_frontier233171_selected_candidate')
    text=text.replace("A/'cross120170_candidate_and_seal_sources_preparation_v1_20261010.json'","A/'frontier233171_candidate_sources_preparation_v1_20261010.json'")
    text=text.replace('passed_normalized132_actual_complete_training_only_official_records','passed_normalized233_actual_TRAIN_official_records_selected_stage_and_frozen_full_inference_pending').replace("len(pilot['records'])==132","len(pilot['records'])==233").replace('selected_by_all132','selected_by_all233')
    text=replace(text,"parent_number=cfg['anchor_round'] if cfg['model'] is None else pilot['actual_scheme_base_round']","parent_number=cfg['anchor_round']")
    text=replace(text,'parent_number in (168,169)','parent_number in (169,170)')
    text=replace(text,"cfg['model'] is None or cfg['weight']==0.","cfg['stage_kind']=='anchor'")
    start=text.index('    assert parent_number==169 and');end=text.index("    freeze=Path(",start)
    text=text[:start]+'''    assert cfg['stage_kind'] in ('dual120_rank_consensus','parent_only_budget_stability')
    components=[];neural_paths=[];independent_proofs=[]
    if cfg['stage_kind']=='dual120_rank_consensus':
        assert parent_number==169 and 0.<cfg['weight']<=1. and cfg['sign'] in (-1.,1.)
        from cross120_after_complete169_native_stage_v2_20261010 import BACKENDS
        pointers={'cross120recent252forward5huber050':'actual_BF16Cross120Recent252Forward5Huber050173_full5_independent_location_v1_20261009.json','cross120recent252rank5huber050':'actual_BF16Cross120Recent252Rank5Huber050174_full5_independent_location_v1_20261009.json'}
        for leaf in best['native_bank_components']:
            bank=Path(leaf['bank']);info=read(bank/'2025/info.json');meta=info['training_meta'];CONFIG=importlib.import_module(BACKENDS[leaf['recipe']][0]).CONFIG
            assert info['status']=='passed_actual_complete_mature_BF16_micro_annual_model' and info['year']==2025
            assert info['configuration']==CONFIG and meta['last']<meta['last_label_end']<meta['cutoff_exclusive']==fold_cutoff(2025)
            component={'name':leaf['name'],'recipe':leaf['recipe'],'source_path':str(bank/'2025/model.joblib'),'path':str(CANDIDATE/(leaf['name']+'_final2025.joblib')),'sha256':info['model_sha256'],'configuration':CONFIG,'training_info':info}
            assert sha(component['source_path'])==component['sha256'];pins[component['source_path']]=component['sha256'];components.append(component)
            neural_folder=Path(read(A/pointers[leaf['recipe']])['output']);neural_paths.append(neural_folder/'combined_raw.parquet');independent_proofs.append(str(neural_folder/'verification.json'))
        assert len(components)==2 and [c['name'] for c in components]==best['ordered_native_components']
    else:
        assert cfg['weight']==cfg['sign']==1. and best['ordered_native_components']==[]
''' +text[end:]
    start=text.index('    # Resolve saved raw-panel locations');end=text.index('    with LockedReadHashCache',start)
    text=text[:start]+"    pins.update({str(p):sha(p) for p in [raw_path,*neural_paths]})\n"+text[end:]
    start=text.index('        neural_frame=pl.read_parquet(');end=text.index('        assert hashlib.sha256',start)
    text=text[:start]+'''        raw=np.load(raw_path,mmap_mode='r')
        if components:
            signals=[]
            for path in neural_paths:
                neural_frame=pl.read_parquet(path);assert neural_frame.select(['ts_code','trade_date']).equals(frame.select(['ts_code','trade_date']));signals.append(neural_frame['pred_raw'].to_numpy())
            from dual_target_daily_rank_consensus_v1_20261010 import transform as consensus,pandas_oracle as consensus_oracle
            neural=consensus(*signals,dates,cfg['mean_weight']);oracle=consensus_oracle(*signals,dates,cfg['mean_weight']);assert np.array_equal(neural.view('u8'),oracle.view('u8'))
            from cross120_after_complete169_native_stage_v2_20261010 import CODECS
            codec=importlib.import_module(CODECS[cfg['kind']]);args=(dates,flags,valid,*((cfg['role'],cfg['weight'],cfg['sign']) if cfg['kind']=='CDF' else (cfg['weight'],cfg['protect_fraction'],cfg['sign'])))
            selected=codec.transform(raw,neural,*args);oracle=codec.pandas_oracle(raw,neural,*args)
        else:
            import budgeted_neural_Top_projection_v1_20261010 as codec
            args=(dates,flags,valid,1.,cfg['budget_fraction'],cfg['margin'],1.)
            selected=codec.transform(raw,np.asarray(raw,dtype=np.float64),*args);oracle=codec.pandas_oracle(raw,np.asarray(raw,dtype=np.float64),*args)
        assert np.array_equal(selected.view('u8'),oracle.view('u8'))
''' +text[end:]
    text=text.replace('actual_all132','actual_all233').replace("str(neural_folder/'verification.json')","independent_proofs")
    # Correct the single occurrence inside the component loop, which must append a path string.
    text=text.replace('independent_proofs.append(independent_proofs)',"independent_proofs.append(str(neural_folder/'verification.json'))")
    text=text.replace("'actual_selected14_native14_cold7_prefit_controls'","'actual_selected14_native_or_pure_postprocessing_and14_cold_controls'")
    start=text.index('        graph[GRAPH_KEY]=');end=text.index('        winner=deepcopy',start)
    text=text[:start]+'''        graph[GRAPH_KEY]={**cfg,'position':'after_complete_qualified_parent','native_components':components,'selected_stage_source':str(native_out/'verification.json'),'original_complete_parent_round':parent_number,'original_complete_parent_graph_preserved':True,'transformation':'two own120 daily rank forecasts then protected permutation, or sequential parent-only Top stability with original first-date state'}
''' +text[end:]
    text=text.replace('expected_scored_records=132','expected_scored_records=233').replace("|{component['sha256']}","|{c['sha256'] for c in components}").replace("'scored_records':132","'scored_records':233")
    text=replace(text,"*([cfg['model']] if component['sha256'] not in {m['sha256'] for m in parent_prediction['models'].values()} else [])","*[c['name'] for c in components if c['sha256'] not in {m['sha256'] for m in parent_prediction['models'].values()}]")
    text=text.replace("'actual6_mature_native_and_full_independent_controls'","'actual_own120_mature_native_and_full_independent_controls'")
    emit('prepare_frontier233171_selected_candidate_v1_20261010.py',text)
    source=A/'seal_cross120170_selected_candidate_v1_20261010.py';originals.append(source);text=common(source.read_text(encoding='utf8'))
    text=text.replace('cross120170_complete_parent_native_replay_verification','frontier233_complete_parent_native_replay_verification').replace('passed_actual_complete169_cross120_two_full_native_independent_replays_and_cold80','passed_actual_whole_qualified_parent_frontier233_two_full_independent_replays_and_cold80')
    text=text.replace('cross120_two_target132_selected_native14_v1','frontier233_selected_native_stage_v1')
    emit('seal_frontier233171_selected_candidate_v1_20261010.py',text)
    create(A/'frontier233171_candidate_sources_preparation_v1_20261010.json',{'status':'compiled_fresh233_candidate_seal_storage_sources_pending_actual_selected_stage_and_full_inference','input_sha256':{str(p):sha(p) for p in [Path(__file__),*originals,*outputs]},'stage_kinds':['anchor','dual120_rank_consensus','parent_only_budget_stability'],'new_quality_scores':0,'actual_future_X_read':False,'test_labels_read':False})
    print({'sources':len(outputs),'actual_future_dispatch':False},flush=True)

if __name__=='__main__':main()
