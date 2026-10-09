"""Freeze deterministic32 registry/collector routes; keep fixed134 scientific base separate from comparison parent."""
from pathlib import Path
import ast,hashlib,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
import prepare_CrossFamily94_round136_sources_v4_20261008 as original
from prepare_CrossFamilyFine145_complete_receivers_v1_20261008 import convert
NAMES={n:convert(n) for n in original.NAMES.values()}
def source_paths():
    names=['prepare_CrossFamilyFine145_complete_receivers_v1_20261008.py','CrossFamilyFine145_receiver_drafts_v1_20261008.json',
        'prepare_CrossFamilyFine145_complete_metadata_v2_20261008.py','CrossFamilyFine145_receiver_preparation_v2_20261008.json',
        'CrossFamilyFine125_round145_plan_v2_20261008.json','CrossFamilyFine145_storage_v1_20261008.py','CrossFamilyFine_complete_parent_CDF_v1_20261008.py',
        'CrossFamilyFine_complete_parent_native_stage_v1_20261008.py','predict_CrossFamilyFine_complete_parent_scheme_v1_20261008.py',
        'run_CrossFamilyFine125_official_comparison_v1_20261008.py','prepare_CrossFamilyFine125_selected_candidate_v1_20261008.py',
        'seal_CrossFamilyFine125_selected_candidate_v1_20261008.py','run_CrossFamilyFine125_round145_full_registration_v1_20261008.py',
        'publish_CrossFamilyFine125_evidence_v1_20261008.py','verify_CrossFamilyFine125_round145_sources_v1_20261008.py',
        'verify_CrossFamilyFine125_prospective_routes_v1_20261008.py','dispatch_CrossFamilyFine145_complete_pipeline_v1_20261008.py',
        'verify_CrossFamilyFine145_D_scoring_scope_v1_20261008.py','CrossFamilyFine145_D_scoring_scope_v1_20261008.json',
        'CrossFamilyFine125_prospective_routes_v1_20261008.json','CrossFamilyFine125_actual_controls_index_v1_20261008.json',
        'CrossFamilyFine125_round145_source_admission_v1_20261008.json','CrossFamilyFine125_round145_source_preparation_v1_20261008.json',
        'CrossFamilyFine125_selected_release_v1_20261008/selected_candidate_ready_for_registration.json','CrossFamilyFine125_scores_github_v1_20261008/receipt.json',
        'prepare_CrossFamilyFine145_actual_math_controls_v1_20261008.py','CrossFamilyFine145_math_control_source_preparation_v1_20261008.json',
        'verify_CrossFamilyFine30_native_historical_hooks_v1_20261008.py','actual_CrossFamilyFine30_native_hooks_location_v1_20261008.json',
        'verify_CrossFamilyFine121_full_historical_controls_v1_20261008.py','actual_CrossFamilyFine121_parent134_location_v1_20261008.json',
        'actual_CrossFamily_bank30_synthetic_location_v1_20261008.json','actual_multiyear_residual_calendar_location_v1_20261008.json',
        'short_content_addressed_native_storage_v2_20261008.py','actual_short_parent_alias_nested_copy_v2_20261008.json',
        'verified_TLS_Git_retry_runtime_v2_20261008.py','exact_native_JSON_archive_runtime_20261007.py','exact_native_pretty_JSON_archive_20261007.py',
        'exact_native_JSON_archive_runtime_full_preflight_20261007/runtime_verification.json','publish_explicit_parent_training_round_v2_20261005.py',
        'all_forecast_percentile_runtime_20261007.py','cached_official_spearman_runtime_20261007.py','resolve_sealed_scientific_protocol_v2_20261007.py']
    return list(dict.fromkeys([Path(__file__),*(A/n for n in names),*(A/n for n in NAMES.values())]))
def generate(parent):
    assert parent in (134,136,141,144)
    result={convert(n):convert(t) for n,t in original.generate(134).items()}
    for n,s in result.items():
        s=s.replace('prepare_CrossFamilyFine125_round145_sources_v4_20261008','prepare_CrossFamilyFine125_round145_sources_v1_20261008')
        s=s.replace("'existing_CrossFamily_saved_native_heads': 30","'existing_CrossFamily_saved_native_heads': 20")
        s=s.replace("r['direct_rank_comparison_configuration']['weight'],", "abs(r['direct_rank_comparison_configuration']['weight']),")
        # Only comparison protocol pointers change; stage-base paths are always read from pilot['actual_scheme_base_round']==134.
        s=s.replace('_r134/',f'_r{parent}/').replace('PREVIOUS_NUMBER = 134',f'PREVIOUS_NUMBER = {parent}')
        s=s.replace("'explicit_parent_round': 134",f"'explicit_parent_round': {parent}").replace('explicit_comparison_parent_round=134',f'explicit_comparison_parent_round={parent}')
        s=s.replace('actual30_CrossFamily_saved_native_heads_source','actual20_CrossFamily_saved_native_heads_source')
        if n.startswith('collect_full_'):
            t=ast.parse(s);fn=next(x for x in t.body if isinstance(x,ast.FunctionDef) and x.name=='collect');assert len(fn.args.args)==3
            guard=fn.body[0];lines=s.splitlines(keepends=True);lines[guard.lineno-1:guard.end_lineno]=['    assert (number, qa_version, expected_records) == (145, 56, 125)\n'];s=''.join(lines)
        if n.startswith('publish_'):
            t=ast.parse(s);call=next(x for x in ast.walk(t) if isinstance(x,ast.Call) and isinstance(x.func,ast.Name) and x.func.id=='collect')
            before=ast.get_source_segment(s,call);s=s.replace(before,'collect(145, 56, 125)',1)
            s=s.replace('actual_complete_QA_version=47','actual_complete_QA_version=56').replace("actual_full_QA_version': 47","actual_full_QA_version': 56")
            start=s.index("    payload[(prefix/'README.md').as_posix()] += (");end=s.index('    previous = ',start)
            s=s[:start]+"    payload[(prefix/'README.md').as_posix()] += ('\\n本轮125项：134、136、141、144四个合格锚点，120项新细权重及零幅度对照；重调固定134完整父方案后的原跨模型阶段。复用20个成熟年度原生模型；121完整/363冷前缀及30原生/30冷检查；完整官方训练连接评分，选择后冻结与原生、独立、重载及冷80复现。完整榜六视图45秒QA56及main，未读取实际测试标签；有限网格不证明穷尽。\\n').encode('utf8')\n"+s[end:]
        compile(s,str(A/n),'exec');result[n]=s
    assert len(result)==8
    return result
def main():
    ready_path=A/'CrossFamilyFine125_selected_release_v1_20261008/selected_candidate_ready_for_registration.json';ready=read(ready_path)
    assert ready['status']=='passed_actual125_selected_candidate_full_graph_and_metrics_and_source_bytes' and ready['sealed_candidate_complete']
    pilot=read(A/'CrossFamilyFine125_official_comparison_v1_20261008/verification.json');assert len(pilot['records'])==125 and pilot['best']==ready['best']
    admission=A/'CrossFamilyFine125_round145_source_admission_v1_20261008.json';proof=read(admission)
    assert proof['status']=='passed_actual20_heads121_fixed_base_CDF363cold30hooks_and32_prospective145_sources'
    for p,d in proof['input_sha256'].items():assert sha(p)==d,p
    generated=generate(pilot['actual_comparison_parent_round']);expected=proof['generated_source_sha256'][str(pilot['actual_comparison_parent_round'])]
    assert set(generated)==set(expected)
    for n,s in generated.items():assert not (A/n).exists() and hashlib.sha256(s.encode()).hexdigest()==expected[n],n
    for n,s in generated.items():(A/n).write_text(s,encoding='utf8',newline='\n')
    create(A/'CrossFamilyFine125_round145_source_preparation_v1_20261008.json',{'status':'passed_actual125_sealed_candidate_and_admitted_full145_QA56_sources',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'round':145,'scored_records':125,'actual_comparison_parent_round':pilot['actual_comparison_parent_round'],
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),ready_path,admission,*(A/n for n in generated)]},'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})
if __name__=='__main__':main()
