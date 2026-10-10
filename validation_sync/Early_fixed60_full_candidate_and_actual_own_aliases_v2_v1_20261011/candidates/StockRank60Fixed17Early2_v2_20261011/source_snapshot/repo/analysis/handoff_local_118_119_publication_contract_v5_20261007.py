"""Replace zero-science idle routes with a nonduplicating real publication contract."""
from pathlib import Path
import ast,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_ready_goss_full_execution_20261006 import start_service
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle,stack
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute
from prepare_local_118_119_protocol_recovery_v4_20261007 import FILES

def main():
    out=A/'local_118_119_publication_contract_v5_actual_handoff_20261007';assert not out.exists();out.mkdir()
    launch=read(A/'local_118_119_protocol_recovery_actual_hidden_launches_v4_20261007.json')
    rows=launch['launches'];held=[];retired=set();next_rows={}
    assert not list((A/'HGB_quarter_numeric28_official_comparison_v4_20261007').glob('case*_official.json'))
    assert not list((A/'quantile_HGB88_official_comparison_v4_20261007').glob('case*_official.json'))
    assert not (A/'HGB_quarter_numeric28_transform_preflight_v4_20261007').exists()
    names=list(rows)
    # Hold the two activation gates first, before their dependent science can start.
    names.sort(key=lambda n:(0 if n in ('HGB_quarter_numeric28_full25_transform_preflight_v4','HGB_quarter_numeric_audit_main_publication_after117_v4') else 1,n))
    try:
        idle={}
        for name in names:
            row=rows[name];assert owned(row),name
            definition=read(A/'service_owned_workflows_20261006'/name/'job_definition.json')
            driver=Path(definition['driver']);lines=driver.read_text(encoding='utf8').splitlines()
            before=stack(row['owned_worker_pid'])
            possible=[f'({driver.name}:{i+1})' for i,line in enumerate(lines) if 'time.sleep(' in line and f'({driver.name}:{i+1})' in before]
            assert len(possible)==1,(name,before)
            parent,worker,proof=suspended_idle(row,possible[0]);held.append((name,parent,worker));idle[name]=proof
        create(out/'actual17_exact_idle_before_and_after.json',idle)
        replacements={n:n.removesuffix('_v4')+'_v5' for n in rows}
        filemap={new:new.replace('_v4_20261007','_v5_20261007') for new in FILES.values()}
        mapping={**replacements,**{o[:-3]:n[:-3] for o,n in filemap.items()},
          'local_118_119_protocol_recovery_actual_hidden_launches_v4_20261007':'local_118_119_publication_contract_v5_actual_hidden_launches_20261007'}
        for stem in ['HGB_quarter_numeric28','quantile_HGB88']:
            number=118 if stem.startswith('HGB_') else 119
            for suffix in ['selected_release','pre_inference_source_freeze','official_comparison',f'round{number}_source_admission',f'round{number}_source_preparation',f'round{number}_actual_registration','controls_github','scores_github','{phase}_github']:
                mapping[f'{stem}_{suffix}_v4_20261007']=f'{stem}_{suffix}_v5_20261007'
            mapping[f'candidates/{stem}_v4_20261007']=f'candidates/{stem}_v5_20261007'
        for stem in ['HGB_quarter_numeric_audit_github','quantile_HGB_bank20_github']:
            mapping[stem+'_v4_20261007']=stem+'_v5_20261007'
        mapping['HGB_quarter_numeric28_transform_preflight_v4_20261007']='HGB_quarter_numeric28_transform_preflight_v5_20261007'
        generated={}
        for old,new in filemap.items():
            original=(A/old).read_text(encoding='utf8')
            if old.startswith('prepare_') and '_round' in old:
                node=next(n for n in ast.parse(original).body if isinstance(n,ast.FunctionDef) and n.name=='main')
                main_text='\n'.join(original.splitlines()[node.lineno-1:node.end_lineno])
                text=f'''from pathlib import Path
import hashlib,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute
import {Path(old).stem} as base
NAMES=base.NAMES
RECOVERY_MAP={mapping!r}
def generate(parent):
    return {{name:substitute(text,RECOVERY_MAP) for name,text in base.generate(parent).items()}}
'''+substitute(main_text,mapping)+"\nif __name__=='__main__':main()\n"
            else:text=substitute(original,mapping)
            if old.startswith('publish_') and 'evidence' in old:
                start=text.index("            if phase=='scores':\n                target=A/")
                end=text.index('    finally:',start)
                text=text[:start]+text[end:]
                assert "create(out/'receipt.json'" in text
                needle='    sources=list(dict.fromkeys(sources));'
                text=text.replace(needle,"    sources += [A/'handoff_local_118_119_publication_contract_v5_20261007.py',A/'local_118_119_publication_contract_v5_actual_handoff_20261007/verification.json']\n"+needle)
            compile(text,str(A/new),'exec');generated[new]=text
        for n in generated:assert not (A/n).exists(),n
        for n,text in generated.items():
            with (A/n).open('x',encoding='utf8',newline='\n') as f:f.write(text)
        sourceproof=out/'source_preparation.json'
        create(sourceproof,{'status':'compiled_fresh20_source_routes_single_actual_scores_receipt',
          'input_sha256':{str(A/n):sha(A/n) for n in generated},'new_native_fits':0,'new_quality_scores':0})
        pins={str(p):sha(p) for p in [Path(__file__),sourceproof,*[A/n for n in generated],A/'resolve_sealed_scientific_protocol_20261007.py']}
        for name,parent,worker in held:
            assert not worker.children()
            worker.terminate();worker.wait(timeout=15);parent.terminate();parent.wait(timeout=15);retired.add(name)
            create(A/'service_owned_workflows_20261006'/name/'administrative_supersession_before_science_v5_20261007.json',{
              'status':'administratively_retired_exact_idle_waiter_not_scientific_completion',
              'identity':rows[name],'successor_service':replacements[name],'scientific_workers_stopped':0,'at_local':time.strftime('%Y-%m-%dT%H:%M:%S')})
        for name in names:
            definition=read(A/'service_owned_workflows_20261006'/name/'job_definition.json')
            next_name=replacements[name];driver=filemap[Path(definition['driver']).name]
            next_rows[next_name]=start_service(next_name,driver,definition['arguments'],pins)
        create(A/'local_118_119_publication_contract_v5_actual_hidden_launches_20261007.json',{'status':'actual17_consoleless_successors_started','input_sha256':pins,'launches':next_rows})
        create(out/'verification.json',{'status':'passed_actual17_exact_idle_zero_science_waiters_and_single_receipt_contract',
          'input_sha256':pins,'retired_waiters':names,'actual_successors':next_rows,
          'new_native_fits':0,'new_quality_scores':0,'scientific_workers_stopped':0,'test_labels_read':False})
        print({'status':'passed','exact_idle_administrative_waiters':len(names)},flush=True)
    finally:
        for name,parent,worker in held:
            if name not in retired:
                for p in (parent,worker):
                    if p.is_running():p.resume()

if __name__=='__main__':main()
