"""Clarify copied display labels using completed, unchanged four-model proofs."""
from pathlib import Path
import argparse
import hashlib
import json
import time

ROOT=Path(__file__).resolve().parents[1]
FAMILIES={'neural_width':57,'portfolio_surrogate':59,'nystrom_ridge':61}
STALE_KEY='eight_independent_actual_native_or_virtual_standalone_compositions_exact'


def read(path):return json.loads(path.read_text(encoding='utf-8-sig'))


def sha(path):
    result=hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda:stream.read(8*1024*1024),b''):result.update(block)
    return result.hexdigest()


def create(path,value):
    with path.open('x',encoding='utf-8') as stream:
        json.dump(value,stream,ensure_ascii=False,indent=2);stream.write('\n')


def main(family,probe=False):
    start=FAMILIES[family]
    plan=ROOT/f'analysis/{family}_complete_output_search_plan_20261004.json'
    complete=ROOT/f'analysis/{family}_complete_scheme_preflight_20261004'
    native=ROOT/f'analysis/{family}_future_models_qa_20261004/verification.json'
    helper=ROOT/f'analysis/verify_{family}_complete_scheme_20261004.py'
    run=ROOT/f'analysis/{family}_scheme_count_audit_run_20261004.json'
    out=ROOT/f'analysis/{family}_scheme_count_metadata_audit_20261004'
    configuration=read(plan)
    names=set(configuration['model_configurations'])
    assert len(names)==configuration['new_native_models']==4
    if probe:
        print(json.dumps({'family':family,'expected_native_models':4,'expected_role_cases':13,
            'expected_standalone_cases':4,'wait_for_actual_final_proof':str(complete/'verification.json'),
            'new_model_fits':0,'new_quality_scores':0}));return
    while not run.exists():time.sleep(10)
    job=read(run)
    for path,digest in job['input_sha256'].items():assert sha(Path(path))==digest,path
    out.mkdir(exist_ok=True)
    inputs={str(path.resolve()):sha(path) for path in (Path(__file__),run,plan,helper)}
    create(out/'frozen_before_actual_proof_audit.json',{'status':'frozen_before_proof_audit',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'family':family,
        'input_sha256':inputs,'expected_native_model_names':sorted(names),
        'new_model_fits':0,'new_quality_scores':0,'test_labels_read':False})
    while True:
        try:proof=read(complete/'verification.json')
        except (FileNotFoundError,json.JSONDecodeError):time.sleep(10);continue
        assert proof['status']=='passed' and proof['new_quality_scores']==0
        break
    parameters=complete/'parameter_andreplay_checks.json'
    assert sha(parameters)==proof['parameter_replay_sha256']
    values=read(parameters)
    assert values['status']=='passed' and values['new_quality_scores']==0
    assert values[STALE_KEY] is True
    assert {item['model'] for item in values['new_role_cases']}==names
    assert len(values['new_role_cases'])==4
    assert all(item['all_three_roles_checked'] for item in values['new_role_cases'])
    assert len(values['role_controls'])==13 and len(values['standalone_controls'])==4
    for index,control in enumerate(values['role_controls']):
        assert control['label_poisoning_bit_identical']
        assert [row['days'] for row in control['prefixes']]==([80,260,975] if index==0 else [80,260])
        assert all(row['bit_identical'] for row in control['prefixes'])
    for control in values['standalone_controls']:
        assert control['label_poisoning_bit_identical']
        assert [row['days'] for row in control['prefixes']]==[80,260,975]
        assert all(row['bit_identical'] for row in control['prefixes'])
    expected={str(start):[49,8,18,25],str(start+1):[25,56,17]}
    assert values['bounded_arm_counts']==configuration['records_per_wave']==expected
    native_proof=read(native)
    assert native_proof['status']=='passed' and native_proof['new_quality_scores']==0
    assert {item['model'] for item in native_proof['native_models']}==names
    assert len(native_proof['native_models'])==4
    helper_path=str(helper.resolve())
    assert proof['input_sha256'][helper_path]==inputs[helper_path]
    candidates=proof['candidate_verification_sha256']
    assert set(candidates)=={'role_baseline','standalone_baseline','role_changed','pure_changed'}
    paths=[complete/'verification.json',parameters,native]
    for label,digest in candidates.items():
        path=complete/label/'candidate/verification.json'
        assert sha(path)==digest
        value=read(path)
        assert value['status']=='passed' and value['validation_score'] is None
        assert (value['rows'],value['days'],value['codes'])==(1599600,344,4650)
        csv=path.parent/'submission.csv';assert sha(csv)==value['csv_sha256']
        paths.extend((path,csv))
    for path,digest in inputs.items():assert sha(Path(path))==digest,path
    output={'status':'passed_with_copied_display_label_clarified',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'family':family,
        'actual_native_model_names':sorted(names),'actual_native_models':4,
        'actual_baseline_plus_three_role_cases_per_model':13,
        'actual_independent_standalone_composition_cases':4,
        'actual_fullfuture_candidate_cases':4,'actual_frozen_records_per_wave':expected,
        'copied_display_key':STALE_KEY,'display_key_literal_eight_is_not_actual_case_count':True,
        'original_frozen_sources_andproofs_retained_unchanged':True,
        'no_algorithm_orinference_orofficial_score_change':True,
        'new_model_fits':0,'new_quality_scores':0,'test_labels_read':False,
        'input_sha256':{**inputs,**{str(path.resolve()):sha(path) for path in paths}},
        'scope':'Counts actual completed native, role, standalone andfuture cases. Corrects interpretation of an inherited field name only. Does not establish subsequent selected-predecessor quality orresource limits.'}
    create(out/'verification.json',output)
    print(json.dumps({'family':family,'status':output['status'],'actual_native_models':4,
        'actual_standalone_cases':4,'new_quality_scores':0}),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('family',choices=FAMILIES)
    parser.add_argument('--probe',action='store_true');args=parser.parse_args()
    main(args.family,args.probe)
