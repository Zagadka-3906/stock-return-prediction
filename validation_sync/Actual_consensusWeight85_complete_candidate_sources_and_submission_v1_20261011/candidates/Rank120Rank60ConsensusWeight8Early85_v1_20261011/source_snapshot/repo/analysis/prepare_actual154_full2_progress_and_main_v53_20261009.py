"""Make the actual successful154 full receiver visible and publish its dependency repair."""
from pathlib import Path
import ast,sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import create,sha
def write(name,text):
    ast.parse(text);p=A/name
    with p.open('x',encoding='utf8',newline='\n') as f:f.write(text)
    return p
def main():
    original=A/'monitor_actual_chronological_optimization_progress_v66_20261009.py';s=original.read_text(encoding='utf8').replace('v66_20261009','v67_20261009')
    replacements={
        'BF16Seed10_155_prior_complete_forecast_duplicate_audit_v1_20261009':'BF16Seed10_155_prior_complete_forecast_duplicate_audit_v2_20261009',
        'BF16Seed10_155_complete_chronological_dispatch_v2_20261009':'BF16Seed10_155_complete_chronological_dispatch_v3_20261009',
        'actual154_corrected_receivers_and_cache_cleanup_main_publication_v79_20261009':'actual154_full_import_and155_dependencies_main_publication_v81_20261009',
        "pipeline['153']['full_registration']=status('BF16Medium78_round153_full_registration_v5_20261009')":"pipeline['154']['original_failed_full_receiver']=pipeline['154']['full_registration']\n    pipeline['154']['full_registration']=status('BF16TwoSeed79_round154_full_registration_v2_20261009')\n    state['two_seed154_frontier']['full_registration']=pipeline['154']['full_registration']\n    pipeline['153']['full_registration']=status('BF16Medium78_round153_full_registration_v5_20261009')"
    }
    for old,new in replacements.items():assert s.count(old)==1,(old,s.count(old));s=s.replace(old,new)
    observer=write('monitor_actual_chronological_optimization_progress_v67_20261009.py',s)
    starter_source=A/'start_actual_recovered_progress_v66_20261009.py';s=starter_source.read_text(encoding='utf8').replace('v66_20261009','v67_20261009').replace('observer_v65_20261009','observer_v66_20261009')
    starter=write('start_actual_recovered_progress_v67_20261009.py',s)
    pub_source=A/'publish_actual154_receivers_cache_cleanup_main_v79_20261009.py';s=pub_source.read_text(encoding='utf8').replace('v79_20261009','v81_20261009')
    marker='    sources=list(dict.fromkeys(sources));assert all(p.is_file() for p in sources)'
    assert s.count(marker)==1
    extra="""    sources.extend([A/'prepare_actual154_full_import_and155_dependencies_v51_20261009.py',
        A/'actual154_full_import_and155_dependency_controls_v51_20261009.json',
        A/'actual154_full_import_and155_recovery_launches_v51_20261009.json',
        A/'BF16TwoSeed154_full_import_recovery_original_failure_v51_20261009.json',
        A/'run_BF16TwoSeed79_round154_full_registration_v5_20261009.py',
        A/'run_BF16TwoSeed154_safe_registration_v6_20261009.py',
        A/'BF16Seed10_155_complete_pipeline_preparation_v3_20261009.json',
        A/'verify_BF16Seed10_155_prior_complete_forecast_duplicate_audit_v2_20261009.py',
        A/'dispatch_BF16Seed10_155_complete_pipeline_v3_20261009.py',
        A/'actual154_corrected_receivers_cache_cleanup_main_v79_receipt_20261009.json',
        A/'prepare_actual154_full2_progress_and_main_v53_20261009.py'])
    for _,driver,_ in read(A/'BF16Seed10_155_complete_pipeline_preparation_v3_20261009.json')['receiver_specs']:sources.append(A/driver)
    for pattern in ('*progress*v67_20261009.py','*progress*v67_20261009.json','*progress*v67_20261009.md'):
        sources.extend(A.glob(pattern))
    for name in ('BF16TwoSeed79_round154_full_registration_v1_20261009','BF16TwoSeed79_round154_full_registration_v2_20261009',
        'BF16Seed10_155_complete_chronological_dispatch_v2_20261009','BF16Seed10_155_complete_chronological_dispatch_v3_20261009',
        'BF16Seed10_155_prior_complete_forecast_duplicate_audit_v1_20261009','BF16Seed10_155_prior_complete_forecast_duplicate_audit_v2_20261009'):
        sources.extend(p for p in (A/'service_owned_workflows_20261006'/name).glob('*') if p.is_file() and p.suffix in ('.json','.log'))
"""
    s=s.replace(marker,extra+marker)
    s=s.replace('同步154准入修复及实际进度和138项历史浏览器缓存清理证据','同步154实际完整榜接收入口修复和155连续依赖及保留失败记录')
    pub=write('publish_actual154_full_import_and155_dependencies_main_v81_20261009.py',s)
    create(A/'actual154_full2_progress_and_main_preparation_v53_20261009.json',{'status':'prepared_actual154_full2_and155_routes_and_main81','input_sha256':{str(p):sha(p) for p in (Path(__file__),original,observer,starter_source,starter,pub_source,pub)},'scientific_models_or_scoring_changed':False})
if __name__=='__main__':main()
