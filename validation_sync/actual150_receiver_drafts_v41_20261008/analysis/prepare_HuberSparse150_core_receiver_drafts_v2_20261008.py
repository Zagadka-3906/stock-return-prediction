"""Prepare complete-score/candidate/storage prototypes for the55-controlled new ensemble; quality stays unadmitted."""
from pathlib import Path
import io
import importlib
import subprocess
import sys
import time
import tokenize

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_JointCrossHuber147_core_receivers_v1_20261008 import save


def convert(source):
    for before,after in [('CrossFamilyFine125','HuberSparse59'),('CrossFamilyFine145','HuberSparse150'),
        ('CrossFamilyFine_complete_parent','HuberSparse_complete_parent'),
        ('nonflag_CPU_CrossFamily_complete_parent_CDF','nonflag_CPU_HuberSparse_complete_parent_CDF'),
        ('CrossFamily_complete_parent_native_replay_verification','HuberSparse_complete_parent_native_replay_verification'),
        ('passed_actual_complete_parent_and_CrossFamily_two_full_native_independent_replays_and_cold80','passed_actual_complete_parent_and_HuberSparse_two_full_native_independent_replays_and_cold80'),
        ('round145','round150'),('full145','full150'),('actual145','actual150'),('_r145','_r150'),
        ('第145轮','第150轮'),('qa_v56','qa_v61'),('qa56','qa61'),('QA56','QA61'),('wave428','wave433'),
        ('actual125','actual59'),('all125','all59'),('anchor125','anchor59'),('125项','59项'),
        ('actual_CrossFamilyFine121_parent134','actual_HuberSparse55_parent134'),('20_existing_native_and121','20_existing_native_and55')]:
        source=source.replace(before,after)
    tokens=list(tokenize.generate_tokens(io.StringIO(source).readline))
    source=tokenize.untokenize([token._replace(string={'145':'150','125':'59','121':'55','363':'165','120':'54','360':'162','56':'61','428':'433'}.get(token.string,token.string)) if token.type==tokenize.NUMBER else token for token in tokens])
    source=source.replace('(134,136,141,144)','(134,146,147,148,149)').replace('(134, 136, 141, 144)','(134, 146, 147, 148, 149)')
    source=source.replace('KrylovGram52_round141_full_registration_v18_20261008','PureRFFHuber128_round149_full_registration_v1_20261008')
    source=source.replace('HuberSparse59_round150_plan_v2_20261008','HuberSparse59_round150_plan_v1_20261008')
    source=source.replace('actual_registration_v2_20261008','actual_registration_v1_20261008')
    source=source.replace('full_registration_v2_file_IO','full_registration_v1_file_IO')
    source=source.replace("kind=row['state_kind']","kind=row.get('native_stage_state_kind',row['state_kind']);storage_kind=row['state_kind']")
    source=source.replace("info['independent_'+kind+","info['independent_'+storage_kind+")
    return source


def main():
    proposal=A/'HuberSparse59_round150_proposal_v1_20261008.json';plan=read(proposal)
    assert len(plan['new_cases'])==55 and plan['new_cases'][0]['amplitude']==0.
    plan={**plan,'new_cases':plan['new_cases'][1:],'original_proposal_sha256':sha(proposal),
        'status':'frozen59_core_receiver_drafts_before_any_quality_source_admission',
        'round':150,'QA_version':61,'wave':433,'expected_scored_cases':59,
        'existing_saved_native_heads':20,'actual_full_OOF_heads':4,
        'graph_key':'nonflag_CPU_HuberSparse_complete_parent_CDF'}
    assert len(plan['new_cases'])==54
    planpath=A/'HuberSparse59_round150_plan_v1_20261008.json';create(planpath,plan)
    pairs=[('CrossFamilyFine145_storage_v1_20261008.py','HuberSparse150_storage_v1_20261008.py'),
        ('verify_CrossFamilyFine145_D_scoring_scope_v1_20261008.py','verify_HuberSparse150_D_scoring_scope_v1_20261008.py'),
        ('run_CrossFamilyFine125_official_comparison_v1_20261008.py','run_HuberSparse59_official_comparison_v1_20261008.py'),
        ('prepare_CrossFamilyFine125_selected_candidate_v1_20261008.py','prepare_HuberSparse59_selected_candidate_v1_20261008.py'),
        ('seal_CrossFamilyFine125_selected_candidate_v1_20261008.py','seal_HuberSparse59_selected_candidate_v1_20261008.py'),
        ('run_CrossFamilyFine125_round145_full_registration_v2_20261008.py','run_HuberSparse59_round150_full_registration_v1_20261008.py')]
    originals=[];products=[]
    for old,new in pairs:
        path=A/old;originals.append(path);source=convert(path.read_text(encoding='utf8'))
        if old.startswith('run_CrossFamilyFine125_official'):
            before="parents={n:A/f'optimization_20261003_r{n}' for n in plan['anchor_rounds']}"
            assert source.count(before)==1
            source=source.replace(before,"parents={n:A/f'optimization_20261003_r{n}' for n in [134,*plan['anchor_rounds']]}")
            source=source.replace('comparison_parent=min(parents,key=',"comparison_parent=min(plan['anchor_rounds'],key=")
            source=source.replace('for n in parents]','for n in plan[\'anchor_rounds\']]')
            before="control['status']=='passed_actual120_new_signed_full_CDF360_cold_controls_and_identity_on_exact134_parent'"
            assert source.count(before)==1
            source=source.replace(before,"control['status']=='passed_actual55_HuberSparse_full_training_CDF_and165_cold_controls_with_exact134_identity'")
            source=source.replace("model':f'crossfamily_group","model':f'HuberSparse_group")
            marker='            mask=codec.selected(dates,flags,valid)'
            # Numeric control matching is added after the complete cases in a prospective refinement;
            # these drafts cannot be dispatched until full source admission and its regression proof.
        if old.startswith('seal_'):
            source=source.replace('HuberSparse59_round150_sources_v2_20261008','HuberSparse59_round150_sources_v1_20261008')
        if old.startswith('run_CrossFamilyFine125_round'):
            source=source.replace('HuberSparse59_round150_sources_v2_20261008','HuberSparse59_round150_sources_v1_20261008')
        products.append(save(new,source))
    storage=importlib.import_module('HuberSparse150_storage_v1_20261008')
    folders=[]
    for access,target in storage.OUTPUTS.items():
        assert access.is_relative_to(ROOT) and target.is_relative_to(Path('E:/赛题五_本机临时/第150轮_20261008'))
        assert not access.exists() and not target.exists()
        access.parent.mkdir(parents=True,exist_ok=True);target.mkdir(parents=True,exist_ok=False)
        def literal(path):return "'"+str(path).replace("'","''")+"'"
        command="$ErrorActionPreference='Stop'\nNew-Item -ItemType Junction -Path "+literal(access)+' -Target '+literal(target)+' | Out-Null'
        result=subprocess.run(['pwsh','-NoProfile','-NonInteractive','-Command',command],capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW)
        assert result.returncode==0,result.stderr.decode('utf8',errors='replace')
        storage.empty(access);folders.append({'access':str(access),'physical_E':str(target)})
    create(A/'HuberSparse150_core_receiver_draft_preparation_v2_20261008.json',{
        'status':'prepared_six_core_receiver_drafts_and_empty_E_outputs_quality_not_admitted',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(path):sha(path) for path in [Path(__file__),proposal,planpath,*originals,*products]},
        'actual55_full165_prefix_and72_native_controls_previously_passed':True,
        'native_kind_separated_from_storage_kind_before_future_inference':True,
        'physical_component_guards_must_allow3_or4':True,'E_outputs':folders,
        'canonical_eight_source_generator_and_phase_isolated_publisher_and_source_admission_and_complete_prospective_checks_still_required':True,
        'prior_complete_forecast_duplicate_audit_still_required':True,'raw_control_SHA_crosschecks_still_required_before_quality':True,
        'new_quality_scores':0,'new_future_inference':0,'new_native_fits':0,'test_labels_read':False})
    print({'prepared_core_drafts':len(products),'verified_empty_E_outputs':len(folders),'quality_admitted':False},flush=True)


if __name__=='__main__':main()
