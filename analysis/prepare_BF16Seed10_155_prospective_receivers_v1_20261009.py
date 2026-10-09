"""Prepare complete individual-seed155 publication, duplicate and56-route contracts before quality."""
from pathlib import Path
import sys,io,tokenize,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
from prepare_BF16Seed10_155_core_drafts_v1_20261009 import route
def main():
    inputs=[Path(__file__)];drafts=[]
    src=A/'publish_BF16Medium78_evidence_v2_20261009.py';dst=A/'publish_BF16Seed10_80_evidence_v1_20261009.py';s=route(src.read_text(encoding='utf8'))
    s=s.replace('SparseAfter14829_round152_full_registration_v1_20261009','BF16TwoSeed79_round154_full_registration_v1_20261009')
    s=s.replace('BF16Seed10_155_actual_full73_training_v1_20261009','BF16Seed10_155_actual_full73_training_v2_20261009')
    s=s.replace('from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle\n','')
    s=s.replace('    held=[]','    from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle\n    held=[]')
    needle="    with safe(Path('E:/赛题五_本机临时/第155轮_20261009')/('safe_'+phase+'_main_v1')):main(phase)";assert s.count(needle)==1
    s=s.replace(needle,"    from serial_main_publication_mutex_v1_20261009 import installed as serial\n    log=Path('E:/赛题五_本机临时/第155轮_20261009')/('safe_'+phase+'_main_v1')\n    with safe(log),serial(log/'serial_mutex.json'):main(phase)")
    drafts.append((src,dst,s))
    src=A/'verify_BF16Medium153_prior_complete_forecast_duplicate_audit_v1_20261009.py';dst=A/'verify_BF16Seed10_155_prior_complete_forecast_duplicate_audit_v1_20261009.py';s=route(src.read_text(encoding='utf8'))
    s=s.replace('SparseAfter14829_round152_full_registration_v1_20261009','BF16TwoSeed79_round154_full_registration_v1_20261009')
    s=s.replace('round152','round154').replace('_r152','_r154')
    needle="    closed('BF16TwoSeed79_round154_full_registration_v1_20261009')";assert s.count(needle)==1
    s=s.replace(needle,needle+"\n    closed('BF16Seed10_155_actual_full73_training_v2_20261009')")
    drafts.append((src,dst,s))
    src=A/'verify_BF16Medium78_prospective_routes_v1_20261009.py';dst=A/'verify_BF16Seed10_80_prospective_routes_v1_20261009.py';s=route(src.read_text(encoding='utf8'))
    s=s.replace('[148,149,150,151,152]','[148,149,150,151,152,153,154]')
    s=s.replace("'round155_full_scope' / source.relative_to(ROOT)","'round155_full_scope' / (source.relative_to(ROOT) if source.is_relative_to(ROOT)")
    s=s.replace('len(outputs)==5','len(outputs)==7').replace('==40','==56').replace('==1500','==2100').replace('==15','==21').replace('==10','==14')
    s=s.replace("'prospective_sources':40","'prospective_sources':56").replace("'graph_controls':1500","'graph_controls':2100").replace("'baselines':15","'baselines':21").replace("'physical_model_ties':10","'physical_model_ties':14")
    s=s.replace('actual40_seed10_155_prospective_sources1500_graphs15_baselines10','actual56_seed10_155_prospective_sources2100_graphs21_baselines14')
    s=s.replace('collect(153, 64, 78)','collect(155, 66, 80)').replace("actual_full_QA_version': 64","actual_full_QA_version': 66").replace("namespace['snapshot'](153)","namespace['snapshot'](155)")
    s=tokenize.untokenize([t._replace(string='66') if t.type==tokenize.NUMBER and t.string=='64' else t for t in tokenize.generate_tokens(io.StringIO(s).readline)])
    s=s.replace("missing={p for p in g.source_paths() if not p.is_file()}","allowed.update({A/'actual_BF16Seed10_155_full73_training_location_v1_20261009.json'})\n    missing={p for p in g.source_paths() if not p.is_file()}")
    drafts.append((src,dst,s))
    assert all(not dst.exists() for _,dst,_ in drafts)
    for src,dst,s in drafts:compile(s,str(dst),'exec');dst.write_text(s,encoding='utf8');inputs.extend((src,dst))
    inputs.extend(A/n for n in ('run_BF16Seed10_80_official_comparison_v1_20261009.py','prepare_BF16Seed10_80_selected_candidate_v1_20261009.py',
        'seal_BF16Seed10_80_selected_candidate_v1_20261009.py','run_BF16Seed10_80_round155_full_registration_v1_20261009.py'))
    create(A/'BF16Seed10_155_actual_receiver_bindings_v1_20261009.json',{'status':'prepared_individual_seed10_155_receivers_before_prospective_and_admission',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in inputs},
        'publisher_predecessor_round':154,'ordered_physical_native_components':1,'own_seed':20261010,
        'official_quality_admitted':False,'test_labels_read':False})
    print({'prospective_sources_expected':56,'graphs_expected':2100,'quality_admitted':False})
if __name__=='__main__':main()
