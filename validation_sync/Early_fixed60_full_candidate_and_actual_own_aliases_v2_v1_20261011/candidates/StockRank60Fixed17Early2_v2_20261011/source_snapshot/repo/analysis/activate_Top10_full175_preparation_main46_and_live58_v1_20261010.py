"""Publish completed own6/full5 evidence and exact47 full175 sources, observe current routes."""
from pathlib import Path
import sys,ast,time,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service,retire
def save(name,text):
    p=A/name;assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p
def main():
    assert allowed()
    from prepare_stock_top10_embedding175_full_registry_sources_v2_20261010 import NAMES,EXTRAS
    fullservice=A/'service_owned_workflows_20261006/StockTop10EmbeddingSmall512_independent_full5_GPU_controls_v1_20261009'
    assert read(fullservice/'service_execution.json')['status']=='passed' and not owned(read(fullservice/'native_launch.json'))
    bank=Path(read(A/'actual_stock_top10_embedding_small512_bank6_location_v1_20261010.json')['output']);assert read(bank/'verification.json')['actual_native_fits']==6
    full=Path(read(A/'actual_StockTop10EmbeddingSmall512_full5_independent_location_v1_20261009.json')['output']);assert read(full/'verification.json')['rows_days_stocks']==[5635800,1212,4650]
    template=A/'publish_Top10_actual_restart_and_six_hooks_actual_main_v45_20261010.py';text=template.read_text(encoding='utf8');tree=ast.parse(text);fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main');node=next(n for n in fn.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='paths' for t in n.targets))
    paths=[Path(p) for p in ast.literal_eval(node.value)]
    extras=['prepare_stock_top10_embedding175_full_registry_sources_v2_20261010.py','admit_Top10_175_exact_storage_preflight_v2_20261010.py','run_StockTop10Embedding175_complete_family_v2_20261010.py','run_StockTop10Embedding175_full_registration_v2_20261010.py','verify_StockTop10Embedding175_full47_preflight_v2_20261010.py','stock_top10_embedding175_full_registry_sources_preparation_v2_20261010.json','stock_top10_embedding175_full_execution_sources_admission_v1_20261010.json','stock_top10_embedding175_full_execution_sources_admission_v2_20261010.json','actual_StockTop10Embedding175_complete47_family_activation_v2_20261010.json','actual_stock_top10_embedding47_after174_normalization_queue_v2_20261010_activation.json','StockTop10Embedding47_selected_native14_v2_20261010_activation.json','actual_stock_top10_embedding_small512_bank6_location_v1_20261010.json','actual_StockTop10EmbeddingSmall512_full5_independent_location_v1_20261009.json']
    paths += [Path(__file__),template,*[A/n for n in NAMES+EXTRAS+extras],*bank.glob('*.json'),*bank.glob('*/info.json'),*bank.glob('*/frozen_training_inputs.json'),*full.glob('*.json')]
    paths += [fullservice/n for n in ('native_launch.json','service_execution.json','job_definition.json')]
    assert all(p.exists() for p in paths)
    lines=text.splitlines(keepends=True);lines[node.lineno-1:node.end_lineno]=['    paths='+repr([str(p) for p in paths])+'\n'];text=''.join(lines)
    for key in ('StockTop10Embedding_verified_BCE_loss_and_runtime_v','StockTop10Embedding_verified_BCE_loss_and_runtime_main_v','StockTop10Embedding_verified_BCE_loss_and_runtime_main_receipt_v'):text=text.replace(key+'45_20261010',key+'46_20261010')
    text=text.replace('passed_actual_Top10_GPU_small32_and_wide2_restart_independent_CPU_and_six_exact_parent_callbacks_annual_fit_and_official_scores_pending','passed_actual_Top10_BCE_six_own_mature_annual_fits_full5635800_independent_replay_controls_and_complete47_full175_sources_official_classifier_scores_pending')
    text=text.replace('保存Top10分类实际GPU重启参数逐位一致性、独立小样本推理和六个完整父方案回调控制；六年度训练进行中，未声明新官方分数','保存Top10分类实际六年度独立训练、五年度5635800行独立解码和冷启动，以及47项选模至完整175轮交付来源；官方分类评分尚未完成')
    pub=save('publish_Top10_actual_own6_full5_and_full175_sources_main_v46_20261010.py',text)
    row=start_service('actual_Top10_own6_full5_and_full175_sources_main_v46_20261010',pub.name,[],{str(pub):sha(pub)});create(A/'actual_Top10_own6_full5_and_full175_sources_main_activation_v46_20261010.json',row)
    observer=A/'monitor_fast_optimization_v57_20261010.py';text=observer.read_text(encoding='utf8').replace('v57_20261010','v58_20261010').replace('v97_20261010','v99_20261010').replace('v29_20261010','v30_20261010')
    needle="    jobs += ['actual_stock_top10_embedding_after174_large_allocation29_screen_v1_20261010'"
    assert text.count(needle)==1
    additional=['actual_stock_top10_embedding47_after174_normalization_queue_v2_20261010','StockTop10Embedding47_selected_native14_v2_20261010','StockTop10Embedding175_complete47_family_v2_20261010','StockTop10Embedding175_selected_candidate_preparation_v1_20261010','StockTop10Embedding175_selected_candidate_sealing_v1_20261010','StockTop10Embedding175_round175_full_registration_v1_20261010','actual_Top10_own6_full5_and_full175_sources_main_v46_20261010']
    text=text.replace(needle,'    jobs += '+repr(additional)+'\n'+needle)
    text=text.replace("'StockRankDual174_complete44_family_v2_20261010'):lines.append", "'StockRankDual174_complete44_family_v2_20261010','StockTop10Embedding175_complete47_family_v2_20261010'):lines.append")
    driver=save('monitor_fast_optimization_v58_20261010.py',text);row=start_service('actual_fast_optimization_progress_v58_20261010',driver.name,[],{str(driver):sha(driver)});create(A/'actual_fast_optimization_progress_v58_activation_20261010.json',row)
    while not (A/'optimization_live_progress_v58_20261010.json').exists():time.sleep(1)
    retire(read(A/'service_owned_workflows_20261006/actual_fast_optimization_progress_v57_20261010/native_launch.json'),'Verified observer58 includes actual47 normalization2, selected14_2, full175 family2 and true completed own6/full5 evidence; scientific workers unchanged.')
    print({'completed_classifier_annual_models':6,'independent_full_rows':5635800,'actual_full175_pipeline':'queued','observer':58,'main46':'started'},flush=True)
if __name__=='__main__':main()
