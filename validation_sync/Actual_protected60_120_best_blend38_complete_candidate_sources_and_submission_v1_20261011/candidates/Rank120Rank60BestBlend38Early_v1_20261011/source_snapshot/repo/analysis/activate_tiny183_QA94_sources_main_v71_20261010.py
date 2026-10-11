"""Publish all exact new full-family sources and real routing CPU evidence onto main."""
from pathlib import Path
import sys,re
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service
def main():
    assert allowed()
    import prepare_StockRank20Tiny183_complete85_pipeline_v1_20261010 as wide
    import prepare_StockRank20Complement182_complete63_pipeline_v1_20261010 as complement
    proofpath=A/'Dual25_verified_recovery_exact_dependency_aliases_v6_20261010.json';proof=read(proofpath)
    extras=['stock_rank20_embedding183_full_execution_sources_admission_v1_20261010.json','prepare_StockRank20Tiny183_complete85_pipeline_v1_20261010.py','publish_rank20_tinyCDF82_stages_main_v68_20261010.py','recover_capacity181_explicit_recipe32_sources_v2_20261010.py','capacity181_actual_recipe32_namespace_recovery_v2_20261010.json','recover_all_actual_terminal_dependency_routes_v6_20261010.py','all_actual_terminal_dependency_routes_endpoint_audit_v6_20261010.json','finish_terminal_routes6_dispatch_and_actual_Top29_main_v80_20261010.py','all_actual_terminal_routes6_resumed_missing_dispatch_and_actual_Top29_identity_v1_20261010.json','verify_terminal_routes6_candidate_and_alias_actual_CPU_v1_20261010.py','terminal_routes6_candidate_aliases_and_recipe32_actual_CPU_v1_20261010.json','stock_rank_wide32_embedding181_full_execution_sources_admission_v2_20261010.json','stock_rank20_embedding182_full_execution_sources_admission_v1_20261010.json','publish_stock_top10_embedding_after174_large_allocation29_completion_v80_20261010.py','stock_top10_embedding29_after174_completion_main_receipt_v60_20261010.json']
    paths=list(dict.fromkeys([Path(__file__),*wide.source_paths(),*complement.source_paths(),proofpath,*[A/n for n in extras],*[Path(p) for p in proof['input_sha256']]]))
    assert all(p.is_file() for p in paths)
    for p in paths:
        if p.suffix=='.py':compile(p.read_text(encoding='utf8'),str(p),'exec')
    template=A/'publish_StockRank20_actual_own6_full5_main_v66_20261010.py';text=template.read_text(encoding='utf8')
    start=text.index('    paths=');end=text.index('    import publish_classifier_consensus_workflows_20261006 as h',start)
    text=text[:start]+'    paths=[Path(__file__),*[Path(p) for p in '+repr([str(p) for p in paths])+']]\n'+text[end:]
    text=text.replace('StockRank20_actual_own6_full5_v66_20261010','Tiny183_QA94_actual_sources_v71_20261010').replace('StockRank20_actual_own6_full5_main_v66_20261010','Tiny183_QA94_actual_sources_main_v71_20261010').replace('StockRank20_actual_own6_full5_main_receipt_v66_20261010','Tiny183_QA94_actual_sources_main_receipt_v71_20261010')
    start=text.index("    payload[(prefix/'manifest.json').as_posix()]");end=text.index('    out=Path(',start)
    manifest={'status':'compiled_exact_full18148_QA92_full18263_QA93_and_actual_routes_CPU111_child9_sources','actual_capacity_parent_callbacks_CPU':12,'actual_route_alias_CPU_cases':111,'actual_nested_child_CPU_cases':9,'full183_records':85,'full183_full_controls':80,'full183_prefix_controls':240,'full183_expected_board':17258,'full183_QA':94,'full182_records':63,'full182_nonidentity_controls':60,'full182_prefix_controls':180,'actual_future_X_read_by_source_publication':False,'new_quality_scores_by_publication':0,'pending_future_qualification_not_claimed_complete':True,'old_sources_and_failed_dispatches_preserved':True}
    text=text[:start]+"    payload[(prefix/'manifest.json').as_posix()]=h.sync.encoded({**"+repr(manifest)+",'files':bindings})\n"+text[end:]
    text,count=re.subn(r"'保存实际股票身份与120维特征二十日排名目标[^']*'",repr('保存第183轮82项微权重互补与3个合格锚点组成的85项完整流程，QA94与17258项完整榜源码；尚未执行未来推理'),text);assert count==1
    publisher=A/'publish_tiny183_QA94_sources_main_v71_20261010.py';assert not publisher.exists();compile(text,str(publisher),'exec');publisher.write_text(text,encoding='utf8',newline='\n')
    name='actual_tiny183_QA94_sources_main_v71_20261010';assert allowed();row=start_service(name,publisher.name,[],{str(publisher):sha(publisher)});create(A/(name+'_activation.json'),row)
    print({'exact_new_source_files':len(paths),'source_CPU_controls_passed':True,'queued_main':name},flush=True)
if __name__=='__main__':main()
