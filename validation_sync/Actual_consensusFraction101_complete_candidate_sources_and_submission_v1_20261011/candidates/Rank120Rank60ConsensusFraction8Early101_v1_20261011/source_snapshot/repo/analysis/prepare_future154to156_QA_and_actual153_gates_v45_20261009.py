"""Repair future administrative gates before quality, preserving all admitted scientific grids."""
from pathlib import Path
from copy import deepcopy
import sys,time,ast
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
QA=A/'actual_QA_collector_path_runtime_v43_20261009.py'

def clone(old,new,edits):
    src,dst=A/old,A/new;s=src.read_text(encoding='utf8')
    for before,after in edits:
        assert before in s,(old,before);s=s.replace(before,after)
    compile(s,str(dst),'exec')
    if dst.exists():assert dst.read_text(encoding='utf8')==s,dst
    else:
        with dst.open('x',encoding='utf8') as f:f.write(s)
    return src,dst

def add_QA(s):
    needle="        with safe(log),serial(log/'serial_mutex.json'),git_io(log/'file_backed_git'),installed_transfer():"
    assert s.count(needle)==1
    return s.replace(needle,"        from actual_QA_collector_path_runtime_v43_20261009 import installed as qa_paths\n"+needle.replace('installed_transfer():','installed_transfer(),qa_paths():'))

def main():
    inputs=[Path(__file__),QA,A/'actual_QA_collector_path_controls_v43_20261009.json'];metas={};dispatches={};audits={}
    config={154:('BF16TwoSeed154','BF16TwoSeed79',2,3),155:('BF16Seed10_155','BF16Seed10_80',1,2),156:('BF16Drop05_156','BF16Drop05_81',2,3)}
    for number,(family,prefix,oldv,newv) in config.items():
        assert not (A/'service_owned_workflows_20261006'/f'{prefix}_round{number}_source_admission_v1_20261009').exists()
        oldmeta=A/f'{family}_complete_pipeline_preparation_v{oldv}_20261009.json';newmeta=A/f'{family}_complete_pipeline_preparation_v{newv}_20261009.json'
        m=deepcopy(read(oldmeta));replacements={};files=[]
        oldadmission=next(driver for sid,driver,_ in m['receiver_specs'] if '_source_admission_' in sid)
        newadmission=f'verify_{prefix}_round{number}_sources_current153_v{newv}_20261009.py'
        changes=[(oldmeta.name,newmeta.name)]
        if number==154:
            changes.append(('BF16Medium78_round153_full_registration_v1_20261009','BF16Medium78_round153_full_registration_v4_20261009'))
            changes.append(('BF16TwoSeed154_prior_complete_forecast_duplicate_audit_v1_20261009','BF16TwoSeed154_prior_complete_forecast_duplicate_audit_v2_20261009'))
        files.extend(clone(oldadmission,newadmission,changes));replacements[oldadmission]=newadmission
        oldsafe=next(driver for sid,driver,_ in m['receiver_specs'] if f'_round{number}_full_registration_' in sid)
        newsafe=f'run_{family}_safe_registration_v{newv}_20261009.py';source=(A/oldsafe).read_text(encoding='utf8')
        assert oldmeta.name in source;source=source.replace(oldmeta.name,newmeta.name)
        source=source.replace(f'/safe_full_main_v{oldv}',f'/safe_full_main_v{newv}')
        if number==154:
            oldfull='run_BF16TwoSeed79_round154_full_registration_v2_20261009.py';newfull='run_BF16TwoSeed79_round154_full_registration_v3_20261009.py'
            files.extend(clone(oldfull,newfull,[('BF16Medium78_round153_full_registration_v1_20261009','BF16Medium78_round153_full_registration_v4_20261009')]))
            assert oldfull in source;source=source.replace(oldfull,newfull)
        source=add_QA(source);compile(source,str(A/newsafe),'exec')
        with (A/newsafe).open('x',encoding='utf8') as f:f.write(source)
        files.extend((A/oldsafe,A/newsafe));replacements[oldsafe]=newsafe
        if number==154:
            oldpub='publish_BF16TwoSeed79_evidence_v1_20261009.py';newpub='publish_BF16TwoSeed79_evidence_v2_20261009.py'
            files.extend(clone(oldpub,newpub,[('BF16Medium78_round153_full_registration_v1_20261009','BF16Medium78_round153_full_registration_v4_20261009'),
                ("'safe_'+phase+'_main_v1'","'safe_'+phase+'_main_v2'")]))
            replacements[oldpub]=newpub
            oldaudit='verify_BF16TwoSeed154_prior_complete_forecast_duplicate_audit_v1_20261009.py';newaudit='verify_BF16TwoSeed154_prior_complete_forecast_duplicate_audit_v2_20261009.py'
            files.extend(clone(oldaudit,newaudit,[('BF16Medium78_round153_full_registration_v1_20261009','BF16Medium78_round153_full_registration_v4_20261009'),
                ('E:/赛题五_本机临时/BF16TwoSeed154_prior_complete_forecast_duplicate_audit_v1_20261009','E:/赛题五_本机临时/BF16TwoSeed154_prior_complete_forecast_duplicate_audit_v2_20261009')]))
            audits[number]=newaudit
        olddispatch=f'dispatch_{family}_complete_pipeline_v{oldv}_20261009.py';newdispatch=f'dispatch_{family}_complete_pipeline_v{newv}_20261009.py'
        hidden_old=next(v for v in (f'{family}_complete_hidden_launches_v{oldv}_20261009',f'{family}_complete_hidden_launches_v1_20261009') if v in (A/olddispatch).read_text(encoding='utf8'))
        changes=[(oldmeta.name,newmeta.name),(hidden_old,f'{family}_complete_hidden_launches_v{newv}_20261009')]
        if number==154:
            changes.extend([('BF16Medium78_round153_full_registration_v1_20261009','BF16Medium78_round153_full_registration_v4_20261009'),
                ('BF16TwoSeed154_prior_complete_forecast_duplicate_audit_v1_20261009','BF16TwoSeed154_prior_complete_forecast_duplicate_audit_v2_20261009')])
        files.extend(clone(olddispatch,newdispatch,changes));dispatches[number]=newdispatch
        m['receiver_specs']=[[sid,replacements.get(driver,driver),args] for sid,driver,args in m['receiver_specs']]
        m['input_sha256'].update({str(p):sha(p) for p in [*inputs,*files,oldmeta]})
        m.update(status='prepared_current153_full4_dependency_and_actual_QA_directory_resolver_before_new_quality',
            at_local=time.strftime('%Y-%m-%dT%H:%M:%S'),administrative_QA_directory_only_changed=True,new_quality_scores=0,test_labels_read=False)
        create(newmeta,m);inputs.extend([oldmeta,newmeta,*files]);metas[number]=newmeta
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    from handoff_joint_goss_round97_full_execution_20261006 import stack,suspended_idle,retire_suspended
    launches={};handoffs=[]
    launches['154_audit']=start('BF16TwoSeed154_prior_complete_forecast_duplicate_audit_v2_20261009',audits[154],[],{str(metas[154]):sha(metas[154]),str(A/audits[154]):sha(A/audits[154])})
    for number,(family,prefix,oldv,newv) in config.items():
        row=start(f'{family}_complete_chronological_dispatch_v{newv}_20261009',dispatches[number],[],{str(metas[number]):sha(metas[number]),str(A/dispatches[number]):sha(A/dispatches[number])})
        launches[str(number)]=row
        #155 originally used controller1;156 used controller1 with driver2.
        oldsid=f'{family}_complete_chronological_dispatch_v{2 if number==154 else 1}_20261009'
        p=A/'service_owned_workflows_20261006'/oldsid/'native_launch.json'
        if p.exists() and owned(read(p)):
            old=read(p);line=next(line for line in stack(old['owned_worker_pid']).splitlines() if '    closed (' in line)
            parent,worker,idle=suspended_idle(old,line)
            try:retire_suspended(old,row)
            except BaseException:
                if worker.is_running():worker.resume()
                if parent.is_running():parent.resume()
                raise
            handoffs.append({'old':old,'new':row,'owned_childfree_idle_stack':idle})
    create(A/'future154to156_QA_and_actual153_gates_hidden_launches_v45_20261009.json',{
        'status':'queued_corrected_three_round_receivers_before_quality','input_sha256':{str(p):sha(p) for p in dict.fromkeys(inputs)},
        'launches':launches,'only_idle_controller_handoffs':handoffs,'scientific_jobs_stopped_or_restarted':0,
        'all_prior_scores_native_proofs_and_failed_originals_preserved':True,'new_quality_scores':0,'test_labels_read':False})
    print({'new_owned_controllers':{n:r['owned_worker_pid'] for n,r in launches.items()},'idle_controller_handoffs':len(handoffs)},flush=True)
if __name__=='__main__':main()
