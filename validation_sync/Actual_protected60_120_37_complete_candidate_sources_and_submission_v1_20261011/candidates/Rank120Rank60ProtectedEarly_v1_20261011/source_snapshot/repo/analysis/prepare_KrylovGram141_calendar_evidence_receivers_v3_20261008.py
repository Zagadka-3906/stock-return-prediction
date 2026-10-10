"""Fresh141 receivers bind calendar evidence to their own CG family, preserving all frozen2 sources."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute
STEMS=('run_KrylovGram52_official_comparison','prepare_KrylovGram52_selected_candidate','seal_KrylovGram52_selected_candidate',
    'run_KrylovGram52_round141_full_registration','publish_KrylovGram52_evidence','verify_KrylovGram52_round141_sources',
    'verify_KrylovGram49_current_parent','prepare_KrylovGram52_round141_sources','verify_KrylovGram52_prospective_routes','queue_KrylovGram141_complete_pipeline')
MAPPING={stem+'_v2_20261008':stem+'_v3_20261008' for stem in STEMS}
for stem in ('KrylovGram49_current_parent_controls','KrylovGram49_current_parent','KrylovGram49_current_parent_full',
    'actual_KrylovGram49_current_parent_location','actual_KrylovGram49_current_parent_full_location',
    'KrylovGram52_round141_source_admission','KrylovGram52_round141_source_preparation','KrylovGram52_actual_controls_index',
    'KrylovGram52_controls_main_publication','KrylovGram52_scores_main_publication','KrylovGram52_official_comparison',
    'KrylovGram52_selected_candidate_preparation','KrylovGram52_selected_candidate_sealing','KrylovGram52_round141_full_registration',
    'KrylovGram52_prospective_routes','KrylovGram141_receiver_preparation','KrylovGram141_receiver_drafts',
    'KrylovGram141_complete_dependency_plan','KrylovGram141_complete_hidden_launches'):
    MAPPING[stem+'_v2_20261008']=stem+'_v3_20261008'

def remap(text):
    value=substitute(text,MAPPING)
    value=value.replace("A/'KrylovGram52_official_comparison_v3_20261008'","A/'KrylovGram52_official_comparison_v1_20261008'")
    value=value.replace('KrylovGram52_official_comparison_v3_20261008/verification.json','KrylovGram52_official_comparison_v1_20261008/verification.json')
    value=value.replace('KrylovGram52_official_comparison_v3_20261008/frozen_before','KrylovGram52_official_comparison_v1_20261008/frozen_before')
    value=value.replace('KrylovGram52_round141_actual_registration_v2_20261008','KrylovGram52_round141_actual_registration_v3_20261008')
    value=value.replace('run_KrylovGram52_round141_full_registration_v2_file_IO','run_KrylovGram52_round141_full_registration_v3_file_IO')
    # The141 family has completed its own24 saved-model calendar and48 independent day controls.
    value=value.replace('actual_SpectralGram_multiyear_calendar_location_v1_20261008','actual_KrylovGram_multiyear_calendar_location_v1_20261008')
    value=value.replace('SpectralGram_multiyear_native_calendar_v1_20261008','KrylovGram_multiyear_native_calendar_v1_20261008')
    return value

def main():
    from KrylovGram141_storage_v1_20261008 import OUTPUTS,empty
    for p in OUTPUTS:empty(p)
    pointer=A/'actual_KrylovGram_multiyear_calendar_location_v1_20261008.json'
    path=Path(read(pointer)['output'])/'verification.json';proof=read(path)
    assert sha(path)==read(pointer)['verification_sha256'] and proof['actual_calendar_cases']==24 and proof['actual_whole_day_controls']==48
    assert proof['status']=='passed_actual24_KrylovGram_saved2025_calendar_controls_and48_day_controls'
    sources=[Path(__file__),pointer,path];outputs=[]
    for stem in (*STEMS[:7],STEMS[-2],STEMS[-1]):
        old=A/(stem+'_v2_20261008.py');sources.append(old);text=remap(old.read_text(encoding='utf8'))
        if 'prospective' in stem:text=text.replace('KrylovGram141_cross_volume_byte_probe_v2','KrylovGram141_cross_volume_byte_probe_v3').replace('cross_volume_byte_probe_v2.bin','cross_volume_byte_probe_v3.bin')
        target=A/(stem+'_v3_20261008.py');assert not target.exists();compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n');outputs.append(target)
    old=A/'prepare_KrylovGram52_round141_sources_v2_20261008.py';sources.append(old)
    text='''"""Receiver3 routes bind original141 science to its own completed calendar controls."""
from pathlib import Path
import hashlib,time
from run_dependency_queue_v3_20261006 import read,sha,create
import prepare_KrylovGram52_round141_sources_v2_20261008 as original
from prepare_KrylovGram141_calendar_evidence_receivers_v3_20261008 import remap
ROOT=original.ROOT;A=original.A;NAMES=original.NAMES
def source_paths():
    paths=[A/remap(p.relative_to(A).as_posix()) for p in original.source_paths()]
    paths += [p for p in original.source_paths() if p.is_file()]
    paths += [Path(__file__),A/'prepare_KrylovGram141_calendar_evidence_receivers_v3_20261008.py',
        A/'KrylovGram141_calendar_evidence_receiver_recovery_v3_20261008.json']
    return list(dict.fromkeys(paths))
def generate(parent):return {name:remap(text) for name,text in original.generate(parent).items()}
def main():
    ready_path=A/'KrylovGram52_selected_release_v1_20261008/selected_candidate_ready_for_registration.json';ready=read(ready_path)
    assert ready['status']=='passed_actual52_selected_candidate_full_graph_and_metrics_and_source_bytes' and ready['sealed_candidate_complete']
    pilot=read(A/'KrylovGram52_official_comparison_v1_20261008/verification.json');assert len(pilot['records'])==52 and pilot['best']==ready['best']
    proof_path=A/'KrylovGram52_round141_source_admission_v3_20261008.json';proof=read(proof_path)
    assert proof['status']=='passed_actual20_heads49_current_CDF147cold24hooks_and24_prospective141_sources'
    for path,digest in proof['input_sha256'].items():assert sha(path)==digest,path
    generated=generate(pilot['actual_comparison_parent_round'])
    for name,text in generated.items():
        assert not (A/name).exists() and hashlib.sha256(text.encode()).hexdigest()==proof['generated_source_sha256'][str(pilot['actual_comparison_parent_round'])][name]
    for name,text in generated.items():(A/name).write_text(text,encoding='utf8',newline='\\n')
    create(A/'KrylovGram52_round141_source_preparation_v3_20261008.json',{
        'status':'passed_actual52_sealed_candidate_and_admitted_full141_QA52_sources','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'round':141,'scored_records':52,'actual_comparison_parent_round':pilot['actual_comparison_parent_round'],
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),ready_path,proof_path,*[A/name for name in generated]]},
        'new_quality_scores':0,'test_labels_read':False})
if __name__=='__main__':main()
'''
    target=A/'prepare_KrylovGram52_round141_sources_v3_20261008.py';assert not target.exists();compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n');outputs.append(target)
    create(A/'KrylovGram141_calendar_evidence_receiver_recovery_v3_20261008.json',{
        'status':'prepared_fresh141_receivers_bind_own_CG24calendar48day_before_quality',
        'input_sha256':{str(p):sha(p) for p in [*sources,*outputs]},'calendar_source':str(path),
        'old2_sources_preserved':True,'native_model_scoring_grid_math_and_physical_outputs_unchanged':True,
        'actual_quality_scores':0,'test_labels_read':False})
    create(A/'KrylovGram141_receiver_drafts_v3_20261008.json',{
        'status':'prepared_complete52_CG_scientific_receivers_with_exact_parent_set_and_own_calendar',
        'input_sha256':{str(p):sha(p) for p in [*sources,*outputs,A/'KrylovGram141_calendar_evidence_receiver_recovery_v3_20261008.json']},
        'eligible_parents':[138,139,140],'new_official_scores':0,'source_routes_and_full_queue_still_required':True,'test_labels_read':False})
    print('Fresh141 source3 binds completed own-CG calendar24/day48; frozen2 science preserved.',flush=True)

if __name__=='__main__':main()
