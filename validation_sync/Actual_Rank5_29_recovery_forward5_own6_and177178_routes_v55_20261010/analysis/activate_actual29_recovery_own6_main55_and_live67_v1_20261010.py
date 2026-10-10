"""Publish actual completed six-year training and immutable score-recovery route evidence."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
from handoff_ready_goss_full_execution_20261006 import start_service,retire
def save(name,text):
    p=A/name;assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p
def main():
    assert allowed();closed('actual_stock_forward5_embedding_own_training_queue_v1_20261010')
    source=A/'monitor_fast_optimization_v66_20261010.py';text=source.read_text(encoding='utf8').replace('progress_v66','progress_v67').replace('handoff_v115','handoff_v117').replace('rankings_v38','rankings_v39')
    extra=['actual_Rank5_large29_verified_terminal_recovery_v1_20261010','actual_stock_rank5_embedding_after171_large29_completion_main_v69_20261010','actual_stock_forward5_embedding_after171_large_allocation29_screen_v2_20261010','actual_stock_forward5_embedding_after171_large29_completion_main_v71_20261010','actual_stock_rank5_embedding48_after176_normalization_queue_v3_20261010','StockRank5Embedding48_selected_native14_v3_20261010','StockRank5Embedding177_complete48_family_v3_20261010','actual_stock_forward5_embedding48_after177_normalization_queue_v3_20261010','StockForward5Embedding48_selected_native14_v3_20261010','StockForward5Embedding178_complete48_family_v4_20261010','actual_29_recovery_forward5_own6_and177178_routes_main_v55_20261010']
    needle='    while True:\n';assert text.count(needle)==1;text=text.replace(needle,'    jobs += '+repr(extra)+'\n'+needle)
    lines=text.splitlines()
    for i,line in enumerate(lines):
        if line.startswith("        for name in ('Frontier233171"):
            line=line.replace('StockRank5Embedding177_complete48_family_v2','StockRank5Embedding177_complete48_family_v3').replace('StockForward5Embedding178_complete48_family_v2','StockForward5Embedding178_complete48_family_v4').replace(",'StockForward5Embedding178_complete48_family_v3_20261010'",'');lines[i]=line
    text='\n'.join(lines)+'\n';observer=save('monitor_fast_optimization_v67_20261010.py',text)
    source=A/'publish_forward5_restart_full178_sources_main_v53_20261010.py';text=source.read_text(encoding='utf8');start=text.index('    paths=[');end=text.index('    import publish_classifier_consensus_workflows_20261006 as h',start)
    names=[Path(__file__).name,'repair_Rank5_29_receipt_and_pending177178_routes_v3_20261010.py','recover_actual_Rank5_large29_terminal_location_v1_20261010.py','stock_rank5_embedding_actual29_terminal_pointer_recovery_v1_20261010.json','stock_rank5_forward5_actual29_pointer_and177178_routes_recovery_v3_20261010.json','run_stock_forward5_embedding_after171_large_allocation29_screen_v2_20261010.py','admit_forward5_large29_exact_service_receipt_v71_20261010.py','stock_forward5_embedding_large29_exact_service_receipt_admission_v71_20261010.json','publish_stock_forward5_embedding_after171_large29_completion_v71_20261010.py','publish_stock_rank5_embedding_after171_large29_completion_v69_20261010.py','monitor_fast_optimization_v67_20261010.py']
    for namespace,number,previous,family in [('rank5',177,176,3),('forward5',178,177,4)]:
        kind='StockRank5Embedding' if namespace=='rank5' else 'StockForward5Embedding';prefix='stock_'+namespace+'_embedding'
        names += [f'normalize_completed_{prefix}_complete48_after{previous}_v3_20261010.py',f'qualify_{prefix}48_selected_native14_v3_20261010.py',f'prepare_{kind}{number}_selected_candidate_v3_20261010.py',f'{prefix}{number}_candidate_sources_preparation_v3_20261010.json',f'verify_{kind}{number}_full48_preflight_v3_20261010.py',f'run_{kind}{number}_full_registration_v3_20261010.py',f'run_{kind}{number}_complete_family_v{family}_20261010.py']
    names.append('run_StockForward5Embedding178_selected_candidate_feature_cache_v4_20261010.py')
    paths=[A/n for n in names];bank=Path(read(A/'actual_stock_forward5_embedding_small512_bank6_location_v1_20261010.json')['output']);proof=read(bank/'verification.json');assert proof['actual_native_fits']==6
    paths += [bank/'verification.json',*bank.glob('*/info.json')]
    for name in ('actual_stock_forward5_embedding_own_training_queue_v1_20261010','actual_stock_forward5_embedding_small512_bank6_v1_20261010','actual_Rank5_large29_verified_terminal_recovery_v1_20261010'):
        paths += [A/'service_owned_workflows_20261006'/name/n for n in ('native_launch.json','service_execution.json','job_definition.json')]
    assert all(p.is_file() for p in paths)
    replacement='    from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import closed\n    closed(\'actual_stock_forward5_embedding_own_training_queue_v1_20261010\')\n    paths=[Path(__file__),*[Path(p) for p in '+repr([str(p) for p in paths])+']]\n'
    text=text[:start]+replacement+text[end:]
    text=text.replace('StockForward5Embedding_actual_restart_full178_sources','Actual_Rank5_29_recovery_forward5_own6_and177178_routes').replace('v53_20261010','v55_20261010').replace('passed_actual_forward5_return_small32_wide2_GPU_restart_smallCPU_nine_parent_callbacks_compiled_full17848_QA89_sources_annual_training_running_no_quality_claim','passed_actual_forward5_six_own64_fits_and_verified29_terminal_pointer_recovery_no_scores_rerun_full1773_1784_sources')
    text=text.replace('保存五日收益股票嵌入实际GPU重启和独立CPU验证，以及48项选优冻结完整推理QA89 main来源；年度训练和正式评分进行中','保存五日收益嵌入实际六年度64轮完整训练，以及29项完成评分索引恢复和177/178依赖修复；原分数未重算、已验证缓存和模型数学不变')
    publisher=save('publish_actual29_recovery_forward5_own6_and177178_routes_main_v55_20261010.py',text)
    retire(read(A/'service_owned_workflows_20261006/actual_fast_optimization_progress_v66_20261010/native_launch.json'),'Replace exact childless observer66 with67 showing actual recovered29, own forward5 six fits and actual1773/1784 routes; scientific workers unchanged')
    for name,p in [('actual_fast_optimization_progress_v67_20261010',observer),('actual_29_recovery_forward5_own6_and177178_routes_main_v55_20261010',publisher)]:
        assert allowed();row=start_service(name,p.name,[],{str(p):sha(p)});create(A/(name+'_activation.json'),row)
    print({'live67_started':True,'actual_own6_and29_recovery_sources_main55_started':True,'new_quality_scores':0},flush=True)
if __name__=='__main__':main()
