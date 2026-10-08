"""After full142 qualification, execute the declared finer TRAIN-only grid with existing native models."""
from pathlib import Path
import io,sys,time,tokenize
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
AMPS=(.00001,.000025,.00005,.0001,.00025,.0005,.001,.0015)
COUNT_MAP={'48':'64','49':'65','52':'68','142':'143','147':'195','1176':'1560'}

def adapt(text):
    value=text
    for old,new in (('ConeRidge52','ConeRidgeFine68'),('ConeRidge49','ConeRidgeFine65'),('ConeRidge24','ConeRidgeFine24'),
        ('ConeRidge142','ConeRidgeFine143'),('ConeRidge_multiyear','ConeRidgeFine_multiyear'),
        ('round142','round143'),('_r142','_r143'),('第142轮','第143轮'),('actual142','actual143'),('full142','full143'),
        ('final142','final143'),('prospective142','prospective143'),('qa53','qa54'),('QA53','QA54'),('qa_v53','qa_v54'),
        ('actual52','actual68'),('actual49','actual65'),('and147','and195'),('195cold','195cold'),('CDF147','CDF195'),('49_current','65_current'),
        ('49full147','65full195'),('49_full147','65_full195'),('WAVES = (425,)','WAVES = (426,)'),
        ('wave=425','wave=426'),('wave425_results','wave426_results'),("'waves': [425]","'waves': [426]")):
        value=value.replace(old,new)
    tokens=list(tokenize.generate_tokens(io.StringIO(value).readline))
    value=tokenize.untokenize([t._replace(string=COUNT_MAP[t.string]) if t.type==tokenize.NUMBER and t.string in COUNT_MAP else t for t in tokens])
    value=value.replace('本轮52项','本轮68项').replace('六种幅度共48项','八种更小幅度共64项').replace('预定52项','预定68项').replace('49完整','65完整').replace('147冷','195冷').replace('all49_nonanchors','all65_nonanchors')
    if 'def collect(number, qa_version, expected_records):' in value:
        value=value.replace('def collect(number, qa_version, expected_records):','def collect(number, expected_records, qa_version):')
        value=value.replace('== (136, 47, 68)','== (143, 54, 68)')
    value=value.replace('actual_complete_QA_version=68','actual_complete_QA_version=54').replace("'actual_full_QA_version': 68","'actual_full_QA_version': 54")
    value=value.replace('collect(143, 68, 53)','collect(143, 68, 54)').replace("'QA_version':53","'QA_version':54")
    value=value.replace("'collect(142, 52, 53)'","'collect(143, 68, 54)'").replace('"namespace[\'snapshot\'](142)"','"namespace[\'snapshot\'](143)"')
    value=value.replace("== full['scored_records'] == 52","== full['scored_records'] == 68")
    value=value.replace('(.0025,.005,.01,.025,.05,.1)',repr(AMPS))
    return value

def save(name,text):
    path=A/name;compile(text,str(path),'exec')
    if path.exists():
        assert name in ('run_ConeRidgeFine68_official_comparison_v1_20261008.py','prepare_ConeRidgeFine68_selected_candidate_v1_20261008.py','seal_ConeRidgeFine68_selected_candidate_v1_20261008.py')
        assert path.read_bytes()==text.encode('utf8'),name
        return path
    path.write_text(text,encoding='utf8',newline='\n');return path

def main():
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    prior=A/'service_owned_workflows_20261006/ConeRidge142_registration_receipt_reconciliation_v2_20261008'
    while not (prior/'native_launch.json').exists() or owned(read(prior/'native_launch.json')):time.sleep(10)
    assert read(prior/'service_execution.json')['status']=='passed'
    assert read(A/'optimization_20261003_r142/full_registration_execution.json')['status']=='passed'
    assert read(A/'github_validation_sync_main_20261005/round142_receipt.json')['status']=='pushed_and_remote_head_verified'
    blueprint=A/'ConeRidgeFine68_round143_blueprint_v1_20261008.json';design=read(blueprint)
    original_plan=A/'ConeRidge52_round142_plan_v1_20261008.json';old=read(original_plan)
    assert tuple(design['amplitudes'])==AMPS and len(design['new_cases'])==64 and design['anchors']==[132,133,134]
    for p,digest in old['input_sha256'].items():assert sha(p)==digest,p
    plan=dict(old);plan.update(status='frozen68_finer_signed_constrained_ridge_cases_before143_quality',
        at_local=time.strftime('%Y-%m-%dT%H:%M:%S'),round=143,amplitudes=list(AMPS),new_cases=design['new_cases'],
        expected_scored_cases=68,expected_transform_cases=65,expected_cold_cases=195,
        additional_native_fits_by_grid=0,own20_models_reused_from_actual_ConeRidge_bank1=True,
        complete142_QA53_main_required_before_this143_quality=True,
        input_sha256={**old['input_sha256'],str(Path(__file__)):sha(__file__),str(blueprint):sha(blueprint),str(original_plan):sha(original_plan)})
    plan_path=A/'ConeRidgeFine68_round143_plan_v1_20261008.json'
    preserved=read(plan_path)
    for key in ('round','amplitudes','new_cases','expected_scored_cases','expected_transform_cases','expected_cold_cases','additional_native_fits_by_grid'):
        assert preserved[key]==plan[key],key
    for path,digest in preserved['input_sha256'].items():assert sha(path)==digest,path
    recovery=A/'ConeRidgeFine143_partial_constructor_recovery_v4_20261008.json'
    assert read(recovery)['status']=='frozen_fresh_driver4_with_exact_three_partial_sources_before_any143_quality'
    for path,digest in read(recovery)['input_sha256'].items():assert sha(path)==digest,path
    originals=[
        'run_ConeRidge52_official_comparison_v1_20261008.py','prepare_ConeRidge52_selected_candidate_v1_20261008.py',
        'seal_ConeRidge52_selected_candidate_v1_20261008.py','run_ConeRidge52_round142_full_registration_v1_20261008.py',
        'publish_ConeRidge52_evidence_v1_20261008.py','verify_ConeRidge52_round142_sources_v1_20261008.py',
        'verify_ConeRidge49_current_parent_v1_20261008.py','ConeRidge142_storage_v1_20261008.py',
        'create_ConeRidge142_output_junctions_v1_20261008.py','verify_ConeRidge142_D_scoring_scope_v1_20261008.py',
        'queue_ConeRidge142_complete_pipeline_v2_20261008.py','verify_ConeRidge49_parent134_historical_v1_20261008.py',
        'verify_ConeRidge24_native_historical_hooks_v1_20261008.py','verify_ConeRidge_multiyear_native_calendar_v1_20261008.py',
        'prepare_ConeRidge142_native_preflight_v1_20261008.py','publish_ConeRidge142_historical_causal_v1_20261008.py',
        'verify_ConeRidge52_prospective_routes_v2_20261008.py','archive_ConeRidge142_completed_scoring_CSV_v1_20261008.py']
    outputs=[];sources=[Path(__file__),blueprint,original_plan,plan_path]
    for name in originals:
        path=A/name;sources.append(path);text=adapt(path.read_text(encoding='utf8')).replace('prepare_ConeRidgeFine143_complete_receivers_v1_20261008.py','prepare_ConeRidgeFine143_complete_receivers_v3_20261008.py')
        if name=='verify_ConeRidge52_prospective_routes_v2_20261008.py':
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
        if 'historical_causal' in name:
            text=text.replace('prepare_ConeRidgeFine143_native_preflight_v1_20261008.py','prepare_ConeRidgeFine143_native_preflight_v1_20261008.py')
        outputs.append(save(adapt(name),text))
    original_generator=A/'prepare_ConeRidge52_round142_sources_v1_20261008.py';sources.append(original_generator)
    tail=adapt(original_generator.read_text(encoding='utf8').split('\ndef main():',1)[1])
    generated='''"""68 declared fine-amplitude routes, with no additional native model fits."""
from pathlib import Path
import hashlib,time
from run_dependency_queue_v3_20261006 import read,sha,create
import prepare_ConeRidge52_round142_sources_v1_20261008 as original
from prepare_ConeRidgeFine68_round143_plan_controls_v4_20261008 import adapt
ROOT=original.ROOT;A=original.A
NAMES={name:adapt(name) for name in original.NAMES.values()}
def generate(parent):return {adapt(name):adapt(text) for name,text in original.generate(parent).items()}
def source_paths():
    existing=[p for p in original.source_paths() if p.is_file()]
    current=[A/adapt(p.relative_to(A).as_posix()) for p in existing]
    current=[p for p in current if p.is_file()]
    required=[Path(__file__).name,'prepare_ConeRidgeFine68_round143_plan_controls_v4_20261008.py','ConeRidgeFine143_partial_constructor_recovery_v4_20261008.json',
        'ConeRidgeFine68_round143_plan_v1_20261008.json','ConeRidgeFine143_storage_v1_20261008.py',
        'ConeRidgeFine143_receiver_drafts_v1_20261008.json','ConeRidgeFine143_receiver_preparation_v1_20261008.json',
        'ConeRidgeFine143_D_scoring_scope_v1_20261008.json','ConeRidgeFine68_prospective_routes_v1_20261008.json',
        'ConeRidgeFine143_native_receiver_preflight_v1_20261008.json',
        'ConeRidgeFine68_actual_controls_index_v1_20261008.json','ConeRidgeFine68_round143_source_admission_v1_20261008.json',
        'ConeRidgeFine68_round143_source_preparation_v1_20261008.json',
        'ConeRidgeFine68_selected_release_v1_20261008/selected_candidate_ready_for_registration.json',
        'ConeRidgeFine68_scores_github_v1_20261008/receipt.json','ConeRidgeFine143_historical_causal_main_v1_20261008/receipt.json']
    return list(dict.fromkeys([*existing,*current,*[A/name for name in [*required,*NAMES.values()]]]))
def main():'''+tail
    outputs.append(save('prepare_ConeRidgeFine68_round143_sources_v1_20261008.py',generated))
    pins={str(p):sha(p) for p in [*sources,*outputs]}
    create(A/'ConeRidgeFine143_receiver_drafts_v1_20261008.json',{
        'status':'prepared_independent68_CPU_receivers_with_completed132133134_parents_after_complete142',
        'input_sha256':pins,'eligible_parents':[132,133,134],'new_official_scores':0,'new_model_fits':0,'test_labels_read':False})
    from ConeRidgeFine143_storage_v1_20261008 import OUTPUTS,EBASE
    create(A/'ConeRidgeFine143_junction_requests_v1_20261008.json',{'workspace':str(ROOT),'E_base':str(EBASE),
        'requests':[{'logical':str(p),'target':str(t)} for p,t in OUTPUTS.items()]})
    from create_ConeRidgeFine143_output_junctions_v1_20261008 import main as junctions
    from verify_ConeRidgeFine143_D_scoring_scope_v1_20261008 import main as dscope
    from prepare_ConeRidgeFine143_native_preflight_v1_20261008 import main as adapters
    junctions();dscope();adapters()
    launches={}
    jobs=[('ConeRidgeFine65_parent134_historical_controls_v1_20261008','verify_ConeRidgeFine65_parent134_historical_v1_20261008.py'),
        ('ConeRidgeFine24_native_historical_hooks_v1_20261008','verify_ConeRidgeFine24_native_historical_hooks_v1_20261008.py'),
        ('ConeRidgeFine_multiyear_native_calendar_v1_20261008','verify_ConeRidgeFine_multiyear_native_calendar_v1_20261008.py')]
    for name,driver in jobs:launches[name]=start(name,driver,[],pins)
    create(A/'actual_ConeRidgeFine68_plan_historical_hidden_launches_v1_20261008.json',{
        'status':'started65_full195_cold24_native24_calendar_with_zero_new_native_fits','input_sha256':pins,'launches':launches,'new_official_scores':0})
    from verify_ConeRidgeFine68_prospective_routes_v2_20261008 import main as prospective
    prospective()
    publisher=A/'publish_ConeRidgeFine143_historical_causal_v1_20261008.py'
    launches['ConeRidgeFine143_historical_causal_main_publication_v1_20261008']=start('ConeRidgeFine143_historical_causal_main_publication_v1_20261008',publisher.name,[],pins)
    from queue_ConeRidgeFine143_complete_pipeline_v2_20261008 import main as queue
    queue()
    archive=A/'archive_ConeRidgeFine143_completed_scoring_CSV_v1_20261008.py'
    launches['ConeRidgeFine143_completed_scoring_CSV_archivist_v1_20261008']=start('ConeRidgeFine143_completed_scoring_CSV_archivist_v1_20261008',archive.name,[],pins)
    create(A/'ConeRidgeFine143_pipeline_preparation_execution_v1_20261008.json',{
        'status':'passed_declared68_fine_amplitude_complete_pipeline_after_full142_qualification',
        'input_sha256':pins,'preliminary_launches':launches,'new_native_fits':0,'new_official_scores':0,
        'actual143_score_and_candidate_and_QA54_main_still_required':True,'test_labels_read':False})
    print('Fine68 complete pipeline dispatched after qualified142; zero new model fits, own65/195 checks before scoring.',flush=True)

if __name__=='__main__':main()
