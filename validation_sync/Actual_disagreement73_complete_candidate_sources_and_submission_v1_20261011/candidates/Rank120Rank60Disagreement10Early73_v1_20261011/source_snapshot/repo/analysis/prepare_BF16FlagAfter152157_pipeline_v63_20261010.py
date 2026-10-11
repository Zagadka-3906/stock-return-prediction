"""Complete immutable157 scoring admission and original QA routes before any new quality score."""
from pathlib import Path
import ast,sys,time
A=Path(__file__).resolve().parent;ROOT=A.parent
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_BF16FlagAfter15222_round157_sources_v1_20261009 import normalize,STATUS

def save(name,text):
    path=A/name;compile(text,str(path),'exec');assert not path.exists()
    path.write_text(text,encoding='utf8',newline='\n');return path

def main():
    files=[Path(__file__)]
    src=A/'run_BF16FlagAfter15222_official_comparison_v2_20261009.py';s=src.read_text(encoding='utf8')
    s=s.replace("    closed('BF16FlagAfter15217_actual_full_training_controls_v1_20261009')",
        "    closed('BF16FlagAfter15222_round157_source_admission_v1_20261009')\n    closed('BF16FlagAfter15222_controls_main_publication_v1_20261009')\n    closed('BF16FlagAfter15217_actual_full_training_controls_v1_20261009')")
    s=s.replace("    OUT.mkdir(parents=True,exist_ok=False)","    from BF16FlagAfter152157_storage_v1_20261009 import empty\n    empty(A/'BF16FlagAfter15222_official_comparison_v1_20261009')")
    s=s.replace("'whole_complete152_branches_preserved_before_new_stage':True,",
        "'whole_complete152_branches_preserved_before_new_stage':True,\n                'whole_complete_parent_branches_preserved_before_new_stage':cfg['model'] is not None,\n                'qualified_anchor_all8_metrics_exact':cfg['model'] is None,\n                'invalid_and_declared_unselected_raw_bits_preserved':cfg['model'] is not None,\n                'actual_cold80_260_975_bits_exact':cfg['model'] is not None,\n                'first2020_active':cfg['model'] is not None and cfg['weight']>0.,\n                'native_bank_source':str(proof),")
    s=s.replace("'passed_actual22_complete152_flag_neural_training_only_official_comparisons'",repr(STATUS))
    s=s.replace("'input_sha256':pins,'records':records,'best':best,","'input_sha256':pins,'records':records,'best':best,'components':{proposal['model_name']:[proposal['model_name']]},")
    files.extend((src,save('run_BF16FlagAfter15222_official_comparison_v3_20261009.py',s)))
    src=A/'verify_BF16Seed10_80_prospective_routes_v1_20261009.py';s=normalize(src.read_text(encoding='utf8'))
    for old,new in [
        ("from prepare_BF16FlagAfter152157_core_drafts_v1_20261009 import best_key","from prepare_BF16FlagAfter152157_core_drafts_v1_20261009 import best_key"),
        ('BF16FlagAfter15222_prospective_routes_v1_20261009.json','BF16FlagAfter15222_prospective_routes_v1_20261010.json'),
        ('run_BF16FlagAfter15222_official_comparison_v1_20261009.py','run_BF16FlagAfter15222_official_comparison_v3_20261009.py'),
        ("t.id=='item'","t.id=='row'"),('[148,149,150,151,152,153,154]','[152,153,154,155,156]'),
        ("len(plan['new_cases'])==73","len(plan['new_cases'])==17"),
        ('optimization_20261003_r148','optimization_20261003_r152'),("'anchor_round':148","'anchor_round':152"),
        ("'actual_scheme_base_round':148","'actual_scheme_base_round':152"),('original_complete_parent_round\']==148','original_complete_parent_round\']==152'),
        ('len(outputs)==7','len(outputs)==5'),('==56','==40'),('==2100','==380'),('==21','==15'),('==14','==10'),
        ("'prospective_sources':56","'prospective_sources':40"),("'graph_controls':2100","'graph_controls':380"),
        ("'baselines':21","'baselines':15"),("'physical_model_ties':14","'physical_model_ties':10"),
        ('BF16FlagAfter15222_actual_receiver_bindings_v1_20261009.json','BF16FlagAfter152157_core_preparation_v62_20261009.json'),
        ('BF16FlagAfter152157_actual_receiver_bindings_v1_20261009.json','BF16FlagAfter152157_core_preparation_v62_20261009.json')]:s=s.replace(old,new)
    # Future receiver outputs are intentionally absent before scientific admission.
    first=s.index('    missing={p for p in g.source_paths()');last=s.index('    sources.extend',first)
    s=s[:first]+"    missing={p for p in g.source_paths() if not p.is_file()}\n    assert all(p.suffix=='.json' or p.name in g.NAMES.values() for p in missing),missing\n"+s[last:]
    s=s.replace('actual56_seed09_157_prospective_sources2100_graphs21_baselines14','actual40_flag_after152157_prospective_sources380_graphs15_baselines10')
    files.extend((src,save('verify_BF16FlagAfter15222_prospective_routes_v1_20261010.py',s)))
    src=A/'run_BF16Seed10_155_safe_registration_v1_20261009.py';s=normalize(src.read_text(encoding='utf8'))
    # Use the current proven storage, chunked report, QA path and main mutex contexts.
    s='''from pathlib import Path
import sys,os
A=Path(__file__).resolve().parent;ROOT=A.parent
sys.path[:0]=[str(ROOT),str(A)]
def main():
    from lossless_chunked_safe_main_runtime_v1_20261009 import installed as safe
    from serial_main_publication_mutex_v1_20261009 import installed as serial
    from verified_TLS_Git_retry_runtime_v2_20261008 import installed as git_io
    from BF16FlagAfter152157_storage_v1_20261009 import installed_transfer
    from actual_QA_collector_path_runtime_v43_20261009 import installed as qa_paths
    count=int(os.environ.get('GIT_CONFIG_COUNT','0'))
    for i,(k,v) in enumerate((('http.proxy','http://127.0.0.1:7897'),('http.version','HTTP/1.1'))):os.environ[f'GIT_CONFIG_KEY_{count+i}']=k;os.environ[f'GIT_CONFIG_VALUE_{count+i}']=v
    os.environ['GIT_CONFIG_COUNT']=str(count+2)
    log=Path('E:/赛题五_本机临时/第157轮_20261009/safe_full_main_v1')
    with safe(log),serial(log/'serial_mutex.json'),git_io(log/'file_backed_git'),installed_transfer(),qa_paths():
        import run_BF16FlagAfter15222_round157_full_registration_v1_20261009 as receiver
        receiver.main()
if __name__=='__main__':main()
'''
    files.extend((src,save('run_BF16FlagAfter152157_safe_registration_v1_20261010.py',s)))
    create(A/'BF16FlagAfter152157_pipeline_preparation_v63_20261010.json',{'status':'prepared_correct22_schema_empty_E_admission_and_original_six_view_QA68',
        'input_sha256':{str(p):sha(p) for p in files},'new_quality_scores':0,'future_X_read':False})
    print('Prepared immutable157 quality v3 and prospective40 /380 graph controls.',flush=True)
if __name__=='__main__':main()
