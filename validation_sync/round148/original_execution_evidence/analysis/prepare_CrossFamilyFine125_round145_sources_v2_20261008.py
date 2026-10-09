"""Fresh registry routes correct scoped numeric guards and use noncolliding QA files; retain all draft1 bytes."""
from pathlib import Path
import ast,hashlib,io,sys,time,tokenize
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
import prepare_CrossFamilyFine125_round145_sources_v1_20261008 as first
QA={f'{prefix}_round145_20261007':f'{prefix}_round145_v2_20261008' for prefix in ('lossless_ranking_runtime_adapter','build_lossless_ranking_display','verify_lossless_ranking_display')}
def source_paths():
    paths=[]
    for p in first.source_paths():
        if p.name in {old+'.py' for old in QA}:continue
        if p.name=='run_CrossFamilyFine125_round145_full_registration_v1_20261008.py':p=A/'run_CrossFamilyFine125_round145_full_registration_v2_20261008.py'
        if p.name=='prepare_CrossFamilyFine125_round145_sources_v1_20261008.py':p=Path(__file__)
        if p.name in first.NAMES.values():p=A/renamed(p.name)
        paths.append(p)
    paths.extend([Path(__file__),Path(first.__file__),A/'prepare_CrossFamilyFine145_complete_metadata_v2_20261008.py',A/'CrossFamilyFine145_receiver_preparation_v2_20261008.json',*(A/n for n in NAMES.values())])
    return list(dict.fromkeys(paths))
def renamed(value):
    for old,new in QA.items():value=value.replace(old,new)
    return value
def generate(parent):
    out={}
    assert parent in (134,136,141,144)
    for n,s in first.generate(134).items():
        s=renamed(s).replace('prepare_CrossFamilyFine125_round145_sources_v1_20261008','prepare_CrossFamilyFine125_round145_sources_v2_20261008')
        tokens=list(tokenize.generate_tokens(io.StringIO(s).readline))
        s=tokenize.untokenize([t._replace(string={'136':'145','47':'56'}.get(t.string,t.string)) if t.type==tokenize.NUMBER else t for t in tokens])
        s=s.replace('_r134/',f'_r{parent}/').replace('PREVIOUS_NUMBER = 134',f'PREVIOUS_NUMBER = {parent}')
        s=s.replace("'explicit_parent_round': 134",f"'explicit_parent_round': {parent}").replace('explicit_comparison_parent_round=134',f'explicit_comparison_parent_round={parent}')
        compile(s,str(A/renamed(n)),'exec');out[renamed(n)]=s
    assert len(out)==8;return out
NAMES={old:renamed(new) for old,new in first.NAMES.items()}
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
