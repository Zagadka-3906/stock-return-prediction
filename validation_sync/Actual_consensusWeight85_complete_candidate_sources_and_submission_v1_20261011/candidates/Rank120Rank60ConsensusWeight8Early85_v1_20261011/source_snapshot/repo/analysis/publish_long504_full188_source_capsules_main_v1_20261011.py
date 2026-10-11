"""Publish actual504 configuration, CPU11, frozen48/QA99 candidate flow and exact queue recovery on main."""
from pathlib import Path
import sys,re,runpy
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed

def main():
    assert allowed()
    template=A/'publish_StockRank20_actual_own6_full5_main_v66_20261010.py'
    proofs=[A/'rank20long_complete48_normalization_native14_sources_admission_v1_20261011.json',
        A/'stock_rank20long_embedding188_full_execution_sources_admission_v1_20261011.json',
        A/'long188_actual_scientific_queue_routes_v2_20261011.json',
        A/'rank20long_complete188_factory_source_admission_v1_20261011.json']
    paths=[Path(__file__),template,ROOT/'后续选模标准.md',*proofs]
    for proof in proofs:
        data=read(proof)
        for p,d in data['input_sha256'].items():assert sha(p)==d,p
        paths += [Path(p) for p in data['input_sha256']]
    config=read(proofs[0])['configuration'];assert config['training_calendar_window']==504 and config['epochs']==64 and config['seed']==20261009
    callbacks=A/'stock_rank20long_embedding_actual_eleven_parent_callbacks_CPU_controls_v1_20261011.json'
    assert len(read(callbacks)['records'])==11
    paths += [callbacks,*[A/r['parent'] for r in read(callbacks)['records']]]
    paths=list(dict.fromkeys(paths));assert all(p.is_file() for p in paths)
    text=template.read_text(encoding='utf8')
    text=text.replace('StockRank20_actual_own6_full5_v66_20261010','StockRank20Long188_sources_v1_20261011').replace('StockRank20_actual_own6_full5_main_v66_20261010','StockRank20Long188_sources_main_v1_20261011').replace('StockRank20_actual_own6_full5_main_receipt_v66_20261010','StockRank20Long188_sources_main_receipt_v1_20261011')
    start=text.index('    paths=');end=text.index('    import publish_classifier_consensus_workflows_20261006 as h',start)
    text=text[:start]+'    paths=[Path(__file__),*[Path(p) for p in '+repr([str(p) for p in paths])+']]\n'+text[end:]
    start=text.index("    payload[(prefix/'manifest.json').as_posix()]");end=text.index('    out=Path(',start)
    manifest={'status':'compiled_long504_full188_candidate_registry_QA99_sources_with_actual_CPU11_and_dependency_routes',
        'configuration':config,'expected_records':48,'expected_full_board':17538,'QA':99,'anchors':[175,187],
        'actual_parent_callback_CPU_checks':11,'normalization_selected_native_and_full_future_qualification_pending':True,
        'legacy_status_and_stdout_text_preserved_actual_configuration_and_fields_authoritative':True,
        'new_model_fits_by_publication':0,'new_quality_scores':0,'actual_future_X_read':False,'test_labels_read':False}
    text=text[:start]+"    payload[(prefix/'manifest.json').as_posix()]=h.sync.encoded({**"+repr(manifest)+",'files':bindings})\n"+text[end:]
    text,count=re.subn(r"'保存实际股票身份与120维特征二十日排名目标[^']*'",repr('冻结504日成熟训练窗口第188轮48项完整候选、175/187锚点与QA99流程，保存11项实际CPU父回调及真实科学队列路由；未完成训练和资格不记为完成'),text);assert count==1
    driver=A/'publish_StockRank20Long188_sources_payload_main_v1_20261011.py'
    assert not driver.exists();compile(text,str(driver),'exec');driver.write_text(text,encoding='utf8',newline='\n')
    assert allowed();runpy.run_path(str(driver),run_name='__main__')

if __name__=='__main__':main()
