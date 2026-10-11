"""Publish full31 follow-up preparation and observe all existing active services."""
from pathlib import Path
import sys,ast,time
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service,retire
def save(name,text):
    p=A/name;assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p
def main():
    assert allowed()
    from prepare_stock_top10_embedding176_full_registry_sources_v2_20261010 import NAMES,EXTRAS
    template=A/'publish_Top10_early171_actual42_actual_main_v48_20261010.py';text=template.read_text(encoding='utf8');tree=ast.parse(text);fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='main');node=next(n for n in fn.body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='paths'for t in n.targets))
    paths=[Path(p)for p in ast.literal_eval(node.value)]
    extras=['prepare_stock_top10_embedding176_full_registry_sources_v2_20261010.py','run_StockTop10Embedding176_complete_family_v2_20261010.py','run_StockTop10Embedding176_full_registration_v2_20261010.py','verify_StockTop10Embedding176_full31_preflight_v2_20261010.py','stock_top10_embedding176_full_registry_sources_preparation_v2_20261010.json','stock_top10_embedding176_full_execution_sources_admission_v2_20261010.json','actual_StockTop10Embedding176_complete31_family_activation_v2_20261010.json','actual_stock_top10_embedding31_after175_normalization_queue_v2_20261010_activation.json','StockTop10Embedding31_selected_native14_v2_20261010_activation.json']
    paths += [Path(__file__),template,*[A/n for n in NAMES+EXTRAS+extras]];assert all(p.exists()for p in paths)
    lines=text.splitlines(keepends=True);lines[node.lineno-1:node.end_lineno]=['    paths='+repr([str(p)for p in paths])+'\n'];text=''.join(lines)
    for key in ('StockTop10Embedding_verified_BCE_loss_and_runtime_v','StockTop10Embedding_verified_BCE_loss_and_runtime_main_v','StockTop10Embedding_verified_BCE_loss_and_runtime_main_receipt_v'):text=text.replace(key+'48_20261010',key+'49_20261010')
    text=text.replace('passed_actual_Top10_six_saved_states42_native42_cold7_prefit_controls_early171_TRAIN29_official_scoring_running','compiled_full176_31_normalizer_selected14_candidate_freeze_registry_QA87_main_sources_actual_early171_29_scoring_running')
    text=text.replace('保存Top10分类实际六状态42项原生、42项冷启动和7项拟合前拒绝检查；提前171轮29项官方评分进行中，不声明提分或完整176交付','保存第176轮31项比较、独立原生检查、冻结和两次完整推理至QA87及main交付来源；提前171轮29项评分进行中，不遗漏可能优于175轮的方案')
    pub=save('publish_Top10_full176_sources_actual_main_v49_20261010.py',text);row=start_service('actual_Top10_full176_sources_main_v49_20261010',pub.name,[],{str(pub):sha(pub)});create(A/'actual_Top10_full176_sources_main_activation_v49_20261010.json',row)
    old=A/'monitor_fast_optimization_v60_20261010.py';text=old.read_text(encoding='utf8').replace('v60_20261010','v61_20261010').replace('v103_20261010','v105_20261010').replace('v32_20261010','v33_20261010')
    needle="    jobs += ['actual_stock_top10_embedding_early171_six_state_native42_v3_20261010']";assert text.count(needle)==1
    additions=['actual_stock_top10_embedding31_after175_normalization_queue_v2_20261010','StockTop10Embedding31_selected_native14_v2_20261010','StockTop10Embedding176_complete31_family_v2_20261010','StockTop10Embedding176_selected_candidate_preparation_v1_20261010','StockTop10Embedding176_selected_candidate_sealing_v1_20261010','StockTop10Embedding176_round176_full_registration_v1_20261010','actual_Top10_full176_sources_main_v49_20261010','actual_Top10_early171_actual42_controls_main_v48_20261010','actual_early171_large29_and_followup31_sources_main_v47_20261010']
    text=text.replace(needle,needle+'\n    jobs += '+repr(additions))
    text=text.replace("'StockTop10Embedding175_complete47_family_v2_20261010'):lines.append","'StockTop10Embedding175_complete47_family_v2_20261010','StockTop10Embedding176_complete31_family_v2_20261010'):lines.append")
    observer=save('monitor_fast_optimization_v61_20261010.py',text);row=start_service('actual_fast_optimization_progress_v61_20261010',observer.name,[],{str(observer):sha(observer)});create(A/'actual_fast_optimization_progress_v61_activation_20261010.json',row)
    while not(A/'optimization_live_progress_v61_20261010.json').exists():time.sleep(1)
    retire(read(A/'service_owned_workflows_20261006/actual_fast_optimization_progress_v60_20261010/native_launch.json'),'Verified observer61 includes exact followup31 and full176_2 services, early29 and existing full175; no scientific worker stopped.')
    print({'full176_pipeline_sources_main49':'queued','actual_observer':61,'actual_early29_scoring':'running'},flush=True)
if __name__=='__main__':main()
