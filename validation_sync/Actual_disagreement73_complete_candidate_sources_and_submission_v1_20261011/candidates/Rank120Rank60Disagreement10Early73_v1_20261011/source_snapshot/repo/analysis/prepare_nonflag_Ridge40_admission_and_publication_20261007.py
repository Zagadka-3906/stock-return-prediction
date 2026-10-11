"""Finish pre-scoring source admission and separate main evidence publication scopes."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]; A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute
from prepare_nonflag_Ridge40_science_routes_20261007 import mapping

def main():
    m=mapping(); files={}
    text=substitute((A/'publish_nonflag_HGB40_evidence_v4_20261007.py').read_text(encoding='utf8'),m)
    text=text.replace("closed('quantile_HGB88_round119_full_registration_v6')","closed('nonflag_HGB40_round120_full_registration_v4')",1)
    text=text.replace("closed('quantile_HGB88_round119_full_registration_v6')","closed('nonflag_residual_Ridge_actual_hooks_and_main_after120')",1)
    text=text.replace('nonflag_HGB10_actual_controls_github_20261007','nonflag_residual_Ridge10_actual_controls_github_20261007')
    text=text.replace('validation_sync/nonflag_HGB40_{phase}_20261007','validation_sync/nonflag_Ridge40_{phase}_20261007')
    text=text.replace('published_actual_nonflag_HGB40_','published_actual_nonflag_Ridge40_').replace('full120_not_yet_qualified','full121_not_yet_qualified')
    start=text.index("            payload[(prefix/'README.md').as_posix()]=("); end=text.index('            scope.reverify()',start)
    text=text[:start]+"            payload[(prefix/'README.md').as_posix()]=('非涨停残差Ridge：两组样本数归一化L2及等权集成，各12幅度，加三个合格锚点及消融，共40项。实际10年度成熟模型；37全量、111冷前缀和3历史原生核对。完整121候选须冻结、重放及QA32。仅main。\\n').encode('utf8')\n"+text[end:]
    text=text.replace("'上传分位数HGB的'","'上传非涨停残差Ridge的'")
    needle="    if phase=='scores':\n        for row in proof['records']:"
    assert text.count(needle)==1
    text=text.replace(needle,"    sources += [A/'prepare_nonflag_Ridge40_science_routes_20261007.py',A/'nonflag_Ridge40_science_route_preparation_20261007.json',A/'prepare_nonflag_Ridge40_admission_and_publication_20261007.py',A/'nonflag_residual_Ridge_codec_20261007.py',A/'nonflag_residual_Ridge_bank10_20261007/verification.json',A/'nonflag_Ridge40_unadmitted_plan_metadata_correction_20261007.json']\n"+needle)
    files['publish_nonflag_Ridge40_evidence_v1_20261007.py']=text
    text=substitute((A/'verify_nonflag_HGB40_round120_sources_v4_20261007.py').read_text(encoding='utf8'),m)
    text=text.replace("'nonflag_residual_HGB10_training'","'nonflag_residual_Ridge_native_bank10'")
    text=text.replace("'nonflag_residual_HGB_native_hook3_preflight',",'')
    text=text.replace("'HGB_quarter_numeric28_round118_full_registration_v5',\n      'quantile_HGB88_round119_full_registration_v6'","'quantile_HGB88_round119_full_registration_v6',\n      'nonflag_HGB40_round120_full_registration_v4'")
    text=text.replace('(112,118,119)','(112,119,120)')
    text=text.replace('prospective120','prospective121').replace('actual120_registry','actual121_registry').replace('full120_future_inference_and_QA31','full121_future_inference_and_QA32')
    text=text.replace('24_prospective120','24_prospective121')
    text=text.replace('register_nonflag_HGB40_round120_artifacts','register_nonflag_Ridge40_round121_artifacts')
    text=text.replace('publish_nonflag_HGB40_round120_full_validation','publish_nonflag_Ridge40_round121_full_validation')
    text=text.replace('round120_full_scope','round121_full_scope').replace("actual_full_QA_version': 31","actual_full_QA_version': 32")
    text=text.replace('collect(120, 31, 40)','collect(121, 32, 40)').replace("namespace['snapshot'](120)","namespace['snapshot'](121)")
    text=text.replace("assert \"if not key.startswith('nonflag_cpu_hgb_')\" in candidate", "assert \"if not key.startswith(('nonflag_cpu_hgb_','nonflag_cpu_ridge_'))\" in candidate")
    # Explicitly test replacing an existing HGB nonflag node, not only adding to a clean graph.
    text=text.replace("'conditional_flag_CPU_HGB_residual_CDF':{'complete_flag_parent':'preserved'}}", "'conditional_flag_CPU_HGB_residual_CDF':{'complete_flag_parent':'preserved'},'nonflag_CPU_HGB_residual_CDF':{'old_branch':'must_be_removed'}}")
    needle="            if names:assert graph['nonflag_CPU_Ridge_residual_CDF']['ordered_equal_mean_components']==names"
    assert text.count(needle)==1
    text=text.replace(needle,"            assert 'nonflag_CPU_HGB_residual_CDF' not in graph\n"+needle)
    needle="    native_path=A/'nonflag_residual_Ridge_native_hook3_preflight_20261007/verification.json';native=read(native_path)"
    assert text.count(needle)==1
    text=text.replace(needle,needle+"\n    assert len(native['records'])==3\n    assert read(A/'nonflag_residual_Ridge_bank10_20261007/verification.json')['actual_native_fits']==10")
    text=text.replace("candidate/'nonflag_residual_Ridge_native_replay_verification.json'", "candidate/'nonflag_residual_Ridge_native_replay_verification.json'")
    files['verify_nonflag_Ridge40_round121_sources_v1_20261007.py']=text
    for name,text in files.items():
        compile(text,str(A/name),'exec'); assert not (A/name).exists(),name
    for name,text in files.items():
        with (A/name).open('x',encoding='utf8',newline='\n') as f:f.write(text)
    create(A/'nonflag_Ridge40_admission_publication_source_preparation_20261007.json',{'status':'compiled_admission_and_single_receipt_Ridge40_main_publishers',
        'input_sha256':{str(A/n):sha(A/n) for n in files},'actual121_full_admission_and_quality_scores_not_yet_claimed':True})
if __name__=='__main__':main()
