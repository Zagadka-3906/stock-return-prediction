"""Prepare six151 receiver drafts with own E outputs and measured55-control scorer guards; not admit quality."""
from pathlib import Path
import re,sys,time,copy
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_JointCrossHuber147_core_receivers_v1_20261008 import save

FILES={
    'HuberSparse150_storage_v1_20261008.py':'RFFSparse151_storage_v1_20261009.py',
    'verify_HuberSparse150_D_scoring_scope_v1_20261008.py':'verify_RFFSparse151_D_scoring_scope_v1_20261009.py',
    'run_HuberSparse59_official_comparison_v2_20261009.py':'run_RFFSparse59_official_comparison_v1_20261009.py',
    'prepare_HuberSparse59_selected_candidate_v2_20261009.py':'prepare_RFFSparse59_selected_candidate_v1_20261009.py',
    'seal_HuberSparse59_selected_candidate_v2_20261009.py':'seal_RFFSparse59_selected_candidate_v1_20261009.py',
    'run_HuberSparse59_round150_full_registration_v2_20261009.py':'run_RFFSparse59_round151_full_registration_v1_20261009.py'}

def convert(source):
    source=source.replace('PureRFFHuber128_round149_full_registration_v1_20261008','PREVIOUS_FULL_151_PLACEHOLDER')
    for old,new in FILES.items():source=source.replace(old,new).replace(old.removesuffix('.py'),new.removesuffix('.py'))
    source=source.replace('run_HuberSparse59_official_comparison_v1_20261008','run_RFFSparse59_official_comparison_v1_20261009')
    source=source.replace('prepare_HuberSparse59_round150_sources_v2_20261009','prepare_RFFSparse59_round151_sources_v1_20261009')
    source=source.replace('HuberSparse150_complete_receiver_refinement_v3_20261009.json','RFFSparse151_core_receiver_draft_preparation_v1_20261009.json')
    source=source.replace('HuberSparse','RFFSparse').replace('RFFSparse150','RFFSparse151').replace('_round150_','_round151_').replace('_r150','_r151').replace('第150轮','第151轮')
    # Date changes apply only to this new scheme, keeping the five parent backends intact.
    source=re.sub(r'(RFFSparse[A-Za-z0-9_/-]*?)_v[12]_20261008',r'\1_v1_20261009',source)
    source=source.replace('RFFSparse_complete_parent_CDF_v1_20261009','RFFSparse_complete_parent_CDF_v3_20261009')
    source=source.replace('RFFSparse_complete_parent_native_stage_v1_20261009','RFFSparse_complete_parent_native_stage_v3_20261009')
    source=source.replace('QA61','QA62').replace('qa_v61_20261007','qa_v62_20261009').replace("'QA61'","'QA62'")
    source=source.replace('publish(150,','publish(151,').replace('lossless(150)','lossless(151)').replace('ensure_display(path, number, create=True)','ensure_display(path, number, create=True)').replace('assert number == 150','assert number == 151')
    source=source.replace('(134,146,147,148,149)','(134,147,148,149,150)')
    source=source.replace('PREVIOUS_FULL_151_PLACEHOLDER','HuberSparse59_round150_full_registration_v1_20261008')
    return source

def main():
    originals=[];products=[]
    for old,new in FILES.items():
        p=A/old;originals.append(p);s=convert(p.read_text(encoding='utf8'))
        if old.startswith('run_HuberSparse59_round'):
            s=s.replace('四个合格锚点、120项细权重重调、零权重恒等对照','四个合格锚点、54项RFF与稀疏残差组合、零权重恒等对照')
        products.append(save(new,s))
    import RFFSparse151_storage_v1_20261009 as storage
    import ctypes,subprocess
    outputs=[]
    for logical,physical in storage.OUTPUTS.items():
        assert not logical.exists() and not physical.exists(),(logical,physical)
        physical.mkdir(parents=True,exist_ok=False);logical.parent.mkdir(parents=True,exist_ok=True)
        result=subprocess.run(['cmd.exe','/d','/c','mklink','/J',str(logical),str(physical)],capture_output=True,text=True,encoding='utf8',errors='replace',creationflags=subprocess.CREATE_NO_WINDOW)
        assert result.returncode==0,result.stderr
        storage.empty(logical);outputs.append({'logical':str(logical),'physical':str(physical),'empty_junction_verified':True})
    proposal_path=A/'RFFSparse59_round151_proposal_v1_20261009.json';proposal=read(proposal_path)
    oldplan=A/'HuberSparse59_round150_plan_v1_20261008.json';plan=copy.deepcopy(read(oldplan))
    plan.update(status='frozen59_RFFSparse151_core_receiver_drafts_before_quality_admission',at_local=time.strftime('%Y-%m-%dT%H:%M:%S'),target_round=151,after_round=150,
        anchor_rounds=proposal['anchor_rounds'],heads=proposal['heads'],new_cases=proposal['new_cases'][1:],graph_key='nonflag_CPU_RFFSparse_complete_parent_CDF')
    plan_path=A/'RFFSparse59_round151_plan_v1_20261009.json';create(plan_path,plan)
    create(A/'RFFSparse151_core_receiver_draft_preparation_v1_20261009.json',{'status':'prepared_six151_receiver_drafts_and_six_empty_E_junctions_before_quality',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in [Path(__file__),*originals,*products,proposal_path,oldplan,plan_path]},
        'outputs':outputs,'inherits_actual55_numeric_hash_and_duplicate_metric_guards':True,'quality_admitted':False,
        'complete32_generated_receivers_and_duplicate_audit_still_required':True,'new_native_fits':0,'new_quality_scores':0,'new_future_inference':0,'test_labels_read':False})
    print({'drafts':len(products),'empty_outputs':len(outputs),'quality_admitted':False},flush=True)
if __name__=='__main__':main()
