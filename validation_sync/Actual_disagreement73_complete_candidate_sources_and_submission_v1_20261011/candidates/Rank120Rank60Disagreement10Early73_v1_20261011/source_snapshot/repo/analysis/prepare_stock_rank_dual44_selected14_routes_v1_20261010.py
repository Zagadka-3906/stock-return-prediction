"""Build actual dynamic one/two-leaf selected14 replay and queue after complete44."""
from pathlib import Path
import sys,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service
def save(name,text):
    p=A/name;assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p
def main():
    assert allowed()
    src=A/'predict_stock_dual_embedding_complete_parent_scheme_v1_20261010.py';text=src.read_text(encoding='utf8')
    text=text.replace('stock_dual_embedding_after_complete_parent_native_stage_v1_20261010','stock_rank_dual44_selected_native_stage_v1_20261010').replace('stock_dual_embedding_complete_parent_native_replay_verification.json','stock_rank_dual44_complete_parent_native_replay_verification.json')
    text=text.replace("assert (len(components)==2)==(spec['stage_kind']=='stock_return_rank_embedding_consensus')","assert len(components) in (1,2) and (len(components)==2)==(spec['stage_kind']=='stock_return_rank_embedding_consensus')")
    predictor=save('predict_stock_rank_dual44_complete_parent_scheme_v1_20261010.py',text)
    src14=A/'qualify_stock_embedding36_selected_native14_v1_20261010.py';text=src14.read_text(encoding='utf8')
    for old,new in [('stock_embedding36_selected_native14','stock_rank_dual44_selected_native14'),('actual_stock_embedding36_after172_normalization_queue_v1_20261010','actual_stock_rank_dual44_after173_normalization_v2_20261010'),('actual_stock_embedding_six_state_native42_v2_20261010','actual_stock_rank_embedding_six_state_native42_v1_20261010'),('stock_embedding_after_complete_qualified_parent_native_stage_v1_20261010','stock_rank_dual44_selected_native_stage_v1_20261010'),('normalize_completed_stock_embedding36_after172_v1_20261010','normalize_stock_rank_and_dual44_after173_v2_20261010'),('actual_stock_embedding_complete36_after172_location_v1_20261010','actual_stock_rank_dual44_after173_location_v1_20261010'),('pilot36','pilot44'),('==36','==44'),('normalized36','normalized44'),('anchor36','anchor44'),('predict_stock_embedding_complete_qualified_parent_scheme_v1_20261010.py',predictor.name),('stock_embedding_actual_four_nested_parent_hooks_CPU_controls_v1_20261010.json','stock_dual_embedding_five_parent_hooks_CPU_controls_v1_20261010.json')]:text=text.replace(old,new)
    old="    bank=Path('E:/赛题五_本机临时')/recipes[cfg['recipe']][1];native=importlib.import_module(stage.BACKENDS[cfg['recipe']][0])"
    assert old in text
    text=text.replace(old,"    leaves=best['native_bank_components'];assert len(leaves) in (1,2)\n    bank=Path(leaves[0]['bank']);native=importlib.import_module(stage.BACKENDS[leaves[0]['recipe']][0])")
    text=text.replace("stage.BACKENDS[cfg['recipe']][1]","stage.BACKENDS[leaves[0]['recipe']][1]")
    marker="    create(OUT/'selected_native14_frozen_before_saved_replays.json'"
    insert="    for leaf in leaves:\n        for source_module in stage.BACKENDS[leaf['recipe']]:\n            p=A/(source_module+'.py');pins[str(p)]=sha(p)\n        own_bank=Path(leaf['bank'])\n        for p in [own_bank/'verification.json',*[own_bank/str(y)/n for y in range(2020,2026) for n in ('info.json','model.joblib')]]:pins[str(p)]=sha(p)\n    for p in [A/'stock_rank_dual44_selected_native_stage_v1_20261010.py',A/'stock_dual_embedding_after_complete_parent_native_stage_v1_20261010.py',A/'stock_rank_embedding_after_complete_qualified_parent_native_stage_v1_20261010.py',A/'stock_identity_embedding_network_v1_20261010.py',A/'stock_rank_dual44_selected14_routes_admission_v1_20261010.json']:pins[str(p)]=sha(p)\n"
    text=text.replace(marker,insert+marker)
    begin=text.index("        info=read(bank/str(year)/'info.json')");end=text.index('        sourceparent=',begin)
    text=text[:begin]+"        component=[]\n        for leaf in leaves:\n            own_bank=Path(leaf['bank']);own_native=importlib.import_module(stage.BACKENDS[leaf['recipe']][0]);info=read(own_bank/str(year)/'info.json')\n            component.append({'name':leaf['name'],'path':str(own_bank/str(year)/'model.joblib'),'sha256':info['model_sha256'],'training_info':info,'configuration':own_native.CONFIG})\n"+text[end:]
    text=text.replace("'actual_saved_states':6,","'actual_saved_states':6*len(leaves),'actual_banks':len(leaves),")
    qualifier=save('qualify_stock_rank_dual44_selected_native14_v1_20261010.py',text)
    for p in (predictor,qualifier):importlib.import_module(p.stem)
    create(A/'stock_rank_dual44_selected14_routes_admission_v1_20261010.json',{'status':'compiled_imported_dynamic_one_or_two_bank_selected14_and_full_parent_predictor_sources_actual_selected_controls_pending','expected_cases':14,'expected_cold':14,'expected_prefit_rejections':7,'saved_states':{'rank_only':6,'return_rank_consensus':12},'input_sha256':{str(p):sha(p) for p in [Path(__file__),src,src14,predictor,qualifier,A/'stock_rank_dual44_selected_native_stage_v1_20261010.py']},'full174_candidate_freeze_and_registry_not_yet_built':True,'new_quality_scores':0,'future_X_read':False,'test_labels_read':False})
    row=start_service('StockRankDual44_selected_native14_v1_20261010',qualifier.name,[],{str(qualifier):sha(qualifier)})
    create(A/'actual_stock_rank_dual44_selected_native14_activation_v1_20261010.json',row)
    print({'actual_selected44_native14':'queued','full174_candidate_freeze_and_registry_pending':True},flush=True)
if __name__=='__main__':main()
