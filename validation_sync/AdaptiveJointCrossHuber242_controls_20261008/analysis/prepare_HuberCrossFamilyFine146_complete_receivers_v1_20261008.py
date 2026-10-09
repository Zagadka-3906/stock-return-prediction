"""Predeclare complete146, retaining its single new stage over136 and all qualified anchors."""
from pathlib import Path
import ast
import io
import json
import subprocess
import sys
import time
import tokenize
ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create


def convert(text):
    # This converter accepts only the proven145 fine receivers, never parent predictors.
    text = text.replace('CrossFamily', 'HuberCrossFamily')
    for before, after in [('round145', 'round146'), ('full145', 'full146'), ('actual145', 'actual146'),
            ('prospective145', 'prospective146'), ('Fine145', 'Fine146'), ('_r145', '_r146'),
            ('第145轮', '第146轮'), ('qa_v56', 'qa_v57'), ('qa56', 'qa57'), ('QA56', 'QA57'),
            ('wave428', 'wave429'), ('parent134', 'parent136'), ('exact134', 'exact136'), ('_r134/', '_r136/')]:
        text = text.replace(before, after)
    tokens = list(tokenize.generate_tokens(io.StringIO(text).readline))
    text = tokenize.untokenize([t._replace(string={'145': '146', '56': '57', '428': '429', '134': '136'}.get(t.string, t.string))
                               if t.type == tokenize.NUMBER else t for t in tokens])
    # Insert the future145 anchor after own-round token substitutions, preventing a self-parent.
    for before, after in [('(136,136,141,144)', '(136,139,141,145)'),
                          ('(136, 136, 141, 144)', '(136, 139, 141, 145)'),
                          ('[136,136,141,144]', '[136,139,141,145]'),
                          ('[136, 136, 141, 144]', '[136, 139, 141, 145]')]:
        text = text.replace(before, after)
    for before, after in [('HuberCrossFamilyFine125_round146_sources_v2_20261008', 'HuberCrossFamilyFine125_round146_sources_v1_20261008'),
            ('HuberCrossFamilyFine125_round146_full_registration_v2_20261008', 'HuberCrossFamilyFine125_round146_full_registration_v1_20261008'),
            ('HuberCrossFamilyFine125_round146_full_registration_v2_file_IO_20261008', 'HuberCrossFamilyFine125_round146_full_registration_v1_file_IO_20261008'),
            ('actual_registration_v2_20261008', 'actual_registration_v1_20261008'),
            ('round146_v2_20261008', 'round146_v1_20261008'),
            ('HuberCrossFamilyFine146_receiver_preparation_v2_20261008', 'HuberCrossFamilyFine146_complete_receiver_preparation_v1_20261008'),
            ('actual_HuberCrossFamily_bank30_synthetic_location_v1_20261008', 'actual_HuberCrossFamilyFine_bank15_location_v1_20261008'),
            ('actual_multiyear_residual_calendar_location_v1_20261008', 'actual_HuberCrossFamilyFine_multiyear_calendar_location_v1_20261008'),
            ('existing_bank30_actual20_relevant_native_records', 'existing_bank15_actual15_relevant_native_records'),
            ('actual20_', 'actual15_'), ('all20 ', 'all15 '), ('All20 ', 'All15 '),
            ('20_heads121', '15_heads121'), ('len(relevant)==20', 'len(relevant)==15'),
            ("len(plan['heads'])==4", "len(plan['heads'])==3"),
            ("bank['actual_model_count']==30 and bank['actual_full_OOF_heads']==6", "bank['actual_model_count']==15 and bank['actual_full_OOF_heads']==3"),
            ("'existing_saved_native_heads':20", "'existing_saved_native_heads':15"),
            ("'existing_HuberCrossFamily_saved_native_heads': 20", "'existing_HuberCrossFamily_saved_native_heads': 15"),
            ("'actual_relevant_saved_native_heads':20", "'actual_relevant_saved_native_heads':15"),
            ("'actual_full_OOF_heads':4", "'actual_full_OOF_heads':3"),
            ("'actual_existing_native_head_audits':20", "'actual_existing_native_head_audits':15"),
            ("'actual_full_native_OOF_heads':4", "'actual_full_native_OOF_heads':3"),
            ("c['actual_calendar_cases']==33 and c['actual_whole_day_controls']==66", "c['actual_calendar_cases']==30 and c['actual_whole_day_controls']==60")]:
        text = text.replace(before, after)
    return text


def save(name, text):
    path = A / name
    compile(text, str(path), 'exec')
    assert not path.exists(), path
    with path.open('x', encoding='utf-8', newline='') as stream:
        stream.write(text)
    return path


def main():
    proposal = A / 'HuberCrossFamilyFine125_round146_proposal_v1_20261008.json'
    plan = read(proposal)
    assert plan['anchor_rounds'] == [136, 139, 141, 145] and len(plan['new_cases']) == 120
    assert plan['scientific_stage_base_round'] == 136 and len(plan['heads']) == 3
    plan.update(status='frozen125_Huber_fine_grid_absolute_weight_ties_and_complete_receivers_before_quality',
                at_local=time.strftime('%Y-%m-%dT%H:%M:%S'), round=146, QA_version=57, wave=429,
                fixed_scientific_stage_base_round=136, existing_saved_native_heads=15, actual_full_OOF_heads=3,
                graph_key='nonflag_CPU_HuberCrossFamily_complete_parent_CDF',
                final_selection_rule='official_S_desc_unique_physical_model_SHA_count_asc_absolute_amplitude_asc_case_asc',
                comparison_parent_rule='official_S_desc_unique_physical_model_SHA_count_asc_round_asc',
                source_receivers_not_yet_admitted=True, original_proposal_sha256=sha(proposal))
    plan['input_sha256'].update({str(Path(__file__)): sha(__file__), str(proposal): sha(proposal)})
    create(A / 'HuberCrossFamilyFine125_round146_plan_v2_20261008.json', plan)
    originals, products = [], []
    for name in ['CrossFamilyFine145_storage_v1_20261008.py', 'verify_CrossFamilyFine145_D_scoring_scope_v1_20261008.py',
                 'run_CrossFamilyFine125_official_comparison_v1_20261008.py', 'prepare_CrossFamilyFine125_selected_candidate_v1_20261008.py',
                 'seal_CrossFamilyFine125_selected_candidate_v1_20261008.py', 'run_CrossFamilyFine125_round145_full_registration_v2_20261008.py',
                 'publish_CrossFamilyFine125_evidence_v1_20261008.py', 'verify_CrossFamilyFine125_round145_sources_v1_20261008.py',
                 'verify_CrossFamilyFine125_prospective_routes_v1_20261008.py', 'dispatch_CrossFamilyFine145_complete_pipeline_v1_20261008.py']:
        source = A / name
        originals.append(source)
        text = convert(source.read_text(encoding='utf-8-sig'))
        # All146 comparisons wait for the previous145 complete qualification.
        text = text.replace("closed('KrylovGram52_round141_full_registration_v18_20261008')",
                            "closed('CrossFamilyFine125_round145_full_registration_v2_20261008')")
        text = text.replace("'KrylovGram52_round141_full_registration_v18_20261008',",
                            "'CrossFamilyFine125_round145_full_registration_v2_20261008',")
        text = text.replace('actual138_fine145_historical_controls_main_publication_v25_20261008',
                            'actual_fine146_historical_controls_main_publication_v30_20261008')
        if name.startswith('verify_CrossFamilyFine125_round145_sources'):
            before = "'HuberCrossFamilyFine121_actual_full_historical_controls_v1_20261008',"
            assert text.count(before) == 1
            text = text.replace(before, before + "'HuberCrossFamilyFine30_multiyear_calendar_controls_v1_20261008',")
        if name.startswith('verify_CrossFamilyFine125_prospective'):
            before = 'def main():\n    import prepare_'
            assert text.count(before) == 1
            text = text.replace(before, "def main():\n    from run_dependency_queue_v3_20261006 import owned\n    calendar_service=A/'service_owned_workflows_20261006/HuberCrossFamilyFine30_multiyear_calendar_controls_v1_20261008'\n    while not (calendar_service/'service_execution.json').exists():time.sleep(5)\n    assert read(calendar_service/'service_execution.json')['status']=='passed'\n    while owned(read(calendar_service/'native_launch.json')):time.sleep(1)\n    import prepare_")
        if name.startswith('dispatch_'):
            before = '    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start'
            assert text.count(before) == 1
            text = text.replace(before, "    benchmark=A/'service_owned_workflows_20261006/actual_full_board_deferred_serialization_benchmark_v1_20261008'\n    while not (benchmark/'service_execution.json').exists():time.sleep(15)\n    while owned(read(benchmark/'native_launch.json')):time.sleep(1)\n    terminal=read(benchmark/'service_execution.json');assert terminal['status'] in ('passed','failed')\n    create(A/'HuberCrossFamilyFine146_execution_cost_slot_handoff_v1_20261008.json',{'status':'original146_runtime_retained_after_actual_benchmark_process_closure','actual_benchmark_terminal':terminal,'new_execution_runtime_not_adopted':True,'new_quality_scores':0})\n" + before)
        products.append(save(convert(name), text))
    # Preserve the proven Huber predictor's complete CrossFamily parent backend.
    source = A / 'predict_HuberCrossFamily_complete_parent_scheme_v1_20261008.py'
    originals.append(source)
    text = source.read_text(encoding='utf-8-sig')
    before = 'from HuberCrossFamily_complete_parent_native_stage_v1_20261008 import after_parent,GRAPH_KEY'
    assert text.count(before) == 1
    products.append(save('predict_HuberCrossFamilyFine_complete_parent_scheme_v1_20261008.py',
                         text.replace(before, 'from HuberCrossFamilyFine_complete_parent_native_stage_v1_20261008 import after_parent,GRAPH_KEY')))
    # Add independent final2025 replay over three remapped training calendars for every signed share.
    source = A / 'verify_HuberCrossFamily_multiyear_native_calendar_v1_20261008.py'
    originals.append(source)
    text = source.read_text(encoding='utf-8-sig')
    text = text.replace('HuberCrossFamily_multiyear', 'HuberCrossFamilyFine_multiyear')
    text = text.replace('HuberCrossFamily_complete_parent', 'HuberCrossFamilyFine_complete_parent')
    text = text.replace('HuberCrossFamily112_round139_plan_v1', 'HuberCrossFamilyFine125_round146_plan_v2')
    text = text.replace('_r134/', '_r136/').replace('R134', 'R136')
    text = text.replace('import os,sys,time', 'import os,sys,time,itertools')
    text = text.replace('for group in range(6):', 'for group,share,amplitude in itertools.product((4,),(.25,.375,.5,.625,.75),(-.001,.001)):')
    text = text.replace("spec={'group':group,'amplitude':.025", "spec={'group':group,'amplitude':amplitude")
    text = text.replace("if family=='CrossFamily':spec['share']=.5;needed=", "if family=='CrossFamily':spec['share']=share;needed=", 1)
    text = text.replace("spec={'group':0,'amplitude':.025", "spec={'group':4,'amplitude':.001")
    text = text.replace('GROUPS[0]', 'GROUPS[4]')
    text = text.replace('actual18_Huber', 'actual30_HuberFine').replace('and36_day', 'and60_day')
    text = text.replace("'actual_calendar_cases':18,'actual_whole_day_controls':36", "'actual_calendar_cases':30,'actual_whole_day_controls':60")
    before = '    for p,d in pins.items():assert sha(p)==d,p'
    assert text.count(before) == 1
    text = text.replace(before, '    assert len(records)==30 and len(rejected)==1\n' + before)
    products.append(save('verify_HuberCrossFamilyFine_multiyear_native_calendar_v1_20261008.py', text))
    # Registry sources are generated once after sealing; all32 variants are pinned first.
    generator = '''"""Complete146 deterministic registry routes; comparisons vary, scientific stage base136 stays fixed."""
from pathlib import Path
import hashlib,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_HuberCrossFamilyFine146_complete_receivers_v1_20261008 import convert
import prepare_CrossFamilyFine125_round145_sources_v2_20261008 as original
NAMES={old:convert(new) for old,new in original.NAMES.items()}
SOURCE_NAMES=__SOURCE_NAMES__
def source_paths():
    return list(dict.fromkeys([Path(__file__),*(A/n for n in SOURCE_NAMES),*(A/n for n in NAMES.values())]))
def generate(parent):
    assert parent in (136,139,141,145)
    result={convert(n):convert(s) for n,s in original.generate(134).items()}
    for n,s in result.items():
        s=s.replace('_r136/',f'_r{parent}/').replace('PREVIOUS_NUMBER = 136',f'PREVIOUS_NUMBER = {parent}')
        s=s.replace("'explicit_parent_round': 136",f"'explicit_parent_round': {parent}").replace('explicit_comparison_parent_round=136',f'explicit_comparison_parent_round={parent}')
        compile(s,str(A/n),'exec');result[n]=s
    assert len(result)==8;return result
def main():
    ready_path=A/'HuberCrossFamilyFine125_selected_release_v1_20261008/selected_candidate_ready_for_registration.json';ready=read(ready_path)
    assert ready['status']=='passed_actual125_selected_candidate_full_graph_and_metrics_and_source_bytes' and ready['sealed_candidate_complete']
    pilot=read(A/'HuberCrossFamilyFine125_official_comparison_v1_20261008/verification.json');assert len(pilot['records'])==125 and pilot['best']==ready['best']
    admission=A/'HuberCrossFamilyFine125_round146_source_admission_v1_20261008.json';proof=read(admission)
    assert proof['status']=='passed_actual15_heads121_fixed_base_CDF363cold30hooks_and32_prospective146_sources'
    for p,d in proof['input_sha256'].items():assert sha(p)==d,p
    generated=generate(pilot['actual_comparison_parent_round']);expected=proof['generated_source_sha256'][str(pilot['actual_comparison_parent_round'])]
    assert set(generated)==set(expected)
    for n,s in generated.items():assert not (A/n).exists() and hashlib.sha256(s.encode()).hexdigest()==expected[n],n
    for n,s in generated.items():(A/n).write_text(s,encoding='utf8',newline='\\n')
    create(A/'HuberCrossFamilyFine125_round146_source_preparation_v1_20261008.json',{'status':'passed_actual125_sealed_candidate_and_admitted_full146_QA57_sources',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'round':146,'scored_records':125,'actual_comparison_parent_round':pilot['actual_comparison_parent_round'],
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),ready_path,admission,*(A/n for n in generated)]},'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})
if __name__=='__main__':main()
'''
    source_names = [p.name for p in products] + [Path(__file__).name,
        'HuberCrossFamilyFine146_complete_receiver_preparation_v1_20261008.json', 'HuberCrossFamilyFine125_round146_plan_v2_20261008.json',
        'HuberCrossFamilyFine125_round146_proposal_v1_20261008.json', 'HuberCrossFamilyFine_complete_parent_CDF_v1_20261008.py',
        'HuberCrossFamilyFine_complete_parent_native_stage_v1_20261008.py', 'verify_HuberCrossFamilyFine30_native_historical_hooks_v1_20261008.py',
        'verify_HuberCrossFamilyFine121_full_historical_controls_v1_20261008.py', 'actual_HuberCrossFamilyFine_bank15_location_v1_20261008.json',
        'actual_HuberCrossFamilyFine30_native_hooks_location_v1_20261008.json', 'actual_HuberCrossFamilyFine121_parent136_location_v1_20261008.json',
        'actual_HuberCrossFamilyFine_multiyear_calendar_location_v1_20261008.json', 'HuberCrossFamilyFine146_D_scoring_scope_v1_20261008.json',
        'HuberCrossFamilyFine125_prospective_routes_v1_20261008.json', 'HuberCrossFamilyFine125_actual_controls_index_v1_20261008.json',
        'HuberCrossFamilyFine125_round146_source_admission_v1_20261008.json', 'HuberCrossFamilyFine125_round146_source_preparation_v1_20261008.json',
        'HuberCrossFamilyFine125_selected_release_v1_20261008/selected_candidate_ready_for_registration.json',
        'HuberCrossFamilyFine125_scores_github_v1_20261008/receipt.json',
        'prepare_HuberCrossFamilyFine146_historical_controls_v1_20261008.py', 'prepare_HuberCrossFamilyFine146_historical_controls_v2_20261008.py',
        'recover_HuberCrossFamilyFine146_historical_factory_v2_20261008.py', 'HuberCrossFamilyFine146_first_factory_failure_v1_20261008.json',
        'HuberCrossFamilyFine146_historical_receiver_preparation_v1_20261008.json',
        'prepare_CrossFamilyFine125_round145_sources_v2_20261008.py', 'prepare_CrossFamilyFine125_round145_sources_v1_20261008.py',
        'prepare_CrossFamilyFine145_complete_receivers_v1_20261008.py', 'prepare_CrossFamily94_round136_sources_v4_20261008.py',
        'prepare_BF16wide40_round135_sources_v4_20261008.py', 'short_content_addressed_native_storage_v2_20261008.py',
        'actual_short_parent_alias_nested_copy_v2_20261008.json', 'verified_TLS_Git_retry_runtime_v2_20261008.py',
        'exact_native_JSON_archive_runtime_20261007.py', 'exact_native_pretty_JSON_archive_20261007.py',
        'exact_native_JSON_archive_runtime_full_preflight_20261007/runtime_verification.json', 'publish_explicit_parent_training_round_v2_20261005.py',
        'all_forecast_percentile_runtime_20261007.py', 'cached_official_spearman_runtime_20261007.py', 'resolve_sealed_scientific_protocol_v2_20261007.py']
    generator = generator.replace('__SOURCE_NAMES__', repr(list(dict.fromkeys(source_names))))
    products.append(save('prepare_HuberCrossFamilyFine125_round146_sources_v1_20261008.py', generator))
    import importlib
    storage = importlib.import_module('HuberCrossFamilyFine146_storage_v1_20261008')
    for path, target in storage.OUTPUTS.items():
        assert path.resolve().is_relative_to(ROOT.resolve()) and not path.exists()
        assert target.resolve().is_relative_to(storage.EBASE.resolve()) and not target.exists()
        target.mkdir(parents=True)
        command = "New-Item -ItemType Junction -Path '" + str(path).replace("'", "''") + "' -Target '" + str(target).replace("'", "''") + "' | Out-Null"
        result = subprocess.run(['pwsh', '-NoProfile', '-NonInteractive', '-Command', command], capture_output=True,
                                creationflags=subprocess.CREATE_NO_WINDOW)
        assert result.returncode == 0, result.stderr
        storage.empty(path)
    create(A / 'HuberCrossFamilyFine146_complete_receiver_preparation_v1_20261008.json',
           {'status': 'prepared_complete146_scientific_receivers_before_calendar_prospective_admission_and_quality',
            'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'input_sha256': {str(p): sha(p) for p in [Path(__file__), proposal, *originals, *products]},
            'expected_official_cases': 125, 'fixed_scientific_stage_base_round': 136, 'anchors': [136, 139, 141, 145],
            'native_states': 15, 'own_calendar_controls_planned': 30, 'own_whole_day_controls_planned': 60,
            'QA_version': 57, 'wave': 429, 'all_large_outputs_on_E': True, 'official_cache_guards_on_D_unchanged': True,
            'original146_serialization_runtime_retained': True, 'new_quality_scores': 0, 'test_labels_read': False})
    print(json.dumps({'status': 'prepared', 'source_files': len(products), 'prospective_controls_still_required': True}), flush=True)


if __name__ == '__main__':
    main()
