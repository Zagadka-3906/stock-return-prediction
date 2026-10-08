"""Prepare complete52-case CG scoring/freeze/inference/registration receivers before quality."""
from pathlib import Path
import io,sys,tokenize
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute

STEMS=('run_SpectralGram52_official_comparison','prepare_SpectralGram52_selected_candidate',
    'seal_SpectralGram52_selected_candidate','run_SpectralGram52_round140_full_registration',
    'publish_SpectralGram52_evidence','verify_SpectralGram52_round140_sources','verify_SpectralGram49_current_parent')

def adapt(text):
    marker='__EXACT_QUALIFIED_PARENT140_REGISTRATION__'
    value=text.replace('HuberCrossFamily112_round139_full_registration_v1_20261008',marker)
    mapping={}
    for stem in (*STEMS,'prepare_SpectralGram52_round140_sources','queue_SpectralGram140_complete_pipeline'):
        target=stem.replace('SpectralGram52','KrylovGram52').replace('SpectralGram49','KrylovGram49').replace('SpectralGram140','KrylovGram141').replace('round140','round141')+'_v1_20261008'
        mapping[stem+'_v2_20261008']=target
        mapping[stem+'_v3_20261008']=target
    for stem in ('SpectralGram49_current_parent_controls','SpectralGram49_current_parent','SpectralGram49_current_parent_full',
        'actual_SpectralGram49_current_parent_location','actual_SpectralGram49_current_parent_full_location',
        'SpectralGram52_round140_source_admission','SpectralGram52_round140_source_preparation','SpectralGram52_actual_controls_index',
        'SpectralGram52_controls_main_publication','SpectralGram52_scores_main_publication','SpectralGram52_official_comparison',
        'SpectralGram52_selected_candidate_preparation','SpectralGram52_selected_candidate_sealing','SpectralGram52_round140_full_registration',
        'SpectralGram52_prospective_routes','SpectralGram141_receiver_preparation'):
        mapping[stem+'_v2_20261008']=stem.replace('SpectralGram','KrylovGram').replace('round140','round141')+'_v1_20261008'
    mapping.update({'actual_SpectralGram24_native_hooks_location_v2_20261008':'actual_KrylovGram24_native_hooks_location_v1_20261008',
        'SpectralGram24_native_historical_hooks_v2_20261008':'KrylovGram24_native_historical_hooks_v1_20261008',
        'actual_SpectralGram20_causal_refit_location_v1_20261008':'actual_KrylovGram20_causal_refit_location_v2_20261008',
        'SpectralGram20_causal_refit_controls_v1_20261008':'KrylovGram20_causal_refit_controls_v2_20261008',
        'SpectralGram52_round140_actual_registration_v3_20261008':'KrylovGram52_round141_actual_registration_v1_20261008',
        'run_SpectralGram52_round140_full_registration_v3_file_IO_20261008':'run_KrylovGram52_round141_full_registration_v1_file_IO_20261008',
        'SpectralGram140_receiver_preparation_v2_20261008':'KrylovGram141_receiver_preparation_v1_20261008',
        'SpectralGram52_prospective_routes_v2_20261008':'KrylovGram52_prospective_routes_v1_20261008'})
    value=substitute(value,mapping)
    for before,after in (('SpectralGram140','KrylovGram141'),('SpectralGram52','KrylovGram52'),('SpectralGram49','KrylovGram49'),
        ('SpectralGram64','KrylovGram64'),('SpectralGram24','KrylovGram24'),('SpectralGram20','KrylovGram20'),
        ('SpectralGram_CDF','KrylovGram_CDF'),('SpectralGram_group','KrylovGram_group'),('zero_SpectralGram','zero_KrylovGram'),
        ('round140','round141'),('full140','full141'),('actual140','actual141'),('final140','final141'),('after139','after140'),
        ('prospective140','prospective141'),('_r140','_r141'),('第140轮','第141轮'),('qa51','qa52'),('QA51','QA52'),('qa_v51','qa_v52'),
        ('WAVES = (423,)','WAVES = (424,)'),('wave=423','wave=424'),('wave423_results','wave424_results'),("'waves': [423]","'waves': [424]"),
        ('正负主成分截断变换','正负重正交共轭梯度变换'),
        ('passed_actual52_CrossFamily_complete_parent_full_official_comparisons','passed_actual52_KrylovGram_complete_parent_full_official_comparisons')):
        value=value.replace(before,after)
    value=value.replace('(137,138,139)','(138,139,140)').replace('(137, 138, 139)','(138, 139, 140)')
    tokens=list(tokenize.generate_tokens(io.StringIO(value).readline))
    value=tokenize.untokenize([token._replace(string={'140':'141','51':'52'}[token.string]) if token.type==tokenize.NUMBER and token.string in ('140','51') else token for token in tokens])
    return value.replace(marker,'SpectralGram52_round140_full_registration_v3_20261008')

def main():
    plan=A/'KrylovGram52_round141_plan_v1_20261008.json';assert read(plan)['expected_scored_cases']==52
    sources=[Path(__file__),plan];outputs={}
    for stem in STEMS:
        version=3 if 'full_registration' in stem else 2
        source=A/(stem+f'_v{version}_20261008.py');sources.append(source)
        target=A/(stem.replace('SpectralGram52','KrylovGram52').replace('SpectralGram49','KrylovGram49').replace('round140','round141')+'_v1_20261008.py')
        text=adapt(source.read_text(encoding='utf8'));assert not target.exists();compile(text,str(target),'exec');outputs[target]=text
    for old,new in (('SpectralGram140_storage_v1_20261008.py','KrylovGram141_storage_v1_20261008.py'),
        ('verify_SpectralGram140_D_scoring_scope_v1_20261008.py','verify_KrylovGram141_D_scoring_scope_v1_20261008.py')):
        source=A/old;sources.append(source);text=adapt(source.read_text(encoding='utf8'));target=A/new
        assert not target.exists();compile(text,str(target),'exec');outputs[target]=text
    for path,text in outputs.items():path.write_text(text,encoding='utf8',newline='\n')
    create(A/'KrylovGram141_receiver_drafts_v1_20261008.json',{
        'status':'prepared_complete52_CG_scientific_receivers_before_quality','input_sha256':{str(p):sha(p) for p in [*sources,*outputs]},
        'new_official_scores':0,'new_future_X_calls':0,'prospective_source_routes_and_queue_still_required':True,'test_labels_read':False})
    from KrylovGram141_storage_v1_20261008 import OUTPUTS,EBASE
    create(A/'KrylovGram141_junction_requests_v1_20261008.json',{'workspace':str(ROOT),'E_base':str(EBASE),'requests':[{'logical':str(p),'target':str(t)} for p,t in OUTPUTS.items()]})
    print('Complete141 scientific receivers compiled; exact parent140 registration3 gate retained.',flush=True)

if __name__=='__main__':main()
