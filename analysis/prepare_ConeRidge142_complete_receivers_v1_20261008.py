"""Prepare an independent full CPU validation route; predeclare all52 results before scoring."""
from pathlib import Path
import io,sys,time,tokenize
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
STEMS=('run_KrylovGram52_official_comparison','prepare_KrylovGram52_selected_candidate',
    'seal_KrylovGram52_selected_candidate','run_KrylovGram52_round141_full_registration','publish_KrylovGram52_evidence',
    'verify_KrylovGram52_round141_sources','verify_KrylovGram49_current_parent')

def adapt(text):
    value=text.replace('KrylovGram','ConeRidge').replace('round141','round142').replace('ConeRidge141','ConeRidge142')
    for before,after in (('full141','full142'),('actual141','actual142'),('final141','final142'),
        ('prospective141','prospective142'),('_r141','_r142'),('第141轮','第142轮'),('qa52','qa53'),('QA52','QA53'),('qa_v52','qa_v53'),
        ('WAVES = (424,)','WAVES = (425,)'),('wave=424','wave=425'),('wave424_results','wave425_results'),("'waves': [424]","'waves': [425]"),
        ('正负重正交共轭梯度变换','正负系数约束岭回归变换'),
        ('(138,139,140)','(132,133,134)'),('(138, 139, 140)','(132, 133, 134)'),
        ('actual_SpectralGram_multiyear_calendar_location_v1_20261008','actual_ConeRidge_multiyear_calendar_location_v1_20261008'),
        ('SpectralGram_multiyear_native_calendar_v1_20261008','ConeRidge_multiyear_native_calendar_v1_20261008'),
        ('SpectralGram52_round140_full_registration_v3_20261008','__ALREADY_QUALIFIED134_NO_WAIT__')):value=value.replace(before,after)
    # Version identifiers are explicit; never replace integer52, which is the number of scored cases.
    names=(*STEMS,'prepare_KrylovGram52_round141_sources','verify_KrylovGram52_prospective_routes','queue_KrylovGram141_complete_pipeline',
        'KrylovGram49_current_parent_controls','KrylovGram49_current_parent','KrylovGram49_current_parent_full',
        'actual_KrylovGram49_current_parent_location','actual_KrylovGram49_current_parent_full_location',
        'KrylovGram52_round141_source_admission','KrylovGram52_round141_source_preparation','KrylovGram52_actual_controls_index',
        'KrylovGram52_controls_main_publication','KrylovGram52_scores_main_publication','KrylovGram52_official_comparison',
        'KrylovGram52_selected_candidate_preparation','KrylovGram52_selected_candidate_sealing','KrylovGram52_round141_full_registration',
        'KrylovGram52_prospective_routes','KrylovGram141_receiver_preparation','KrylovGram141_receiver_drafts',
        'KrylovGram52_round141_actual_registration')
    for name in names:
        new=name.replace('KrylovGram','ConeRidge').replace('round141','round142').replace('ConeRidge141','ConeRidge142')
        value=value.replace(new+'_v2_20261008',new+'_v1_20261008')
    for before,after in (
        ('nonflag_ConeRidge64_streamed_v2_20261008','nonflag_ConeRidge64_streamed_v1_20261008'),
        ('ConeRidge20_causal_refit_v2_20261008','ConeRidge20_causal_refit_v1_20261008'),
        ('ConeRidge20_causal_refit_controls_v2_20261008','ConeRidge20_causal_refit_controls_v1_20261008'),
        ('actual_ConeRidge20_causal_refit_location_v2_20261008','actual_ConeRidge20_causal_refit_location_v1_20261008'),
        ('run_ConeRidge52_round142_full_registration_v2_file_IO','run_ConeRidge52_round142_full_registration_v1_file_IO')):value=value.replace(before,after)
    tokens=list(tokenize.generate_tokens(io.StringIO(value).readline))
    value=tokenize.untokenize([t._replace(string='142') if t.type==tokenize.NUMBER and t.string=='141' else t for t in tokens])
    value=value.replace('collect(142, 52, 52)','collect(142, 52, 53)').replace("'QA_version':52","'QA_version':53")
    value=value.replace("closed('__ALREADY_QUALIFIED134_NO_WAIT__')",'assert_already_qualified_parents()')
    value=value.replace(",'__ALREADY_QUALIFIED134_NO_WAIT__'",'').replace("'__ALREADY_QUALIFIED134_NO_WAIT__',",'')
    value=value.replace(",\n        '__ALREADY_QUALIFIED134_NO_WAIT__'",'')
    value=value.replace(",'__ALREADY_QUALIFIED134_NO_WAIT__'",'')
    assert '__ALREADY_QUALIFIED134_NO_WAIT__' not in value
    return value

def qualification_helper():
    return '''\n\ndef assert_already_qualified_parents():
    for number in (132,133,134):
        assert read(A/f'optimization_20261003_r{number}/full_registration_execution.json')['status']=='passed'
        assert read(A/f'github_validation_sync_main_20261005/round{number}_receipt.json')['status']=='pushed_and_remote_head_verified'
'''

def main():
    folder=A/'service_owned_workflows_20261006/ConeRidge142_plan_controls_preparation_v1_20261008'
    while owned(read(folder/'native_launch.json')):time.sleep(10)
    assert read(folder/'service_execution.json')['status']=='passed'
    plan=A/'ConeRidge52_round142_plan_v1_20261008.json';assert read(plan)['anchors']==[132,133,134]
    sources=[Path(__file__),plan];outputs=[]
    for stem in STEMS:
        old=A/(stem+'_v2_20261008.py');sources.append(old);text=adapt(old.read_text(encoding='utf8'))
        # Old parent-stage quality waits are replaced by already completed132133134 evidence.
        text=text.replace("    for name in ('ConeRidge24_native_historical_hooks_v1_20261008',", "    assert_already_qualified_parents()\n    for name in ('ConeRidge24_native_historical_hooks_v1_20261008',")
        text=text.replace('Exact qualified140 parent admitted','Exact already qualified134 parent admitted')
        text=text.replace('final142_current_parent_controls_still_required_after140_is_qualified=False','final142_current_parent_controls_still_required_after_qualified134=False')
        assert '\nif __name__' in text
        text=text.replace('\nif __name__',qualification_helper()+'\nif __name__')
        target=A/(stem.replace('KrylovGram','ConeRidge').replace('round141','round142')+'_v1_20261008.py')
        assert not target.exists();compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n');outputs.append(target)
    for filename in ('KrylovGram141_storage_v1_20261008.py','verify_KrylovGram141_D_scoring_scope_v1_20261008.py',
        'create_KrylovGram141_output_junctions_v1_20261008.py','queue_KrylovGram141_complete_pipeline_v2_20261008.py'):
        old=A/filename;sources.append(old);text=adapt(old.read_text(encoding='utf8'))
        text=text.replace('==1029','==1176').replace('and1029 full graph','and1176 full graph')
        target=A/filename.replace('KrylovGram','ConeRidge').replace('ConeRidge141','ConeRidge142').replace('_v2_20261008','_v1_20261008')
        assert not target.exists();compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n');outputs.append(target)
    create(A/'ConeRidge142_receiver_drafts_v1_20261008.json',{
        'status':'prepared_independent52_CPU_receivers_with_completed132133134_parent_set_before_quality',
        'input_sha256':{str(p):sha(p) for p in [*sources,*outputs]},'eligible_parents':[132,133,134],
        'original135141_frozen_sources_preserved':True,'unfinished135141_scientific_service_dependency':False,
        'new_official_scores':0,'new_model_fits':0,'source_routes_and_actual_queue_still_required':True,'test_labels_read':False})
    from ConeRidge142_storage_v1_20261008 import OUTPUTS,EBASE
    create(A/'ConeRidge142_junction_requests_v1_20261008.json',{'workspace':str(ROOT),'E_base':str(EBASE),
        'requests':[{'logical':str(p),'target':str(t)} for p,t in OUTPUTS.items()]})
    print('Independent142 CPU receivers compiled; anchors132133134, no unfinished neural quality waits.',flush=True)

if __name__=='__main__':main()
