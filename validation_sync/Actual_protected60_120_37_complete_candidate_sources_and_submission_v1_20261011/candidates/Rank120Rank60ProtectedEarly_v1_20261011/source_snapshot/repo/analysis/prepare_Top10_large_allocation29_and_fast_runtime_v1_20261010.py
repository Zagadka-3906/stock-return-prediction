"""Predeclare broad classifier allocation tests, with unchanged official evaluation."""
from pathlib import Path
import ast,sys,json,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service,retire

def save(name,text):
    p=A/name;assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p

def main():
    assert allowed()
    old=A/'run_stock_top10_embedding_after174_fast17_screen_v1_20261010.py'
    text=old.read_text(encoding='utf8');start=text.index('def cases():');end=text.index('\n\ndef main():',start)
    cases="""def cases():
    rows=[{'kind':'anchor174','role':None,'weight':0.,'sign':1.,'protect_fraction':None}]
    for role in ('nonflag_valid','all_valid'):
        for sign in (1.,-1.):
            for weight in (.032,.064,.125,.25,.5,.75,1.):
                rows.append({'kind':'CDF','role':role,'weight':weight,'sign':sign,'protect_fraction':None})
    assert len(rows)==29;return rows
"""
    text=text[:start]+cases+text[end:]
    text=text.replace('after174_high_impact17_screen_v1','after174_large_allocation29_screen_v1')
    text=text.replace("'expected_cases':17","'expected_cases':29").replace("'new_quality_score_records':17","'new_quality_score_records':29").replace("'actual_nonidentity_full_controls':16","'actual_nonidentity_full_controls':28").replace("'actual_nonidentity_prefix_controls':48","'actual_nonidentity_prefix_controls':84")
    text=text.replace('frozen17_own_stock_embedding_return1d_after174_hypotheses_after_own6_full5_independent_qualification_selected_six_state_stage_pending','frozen29_own_Top10_BCE_large_allocation_and_all_valid_hypotheses_after_own6_full5_independent_qualification')
    text=text.replace('passed17_own_stock_embedding_one_day_return_after174_TRAIN_only_CDF_tiny_weights_and_protected_tail_official_comparisons','passed29_own_Top10_BCE_large_CDF_allocation_TRAIN_only_official_comparisons')
    # Serialize full scoring panels: no extra fits and no concurrent large panel.
    needle="    closed('StockRankDual174_complete44_family_v2_20261010')"
    assert text.count(needle)==1
    text=text.replace(needle,"    closed('actual_stock_top10_embedding_after174_fast17_screen_v1_20261010')\n"+needle)
    screen=save('run_stock_top10_embedding_after174_large_allocation29_screen_v1_20261010.py',text)
    module=importlib.import_module(screen.stem);plan=module.cases();assert len(plan)==29
    # Real TRAIN rows exercise both roles, signs, full replacement and prefixes.
    import polars as pl,numpy as np
    import BF16Medium153_complete_parent_rank_CDF_v1_20261009 as codec
    frame=pl.read_parquet(A/'connected_validation_20261002/combined_fold_frame.parquet',columns=['trade_date','flag_limit_up','price_valid']).head(13950)
    dates,flags,valid=[frame[k].to_numpy() for k in ('trade_date','flag_limit_up','price_valid')]
    parent=np.asarray(np.load(A/'optimization_20261003_r170/selected_validation.npy',mmap_mode='r')[:13950],dtype=np.float64)
    raw=np.ascontiguousarray(np.sin(np.arange(13950)*.021),dtype=np.float64);raw[~valid]=-1e6
    controls=[]
    exact=lambda x,y:np.array_equal(np.asarray(x).view('u8'),np.asarray(y).view('u8'))
    for c in plan[1:]:
        args=(c['role'],c['weight'],c['sign'])
        actual=codec.transform(parent,raw,dates,flags,valid,*args)
        assert exact(actual,codec.pandas_oracle(parent,raw,dates,flags,valid,*args))
        mask=codec.selected(flags,valid,c['role']);assert exact(actual[~mask],parent[~mask])
        for n in (4650,9300):assert exact(actual[:n],codec.transform(parent[:n],raw[:n],dates[:n],flags[:n],valid[:n],*args))
        controls.append({'configuration':c,'actual_TRAIN_rows':13950,'independent_Pandas_exact':True,'actual_1_and_2_day_prefix_exact':True})
    predictor=A/'predict_stock_rank_embedding_complete_qualified_parent_scheme_v1_20261010.py'
    text=predictor.read_text(encoding='utf8').replace('stock_rank_embedding','stock_top10_embedding').replace('STOCK_RANK_EMBEDDING','STOCK_TOP10_EMBEDDING').replace('(169,170,171,172,173)','(169,170,171,172,173,174)')
    text=text.replace('stock_top10_embedding_after_complete_qualified_parent_native_stage_v1_20261010','stock_top10_embedding_after_complete_qualified_parent_native_stage_v2_20261010')
    needle='def parent_filename(graph):\n'
    text=text.replace(needle,needle+"    from stock_rank_dual44_selected_native_stage_v1_20261010 import GRAPH_KEY as key174\n    if key174 in graph:return 'predict_stock_rank_dual44_complete_parent_scheme_v1_20261010.py'\n    from stock_rank_embedding_after_complete_qualified_parent_native_stage_v1_20261010 import GRAPH_KEY as rank_key\n    if rank_key in graph:return 'predict_stock_rank_embedding_complete_qualified_parent_scheme_v1_20261010.py'\n")
    predictor2=save('predict_stock_top10_embedding_complete_qualified_parent_scheme_v1_20261010.py',text)
    # Global replacement changes the return-parent import; restore exact return hook.
    # It is a source-generation step before this new file is pinned or launched.
    text=predictor2.read_text(encoding='utf8').replace("from stock_embedding_after_complete_qualified_parent_native_stage_v1_20261010", "from stock_embedding_after_complete_qualified_parent_native_stage_v1_20261010")
    pred=importlib.import_module(predictor2.stem)
    parents=['predict_fast_neural_frontier169_complete_scheme_v2_20261010.py','predict_cross120170_complete169_scheme_v1_20261010.py','predict_frontier233_complete_parent_scheme_v1_20261010.py','predict_frontier133_complete_qualified_parent_scheme_v1_20261010.py','predict_stock_embedding_complete_qualified_parent_scheme_v1_20261010.py','predict_stock_rank_dual44_complete_parent_scheme_v1_20261010.py']
    hooks=[]
    for filename in parents:
        p=A/filename;source=p.read_text(encoding='utf8');modified=pred.prepared_parent(source)
        assert modified.count('return STOCK_TOP10_EMBEDDING_AFTER_WHOLE_QUALIFIED_PARENT(context,value)')==1
        compile(modified,str(p),'exec');hooks.append({'parent':filename,'sha256':sha(p),'exact_single_hook_compiles':True})
    proof=A/'stock_top10_large_allocation29_predeclared_actual_CPU_admission_v1_20261010.json'
    create(proof,{'status':'passed_actual28_TRAIN_codec_cases_Pandas_and_prefix_controls_predeclared29_classifier_scores_pending','cases':plan,'controls':controls,'whole_parent_source_hook_admission':hooks,'input_sha256':{str(p):sha(p) for p in (Path(__file__),old,screen,predictor,predictor2,A/'stock_top10_independent_training_schedule_admission_v3_20261010.json')},'classifier_training_or_quality_scores_not_claimed_by_CPU_controls':True,'new_fits':0,'new_quality_scores':0,'future_X_read':False,'test_labels_read':False})
    pub=A/'publish_stock_top10_embedding_after174_completion_v59_20261010.py';text=pub.read_text(encoding='utf8')
    for left,right in [('after174_fast17_screen_v1','after174_large_allocation29_screen_v1'),('after174_high_impact17_screen_v1','after174_large_allocation29_screen_v1'),('embedding17_after174_completion','embedding29_after174_completion'),('v59_20261010','v60_20261010'),('==17','==29'),('==16','==28'),('==48','==84'),("'scored_records':17","'scored_records':29"),('passed17_actual','passed29_actual'),('records16_full48','records28_full84')]:text=text.replace(left,right)
    text=text.replace('    paths=[*native.glob',f"    paths=[A/{proof.name!r},A/{predictor2.name!r},*native.glob")
    pub60=save('publish_stock_top10_embedding_after174_large_allocation29_completion_v60_20261010.py',text)
    activated=[]
    for name,driver in [('actual_stock_top10_embedding_after174_large_allocation29_screen_v1_20261010',screen),('actual_stock_top10_embedding_after174_large_allocation29_completion_main_v60_20261010',pub60)]:
        assert allowed();row=start_service(name,driver.name,[],{str(driver):sha(driver),str(proof):sha(proof)});create(A/(name+'_activation.json'),row);activated.append(row)
    create(A/'actual_stock_top10_large_allocation29_activation_v1_20261010.json',{'status':'actual_predeclared29_score_and_main60_queues_started','services':activated,'new_quality_scores':0})
    # Keep existing v55 scientific snapshots; successor observes actual schedule3.
    observer=A/'monitor_fast_optimization_v55_20261010.py';text=observer.read_text(encoding='utf8').replace('v55_20261010','v56_20261010').replace('v93_20261010','v95_20261010').replace('v27_20261010','v28_20261010')
    text=text.replace('actual_stock_top10_embedding_own_training_queue_v2_20261010','actual_stock_top10_embedding_own_training_queue_v3_20261010').replace('actual_stock_top10_embedding_native42_and_after174_fast17_queue_v2_20261010','actual_stock_top10_embedding_native42_and_after174_fast17_queue_v3_20261010')
    text=text.replace("    families=['StockTop10", "    jobs += ['actual_stock_top10_embedding_after174_large_allocation29_screen_v1_20261010','actual_stock_top10_embedding_after174_large_allocation29_completion_main_v60_20261010']\n    families=['StockTop10EmbeddingSmall512_after174_large_allocation29_screen_v1_20261010','StockTop10")
    obs=save('monitor_fast_optimization_v56_20261010.py',text);row=start_service('actual_fast_optimization_progress_v56_20261010',obs.name,[],{str(obs):sha(obs)});create(A/'actual_fast_optimization_progress_v56_activation_20261010.json',row)
    import time
    while not (A/'optimization_live_progress_v56_20261010.json').exists():time.sleep(1)
    retire(read(A/'service_owned_workflows_20261006/actual_fast_optimization_progress_v55_20261010/native_launch.json'),'Verified successor56 records actual independent Top10 schedule3 and added predeclared large-allocation29. No scientific worker retired.')
    print({'predeclared_new_cases':29,'actual_real_TRAIN_codec_controls':28,'observer':56,'classifier_GPU_training': 'check live actual service'},flush=True)
if __name__=='__main__':main()
