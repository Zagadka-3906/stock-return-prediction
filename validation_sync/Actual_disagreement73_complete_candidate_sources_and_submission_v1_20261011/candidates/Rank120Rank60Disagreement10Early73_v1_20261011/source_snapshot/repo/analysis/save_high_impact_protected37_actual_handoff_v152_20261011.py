"""Record actual scores and owned processes without promoting pending experiments to submissions."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import sys,hashlib,psutil
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed

def main():
    assert allowed()
    proofs=[A/'rank20_two_seed_protected_tail37_predeclared_plan_v1_20261011.json',
        A/'rank20_two_seed_protected_selected_native14_sources_admission_v1_20261011.json',
        A/'rank20_two_seed_protected37_publication_sources_v1_20261011.json']
    for proof in proofs:
        for p,d in read(proof)['input_sha256'].items():assert sha(p)==d,p
    names=['actual_rank20_two_seed_after175_complement49_screen_v1_20261010',
        'actual_rank20_two_seed_native84_v1_20261010',
        'actual_rank20_two_seed_after175_protected_tail37_screen_v1_20261011',
        'actual_rank20_two_seed_protected_selected_native14_v1_20261011',
        'actual_Rank20_two_seed_protected37_stages_main_v1_20261011',
        'actual_Rank20_two_seed_protected_native14_stages_main_v1_20261011',
        'actual_stock_rank20long_embedding_small512_bank6_v1_20261010',
        'actual_fast_optimization_progress_v89_20261011']
    services={}
    for name in names:
        folder=A/'service_owned_workflows_20261006'/name
        launch=read(folder/'native_launch.json')
        execution=read(folder/'service_execution.json') if (folder/'service_execution.json').exists() else {}
        live=owned(launch)
        assert execution.get('status')!='failed',(name,execution)
        assert launch['actual_native_console_handle']==0,name
        services[name]={'execution':execution,'owned_live':live,'identity':launch}
    index_sha=hashlib.sha256((ROOT/'.git/index').read_bytes()).hexdigest()
    assert index_sha=='ed2fa41598113343f7cf84c4ff16f7685c9ed3e079c16edf869c2c32019d3406'
    output=Path('E:/赛题五_本机临时')
    progress={}
    for family in ['StockRank20TwoSeed_after175_complement49_screen_v1_20261010','StockRank20TwoSeed_after175_protected_tail37_screen_v1_20261011']:
        folder=output/family
        progress[family]=read(folder/'best_so_far.json') if (folder/'best_so_far.json').exists() else {'completed_cases':0,'not_started_scoring_yet':True}
    bank=output/'stock_rank20long_embedding_small512_BF16_bank6_v1_20261010'
    complete=[y for y in range(2020,2026) if (bank/str(y)/'info.json').exists()]
    receipts={}
    for name in ['Rank20_two_seed_protected37_sources_main_receipt_v1_20261011.json','Rank20_two_seed_protected37_sources_selected14_main_receipt_v1_20261011.json','Rank20_two_seed_protected37_official37_main_receipt_v1_20261011.json','Rank20_two_seed_protected37_selected14_main_receipt_v1_20261011.json']:
        p=A/name;receipts[name]=read(p) if p.exists() else {'status':'pending_not_claimed_uploaded'}
    now=datetime.now(timezone(timedelta(hours=8))).isoformat()
    create(A/'actual_high_impact_protected37_and_selected14_handoff_v152_20261011.json',{
        'status':'progress_new_predeclared37_larger_protected_rank_changes_and_selected14_native_queue',
        'at_local':now,'deadline_local':read(A/'current_user_runtime_control_20261010.json')['stop_at_local'],
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),*proofs]},'services':services,
        'actual_TRAIN_screen_progress':progress,'long504_completed_annual_models':complete,
        'long504_no_uncompleted_models_or_scores_marked_complete':True,'receipts':receipts,
        'best_fully_qualified_delivery':read(A/'latest_verified_submission_delivery_v2_20261008.json'),
        'source_of_hypothesis':'TRAIN rank20 complement supports testing both signs of larger raw-rank perturbations with protected head; no gain guaranteed',
        'adaptive_TRAIN_selection_bias_uncorrected':True,'existing_scientific_sources_SHA_unchanged':True,
        'new_model_fits_by_protected37':0,'new_quality_scores_by_preparation':0,'selected_future_submission_pipeline_pending':True,
        'actual_future_X_read_by_new_preparation':False,'test_labels_read':False,'root_git_index_sha256_unchanged':index_sha,
        'RAM_available_GiB':psutil.virtual_memory().available/2**30,
        'next_actions':['Finish actual CDF49 and protected37 official scores without rerunning them',
            'Complete long504 own6/full5/native42/46 with durable checkpoints',
            'Finish highest TRAIN winner183 full qualification and main, then seed10 full186 pipeline',
            'Route only actual winning two-seed specification into complete normalization/candidate/board pipeline; native14 alone is not submission qualification',
            'Verify all source and actual completed-score main receipts; preserve original failures',
            'Stop at actual user deadline11:00 and preserve recovery evidence']})
    print({'actual_progress_saved':True,'CDF49_completed':progress['StockRank20TwoSeed_after175_complement49_screen_v1_20261010'].get('completed_cases'),
        'long504_complete_models':len(complete),'protected37_submission_qualified':False},flush=True)

if __name__=='__main__':main()
