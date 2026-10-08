"""Fresh receivers restore the exact138139140 parent set before any141 quality work."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute
STEMS=('run_KrylovGram52_official_comparison','prepare_KrylovGram52_selected_candidate',
    'seal_KrylovGram52_selected_candidate','run_KrylovGram52_round141_full_registration','publish_KrylovGram52_evidence',
    'verify_KrylovGram52_round141_sources','verify_KrylovGram49_current_parent','prepare_KrylovGram52_round141_sources')
MAPPING={stem+'_v1_20261008':stem+'_v2_20261008' for stem in STEMS}
for stem in ('KrylovGram49_current_parent_controls','KrylovGram49_current_parent','KrylovGram49_current_parent_full',
    'actual_KrylovGram49_current_parent_location','actual_KrylovGram49_current_parent_full_location',
    'KrylovGram52_round141_source_admission','KrylovGram52_round141_source_preparation','KrylovGram52_actual_controls_index',
    'KrylovGram52_controls_main_publication','KrylovGram52_scores_main_publication','KrylovGram52_official_comparison',
    'KrylovGram52_selected_candidate_preparation','KrylovGram52_selected_candidate_sealing','KrylovGram52_round141_full_registration',
    'KrylovGram52_prospective_routes','KrylovGram141_receiver_preparation','KrylovGram141_receiver_drafts','queue_KrylovGram141_complete_pipeline'):
    MAPPING[stem+'_v1_20261008']=stem+'_v2_20261008'

def remap(text):
    value=substitute(text,MAPPING).replace('(138,139,141)','(138,139,140)').replace('(138, 139, 141)','(138, 139, 140)')
    value=value.replace("A/'KrylovGram52_official_comparison_v2_20261008'","A/'KrylovGram52_official_comparison_v1_20261008'")
    value=value.replace('KrylovGram52_official_comparison_v2_20261008/verification.json','KrylovGram52_official_comparison_v1_20261008/verification.json')
    value=value.replace('KrylovGram52_official_comparison_v2_20261008/frozen_before','KrylovGram52_official_comparison_v1_20261008/frozen_before')
    value=value.replace('KrylovGram52_round141_actual_registration_v1_20261008','KrylovGram52_round141_actual_registration_v2_20261008')
    value=value.replace('run_KrylovGram52_round141_full_registration_v1_file_IO_20261008','run_KrylovGram52_round141_full_registration_v2_file_IO_20261008')
    return value

def adapt(text):
    from prepare_KrylovGram141_complete_receivers_v1_20261008 import adapt as original
    return remap(original(text))

def main():
    from KrylovGram141_storage_v1_20261008 import OUTPUTS,empty
    for p in OUTPUTS:empty(p)
    assert not any((A/'service_owned_workflows_20261006').glob('KrylovGram52_official_comparison_*'))
    sources=[Path(__file__),A/'KrylovGram141_receiver_drafts_v1_20261008.json'];outputs=[]
    for stem in STEMS[:-1]:
        source=A/(stem+'_v1_20261008.py');sources.append(source);text=remap(source.read_text(encoding='utf8'))
        assert '(138,139,141)' not in text and '(138, 139, 141)' not in text
        target=A/(stem+'_v2_20261008.py');assert not target.exists();compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n');outputs.append(target)
    source=A/'prepare_KrylovGram52_round141_sources_v1_20261008.py';sources.append(source)
    text=remap(source.read_text(encoding='utf8')).replace('from prepare_KrylovGram141_complete_receivers_v1_20261008 import adapt','from prepare_KrylovGram141_parent_set_recovery_v2_20261008 import adapt')
    text=text.replace("names=[Path(__file__).name,", "names=[Path(__file__).name,'prepare_KrylovGram141_parent_set_recovery_v2_20261008.py','KrylovGram141_parent_set_recovery_v2_20261008.json',")
    # The original9 drafts remain immutable evidence; fresh2 scientific outputs are pinned by the recovery proof.
    target=A/'prepare_KrylovGram52_round141_sources_v2_20261008.py';assert not target.exists();compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n');outputs.append(target)
    create(A/'KrylovGram141_parent_set_recovery_v2_20261008.json',{
        'status':'prepared_fresh141_receivers_with_exact138139140_parent_set_before_quality',
        'input_sha256':{str(p):sha(p) for p in [*sources,*outputs]},'eligible_parents':[138,139,140],
        'old_sources_and_empty_output_scopes_preserved':True,'new_official_scores':0,'new_model_fits':0,'test_labels_read':False})
    create(A/'KrylovGram141_receiver_drafts_v2_20261008.json',{
        'status':'prepared_complete52_CG_scientific_receivers_with_exact_parent_set_before_quality',
        'input_sha256':{str(p):sha(p) for p in [*sources,*outputs,A/'KrylovGram141_parent_set_recovery_v2_20261008.json']},
        'eligible_parents':[138,139,140],'new_official_scores':0,'source_routes_and_full_queue_still_required':True,'test_labels_read':False})
    print('Fresh2 receivers admit exact138139140 parents; no141 scoring or inference executed.',flush=True)

if __name__=='__main__':main()
