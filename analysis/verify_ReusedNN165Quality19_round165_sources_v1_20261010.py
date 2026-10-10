"""Admit the frozen22 cases after full17, native14, original full5 and prior forecast hash audit."""
from pathlib import Path
import sys,time,hashlib
A=Path(__file__).resolve().parent;ROOT=A.parent
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned

def closed(name):
    folder=A/'service_owned_workflows_20261006'/name
    while not (folder/'native_launch.json').exists() or owned(read(folder/'native_launch.json')):time.sleep(5)
    assert read(folder/'service_execution.json')['status']=='passed',name

def main():
    for name in ('ReusedNN164Quality19_round164_full_registration_v1_20261009',
                 'ReusedNN165Full17_actual_full_training_controls_v1_20261009',
                 'ReusedNN165Stage_actual_native14_calendar_v1_20261009'):closed(name)
    import prepare_ReusedNN165Quality19_round165_sources_v1_20261009 as g
    prospective_path=A/'ReusedNN165Quality19_prospective_routes_v2_20261010.json';prospective=read(prospective_path)
    assert (prospective['prospective_sources'],len(prospective['graph_controls']),len(prospective['baseline_controls']),len(prospective['physical_model_count_absolute_weight_sort_controls']))==(16, 152, 6, 4)
    pins=dict(prospective['input_sha256'])
    for p,d in pins.items():assert sha(p)==d,p
    pointers=[A/n for n in ('actual_ReusedNN165Full17_full_training_location_v1_20261009.json',
        'actual_ReusedNN165Stage_native14_calendar_location_v1_20261009.json','actual_BF16TopWeightedHuber010165_full5_independent_location_v1_20261009.json')]
    proofs=[]
    for ptr in pointers:
        proof=Path(read(ptr)['output'])/'verification.json';assert sha(proof)==read(ptr)['verification_sha256'];proofs.append(proof)
    full,native,independent=map(read,proofs)
    assert (full['actual_parent_round'],full['actual_full_cases'],full['actual_cold_cases'])==(152,17,51)
    assert (native['actual_saved_states'],native['actual_historical_cases'],native['actual_calendar_cases'],native['actual_cold_cases'])==(6,10,4,14)
    assert len(native['prefit_rejections'])==7 and len(independent['records'])==5 and independent['rows_days_stocks']==[5635800,1212,4650]
    plan_path=A/'ReusedNN165Quality19_round165_plan_v1_20261009.json';plan=read(plan_path)
    bank=Path(plan['native_bank']);states=[];metadata=[*pointers,*proofs,plan_path,prospective_path,Path(__file__),Path(g.__file__),bank/'verification.json']
    for year in range(2020,2026):
        info_path=bank/str(year)/'info.json';info=read(info_path);meta=info['training_meta']
        assert info['year']==year and meta['last']<meta['cutoff_exclusive'] and meta['last_label_end']<=meta['cutoff_exclusive']
        assert meta['actual_future_training_label_poisoning_population_exact'] and sha(bank/str(year)/'model.joblib')==info['model_sha256']
        metadata.append(info_path);states.append({'year':year,'model_sha256':info['model_sha256'],'training_meta':meta})
    for year in (152, 164):
        folder=A/f'optimization_20261003_r{year}';receipt=A/f'github_validation_sync_main_20261005/round{year}_receipt.json'
        assert read(folder/'full_registration_execution.json')['status']=='passed' and read(receipt)['status']=='pushed_and_remote_head_verified'
        metadata.extend((folder/'full_registration_execution.json',folder/'calibrated_csv_official.json',receipt))
    # Audit immutable measured forecast hashes directly, avoiding deserializing a multi-GB display report.
    prior={};audited=[]
    for folder in sorted(A.glob('*official_comparison*')):
        if not folder.is_dir() or folder.name.startswith('ReusedNN165Quality19'):continue
        for path in sorted(folder.glob('case*_official.json')):
            row=read(path);digest=row.get('prediction_numeric_bytes_sha256')
            if digest and row.get('metrics') and (row.get('whole_complete_parent_branches_preserved_before_new_stage') or row.get('qualified_anchor_all8_metrics_exact')):
                prior.setdefault(digest,[]).append({'source':str(path),'metrics':row['metrics']})
                audited.append(path)
    import numpy as np
    base_path=A/'optimization_20261003_r152/selected_validation.npy';base=np.load(base_path,mmap_mode='r')
    base_digest=hashlib.sha256(memoryview(np.ascontiguousarray(base)).cast('B')).hexdigest();del base
    baseline=read(A/'optimization_20261003_r152/calibrated_csv_official.json')['metrics']
    audited.append(base_path)
    prior.setdefault(base_digest,[]).append({'source':str(base_path),'metrics':baseline})
    matches=[]
    for row in full['controls']:
        assert row['configuration']==plan['new_cases'][row['case']]
        previous=prior.get(row['numeric_sha256'],[])
        if not row['configuration']['weight']:
            assert row['numeric_sha256']==base_digest
            assert all(p['metrics']==baseline for p in previous)
        matches.append({'case':row['case'],'numeric_sha256':row['numeric_sha256'],'prior_measured_forecast_matches':previous})
    audit_path=A/'ReusedNN165Stage_prior_forecast_hash_audit_v1_20261010.json'
    create(audit_path,{'status':'passed_actual17_direct_immutable_forecast_hash_audit_and_zero152_all8_metrics',
        'input_sha256':{str(p):sha(p) for p in audited},'records':matches,'actual_eligible_saved_score_records':len(audited)-1,
        'display_report_not_deserialized':True,'global_uniqueness_not_claimed':True,'new_quality_scores':0})
    metadata.append(audit_path)
    for proof in (full,native,independent):
        for p,d in proof['input_sha256'].items():assert sha(p)==d,p;pins[p]=d
    pins.update({str(p):sha(p) for p in metadata})
    index=A/'ReusedNN165Quality19_actual_controls_index_v1_20261009.json'
    create(index,{'status':'passed_actual6_reused_seed09_states14_native17_full51_cold_controls',
        'input_sha256':pins,'original_external_metadata':{str(p):read(p) for p in metadata if not p.is_relative_to(ROOT) and p.suffix=='.json'},
        'actual6_saved_states':states,'prior_forecast_hash_audit':str(audit_path),'new_native_fits':0,'test_labels_read':False})
    outputs={str(n):{name:hashlib.sha256(text.encode()).hexdigest() for name,text in g.generate(n).items()} for n in (152, 164)}
    assert outputs==prospective['generated_source_sha256']
    pins[str(index)]=sha(index)
    create(A/'ReusedNN165Quality19_round165_source_admission_v1_20261009.json',{
        'status':'passed_actual6_saved_states14_native17_full51_cold40_routes380_graphs_and_prior_hash_audit',
        'input_sha256':pins,'generated_source_sha256':outputs,'actual_saved_states':6,'actual_full_cases':17,'actual_cold_cases':51,
        'complete40_routes_and_graph_controls_passed':True,'prior_complete_forecast_duplicate_audit_passed':True,
        'quality_scoring_admitted_cases':19,'new_quality_scores_by_admission':0,'test_labels_read':False})
    print('Actual157 admitted: full17/cold51, native14/cold14, 40routes/380graphs.',flush=True)

if __name__=='__main__':main()
