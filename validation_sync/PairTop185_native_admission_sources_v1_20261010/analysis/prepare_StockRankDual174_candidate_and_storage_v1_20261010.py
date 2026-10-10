"""Freeze either selected rank leaf or complementary two-leaf graph after complete44."""
from pathlib import Path
import sys,importlib,re
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def save(name,text):
    p=A/name;assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p
def route(text):
    mapping={'StockEmbedding173':'StockRankDual174','stock_embedding173':'stock_rank_dual174','stock_embedding36_selected_native14':'stock_rank_dual44_selected_native14','StockEmbedding36_selected_native14':'StockRankDual44_selected_native14','stock_embedding_after_complete_qualified_parent_native_stage_v1_20261010':'stock_rank_dual44_selected_native_stage_v1_20261010','predict_stock_embedding_complete_qualified_parent_scheme_v1_20261010':'predict_stock_rank_dual44_complete_parent_scheme_v1_20261010','stock_embedding_after_complete_qualified_parent_v1_20261010':'stock_rank_dual44_after_complete_parent_v1_20261010','normalize_completed_stock_embedding36_after172_v1_20261010':'normalize_stock_rank_and_dual44_after173_v2_20261010','stock_embedding_complete_parent_native_replay_verification':'stock_rank_dual44_complete_parent_native_replay_verification','passed_actual_complete_qualified_parent_stock_embedding_two_full_native_independent_replays_and_cold80':'passed_actual_whole_qualified_parent_frontier233_two_full_independent_replays_and_cold80','pilot36':'pilot44','normalized36':'normalized44','anchor36':'anchor44','actual36':'actual44','all36':'all44','第173轮':'第174轮'}
    return re.sub('|'.join(re.escape(k) for k in sorted(mapping,key=len,reverse=True)),lambda m:mapping[m.group()],text)
def main():
    assert allowed();inputs=[];outputs=[]
    source=A/'stock_embedding173_storage_v1_20261010.py';inputs.append(source);text=route(source.read_text(encoding='utf8')).replace('r173','r174').replace('round173','round174').replace('number == 173','number == 174').replace('qa_v84','qa_v85').replace('QA84','QA85')
    storage=save('stock_rank_dual174_storage_v1_20261010.py',text);outputs.append(storage)
    source=A/'prepare_StockEmbedding173_selected_candidate_v1_20261010.py';inputs.append(source);text=route(source.read_text(encoding='utf8'))
    text=text.replace("len(pilot['records'])==36","len(pilot['records'])==44").replace('parent_number in (170,172)','parent_number in (170,173)').replace('expected_scored_records=36','expected_scored_records=44').replace("'scored_records':36","'scored_records':44")
    text=text.replace("GRAPH_KEY='stock_rank_dual44_after_complete_parent_v1_20261010'","GRAPH_KEY='stock_rank_dual44_after_complete_parent_v1_20261010'\nCODECS={'CDF':'BF16Medium153_complete_parent_rank_CDF_v1_20261009','valid_pool_protection_v1':'protected_upper_tail_rank_permutation_v1_20261010','official_Top_protection_v2':'protected_official_top_rank_permutation_v2_20261010'}")
    begin=text.index('    from normalize_stock_rank_and_dual44_after173_v2_20261010 import RECIPES');end=text.index('    freeze=Path(',begin)
    components="""    leaves=best['native_bank_components'];assert len(leaves) in (1,2)
    assert (len(leaves)==2)==(cfg['stage_kind']=='stock_return_rank_embedding_consensus')
    transform=importlib.import_module(CODECS[cfg['codec']]).transform
    components=[]
    for leaf in leaves:
        bank=Path(leaf['bank']);CONFIG=importlib.import_module(native_stage.BACKENDS[leaf['recipe']][0]).CONFIG
        info=read(bank/'2025/info.json');meta=info['training_meta']
        assert info['status']=='passed_actual_complete_mature_BF16_micro_annual_model' and info['year']==2025
        assert info['configuration']==CONFIG and meta['last']<meta['cutoff_exclusive']==fold_cutoff(2025) and meta['last_label_end']<=meta['cutoff_exclusive']
        component={'name':leaf['name'],'source_path':str(bank/'2025/model.joblib'),'path':str(CANDIDATE/(leaf['name']+'_final2025.joblib')),'sha256':info['model_sha256'],'configuration':CONFIG,'training_info':info}
        assert sha(component['source_path'])==component['sha256'];pins[component['source_path']]=component['sha256'];components.append(component)
"""
    text=text[:begin]+components+text[end:]
    begin=text.index("    own_pointer='actual_StockEmbeddingSmall512_full5_independent_location_v1_20261009.json'");end=text.index('    with LockedReadHashCache(pins)',begin)
    own="""    own_pointers={'stock_embedding16_cross120_return1d_recent252_small512_BF16_e24':'actual_StockEmbeddingSmall512_full5_independent_location_v1_20261009.json','stock_rank_embedding16_cross120_rank1d_recent252_small512_BF16_e24':'actual_StockRankEmbeddingSmall512_full5_independent_location_v1_20261009.json'}
    neural_folders=[Path(read(A/own_pointers[leaf['recipe']])['output']) for leaf in leaves]
    neural_paths=[folder/'combined_raw.parquet' for folder in neural_folders]
    neural_folder=neural_folders[0];neural_path=neural_paths[0]
    for p in [raw_path,*neural_paths,*[f/'verification.json' for f in neural_folders]]:pins[str(p)]=sha(p)
"""
    text=text[:begin]+own+text[end:]
    text=text.replace("        assert cfg['stage_kind']=='stock_embedding_return1d_direct' and cfg['decay'] is None","        assert cfg['decay'] is None\n        if len(leaves)==2:\n            import dual_target_daily_rank_consensus_v1_20261010 as dual\n            second=pl.read_parquet(neural_paths[1]);assert second.select(['ts_code','trade_date']).equals(frame.select(['ts_code','trade_date']))\n            neural=dual.transform(neural,second['pred_raw'].to_numpy(),dates,cfg['mean_weight'])\n            del second\n        else:assert cfg['stage_kind']=='stock_rank_embedding_rank1d_direct'")
    text=text.replace("'native_component':component","'native_components':components").replace('native_stage.CODECS','CODECS')
    text=text.replace("unique={c['sha256'] for c in parent_prediction['models'].values()}|{component['sha256']}","unique={c['sha256'] for c in parent_prediction['models'].values()}|{c['sha256'] for c in components}")
    old="'native_component_names':list(dict.fromkeys([*parent_record['native_component_names'],*([cfg['model']] if component['sha256'] not in {m['sha256'] for m in parent_prediction['models'].values()} else [])]))"
    new="'native_component_names':list(dict.fromkeys([*parent_record['native_component_names'],*[c['name'] for c in components if c['sha256'] not in {m['sha256'] for m in parent_prediction['models'].values()}]]))"
    assert old in text;text=text.replace(old,new)
    text=text.replace("'actual6_mature_native_and_full_independent_controls':str(neural_folder/'verification.json')","'actual_own_mature_banks_and_full_independent_controls':[str(f/'verification.json') for f in neural_folders]")
    candidate=save('prepare_StockRankDual174_selected_candidate_v1_20261010.py',text);outputs.append(candidate)
    source=A/'seal_StockEmbedding173_selected_candidate_v1_20261010.py';inputs.append(source);text=route(source.read_text(encoding='utf8'))
    seal=save('seal_StockRankDual174_selected_candidate_v1_20261010.py',text);outputs.append(seal)
    c=importlib.import_module(candidate.stem);s=importlib.import_module(storage.stem)
    assert c.GRAPH_KEY=='stock_rank_dual44_after_complete_parent_v1_20261010' and len(s.OUTPUTS)==6 and s.EBASE.name=='第174轮_20261010'
    assert "'native_components':components" in text or "'native_components':components" in candidate.read_text(encoding='utf8')
    create(A/'stock_rank_dual174_candidate_sources_preparation_v1_20261010.json',{'status':'compiled44_selected_single_rank_or_dual_embedding_candidate_freeze_and_six_E_outputs_no_future_read','input_sha256':{str(p):sha(p) for p in [Path(__file__),*inputs,*outputs,A/'stock_rank_dual44_selected14_routes_admission_v1_20261010.json']},'expected_records':44,'parent_rounds':[170,173],'new_native_fits':0,'new_quality_scores':0,'actual_selected_full_future_and_registry_QA85_main_pending':True,'test_labels_read':False})
    print({'candidate44_sources':'prepared','actual_full_future_inference':False},flush=True)
if __name__=='__main__':main()
