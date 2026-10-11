"""Preserve partial failed constructor3; resume exact bytes through a fresh driver4."""
from pathlib import Path
import sys, time
ROOT=Path(__file__).resolve().parents[1]; A=ROOT/'analysis'; sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create, owned

def main():
    failed=A/'service_owned_workflows_20261006/ConeRidgeFine143_plan_controls_preparation_v3_20261008'
    assert not owned(read(failed/'native_launch.json'))
    assert read(failed/'service_execution.json')['status']=='failed'
    assert 'run_ConeRidge142_registration_receipt_reconciliation_v2_20261008.py' in (failed/'stderr.log').read_text(encoding='utf8')
    original=A/'prepare_ConeRidgeFine68_round143_plan_controls_v3_20261008.py'
    target=A/'prepare_ConeRidgeFine68_round143_plan_controls_v4_20261008.py'; assert not target.exists()
    text=original.read_text(encoding='utf8')
    wrong="'run_ConeRidge142_registration_receipt_reconciliation_v2_20261008.py'"
    assert text.count(wrong)==1
    text=text.replace(wrong,"'run_ConeRidge52_round142_full_registration_v1_20261008.py'")
    before="path=A/name;assert not path.exists();compile(text,str(path),'exec');path.write_text(text,encoding='utf8',newline='\\n');return path"
    after="""path=A/name;compile(text,str(path),'exec')
    if path.exists():
        assert name in ('run_ConeRidgeFine68_official_comparison_v1_20261008.py','prepare_ConeRidgeFine68_selected_candidate_v1_20261008.py','seal_ConeRidgeFine68_selected_candidate_v1_20261008.py')
        assert path.read_bytes()==text.encode('utf8'),name
        return path
    path.write_text(text,encoding='utf8',newline='\\n');return path"""
    assert text.count(before)==1; text=text.replace(before,after)
    before="plan_path=A/'ConeRidgeFine68_round143_plan_v1_20261008.json';create(plan_path,plan)"
    after="""plan_path=A/'ConeRidgeFine68_round143_plan_v1_20261008.json'
    preserved=read(plan_path)
    for key in ('round','amplitudes','new_cases','expected_scored_cases','expected_transform_cases','expected_cold_cases','additional_native_fits_by_grid'):
        assert preserved[key]==plan[key],key
    for path,digest in preserved['input_sha256'].items():assert sha(path)==digest,path
    recovery=A/'ConeRidgeFine143_partial_constructor_recovery_v4_20261008.json'
    assert read(recovery)['status']=='frozen_fresh_driver4_with_exact_three_partial_sources_before_any143_quality'
    for path,digest in read(recovery)['input_sha256'].items():assert sha(path)==digest,path"""
    assert text.count(before)==1; text=text.replace(before,after)
    text=text.replace('from prepare_ConeRidgeFine68_round143_plan_controls_v3_20261008 import adapt','from prepare_ConeRidgeFine68_round143_plan_controls_v4_20261008 import adapt')
    text=text.replace("'prepare_ConeRidgeFine68_round143_plan_controls_v3_20261008.py',","'prepare_ConeRidgeFine68_round143_plan_controls_v4_20261008.py','ConeRidgeFine143_partial_constructor_recovery_v4_20261008.json',")
    before="if 'historical_causal' in name:"
    # Execute both the callable signature and its forwarding argument order before any quality.
    insertion="""if name=='verify_ConeRidge52_prospective_routes_v2_20261008.py':
            needle="        paths.append({'parent':parent,'actual68_records_QA54':True})"
            assert needle in text
            contract='''        collector_tree=ast.parse(generated['collect_full_lossless_round143_qa54_20261007.py'])
        function=next(node for node in collector_tree.body if isinstance(node,ast.FunctionDef) and node.name=='collect')
        forwarded=[]
        def actual_contract(n,q,c):
            forwarded.append((n,q,c));return {'contract_executed':True}
        scope={'namespace':{'collect':actual_contract}}
        exec(compile(ast.fix_missing_locations(ast.Module(body=[function],type_ignores=[])),'<actual143collector-contract>','exec'),scope)
        assert scope['collect'](143,68,54)=={'contract_executed':True}
        assert forwarded==[(143,54,68)]
        for invalid in ((142,68,54),(143,54,68),(143,67,54)):
            try:scope['collect'](*invalid)
            except AssertionError:pass
            else:raise AssertionError(('invalid collector call accepted',invalid))
'''
            text=text.replace(needle,contract+needle)
        if 'historical_causal' in name:"""
    assert text.count(before)==1; text=text.replace(before,insertion)
    compile(text,str(target),'exec')
    partial=[A/name for name in ('run_ConeRidgeFine68_official_comparison_v1_20261008.py','prepare_ConeRidgeFine68_selected_candidate_v1_20261008.py','seal_ConeRidgeFine68_selected_candidate_v1_20261008.py')]
    assert all(p.is_file() for p in partial)
    from prepare_ConeRidgeFine68_round143_plan_controls_v3_20261008 import adapt
    for p,old in zip(partial,('run_ConeRidge52_official_comparison_v1_20261008.py','prepare_ConeRidge52_selected_candidate_v1_20261008.py','seal_ConeRidge52_selected_candidate_v1_20261008.py')):
        expected=adapt((A/old).read_text(encoding='utf8')).replace('prepare_ConeRidgeFine143_complete_receivers_v1_20261008.py','prepare_ConeRidgeFine143_complete_receivers_v3_20261008.py')
        assert p.read_bytes()==expected.encode('utf8'),p
    target.write_text(text,encoding='utf8',newline='\n')
    sources=[Path(__file__),original,target,A/'ConeRidgeFine68_round143_plan_v1_20261008.json',*partial,
        failed/'native_launch.json',failed/'service_execution.json',failed/'stderr.log']
    create(A/'ConeRidgeFine143_partial_constructor_recovery_v4_20261008.json',{
        'status':'frozen_fresh_driver4_with_exact_three_partial_sources_before_any143_quality',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in sources},
        'frozen_plan1_and_three_partial_sources_byte_preserved':True,'failed_source3_and_logs_preserved':True,
        'changes':'restore only original template filename; verify existing immutable bytes; pin fresh4 provenance; execute collector argument contract',
        'new_model_fits':0,'new_official_scores':0,'new_inference_calls':0,'test_labels_read':False})
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    row=start('ConeRidgeFine143_plan_controls_preparation_v4_20261008',target.name,[],{str(target):sha(target)})
    create(A/'ConeRidgeFine143_plan_controls_preparation_hidden_launch_v4_20261008.json',row)
    print('Fresh Fine143 constructor4 started; failed3 and immutable partial bytes preserved.',flush=True)

if __name__=='__main__':main()
