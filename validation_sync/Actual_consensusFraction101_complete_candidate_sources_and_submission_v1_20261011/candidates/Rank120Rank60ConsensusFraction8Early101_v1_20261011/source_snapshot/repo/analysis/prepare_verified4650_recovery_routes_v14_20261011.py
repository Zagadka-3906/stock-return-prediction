"""Replace only failed or proven idle dependency helpers; never restart completed science."""
from pathlib import Path
import sys,re,subprocess,psutil
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
from handoff_ready_goss_full_execution_20261006 import retire
PROOF=A/'verified4650_recovery_routes_v14_20261011.json'

def main():
    assert allowed();oldpath=A/'complete180_registered_continuation_routes_v13_20261011.json';old=read(oldpath)
    tasks=[];replacements={};inspections=[]
    extras=[('actual_three_cached_mixed149_after188_normalization_v1_20261011','normalize_completed_three_cached_mixed149_after188_v1_20261011.py'),
            ('actual_three_cached_mixed149_selected_native14_v1_20261011','qualify_three_cached_mixed149_selected_native14_v1_20261011.py'),
            ('MixedObjectiveWindow189_complete149_family_v3_20261011','run_MixedObjectiveWindow189_complete_family_v3_20261011.py'),
            ('actual_near_protected39_after189_normalization_v1_20261011','normalize_completed_near_protected39_after189_v1_20261011.py'),
            ('actual_near_protected39_selected_native14_v1_20261011','qualify_near_protected39_selected_native14_v1_20261011.py'),
            ('MixedProtected190_complete39_family_v1_20261011','run_MixedProtected190_complete_family_v1_20261011.py'),
            ('actual_near_refined27_after190_normalization_v1_20261011','normalize_completed_near_refined27_after190_v1_20261011.py'),
            ('actual_near_refined27_selected_native14_v1_20261011','qualify_near_refined27_selected_native14_v1_20261011.py'),
            ('MixedRefined191_complete27_family_v1_20261011','run_MixedRefined191_complete_family_v1_20261011.py'),
            ('actual_rank5_rank20_mixed_selected_native14_v1_20261011','verify_rank5_rank20_mixed_selected_native14_v1_20261011.py'),
            ('actual_rank5_rank20_near_protected_selected_native14_v1_20261011','verify_rank5_rank20_near_protected_selected_native14_v1_20261011.py')]
    candidates=[*old['remaining_tasks'][8:],*extras]
    for name,driver in candidates:
        f=A/'service_owned_workflows_20261006'/name;identity=read(f/'native_launch.json')
        terminal=read(f/'service_execution.json') if (f/'service_execution.json').exists() else None
        if not owned(identity) and terminal and terminal['status']=='passed':continue
        stack=None
        if owned(identity):
            assert not psutil.Process(identity['owned_worker_pid']).children(),name
            stack=subprocess.run([str(ROOT/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'),'dump','--pid',str(identity['owned_worker_pid'])],capture_output=True,text=True,encoding='utf8',check=True).stdout
            assert '(idle)' in stack and 'closed' in stack,name
        else:assert terminal and terminal['status']=='failed',(name,terminal)
        new='recovery14_'+name.removeprefix('registered13_');assert not (A/'service_owned_workflows_20261006'/new/'native_launch.json').exists()
        replacements[name]=new;tasks.append((new,driver));inspections.append({'name':name,'identity':identity,'terminal':terminal,'idle_stack':stack})
    # All scientific outputs downstream of the failed native85 remain uncreated.
    for number in range(183,192):
        assert not (ROOT/f'candidates/optimization_20261003_r{number}').exists(),number
        assert not (A/f'optimization_20261003_r{number}').exists(),number
    aliases=dict(old['service_aliases']);aliases.update(replacements)
    for key,value in list(aliases.items()):aliases[key]=replacements.get(value,value)
    aliases['actual_three_cached_mixed149_after186_normalization_v1_20261011']=replacements['actual_three_cached_mixed149_after188_normalization_v1_20261011']
    # Future candidate/sealer/registration identities have never been dispatched.
    for key,value in list(aliases.items()):
        if value.startswith('registered13_') and any(token in value for token in ('183','184','185','186','187','188')):
            f=A/'service_owned_workflows_20261006'/value
            if not (f/'native_launch.json').exists():aliases[key]='recovery14_'+value.removeprefix('registered13_');aliases[value]=aliases[key]
    for family in ('MixedObjectiveWindow189','MixedProtected190','MixedRefined191'):
        for tail in ('selected_candidate_preparation','selected_candidate_sealing'):
            name=family+'_'+tail+'_v1_20261010';assert not (A/'service_owned_workflows_20261006'/name/'native_launch.json').exists();aliases[name]='recovery14_'+name
        number={'MixedObjectiveWindow189':189,'MixedProtected190':190,'MixedRefined191':191}[family]
        name=family+f'_round{number}_full_registration_v1_20261010';assert not (A/'service_owned_workflows_20261006'/name/'native_launch.json').exists();aliases[name]='recovery14_'+name
    legacy_sources=[Path(p) for p in old['input_sha256'] if Path(p).suffix=='.py' and Path(p).name.endswith('_v13.py')]
    mapping={p.name:p.name.replace('_v13.py','_v14_4650.py') for p in legacy_sources}
    mapping['route_complete_registered180_v13_20261011']='route_verified4650_recovery_v14_20261011'
    pattern=re.compile('|'.join(re.escape(k) for k in sorted(mapping,key=len,reverse=True)))
    outputs=[]
    for p in legacy_sources:
        q=A/mapping[p.name];assert not q.exists();text=pattern.sub(lambda m:mapping[m.group()],p.read_text(encoding='utf8'));compile(text,str(q),'exec');q.write_text(text,encoding='utf8',newline='\n');outputs.append(q)
    wrappers={k:mapping.get(v,v) for k,v in old['driver_wrappers'].items()}
    for _,driver in tasks:
        if driver not in wrappers:
            q=A/(Path(driver).stem+'_recovery14_wrapper.py');assert not q.exists()
            text="from pathlib import Path\nimport sys\nA=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]\nfrom route_verified4650_recovery_v14_20261011 import execute\nif __name__=='__main__':execute("+repr(driver)+")\n"
            compile(text,str(q),'exec');q.write_text(text,encoding='utf8',newline='\n');outputs.append(q);wrappers[driver]=q.name
    overrides={'qualify_stock_rank20_embedding85_selected_native14_v5_20261010.py':'qualify_stock_rank20_embedding85_selected_native14_v6_20261011.py',
               'prepare_StockRank20Embedding183_selected_candidate_v5_20261010.py':'prepare_StockRank20Embedding183_selected_candidate_v6_20261011.py'}
    factories=old['source_factories']+['prepare_MixedObjectiveWindow189_complete149_pipeline_v3_20261011','prepare_MixedProtected190_complete39_pipeline_v1_20261011','prepare_MixedRefined191_complete27_pipeline_v1_20261011']
    pins={str(p):sha(p) for p in [Path(__file__),A/'route_verified4650_recovery_v14_20261011.py',oldpath,
          A/'stock_rank20_183_actual4650_cardinality_recovery_admission_v1_20261011.json',
          *[A/n for n in overrides.values()],A/'register_StockRank20Embedding183_round183_artifacts_v4_20261011.py',*outputs]}
    create(PROOF,{'status':'compiled_actual4650_fresh_routes_before_new_native_and_future_dispatch','service_aliases':aliases,'driver_wrappers':wrappers,
           'actual_source_overrides':overrides,'source_factories':factories,'remaining_tasks':tasks,'input_sha256':pins,
           'original_failures_preserved':True,'verified_idle_helpers':inspections,'actual_stock_count':4650,'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})
    for row in inspections:
        if owned(row['identity']):
            assert allowed();assert not psutil.Process(row['identity']['owned_worker_pid']).children()
            retire(row['identity'],'Replace exact idle dependency helper after actual183 cardinality failure; fresh4650 native and routes, no science output overwritten')
    for name,driver in tasks:
        assert allowed();row=start_service(name,wrappers[driver],[],{str(PROOF):sha(PROOF),str(A/'route_verified4650_recovery_v14_20261011.py'):sha(A/'route_verified4650_recovery_v14_20261011.py')})
        create(A/(name+'_activation.json'),row)
    print({'actual_recovery14_dispatched':len(tasks),'new_native_fits':0,'completed_scores_reused':True},flush=True)

if __name__=='__main__':main()
