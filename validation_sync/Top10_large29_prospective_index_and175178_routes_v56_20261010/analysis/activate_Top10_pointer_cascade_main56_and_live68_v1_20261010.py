"""Publish prospective corrected index/routes and observe actual current full families."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service,retire
def save(name,text):
    p=A/name;assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p
def main():
    assert allowed();source=A/'monitor_fast_optimization_v67_20261010.py';text=source.read_text(encoding='utf8').replace('progress_v67','progress_v68').replace('handoff_v117','handoff_v119').replace('rankings_v39','rankings_v40')
    families=['StockTop10Embedding175_complete47_family_v3_20261010','StockTop10Embedding176_complete31_family_v3_20261010','StockRank5Embedding177_complete48_family_v4_20261010','StockForward5Embedding178_complete48_family_v5_20261010']
    extra=['actual_stock_top10_embedding_after174_large_allocation29_screen_v2_20261010','actual_stock_top10_embedding_after174_large_allocation29_completion_main_v72_20261010','actual_Top10_large29_index_and175178_cascade_main_v56_20261010',*families]
    for prefix,count,after,version,kind in [('stock_top10_embedding',47,174,3,'StockTop10Embedding'),('stock_top10_embedding',31,175,3,'StockTop10Embedding'),('stock_rank5_embedding',48,176,4,'StockRank5Embedding'),('stock_forward5_embedding',48,177,4,'StockForward5Embedding')]:
        extra += [f'actual_{prefix}{count}_after{after}_normalization_queue_v{version}_20261010',f'{kind}{count}_selected_native14_v{version}_20261010']
    needle='    while True:\n';assert text.count(needle)==1;text=text.replace(needle,'    jobs += '+repr(extra)+'\n'+needle)
    replacements={'StockTop10Embedding175_complete47_family_v2':'StockTop10Embedding175_complete47_family_v3','StockTop10Embedding176_complete31_family_v2':'StockTop10Embedding176_complete31_family_v3','StockRank5Embedding177_complete48_family_v3':'StockRank5Embedding177_complete48_family_v4','StockForward5Embedding178_complete48_family_v4':'StockForward5Embedding178_complete48_family_v5'}
    lines=text.splitlines()
    for i,line in enumerate(lines):
        if line.startswith("        for name in ('Frontier233171"):
            for old,new in replacements.items():line=line.replace(old,new)
            lines[i]=line
    observer=save('monitor_fast_optimization_v68_20261010.py','\n'.join(lines)+'\n')
    proof=A/'Top10_large29_pending_index_and_full175178_cascade_admission_v5_20261010.json';paths=[Path(__file__),proof,A/'prevent_Top10_large29_pointer_collision_and_cascade_routes_v4_20261010.py',A/'prevent_Top10_large29_pointer_collision_and_cascade_routes_v5_20261010.py',observer]
    paths += [Path(p) for p in read(proof)['input_sha256']]
    for prefix,number,ver in [('stock_top10_embedding',175,3),('stock_top10_embedding',176,3),('stock_rank5_embedding',177,4),('stock_forward5_embedding',178,4)]:paths.append(A/f'{prefix}{number}_candidate_sources_preparation_v{ver}_20261010.json')
    assert all(p.is_file() for p in paths)
    source=A/'publish_actual29_recovery_forward5_own6_and177178_routes_main_v55_20261010.py';text=source.read_text(encoding='utf8');start=text.index('    from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import closed');end=text.index('    import publish_classifier_consensus_workflows_20261006 as h',start)
    text=text[:start]+'    paths=[Path(__file__),*[Path(p) for p in '+repr([str(p) for p in dict.fromkeys(paths)])+']]\n'+text[end:]
    text=text.replace('Actual_Rank5_29_recovery_forward5_own6_and177178_routes','Top10_large29_prospective_index_and175178_routes').replace('v55_20261010','v56_20261010').replace('passed_actual_forward5_six_own64_fits_and_verified29_terminal_pointer_recovery_no_scores_rerun_full1773_1784_sources','compiled_exact_Top10_large29_index_before_scoring_same47_31_48_48_and_full1753_1763_1774_1785_routes_no_scientific_restarts')
    text=text.replace('保存五日收益嵌入实际六年度64轮完整训练，以及29项完成评分索引恢复和177/178依赖修复；原分数未重算、已验证缓存和模型数学不变','预防尚未开始的Top10大权重29项结果索引冲突，冻结的47/31/48/48项比较保持不变；175至178精确依赖和已验证推理缓存保留')
    publisher=save('publish_Top10_prospective_index_and175178_cascade_main_v56_20261010.py',text)
    retire(read(A/'service_owned_workflows_20261006/actual_fast_optimization_progress_v67_20261010/native_launch.json'),'Replace childless observer67 with68 showing actual corrected1753/1763/1774/1785; scientific workers unchanged')
    for name,p in [('actual_fast_optimization_progress_v68_20261010',observer),('actual_Top10_large29_index_and175178_cascade_main_v56_20261010',publisher)]:
        assert allowed();row=start_service(name,p.name,[],{str(p):sha(p)});create(A/(name+'_activation.json'),row)
    print({'live68_started':True,'exact_current_cascade_source_main56_started':True},flush=True)
if __name__=='__main__':main()
