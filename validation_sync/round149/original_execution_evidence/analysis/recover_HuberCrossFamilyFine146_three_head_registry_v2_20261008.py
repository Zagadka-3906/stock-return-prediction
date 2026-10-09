"""Fresh146 receivers admit exactly the three declared group4 heads; retain all first failures."""
from pathlib import Path
import json
import sys
import time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start

DRIVERS={name:name.replace('_v1_20261008','_v2_20261008') for name in [
    'prepare_HuberCrossFamilyFine125_round146_sources_v1_20261008.py',
    'verify_HuberCrossFamilyFine125_round146_sources_v1_20261008.py',
    'publish_HuberCrossFamilyFine125_evidence_v1_20261008.py',
    'run_HuberCrossFamilyFine125_official_comparison_v1_20261008.py',
    'prepare_HuberCrossFamilyFine125_selected_candidate_v1_20261008.py',
    'seal_HuberCrossFamilyFine125_selected_candidate_v1_20261008.py',
    'run_HuberCrossFamilyFine125_round146_full_registration_v1_20261008.py',
    'dispatch_HuberCrossFamilyFine146_complete_pipeline_v1_20261008.py']}
SERVICES={name:name.replace('_v1_20261008','_v2_20261008') for name in [
    'HuberCrossFamilyFine146_complete_prospective_controls_v1_20261008',
    'HuberCrossFamilyFine125_round146_source_admission_v1_20261008',
    'HuberCrossFamilyFine125_controls_main_publication_v1_20261008',
    'HuberCrossFamilyFine125_official_comparison_v1_20261008',
    'HuberCrossFamilyFine125_scores_main_publication_v1_20261008',
    'HuberCrossFamilyFine125_selected_candidate_preparation_v1_20261008',
    'HuberCrossFamilyFine125_selected_candidate_sealing_v1_20261008',
    'HuberCrossFamilyFine125_round146_full_registration_v1_20261008']}


def adapt(text):
    for old,new in DRIVERS.items():text=text.replace(old.removesuffix('.py'),new.removesuffix('.py'))
    # The comparison output is an admitted empty E-backed folder v1; version2 here denotes only the service.
    for old,new in SERVICES.items():
        if old=='HuberCrossFamilyFine125_official_comparison_v1_20261008':continue
        text=text.replace(old,new)
    text=text.replace("closed('HuberCrossFamilyFine125_official_comparison_v1_20261008')", "closed('HuberCrossFamilyFine125_official_comparison_v2_20261008')")
    text=text.replace("'HuberCrossFamilyFine125_official_comparison_v1_20261008',", "'HuberCrossFamilyFine125_official_comparison_v2_20261008',")
    text=text.replace("else 'HuberCrossFamilyFine125_official_comparison_v1_20261008'", "else 'HuberCrossFamilyFine125_official_comparison_v2_20261008'")
    text=text.replace('HuberCrossFamilyFine125_prospective_routes_v1_20261008.json','HuberCrossFamilyFine125_prospective_routes_v2_20261008.json')
    text=text.replace('actual_registration_v1_20261008','actual_registration_v2_20261008')
    text=text.replace('round146_full_registration_v1_file_IO_20261008','round146_full_registration_v2_file_IO_20261008')
    return text


def main():
    failure=A/'service_owned_workflows_20261006/HuberCrossFamilyFine146_complete_prospective_controls_v1_20261008/service_execution.json'
    assert read(failure)['status']=='failed'
    originals=[A/name for name in DRIVERS if not name.startswith('prepare_HuberCrossFamilyFine125_round146_sources')]
    products=[]
    for source in originals:
        text=adapt(source.read_text(encoding='utf-8-sig'));target=A/DRIVERS[source.name];compile(text,str(target),'exec')
        assert not target.exists()
        with target.open('x',encoding='utf8',newline='') as stream:stream.write(text)
        products.append(target)
    generator='''"""Fresh32 registry routes bind exactly three Huber/Bayes heads and the actual version2 workflow."""
from pathlib import Path
import hashlib,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
import prepare_HuberCrossFamilyFine125_round146_sources_v1_20261008 as original
from recover_HuberCrossFamilyFine146_three_head_registry_v2_20261008 import adapt,DRIVERS
NAMES=original.NAMES
def source_paths():
    out=[]
    for p in original.source_paths():
        if p.name in DRIVERS:p=A/DRIVERS[p.name]
        if p.name=='verify_HuberCrossFamilyFine125_prospective_routes_v1_20261008.py':p=A/'verify_HuberCrossFamilyFine125_prospective_routes_v3_20261008.py'
        if p.name=='HuberCrossFamilyFine125_prospective_routes_v1_20261008.json':p=A/'HuberCrossFamilyFine125_prospective_routes_v2_20261008.json'
        out.append(p)
    out += [Path(__file__),Path(original.__file__),A/'recover_HuberCrossFamilyFine146_three_head_registry_v2_20261008.py',A/'HuberCrossFamilyFine146_three_head_receiver_recovery_v2_20261008.json',A/'verify_HuberCrossFamilyFine125_prospective_routes_v2_20261008.py']
    return list(dict.fromkeys(out))
def generate(parent):
    outputs={}
    for n,s in original.generate(parent).items():
        s=adapt(s)
        if n.startswith('register_'):
            before="len(measured['ordered_native_components']) in (2,4)";assert s.count(before)==1
            s=s.replace(before,"len(measured['ordered_native_components']) == 3")
        if n.startswith('publish_'):
            s=s.replace('134、136、141、144','136、139、141、145').replace('固定134完整父方案','固定136完整父方案').replace('复用20个成熟年度原生模型','复用15个成熟年度原生模型')
        compile(s,str(A/n),'exec');outputs[n]=s
    assert len(outputs)==8;return outputs
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
    target=A/'prepare_HuberCrossFamilyFine125_round146_sources_v2_20261008.py';compile(generator,str(target),'exec')
    with target.open('x',encoding='utf8',newline='') as stream:stream.write(generator)
    products.append(target)
    old=A/'verify_HuberCrossFamilyFine125_prospective_routes_v2_20261008.py'
    text=adapt(old.read_text(encoding='utf8'));target=A/'verify_HuberCrossFamilyFine125_prospective_routes_v3_20261008.py';compile(text,str(target),'exec')
    with target.open('x',encoding='utf8',newline='') as stream:stream.write(text)
    products.append(target)
    prep=A/'HuberCrossFamilyFine146_three_head_receiver_recovery_v2_20261008.json'
    pins={str(p):sha(p) for p in [Path(__file__),failure,old,*originals,*products]}
    create(prep,{'status':'prepared_fresh146_three_head_registry_receivers_after_actual_prospective_guard_failure_before_quality',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,
        'first_registry_guard_incorrectly_admitted_only2_or4_heads':True,'correct_declared_group4_heads':3,
        'official_scoring_native_CDF_and_independent_inference_mathematics_unchanged':True,
        'old_source_files_and_first_failure_preserved':True,'actual146_official_scores':0,'test_labels_read':False})
    pins[str(prep)]=sha(prep)
    prospective=start('HuberCrossFamilyFine146_complete_prospective_controls_v2_20261008',products[-1].name,[],pins)
    dispatch=start('HuberCrossFamilyFine146_complete_chronological_dispatch_v2_20261008',
                   'dispatch_HuberCrossFamilyFine146_complete_pipeline_v2_20261008.py',[],pins)
    create(A/'HuberCrossFamilyFine146_complete_recovered_hidden_launches_v2_20261008.json',
           {'status':'started_fresh_prospective2_and_complete_dispatch2_before_any146_quality',
            'prospective':prospective,'dispatch':dispatch,'input_sha256':pins,'new_quality_scores':0,'test_labels_read':False})
    print(json.dumps({'prospective_worker':prospective['owned_worker_pid'],'dispatch_worker':dispatch['owned_worker_pid']},ensure_ascii=False),flush=True)
if __name__=='__main__':main()
