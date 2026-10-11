"""Fresh accurate metadata/source routing, then seven actual receivers after existing current-parent2."""
from pathlib import Path
import sys,time,hashlib,ast
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create

FILES=[
    'run_ConeRidgeAlpha100_official_comparison_v1_20261008.py',
    'prepare_ConeRidgeAlpha100_selected_candidate_v1_20261008.py',
    'seal_ConeRidgeAlpha100_selected_candidate_v1_20261008.py',
    'run_ConeRidgeAlpha100_round144_full_registration_v1_20261008.py',
    'publish_ConeRidgeAlpha100_evidence_v1_20261008.py',
    'verify_ConeRidgeAlpha100_round144_sources_v1_20261008.py',
    'prepare_ConeRidgeAlpha100_round144_sources_v1_20261008.py',
]
MAPPING={p:p.replace('_v1_','_v2_') for p in FILES}
MAPPING.update({
    'ConeRidgeAlpha100_round144_source_admission_v1_20261008.json':'ConeRidgeAlpha100_round144_source_admission_v2_20261008.json',
    'ConeRidgeAlpha100_round144_source_preparation_v1_20261008.json':'ConeRidgeAlpha100_round144_source_preparation_v2_20261008.json',
    'ConeRidgeAlpha100_prospective_routes_v1_20261008.json':'ConeRidgeAlpha100_prospective_routes_v2_20261008.json',
    'ConeRidgeAlpha144_receiver_preparation_v1_20261008.json':'ConeRidgeAlpha144_receiver_preparation_v2_20261008.json',
    'passed_actual48_prospective143_sources':'passed_actual24_prospective144_sources',
    'and24_prospective143_sources':'and24_prospective144_sources',
    "'existing_SpectralGram_saved_native_heads': 20":"'existing_ConeRidgeAlpha_saved_native_heads': 40",
})

def corrected(text):
    for before,after in MAPPING.items():text=text.replace(before,after)
    return text
def save(name,text):
    p=A/name;assert not p.exists(),p;compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p

def main():
    sources=[Path(__file__)];outputs=[]
    for filename in FILES:
        source=A/filename;sources.append(source);text=corrected(source.read_text(encoding='utf8'))
        if filename.startswith('prepare_ConeRidgeAlpha100_round144_sources'):
            text=text.replace('from prepare_ConeRidgeAlpha144_complete_receivers_v1_20261008 import adapt',
                'from prepare_ConeRidgeAlpha144_complete_receivers_v1_20261008 import adapt as original_adapt\nfrom complete_ConeRidgeAlpha144_metadata_and_queue_v2_20261008 import corrected\ndef adapt(text):return corrected(original_adapt(text))')
            needle='    return list(dict.fromkeys([Path(__file__),*dependencies,*current,*[A/p for p in required],*[A/name for name in NAMES.values()]]))'
            assert needle in text
            text=text.replace(needle,'    return list(dict.fromkeys([Path(corrected(str(p))) for p in [Path(__file__),*dependencies,*current,*[A/p for p in required],*[A/name for name in NAMES.values()]]]))')
        outputs.append(save(MAPPING[filename],text))
    source=A/'verify_ConeRidgeAlpha100_prospective_routes_v3_20261008.py';sources.append(source)
    text=corrected(source.read_text(encoding='utf8')).replace('cross_volume_byte_probe_v2','cross_volume_byte_probe_v4')
    outputs.append(save('verify_ConeRidgeAlpha100_prospective_routes_v4_20261008.py',text))
    pins={str(p):sha(p) for p in [*sources,*outputs]}
    create(A/'ConeRidgeAlpha144_metadata_receiver_correction_v2_20261008.json',{
        'status':'frozen_correct_actual24_prospective144_and40_bank_metadata_before_any_quality',
        'input_sha256':pins,'mapping':MAPPING,'original_sources_and_partial_proofs_preserved':True,
        'new_quality_scores':0,'native_math_grid_and_existing_auxiliary_control_sources_unchanged':True,'test_labels_read':False})
    from verify_ConeRidgeAlpha100_prospective_routes_v4_20261008 import main as prospective
    prospective()
    proof_path=A/'ConeRidgeAlpha100_prospective_routes_v2_20261008.json';proof=read(proof_path)
    assert proof['actual_prospective_sources']==24 and proof['actual_graph_controls']==2619
    for path,digest in proof['input_sha256'].items():assert sha(path)==digest,path
    import prepare_ConeRidgeAlpha100_round144_sources_v2_20261008 as generator
    # Execute an actual collector forwarding contract for all three parents, independently of text checks.
    contracts=[]
    for parent in (132,134,143):
        generated=generator.generate(parent);tree=ast.parse(generated['collect_full_lossless_round144_qa55_20261007.py'])
        fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='collect');calls=[]
        def delegate(n,q,c):calls.append((n,q,c));return True
        scope={'namespace':{'collect':delegate}}
        exec(compile(ast.fix_missing_locations(ast.Module(body=[fn],type_ignores=[])),'<144actual>','exec'),scope)
        assert scope['collect'](144,100,55) is True and calls==[(144,55,100)]
        contracts.append({'parent':parent,'actual_forwarded_arguments':calls})
    create(A/'ConeRidgeAlpha144_actual_collector_contracts_v2_20261008.json',{
        'status':'passed_actual_three100_QA55_forwarding_contracts','contracts':contracts,
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),proof_path,Path(generator.__file__)]}})
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    jobs=[
        ('ConeRidgeAlpha100_round144_source_admission_v1_20261008',MAPPING[FILES[5]],[]),
        ('ConeRidgeAlpha100_controls_main_publication_v1_20261008',MAPPING[FILES[4]],['controls']),
        ('ConeRidgeAlpha100_official_comparison_v1_20261008',MAPPING[FILES[0]],[]),
        ('ConeRidgeAlpha100_scores_main_publication_v1_20261008',MAPPING[FILES[4]],['scores']),
        ('ConeRidgeAlpha100_selected_candidate_preparation_v1_20261008',MAPPING[FILES[1]],[]),
        ('ConeRidgeAlpha100_selected_candidate_sealing_v1_20261008',MAPPING[FILES[2]],[]),
        ('ConeRidgeAlpha100_round144_full_registration_v1_20261008',MAPPING[FILES[3]],[])]
    pins.update({str(proof_path):sha(proof_path)})
    create(A/'ConeRidgeAlpha144_complete_dependency_plan_v2_20261008.json',{
        'status':'frozen100_actual_complete_pipeline_before_quality','jobs':jobs,'input_sha256':pins,
        'existing_current_parent_service':'ConeRidgeAlpha97_current_parent_controls_v2_20261008',
        'expected_scored_cases':100,'QA_version':55,'new_native_fits':0,'test_labels_read':False})
    launches={name:start(name,driver,args,pins) for name,driver,args in jobs}
    create(A/'ConeRidgeAlpha144_complete_hidden_launches_v2_20261008.json',{
        'status':'started_seven_receivers_after_actual_current_parent2_for_complete100_pipeline',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'launches':launches,'input_sha256':pins,
        'expected_scored_cases':100,'QA_version':55,'actual_quality_scores_by_dispatch':0,
        'candidate_actual_future_freeze_replays_main_still_required':True,'test_labels_read':False})
    print('Seven true Alpha144 complete receivers dispatched after24/2619 and actual three collector contracts.',flush=True)

if __name__=='__main__':main()
