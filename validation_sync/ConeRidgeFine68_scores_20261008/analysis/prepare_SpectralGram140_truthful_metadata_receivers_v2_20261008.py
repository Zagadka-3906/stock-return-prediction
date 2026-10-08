"""Fresh2 receivers correct bookkeeping before first score; scientific math/model bytes remain unchanged."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute
STEMS=('verify_SpectralGram49_current_parent','verify_SpectralGram52_round140_sources',
    'run_SpectralGram52_official_comparison','prepare_SpectralGram52_selected_candidate',
    'seal_SpectralGram52_selected_candidate','run_SpectralGram52_round140_full_registration',
    'publish_SpectralGram52_evidence','queue_SpectralGram140_complete_pipeline',
    'prepare_SpectralGram52_round140_sources')
MAPPING={stem+'_v1_20261008':stem+'_v2_20261008' for stem in STEMS}
for stem in ('SpectralGram49_current_parent_controls','SpectralGram49_current_parent',
    'SpectralGram49_current_parent_full','actual_SpectralGram49_current_parent_location','actual_SpectralGram49_current_parent_full_location',
    'SpectralGram52_round140_source_admission','SpectralGram52_round140_source_preparation','SpectralGram52_controls_main_publication',
    'SpectralGram52_scores_main_publication','SpectralGram52_official_comparison','SpectralGram52_selected_candidate_preparation',
    'SpectralGram52_selected_candidate_sealing','SpectralGram52_round140_full_registration','SpectralGram52_actual_controls_index',
    'SpectralGram140_receiver_preparation','SpectralGram140_complete_dependency_plan','SpectralGram140_complete_hidden_launches'):
    MAPPING[stem+'_v1_20261008']=stem+'_v2_20261008'
MAPPING['SpectralGram52_prospective_routes_v1_20261008']='SpectralGram52_prospective_routes_v2_20261008'
MAPPING['verify_SpectralGram52_prospective_routes_v1_20261008']='verify_SpectralGram52_prospective_routes_v3_20261008'


def remap(text):
    value=substitute(text,MAPPING)
    # Service identifiers are2; the six already-admitted empty physical outputs stay1.
    value=value.replace("A/'SpectralGram52_official_comparison_v2_20261008'","A/'SpectralGram52_official_comparison_v1_20261008'")
    value=value.replace('SpectralGram52_official_comparison_v2_20261008/verification.json','SpectralGram52_official_comparison_v1_20261008/verification.json')
    value=value.replace('SpectralGram52_official_comparison_v2_20261008/frozen_before','SpectralGram52_official_comparison_v1_20261008/frozen_before')
    return value


def main():
    launches=read(A/'SpectralGram140_complete_hidden_launches_v1_20261008.json')['launches']
    for name,row in launches.items():assert owned(row) and not Path(row['stderr']).stat().st_size,name
    assert not any((A/'SpectralGram52_official_comparison_v1_20261008').iterdir())
    assert not Path('E:/赛题五_本机临时/SpectralGram49_current_parent_v1_20261008').exists()
    sources=[Path(__file__),A/'SpectralGram140_complete_hidden_launches_v1_20261008.json'];outputs=[]
    for stem in STEMS[:-1]:
        source=A/(stem+'_v1_20261008.py');text=remap(source.read_text(encoding='utf8'));sources.append(source)
        if stem=='verify_SpectralGram52_round140_sources':
            text=text.replace("'actual_cold_transform_controls':327","'actual_cold_transform_controls':147")
            text=text.replace("'actual_calendar_cases':18","'actual_calendar_cases':24")
            text=text.replace('139 first quality admitted after actual25,109/327,18 hooks','140 first quality admitted after actual20,49/147,24 hooks')
        elif stem=='verify_SpectralGram49_current_parent':
            text=text.replace('final139_current_parent_controls_still_required_after138_is_qualified=False','final140_current_parent_controls_still_required_after139_is_qualified=False')
            text=text.replace('passed_current_parent109_327_on_E','passed_current_parent49_147_on_E')
            text=text.replace('Exact qualified139 parent admitted by completed109/327','Exact qualified140 parent admitted by completed49/147')
        elif stem=='queue_SpectralGram140_complete_pipeline':
            text=text.replace('Eight consoleless139 workers started','Eight consoleless140 workers started')
        target=A/(stem+'_v2_20261008.py');assert not target.exists();compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n');outputs.append(target)
    # The immutable prior generator supplies the same mathematics, with only receiver identifiers changed.
    text='''"""Fresh2 identifiers for the same52-case registry and QA51 mathematics."""
from pathlib import Path
import hashlib,time
from run_dependency_queue_v3_20261006 import read,sha,create
import prepare_SpectralGram52_round140_sources_v1_20261008 as original
from prepare_SpectralGram140_truthful_metadata_receivers_v2_20261008 import remap
ROOT=original.ROOT;A=original.A;NAMES=original.NAMES
def source_paths():
    paths=[A/remap(p.relative_to(A).as_posix()) for p in original.source_paths()]
    paths += [p for p in original.source_paths() if p.is_file()]
    paths += [Path(__file__),A/'prepare_SpectralGram140_truthful_metadata_receivers_v2_20261008.py',
        A/'SpectralGram140_truthful_metadata_receiver_preparation_v2_20261008.json',A/'verify_SpectralGram52_prospective_routes_v3_20261008.py']
    return list(dict.fromkeys(paths))
def generate(parent):return {name:remap(text) for name,text in original.generate(parent).items()}
def main():
    ready_path=A/'SpectralGram52_selected_release_v1_20261008/selected_candidate_ready_for_registration.json';ready=read(ready_path)
    assert ready['status']=='passed_actual52_selected_candidate_full_graph_and_metrics_and_source_bytes' and ready['sealed_candidate_complete']
    pilot=read(A/'SpectralGram52_official_comparison_v1_20261008/verification.json');assert len(pilot['records'])==52 and pilot['best']==ready['best']
    proof_path=A/'SpectralGram52_round140_source_admission_v2_20261008.json';proof=read(proof_path)
    assert proof['status']=='passed_actual20_heads49_current_CDF147cold24hooks_and24_prospective140_sources'
    for path,digest in proof['input_sha256'].items():assert sha(path)==digest,path
    generated=generate(pilot['actual_comparison_parent_round'])
    for name,text in generated.items():
        assert not (A/name).exists() and hashlib.sha256(text.encode()).hexdigest()==proof['generated_source_sha256'][str(pilot['actual_comparison_parent_round'])][name]
    for name,text in generated.items():(A/name).write_text(text,encoding='utf8',newline='\\n')
    create(A/'SpectralGram52_round140_source_preparation_v2_20261008.json',{
        'status':'passed_actual52_sealed_candidate_and_admitted_full140_QA51_sources','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'round':140,'scored_records':52,'actual_comparison_parent_round':pilot['actual_comparison_parent_round'],
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),ready_path,proof_path,*[A/name for name in generated]]},
        'new_quality_scores':0,'test_labels_read':False})
if __name__=='__main__':main()
'''
    target=A/'prepare_SpectralGram52_round140_sources_v2_20261008.py';assert not target.exists();compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n');outputs.append(target)
    source=A/'verify_SpectralGram52_prospective_routes_v2_20261008.py';sources.append(source);text=remap(source.read_text(encoding='utf8'))
    text=text.replace('HuberCrossFamily139_cross_volume_byte_probe_v1','SpectralGram140_cross_volume_byte_probe_v2').replace('SpectralGram140_cross_volume_byte_probe_v1','SpectralGram140_cross_volume_byte_probe_v2')
    text=text.replace('cross_volume_byte_probe_v1.bin','cross_volume_byte_probe_v2.bin')
    target=A/'verify_SpectralGram52_prospective_routes_v3_20261008.py';assert not target.exists();compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n');outputs.append(target)
    create(A/'SpectralGram140_truthful_metadata_receiver_preparation_v2_20261008.json',{
        'status':'prepared_fresh2_receivers_before_any140_score_or_current_native_control','input_sha256':{str(p):sha(p) for p in [*sources,*outputs]},
        'fixed_fields':{'actual_cold_transform_controls':147,'actual_calendar_cases':24,'final140_current_parent_controls_still_required_after139_is_qualified':False},
        'scientific_model_and_math_and_grid_and_physical_output_bytes_unchanged':True,'actual_quality_scores':0,
        'old_eight_queue_jobs_still_live_pending_prospective3_then_exact_retirement':True,'test_labels_read':False})
    print('Fresh2 truthful metadata receivers and prospective3 prepared; original scientific bytes preserved.',flush=True)


if __name__=='__main__':main()
