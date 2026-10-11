"""Prepare52 untested fine Ridge amplitudes using already qualified annual native models."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from nonflag_RidgeFine52_round128_mapping_20261007 import convert

def main():
    old_names=['run_nonflag_Ridge40_official_comparison_v1_20261007.py',
      'run_nonflag_Ridge40_admitted_comparison_v1_20261007.py',
      'prepare_nonflag_Ridge40_selected_candidate_v1_20261007.py','seal_nonflag_Ridge40_selected_candidate_v1_20261007.py',
      'publish_nonflag_Ridge40_evidence_v1_20261007.py','run_nonflag_Ridge40_round121_full_registration_v1_20261007.py',
      'verify_nonflag_Ridge40_round121_sources_v1_20261007.py',
      'verify_nonflag_residual_Ridge37_transform_20261007.py',
      'predict_nonflag_residual_Ridge_complete_scheme_20261007.py',
      'nonflag_residual_Ridge_compatible_parent_20261007.py']
    outputs={}
    for name in old_names:
        old=A/name;new=convert(name);text=convert(old.read_text(encoding='utf8'))
        if name.startswith('run_nonflag_Ridge40_official'):
            needle='    while psutil.virtual_memory().available<11*2**30:time.sleep(15)'
            assert text.count(needle)==1
            text=text.replace(needle,"    gate=A/'actual4_official_scoring_8_5GiB_gate_preflight_20261007/verification.json'\n    assert read(gate)['status']=='passed_actual4_uncached_full_official_calls_at_8_5GiB_start_gate_all8_and_CSV_and_input_bits_exact'\n    while psutil.virtual_memory().available<8.5*2**30:time.sleep(15)")
        elif name.startswith('verify_nonflag_residual_Ridge37'):
            text=text.replace("print({'status':'passed','full_cases':37,'cold_controls':111}","print({'status':'passed','full_cases':49,'cold_controls':147}")
        elif name.startswith('nonflag_residual_Ridge_compatible'):
            # The retained106 core remains the authority for all nonflag replacement families.
            text=text.replace("    value.pop('nonflag_CPU_Ridge_residual_CDF',None)",
              "    value.pop('nonflag_CPU_Ridge_residual_CDF',None)\n    value.pop('nonflag_CPU_RFFRidge_residual_CDF',None)\n    value.pop('nonflag_CPU_RFF128_residual_CDF',None)")
        elif name.startswith('verify_nonflag_Ridge40'):
            text=text.replace("'nonflag_CPU_HGB_residual_CDF':{'old_branch':'must_be_removed'}",
              "'nonflag_CPU_HGB_residual_CDF':{'old_branch':'must_be_removed'},'nonflag_CPU_RFFRidge_residual_CDF':{'old_RFF32':'remove'},'nonflag_CPU_RFF128_residual_CDF':{'old_RFF128':'remove'}")
            text=text.replace("            assert 'nonflag_CPU_HGB_residual_CDF' not in graph",
              "            assert 'nonflag_CPU_HGB_residual_CDF' not in graph and 'nonflag_CPU_RFFRidge_residual_CDF' not in graph and 'nonflag_CPU_RFF128_residual_CDF' not in graph")
        compile(text,str(A/new),'exec');outputs[new]=text
    for name,text in outputs.items():
        assert not (A/name).exists(),name
        (A/name).write_text(text,encoding='utf8',newline='\n')
    plan=read(A/'nonflag_Ridge40_plan_20261007.json')
    weights=[.0005,.00075,.000875,.001,.001125,.001375,.0015,.001625,.00175,.001875,.002,.002125,.00225,.002375,.002625,.00275]
    assert len(weights)==16 and not set(weights)&set(plan['weights'])
    plan.update(status='frozen_fine52_Ridge_before_controls_or_official_scores',at_local=time.strftime('%Y-%m-%dT%H:%M:%S'),
      round=128,wave=411,qualified_anchor_rounds=[112,121,127],after_round=127,weights=weights,
      expected_scored_records=52,expected_full_transform_controls=49,expected_cold_prefix_controls=147,
      selection='highest_full_connected_official_score_after_real127_closure_and_actual128_source_admission',
      full_future_candidate_native_replays_and_QA39_required=True)
    plan.pop('full_future_candidate_native_replays_and_QA32_required',None)
    plan_path=A/'nonflag_RidgeFine52_plan_20261007.json';create(plan_path,plan)
    sources=[Path(__file__),A/'nonflag_RidgeFine52_round128_mapping_20261007.py',
      A/'prepare_nonflag_RidgeFine52_round128_sources_v1_20261007.py',plan_path,
      A/'actual4_official_scoring_8_5GiB_gate_preflight_20261007/verification.json',
      *[A/n for n in outputs],*[A/n for n in old_names]]
    create(A/'nonflag_RidgeFine52_science_route_preparation_20261007.json',{
      'status':'compiled_fresh52_fine_Ridge_scoring_freeze_and_full128_routes',
      'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in sources},
      'new_quality_scores':0,'new_native_fits':0,'test_labels_read':False})
    print({'status':'compiled','fresh_sources':len(outputs),'scored_plan_cases':52},flush=True)

if __name__=='__main__':main()
