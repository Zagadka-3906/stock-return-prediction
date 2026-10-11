"""Prepare receiver contracts and prospective checks; do not admit quality scoring."""
from pathlib import Path
import sys,io,tokenize,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
from prepare_BF16TwoSeed154_core_drafts_v1_20261009 import route,replace
def main():
    old=A/'publish_BF16Medium78_evidence_v2_20261009.py';pub=A/'publish_BF16TwoSeed79_evidence_v1_20261009.py'
    s=route(old.read_text(encoding='utf8'))
    s=replace(s,"closed('SparseAfter14829_round152_full_registration_v1_20261009')","closed('BF16Medium78_round153_full_registration_v1_20261009')")
    s=s.replace('passed_actual6_medium153_states42_native73_full219_cold_controls','passed_actual12_two_seed154_states42_native73_full219_cold_controls')
    s=s.replace("'actual_existing_native_head_audits':6","'actual_existing_native_head_audits':12").replace("'actual_full_native_OOF_heads':1","'actual_full_native_OOF_heads':2")
    s=replace(s,'from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle\n','')
    s=replace(s,'    held=[]','    from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle\n    held=[]')
    s=replace(s,"    with safe(Path('E:/赛题五_本机临时/第154轮_20261009')/('safe_'+phase+'_main_v1')):main(phase)",
        "    from serial_main_publication_mutex_v1_20261009 import installed as serial\n    log=Path('E:/赛题五_本机临时/第154轮_20261009')/('safe_'+phase+'_main_v1')\n    with safe(log),serial(log/'serial_mutex.json'):main(phase)")
    compile(s,str(pub),'exec');assert not pub.exists();pub.write_text(s,encoding='utf8')
    oldproof=A/'verify_BF16Medium78_prospective_routes_v1_20261009.py';prospective=A/'verify_BF16TwoSeed79_prospective_routes_v1_20261009.py'
    s=route(oldproof.read_text(encoding='utf8')).replace('run_BF16TwoSeed79_official_comparison_v2','run_BF16TwoSeed79_official_comparison_v1')
    s=s.replace('run_BF16TwoSeed79_round154_full_registration_v3','run_BF16TwoSeed79_round154_full_registration_v1')
    s=s.replace('publish_BF16TwoSeed79_evidence_v2','publish_BF16TwoSeed79_evidence_v1')
    s=s.replace('BF16TwoSeed154_actual_receiver_bindings_v2','BF16TwoSeed154_actual_receiver_bindings_v1')
    s=replace(s,"[148,149,150,151,152]","[148,149,150,151,152,153]")
    s=s.replace('len(outputs)==5','len(outputs)==6').replace('==40','==48').replace('==1500','==1800').replace('==15','==18').replace('==10','==12')
    s=s.replace('prospective_sources\':40','prospective_sources\':48').replace('graph_controls\':1500','graph_controls\':1800').replace('baselines\':15','baselines\':18').replace('physical_model_ties\':10','physical_model_ties\':12')
    s=s.replace('actual40_medium153_prospective_sources1500_graphs15_baselines10','actual48_two_seed154_prospective_sources1800_graphs18_baselines12')
    s=replace(s,"'round154_full_scope' / source.relative_to(ROOT)","'round154_full_scope' / (source.relative_to(ROOT) if source.is_relative_to(ROOT)")
    s=replace(s,"[plan['model_name']] if c['weight'] else []","plan['native_component_names'] if c['weight'] else []")
    s=replace(s,"assert new['first2020_active'] and new['original_complete_parent_round']==148 and new['invalid_signal_bits_preserved']",
        "assert new['first2020_active'] and new['original_complete_parent_round']==148 and new['invalid_signal_bits_preserved']\n                    assert new['seed_weights']==[.5,.5] and new['seed_values']==[20261009,20261010]\n                    assert new['ordered_native_component_names']==plan['native_component_names']")
    s=tokenize.untokenize([t._replace(string='65') if t.type==tokenize.NUMBER and t.string=='64' else t for t in tokenize.generate_tokens(io.StringIO(s).readline)])
    s=s.replace('collect(154, 64, 79)','collect(154, 65, 79)')
    # Explicitly declared future-only files; none are treated as verified yet.
    s=replace(s,"missing={p for p in g.source_paths() if not p.is_file()}",
        "allowed.update({A/'verify_BF16TwoSeed79_round154_sources_v1_20261009.py',A/'verify_BF16TwoSeed154_prior_complete_forecast_duplicate_audit_v1_20261009.py'})\n    missing={p for p in g.source_paths() if not p.is_file()}")
    compile(s,str(prospective),'exec');assert not prospective.exists();prospective.write_text(s,encoding='utf8')
    olddup=A/'verify_BF16Medium153_prior_complete_forecast_duplicate_audit_v1_20261009.py';dup=A/'verify_BF16TwoSeed154_prior_complete_forecast_duplicate_audit_v1_20261009.py'
    s=route(olddup.read_text(encoding='utf8'))
    s=s.replace('SparseAfter14829_round152_full_registration_v1_20261009','BF16Medium78_round153_full_registration_v1_20261009')
    s=s.replace('round152','round153').replace('_r152','_r153')
    s=s.replace('passed_actual73_full5635800_medium153_signed_rank_mix_and219_cold_prefixes','passed_actual73_full5635800_two_seed154_signed_rank_mix_and219_cold_prefixes')
    s=replace(s,"proposal['new_cases']","proposal['scientific_cases']")
    s=replace(s,"    closed('BF16Medium78_round153_full_registration_v1_20261009')",
        "    closed('BF16Medium78_round153_full_registration_v1_20261009')\n    closed('BF16TwoSeed154_actual_full73_training_v1_20261009')")
    compile(s,str(dup),'exec');assert not dup.exists();dup.write_text(s,encoding='utf8')
    sources=[Path(__file__),old,pub,oldproof,prospective,olddup,dup,A/'run_BF16TwoSeed79_official_comparison_v1_20261009.py',
        A/'prepare_BF16TwoSeed79_selected_candidate_v1_20261009.py',A/'seal_BF16TwoSeed79_selected_candidate_v1_20261009.py',
        A/'run_BF16TwoSeed79_round154_full_registration_v1_20261009.py']
    create(A/'BF16TwoSeed154_actual_receiver_bindings_v1_20261009.json',{
        'status':'prepared_two_seed154_receivers_before_complete_prospective_and_admission',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in sources},
        'publisher_predecessor_round':153,'current_scoring_source':'run_BF16TwoSeed79_official_comparison_v1_20261009.py',
        'current_publisher_source':pub.name,'current_registration_source':'run_BF16TwoSeed79_round154_full_registration_v1_20261009.py',
        'ordered_physical_native_components':2,'observed_identical_forecast_all8_metric_comparison_in_actual_score_loop':True,
        'official_quality_admitted':False,'test_labels_read':False})
    print({'prospective_sources_expected':48,'graph_controls_expected':1800,'quality_admitted':False},flush=True)
if __name__=='__main__':main()
