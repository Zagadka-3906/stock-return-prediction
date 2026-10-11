"""Preserve the unlaunched186 source-admission failure and generate a fresh version with actual API checks."""
from pathlib import Path
import sys,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed

def main():
    assert allowed()
    source=A/'prepare_StockRank20Seed10Embedding186_complete48_pipeline_v1_20261011.py'
    old=importlib.import_module(source.stem)
    assert not (A/old.PROOF).exists()
    assert not (A/'service_owned_workflows_20261006/StockRank20Seed10Embedding186_complete48_family_v1_20261011').exists()
    storage=importlib.import_module(Path(old.EXTRAS[2]).stem)
    assert all(not p.exists() and not q.exists() for p,q in storage.OUTPUTS.items())
    generated=[A/old.FILE_MAP[n] for n in old.OLD_FILES if n not in old.previous.EXTRAS[:2]]
    assert all(p.is_file() for p in generated)
    for p in generated:compile(p.read_text(encoding='utf8'),str(p),'exec')
    text=source.read_text(encoding='utf8')
    corrections={
        "'_v1_20261011.py',new)":"'_v2_20261011.py',new)",
        "stock_rank20seed10_embedding186_full_execution_sources_admission_v1_20261011.json":"stock_rank20seed10_embedding186_full_execution_sources_admission_v2_20261011.json",
        "stock_rank20seed10_embedding186_full_family_preflight_v1_20261011.json":"stock_rank20seed10_embedding186_full_family_preflight_v2_20261011.json",
        "stock_rank20seed10_embedding186_candidate_sources_preparation_v1_20261011.json":"stock_rank20seed10_embedding186_candidate_sources_preparation_v2_20261011.json",
        "stock_rank20seed10_embedding186_full_registry_sources_preparation_v1_20261011.json":"stock_rank20seed10_embedding186_full_registry_sources_preparation_v2_20261011.json",
        "actual_feature120_verified_memoization_TRAIN344_benchmark_v1_20261010.json":"actual_feature120_verified_memoization_TRAIN344_location_v1_20261010.json",
        "    assert '17402' in (A/NAMES[5]).read_text(encoding='utf8')":"    assert 'len(report[\"connected\"])' in (A/NAMES[5]).read_text(encoding='utf8'), 'Board codec must preserve the actual full dynamic record count'",
        "native.CONFIG['training_window']==252":"native.CONFIG['training_calendar_window']==252",
        "name='StockRank20Seed10Embedding186_complete48_family_v1_20261011'":"name='StockRank20Seed10Embedding186_complete48_family_v2_20261011'",
    }
    for oldtext,newtext in corrections.items():
        assert oldtext in text,oldtext;text=text.replace(oldtext,newtext)
    driver=A/'prepare_StockRank20Seed10Embedding186_complete48_pipeline_v2_20261011.py'
    assert not driver.exists();compile(text,str(driver),'exec');driver.write_text(text,encoding='utf8',newline='\n')
    proof=A/'seed10_full186_source_admission_recovery_v2_20261011.json'
    create(proof,{'status':'preserved_original_source_admission_assertion_before_any_source_proof_future_dispatch_or_registration',
        'original_error':'AssertionError: expected literal17402 in dynamic-count lossless builder; no scientific worker launched',
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),source,driver,*generated]},
        'actual_configuration_key':'training_calendar_window','actual_feature_benchmark_pointer':corrections['actual_feature120_verified_memoization_TRAIN344_benchmark_v1_20261010.json'],
        'original_source_files_preserved':True,'fresh_generated_source_versions':2,
        'dynamic_full_board_count_verified_by_existing_full_collector_not_invented_literal':True,
        'new_quality_scores':0,'new_model_fits':0,'actual_future_X_read':False,'test_labels_read':False})
    print({'fresh_full186_factory_v2_created':True,'scientific_outputs_unchanged_and_unstarted':True},flush=True)

if __name__=='__main__':main()
