"""Select highest actual connected TRAIN score among two frozen families and qualified anchors."""
from pathlib import Path
import sys,time,hashlib
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
OUT=Path('E:/赛题五_本机临时/stock_rank_dual_complete44_after173_v1_20261010')
RECIPES={'stock_embedding16_cross120_return1d_recent252_small512_BF16_e24':('rank_MLP512_StockEmbedding16_Cross120Recent252ReturnHuber050_seed09_e24','stock_embedding_small512_BF16_bank6_v1_20261010'),'stock_rank_embedding16_cross120_rank1d_recent252_small512_BF16_e24':('rank_MLP512_StockRankEmbedding16_Cross120Recent252RankHuber010_seed09_e24','stock_rank_embedding_small512_BF16_bank6_v1_20261010')}
def main():
    assert allowed();planpath=A/'stock_rank_dual44_after173_selection_plan_v1_20261010.json';plan=read(planpath)
    closed('StockEmbedding173_complete36_family_v3_20261010')
    for family in plan['families']:
        closed(family['actual_service']);closed(family['publisher'])
        assert read(A/family['main_receipt'])['status']=='pushed_and_remote_head_verified'
    import numpy as np
    pins={str(p):sha(p) for p in [Path(__file__),planpath]};records=[];anchors={};hashes={}
    for number in (170,173):
        release=A/f'optimization_20261003_r{number}';candidate=ROOT/f'candidates/optimization_20261003_r{number}'
        receipt=A/f'github_validation_sync_main_20261005/round{number}_receipt.json'
        assert read(receipt)['status']=='pushed_and_remote_head_verified' and read(release/'full_registration_execution.json')['status']=='passed'
        winner=read(release/'selection.json')['winner'];metrics=read(release/'calibrated_csv_official.json')['metrics'];assert winner['metrics']==metrics
        models=read(candidate/'verification.json')['models'];hashes[number]={r['sha256'] for r in models.values()};assert len(models)==len(hashes[number])
        value=np.load(release/'selected_validation.npy',mmap_mode='r');numeric=hashlib.sha256(memoryview(np.ascontiguousarray(value)).cast('B')).hexdigest();capsule=Path(winner['official_score_cache']['official_metrics_source']);assert read(capsule)['metrics']==metrics
        row={'case':len(records),'configuration':{'stage_kind':'anchor','anchor_round':number,'model':None,'recipe':None,'weight':0.,'sign':1.,'codec':None,'decay':None},'metrics':metrics,'connected_final_score':metrics['final_score'],'expected_unique_native_models':len(models),'prediction_numeric_bytes_sha256':numeric,'official_score_cache':winner['official_score_cache'],'official_metric_capsule_sha256':sha(capsule),'actual_return_mapping':winner['causal_return_mapping'],'ordered_native_components':[],'native_bank_components':[],'qualified_anchor_all8_metrics_exact':True,'submission_qualified':True,'test_labels_read':False}
        records.append(row);anchors[number]=row
        for p in [receipt,release/'full_registration_execution.json',release/'selection.json',release/'calibrated_csv_official.json',release/'selected_validation.npy',candidate/'verification.json',capsule]:pins[str(p)]=sha(p)
    leaves={}
    for recipe,(name,bankname) in RECIPES.items():
        bank=Path('E:/赛题五_本机临时')/bankname;info=read(bank/'2025/info.json');assert read(bank/'verification.json')['actual_native_fits']==6 and info['configuration']['epochs']==24
        leaves[recipe]={'name':name,'recipe':recipe,'bank':str(bank),'sha256':info['model_sha256']}
        for p in [bank/'verification.json',*[bank/str(y)/n for y in range(2020,2026) for n in ('model.joblib','info.json')]]:pins[str(p)]=sha(p)
    full=prefix=0
    for family in plan['families']:
        folder=Path('E:/赛题五_本机临时')/family['folder'];proofpath=folder/'verification.json';proof=read(proofpath)
        count=family['records'];base=family['base_round'];assert len(proof['records'])==proof['new_quality_score_records']==count
        assert proof['actual_nonidentity_full_controls']==count-1 and proof['actual_nonidentity_prefix_controls']==3*(count-1)
        full+=count-1;prefix+=3*(count-1)
        for p,d in proof['input_sha256'].items():assert sha(p)==d,p
        pins.update(proof['input_sha256']);pins[str(proofpath)]=sha(proofpath);pins[str(A/family['main_receipt'])]=sha(A/family['main_receipt'])
        for original in proof['records']:
            identity=original['case']==0;cfg=dict(original['configuration']);own=[] if identity else [leaves[r] for r in family['recipes']]
            cfg.update(stage_kind='anchor' if identity else family['stage_kind'],anchor_round=base,model=None if identity else own[0]['name'],recipe=None if identity else family['recipe'],codec=None if identity else cfg['kind'],decay=None,first2020_active=not identity)
            if identity:assert original['metrics']==anchors[base]['metrics'] and original['prediction_numeric_sha256']==anchors[base]['prediction_numeric_bytes_sha256']
            recordpath=folder/f"case{original['case']:03d}_official.json";control=folder/f"case{original['case']:03d}_controls.json";capsule=Path(original['official_score_cache']['official_metrics_source'])
            assert read(recordpath)==original and sha(control)==original['control_sha256'] and sha(capsule)==original['official_metric_capsule_sha256'] and read(capsule)['metrics']==original['metrics']
            records.append({**original,'case':len(records),'configuration':cfg,'family':family['folder'],'original_screen_case':original['case'],'original_screen_record':str(recordpath),'prediction_numeric_bytes_sha256':original['prediction_numeric_sha256'],'expected_unique_native_models':len(hashes[base]|{r['sha256'] for r in own}),'ordered_native_components':[r['name'] for r in own],'native_bank_components':own,'qualified_anchor_all8_metrics_exact':identity,'submission_qualified':identity,'test_labels_read':False})
            for p in [recordpath,control,capsule]:pins[str(p)]=sha(p)
    assert (len(records),full,prefix)==(44,40,120)
    best=min(records,key=lambda r:(-r['connected_final_score'],r['expected_unique_native_models'],abs(r['configuration']['weight']),r['case']))
    assert best['connected_final_score']>=anchors[173]['connected_final_score']
    for p,d in pins.items():assert sha(p)==d,p
    OUT.mkdir(exist_ok=False)
    create(OUT/'pilot44.json',{'status':'passed_normalized44_actual_TRAIN_records_exact_selected_stage_and_full_future_pending','records':records,'best':best,'input_sha256':pins,'expected_scored_records':44,'actual_nonidentity_full_controls':40,'actual_nonidentity_prefix_controls':120,'actual_comparison_parent_round':173,'actual_scheme_base_round':best['configuration']['anchor_round'],'new_quality_scores_by_normalization':0,'new_native_fits':0,'actual_future_X_read':False,'test_labels_read':False,'submission_qualified':False})
    create(OUT/'verification.json',{'status':'passed_normalized44_actual_records_selected14_and_full_registration_pending','pilot_sha256':sha(OUT/'pilot44.json'),'new_quality_scores':0,'full_candidate_qualified':False})
    create(A/'actual_stock_rank_dual44_after173_location_v1_20261010.json',{'output':str(OUT),'pilot_sha256':sha(OUT/'pilot44.json'),'verification_sha256':sha(OUT/'verification.json')})
if __name__=='__main__':main()
