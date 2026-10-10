"""Preserve failed generator controls and repair only new GOSS metadata/version routing."""
from pathlib import Path
import hashlib
import json
import re

A = Path(__file__).resolve().parent


def create(name, text):
    compile(text, str(A/name), 'exec')
    with (A/name).open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(text)


def convert(text):
    text = re.sub(r'(ready_goss_reference[^\s\x27\x22/]*?)(?<!_v2)_20261006', r'\g<1>_v2_20261006', text)
    text = text.replace('[37,96,17]', '[37,84,17]').replace('[37, 96, 17]', '[37, 84, 17]')
    text = text.replace("f'optimize_training_round{number}_v2'", "f'optimize_training_round{number}_v3'")
    text = text.replace("f'finalize_training_round{number}_v2'", "f'finalize_training_round{number}_v3'")
    text = text.replace("f'optimize_training_round{parent_number}_v2'", "f'optimize_training_round{parent_number}_v3' if parent_number==95 else f'optimize_training_round{parent_number}_v2'")
    text = text.replace("f'optimize_training_round{number}_v2.py'", "f'optimize_training_round{number}_v3.py'")
    text = text.replace("f'finalize_training_round{number}_v2.py'", "f'finalize_training_round{number}_v3.py'")
    text = text.replace("f'run_training_round{number}_v2_pipeline.py'", "f'run_training_round{number}_v3_pipeline.py'")
    text = text.replace('explicit_parent_release_engine_v2_20261005', 'ready_goss_reference_release_engine_v2_20261006')
    text = text.replace("('optimize_training_round95_v2.py','finalize_training_round95_v2.py')", "('optimize_training_round95_v3.py','finalize_training_round95_v3.py')")
    text = text.replace("('_v2.py')", "('_v3.py')").replace("name.replace('_v2.py','.py')", "name.replace('_v3.py','.py')")
    # Copy both the unchanged inherited V2 factories and new V3 factories as aliases.
    text = text.replace("name.endswith('_v3.py')", "name.endswith(('_v2.py','_v3.py'))")
    text = text.replace("name.replace('_v3.py','.py')", "name.replace('_v2.py','.py').replace('_v3.py','.py')")
    text = text.replace("('_v2')", "('_v3')")
    text = text.replace("('_v2_pipeline')", "('_v3_pipeline')")
    text = text.replace("('optimize_training_round', '_v2')", "('optimize_training_round', '_v3')")
    text = text.replace("('finalize_training_round', '_v2')", "('finalize_training_round', '_v3')")
    text = text.replace("('run_training_round', '_v2_pipeline')", "('run_training_round', '_v3_pipeline')")
    text = text.replace("f'{prefix}{number}_v2.py'", "f'{prefix}{number}_v3.py'")
    text = text.replace("f'optimize_training_round{84 if number==95 else 95}_v2.py'", "f'optimize_training_round{84 if number==95 else 95}_{\"v2\" if number==95 else \"v3\"}.py'")
    text = text.replace('Execute the FM drivers', 'Execute the GOSS drivers')
    return text


def main():
    record = json.loads((A/'ready_goss_reference_source_generation_20261006.json').read_text(encoding='utf-8'))
    for path, digest in record['sources_sha256'].items():
        assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==digest,path
    failure = {'status':'failed_synthetic_generator_declaration_check_before_actual_quality',
        'exception':'AssertionError: counts per wave did not equal expected',
        'cause':'Word-boundary round renumbering also changed standalone wave count 84 to round number 96.',
        'expected_actual_standalone_wave_counts':[37,84,17], 'incorrect_declared_counts':[37,96,17],
        'original_sources_sha256_preserved':record['sources_sha256'],
        'actual_quality_records':0,'new_native_fits':0,'test_labels_read':False}
    with (A/'ready_goss_reference_generator_preflight_20261006/failure.json').open('x',encoding='utf-8') as stream:
        json.dump(failure,stream,ensure_ascii=False,indent=2)
    for prefix in ('', 'run_', 'check_', 'predict_', 'verify_'):
        pass
    for old in ('ready_goss_reference_search_engine_20261006.py',
                'run_ready_goss_reference_round_20261006.py',
                'check_ready_goss_reference_scheme_20261006.py',
                'predict_ready_goss_reference_scheme_20261006.py',
                'verify_ready_goss_reference_generators_20261006.py',
                'verify_ready_goss_reference_execution_20261006.py'):
        new=old.replace('_20261006.py','_v2_20261006.py')
        create(new,convert((A/old).read_text(encoding='utf-8')))
    release=(A/'explicit_parent_release_engine_v2_20261005.py').read_text(encoding='utf-8')
    release=release.replace("f'optimize_training_round{number}_v2'", "f'optimize_training_round{number}_v3'")
    release=release.replace("f'analysis/finalize_training_round{number}_v2.py'", "f'analysis/finalize_training_round{number}_v3.py'")
    create('ready_goss_reference_release_engine_v2_20261006.py',release)
    for number,parent in ((95,84),(96,95)):
        parent_version='v2' if parent==84 else 'v3'
        create(f'optimize_training_round{number}_v3.py',f'import sys\nimport optimize_training_round{parent}_{parent_version}\nfrom ready_goss_reference_search_engine_v2_20261006 import install\ninstall({number},globals())\nsys.modules["optimize_training_round{number}"]=sys.modules[__name__]\nsys.modules["optimize_training_round{number}_v2"]=sys.modules[__name__]\n')
        create(f'finalize_training_round{number}_v3.py',f'from ready_goss_reference_release_engine_v2_20261006 import install\ninstall({number},globals())\n')
        create(f'run_training_round{number}_v3_pipeline.py',f'from run_ready_goss_reference_round_v2_20261006 import main\nif __name__=="__main__":main({number})\n')
    plan=json.loads((A/'ready_goss_reference_complete_plan_20261006.json').read_text(encoding='utf-8'))
    plan.update(failed_original_generator_control_preserved=True, effective_factory_versions={'95':'v3','96':'v3'}, source_versions_preserved=True)
    with (A/'ready_goss_reference_complete_plan_v2_20261006.json').open('x',encoding='utf-8') as stream:
        json.dump(plan,stream,ensure_ascii=False,indent=2)
    for path,digest in record['sources_sha256'].items():
        assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==digest,path
    print('created_versioned_GOSS_95_96_repair_original_sources_preserved',flush=True)


if __name__=='__main__':
    main()
