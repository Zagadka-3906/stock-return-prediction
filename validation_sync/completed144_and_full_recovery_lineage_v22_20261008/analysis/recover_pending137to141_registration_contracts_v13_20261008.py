"""Fresh pending receivers preserve science while correcting frozen future collector routing."""
from pathlib import Path
import ast, hashlib, importlib, re, subprocess, sys, time
ROOT=Path(__file__).resolve().parents[1]; A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
SPECS=[
 (137,52,48,'Huber137_complete_hidden_launches_v3_20261008.json','prepare_Huber52_round137_sources_v3_20261008','verify_Huber52_prospective_routes_v3_20261008', (134,135,136)),
 (138,40,49,'BF16reverse138_complete_hidden_launches_v1_20261008.json','prepare_BF16reverse40_round138_sources_v1_20261008','verify_BF16reverse40_prospective_routes_v1_20261008',(135,136,137)),
 (139,112,50,'HuberCrossFamily139_complete_hidden_launches_v1_20261008.json','prepare_HuberCrossFamily112_round139_sources_v1_20261008','verify_HuberCrossFamily112_prospective_routes_v1_20261008',(136,137,138)),
 (140,52,51,'SpectralGram140_complete_hidden_launches_v4_20261008.json','prepare_SpectralGram52_round140_sources_v2_20261008','verify_SpectralGram52_prospective_routes_v3_20261008',(137,138,139)),
 (141,52,52,'KrylovGram141_complete_hidden_launches_v3_20261008.json','prepare_KrylovGram52_round141_sources_v3_20261008','verify_KrylovGram52_prospective_routes_v3_20261008',(138,139,140))]
MAPPING={};CONFIG=[]
def version12(value):return re.sub(r'_v\d+_20261008','_v13_20261008',value)
def initialize():
    if CONFIG:return
    for n,count,qa,index,generator,prospective,parents in SPECS:
        launches=dict(read(A/index)['launches']);assert len(launches)==(7 if n==138 else 8)
        if n==138:
            for service in ('BF16_reverse_rank_CDF_actual_full37_controls_v1_20261008','BF16_reverse_complete_parent_actual_historical_native_hook3_v1_20261008'):
                launches[service]=read(A/'service_owned_workflows_20261006'/service/'native_launch.json')
        cfg={'round':n,'count':count,'qa':qa,'index':index,'generator':generator,'prospective':prospective,'parents':parents,'launches':launches}
        CONFIG.append(cfg)
        for name,row in launches.items():
            if n==137 and name.startswith('HuberIRLS64_49_current_parent_controls_'):continue
            MAPPING[name]=version12(name)
            stem=Path(row['original_driver']).stem;MAPPING[stem]=version12(stem)
        MAPPING[generator]=version12(generator);MAPPING[prospective]=version12(prospective)
        texts=[(A/(generator+'.py')).read_text(encoding='utf8'),(A/(prospective+'.py')).read_text(encoding='utf8')]
        texts += [Path(row['original_driver']).read_text(encoding='utf8') for row in launches.values()]
        for text in texts:
            for value in re.findall(r'[A-Za-z_0-9]+_v\d+_20261008',text):
                if any(word in value for word in ('_round'+str(n)+'_source_admission','_round'+str(n)+'_source_preparation',
                    '_actual_controls_index','_prospective_routes','_receiver_preparation','_receiver_drafts','_round'+str(n)+'_actual_registration')):
                    if value.startswith(('Huber52','Huber137','BF16reverse40','BF16reverse138','HuberCrossFamily112','HuberCrossFamily139','SpectralGram52','SpectralGram140','KrylovGram52','KrylovGram141')):
                        MAPPING[value]=version12(value)
                if n!=137 and ('current_parent' in value) and value.startswith(('BF16reverse','actual_BF16reverse','HuberCrossFamily','actual_HuberCrossFamily','SpectralGram','actual_SpectralGram','KrylovGram','actual_KrylovGram')):
                    MAPPING[value]=version12(value)
        # Keep immutable physical scoring/release and phase receipts at their declared paths.
        cfg['physical_comparison']=next(name for name in re.findall(r"(?:OUT\s*=\s*A\s*/\s*|A\s*/\s*)['\"]([^'\"]+official_comparison_v\d+_20261008)['\"]",texts[-1]+''.join(texts)) if (A/name).is_dir())

    MAPPING.update({
        'BF16wide40_round135_full_registration_v4_20261008':'BF16wide40_round135_full_registration_v7_20261008',
        'CrossFamily94_round136_full_registration_v4_20261008':'CrossFamily94_round136_full_registration_v5_20261008',
        'HuberIRLS64_49_current_parent_controls_v4_20261008':'HuberIRLS64_49_current_parent_controls_v5_20261008',
        'verify_HuberIRLS64_49_current_parent_v4_20261008':'verify_HuberIRLS64_49_current_parent_v5_20261008',
        'actual_HuberIRLS64_49_current_parent_location_v4_20261008':'actual_HuberIRLS64_49_current_parent_location_v5_20261008'})

def remap(text):
    initialize();value=text; protected={}
    physical={c['physical_comparison'] for c in CONFIG}
    for name in physical:
        for token in ("A/'"+name+"'","A / '"+name+"'",name+'/'):
            placeholder='__PRESERVED_PHYSICAL_OUTPUT_'+str(len(protected))+'__'
            if token in value:protected[placeholder]=token;value=value.replace(token,placeholder)
    for old,new in sorted(MAPPING.items(),key=lambda pair:-len(pair[0])):value=value.replace(old,new)
    for token,original in protected.items():value=value.replace(token,original)
    for cfg in CONFIG:
        for row in cfg['launches'].values():
            stem=Path(row['original_driver']).stem
            if '_full_registration_' in stem:
                prefix=stem.split('_20261008')[0]
                value=value.replace(prefix+'_file_IO_',version12(stem).split('_20261008')[0]+'_file_IO_')
    return value

def corrected_generated(number,generated):
    initialize();cfg=next(c for c in CONFIG if c['round']==number);out={}
    for name,text in generated.items():
        value=remap(text)
        if name.startswith('collect_full_'):
            tree=ast.parse(value);function=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='collect')
            guard=function.body[0];assert isinstance(guard,ast.Assert)
            lines=value.splitlines(keepends=True)
            assert len(function.args.args)==3 and [x.arg for x in function.args.args]==['number','qa_version','expected_records']
            lines[guard.lineno-1:guard.end_lineno]=[f"    assert (number, qa_version, expected_records) == ({number}, {cfg['qa']}, {cfg['count']})\n"]
            value=''.join(lines)
        if name.startswith('publish_'):
            tree=ast.parse(value);call=next(x for x in ast.walk(tree) if isinstance(x,ast.Call) and isinstance(x.func,ast.Name) and x.func.id=='collect')
            lines=value.splitlines(keepends=True);line=lines[call.lineno-1]
            old=ast.get_source_segment(value,call);assert old in line
            lines[call.lineno-1]=line.replace(old,f"collect({number}, {cfg['qa']}, {cfg['count']})");value=''.join(lines)
            value=re.sub(r'actual_complete_QA_version=\d+',f"actual_complete_QA_version={cfg['qa']}",value)
            value=re.sub(r"('actual_full_QA_version':\s*)\d+",lambda m:m[1]+str(cfg['qa']),value)
        compile(value,str(A/name),'exec');out[name]=value
    return out

def save(path,text):
    assert not path.exists(),path;compile(text,str(path),'exec');path.write_text(text,encoding='utf8',newline='\n')

def prepare():
    initialize();audit=read(A/'future_registration_collector_contract_audit_v2_20261008.json')
    assert [r['round'] for r in audit['records'] if not r['contract_passed']]==[137,138,139,140,141]
    outputs=[];sources=[Path(__file__),A/'future_registration_collector_contract_audit_v2_20261008.json']
    products=[]
    for cfg in CONFIG:
        n=cfg['round']; module=importlib.import_module(cfg['generator']); original_text=Path(module.__file__).read_text(encoding='utf8')
        tail=remap(original_text.split('\ndef main():',1)[1])
        # Some wrappers expose a compressed main declaration; the exact function body is still copied.
        prefix=f'''"""Fresh registration9: unchanged model/grid; explicit collector contract and chronological services."""
from pathlib import Path
import hashlib,time
from run_dependency_queue_v3_20261006 import read,sha,create
import {cfg['generator']} as original
from recover_pending137to141_registration_contracts_v13_20261008 import remap,corrected_generated
ROOT=original.ROOT;A=original.A;NAMES=original.NAMES
def source_paths():
    previous=original.source_paths()
    current=[A/remap(p.relative_to(A).as_posix()) for p in previous]
    retained=[p for p in previous if p.is_file()]
    return list(dict.fromkeys([*current,*retained,Path(__file__),A/'recover_pending137to141_registration_contracts_v13_20261008.py',A/'pending137to141_receiver_preparation_v13_20261008.json',A/'prepare_pending137to141_fresh_closed_dependencies_v13_20261008.py',A/'short_content_addressed_native_storage_v2_20261008.py',A/'actual_short_parent_alias_nested_copy_v2_20261008.json']))
def generate(parent):return corrected_generated({n},original.generate(parent))
def main():'''
        generated=prefix+tail;products.append((A/(version12(cfg['generator'])+'.py'),generated));sources.append(Path(module.__file__))
        for name,row in cfg['launches'].items():
            if name not in MAPPING or name.startswith('HuberIRLS64_49_current_parent_controls_'):continue
            old=Path(row['original_driver']);sources.append(old);value=remap(old.read_text(encoding='utf8'))
            if old.stem.startswith('prepare_') and '_selected_candidate_' in old.stem:
                if n==137:value=value.replace("freeze=A/'Huber52_pre_inference_source_freeze_v1_20261008'", "freeze=Path('E:/赛题五_本机临时/第137轮_20261008/pre_inference_source_freeze_v13')")
                if n==138:value=value.replace("freeze=A/'BF16reverse40_pre_inference_source_freeze_v1_20261008'", "freeze=Path('E:/赛题五_本机临时/第138轮_20261008/pre_inference_source_freeze_v13')")
                line="            prediction,storage=predict(ns,selection,CANDIDATE,parent_candidate/'cohort_curve.json',OUT/'future_return_mapping.json');output_scope.reverify()"
                assert value.count(line)==1,old
                value=value.replace(line,"            from short_content_addressed_native_storage_v2_20261008 import installed as short_storage\n            with short_storage(ns,freeze/'model_source_aliases') as alias_contract:\n                prediction,storage=predict(ns,selection,CANDIDATE,parent_candidate/'cohort_curve.json',OUT/'future_return_mapping.json')\n            create(OUT/'short_native_source_aliases_execution.json',alias_contract)\n            output_scope.reverify()")
            if old.stem.startswith('seal_') and '_selected_candidate_' in old.stem:
                line="        target=candidate/'evidence'/source.relative_to(A);target.parent.mkdir(parents=True,exist_ok=True);os.link(source,target);assert sha(target)==sha(source)"
                assert value.count(line)==1,old
                value=value.replace(line,"        relative=source.relative_to(A) if source.is_relative_to(A) else Path('external_frozen_metadata')/(sha(source)+'_'+source.name)\n        target=candidate/'evidence'/relative;target.parent.mkdir(parents=True,exist_ok=True)\n        if target.exists():assert sha(target)==sha(source)\n        else:os.link(source,target)\n        assert sha(target)==sha(source)")
            products.append((A/(MAPPING[old.stem]+'.py'),value))
        prospective=A/(cfg['prospective']+'.py');sources.append(prospective)
        value=remap(prospective.read_text(encoding='utf8'))
        if n==138:
            for before,after in {
                'verify_BF16reverse138_D_scoring_scope_v2_20261008':'verify_BF16reverse138_D_scoring_scope_v1_20261008',
                'BF16reverse138_D_scoring_scope_v2_20261008.json':'BF16reverse138_D_scoring_scope_v1_20261008.json',
                ",A/'actual_BF16reverse138_complete_dependency_recovery_v5_20261008.json'":"",
                ",A/'actual_BF16reverse138_D_scoring_receiver_recovery_v4_20261008.json'":""}.items():value=value.replace(before,after)

        # New exclusive D/E transfer probe names avoid collisions with every retained preflight.
        value=re.sub(r'(transfer_probe|cross_volume_byte_probe)_v\d+',r'\1_v13',value)
        products.append((A/(version12(cfg['prospective'])+'.py'),value))
        for old,new in MAPPING.items():
            if any(word in old for word in ('receiver_preparation','receiver_drafts')) and (A/(old+'.json')).is_file():
                if new+'.json' in value and 'create(A/\''+new+'.json' not in value:
                    products_meta={'status':'prepared_fresh_registration9_metadata_before_actual_prospective_checks',
                        'original_passed_metadata':str(A/(old+'.json')),'original_sha256':sha(A/(old+'.json')),
                        'fresh_prospective_checks_required':True,'new_quality_scores':0}
                    if not (A/(new+'.json')).exists():create(A/(new+'.json'),products_meta)
        # Prospective verifiers hash an existing queue file; a frozen declarative clone suffices.
        for queue in re.findall(r"([A-Za-z_0-9]*queue[A-Za-z_0-9]*_v\d+_20261008\.py)",prospective.read_text(encoding='utf8')):
            old=A/queue
            if old.is_file():sources.append(old)
    unique={str(path):(path,text) for path,text in products}
    for path,text in unique.values():assert not path.exists();compile(text,str(path),'exec')
    for path,text in unique.values():save(path,text);outputs.append(path)
    for old,new in MAPPING.items():
        source=A/(old+'.json');target=A/(new+'.json')
        if 'receiver_drafts' in old and source.is_file() and not target.exists():
            create(target,{'status':'prepared_fresh12_declarative_drafts_before_actual_prospective_checks',
                'original_source':str(source),'original_sha256':sha(source),'new_official_scores':0,'test_labels_read':False})
    # Pin all generated surfaces before execution; receiver preflight checks additionally pin their actual sources.
    create(A/'pending137to141_receiver_preparation_v13_20261008.json',{
        'status':'prepared_fresh_five_round_registration_receivers_before_quality',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in dict.fromkeys([*sources,*outputs])},
        'mapping':MAPPING,'rounds':[137,138,139,140,141],'source_files':len(outputs),
        'native_models_grid_and_physical_scoring_outputs_unchanged':True,'new_quality_scores':0,'new_inference_calls':0,'test_labels_read':False})
    print('Fresh11 source surfaces frozen; no workers retired yet.',flush=True)

def controls():
    initialize();records=[];proof=read(A/'pending137to141_receiver_preparation_v13_20261008.json')
    for path,digest in proof['input_sha256'].items():assert sha(path)==digest,path
    for cfg in CONFIG:
        module=importlib.import_module(version12(cfg['generator']))
        for parent in cfg['parents']:
            generated=module.generate(parent);assert len(generated)==8
            collector=next(text for name,text in generated.items() if name.startswith('collect_full_'));tree=ast.parse(collector)
            fn=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='collect');forwarded=[]
            namespace={'namespace':{'collect':lambda *args:forwarded.append(args)}}
            exec(compile(ast.fix_missing_locations(ast.Module(body=[fn],type_ignores=[])),'<fresh11collector>','exec'),namespace)
            namespace['collect'](cfg['round'],cfg['qa'],cfg['count']);assert forwarded==[(cfg['round'],cfg['qa'],cfg['count'])]
            records.append({'round':cfg['round'],'parent':parent,'actual_argument_contract_passed':True})
        importlib.import_module(version12(cfg['prospective'])).main()
        print('Fresh11 complete prospective routes passed for round'+str(cfg['round']),flush=True)
    create(A/'pending137to141_collector_controls_v13_20261008.json',{'status':'passed_all15_collectors_and_five_complete_prospective_preflights',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'records':records,'new_quality_scores':0,'new_inference_calls':0,'test_labels_read':False})

def dispatch():
    initialize();import psutil
    assert read(A/'pending137to141_collector_controls_v13_20261008.json')['status']=='passed_all15_collectors_and_five_complete_prospective_preflights'
    fitter=read(A/'service_owned_workflows_20261006/actual_neural_BF16_micro8192_bank6_v2_20261008/native_launch.json');assert owned(fitter)
    audits={};pairs=[]
    for cfg in CONFIG:
        assert not any((A/cfg['physical_comparison']).iterdir())
        for name,row in cfg['launches'].items():
            if name not in MAPPING or name.startswith('HuberIRLS64_49_current_parent_controls_'):continue
            assert owned(row) and Path(row['stderr']).stat().st_size==0,name
            result=subprocess.run([str(ROOT/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'),'dump','--pid',str(row['owned_worker_pid'])],capture_output=True,text=True,encoding='utf8',errors='replace',timeout=10,creationflags=subprocess.CREATE_NO_WINDOW)
            assert result.returncode==0 and ('    closed (' in result.stdout or ('    main (seal_' in result.stdout) or ('    main (run_' in result.stdout and '_full_registration_' in result.stdout)),(name,result.stdout)
            worker=psutil.Process(row['owned_worker_pid']);parent=psutil.Process(row['pid'])
            assert worker.memory_info().rss<256*2**20 and not worker.children()
            assert parent.create_time()==row['owned_parent_creation_time'] and worker.parent().pid==parent.pid
            audits[name]={'identity':row,'actual_idle_stack':result.stdout};pairs.append((name,parent,worker))
    assert len(pairs)==40
    create(A/'pending137to141_exact_idle_audit_v13_20261008.json',{'status':'passed40_owned_idle_receivers_before_any_quality','audits':audits,'GPU_training_untouched':True})
    for name,parent,worker in reversed(pairs):
        row=audits[name]['identity'];assert owned(row)
        worker.terminate();worker.wait(timeout=10)
        try:
            if parent.is_running():assert parent.create_time()==row['owned_parent_creation_time'];parent.terminate();parent.wait(timeout=10)
        except psutil.NoSuchProcess:pass
        create(A/'service_owned_workflows_20261006'/name/'administrative_collector_supersession_v13_20261008.json',{
            'status':'superseded_exact_owned_idle_receiver_before_quality','identity':row,'replacement':MAPPING[name],
            'original_sources_and_logs_preserved':True,'training_workers_stopped':0,'new_official_scores':0})
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    all_rows={};base=A/'pending137to141_receiver_preparation_v13_20261008.json';pins={str(base):sha(base),str(Path(__file__)):sha(__file__),str(A/'pending137to141_collector_controls_v13_20261008.json'):sha(A/'pending137to141_collector_controls_v13_20261008.json')}
    for cfg in CONFIG:
        rows={}
        for name,row in cfg['launches'].items():
            if name not in MAPPING:rows[name]=row;assert owned(row);continue
            target=Path(row['original_driver']);driver=MAPPING[target.stem]+'.py'
            rows[MAPPING[name]]=start(MAPPING[name],driver,row['original_arguments'],{**pins,str(A/driver):sha(A/driver)})
        create(A/('round'+str(cfg['round'])+'_complete_hidden_launches_v13_20261008.json'),{
            'status':'started_exact8_fresh_collector11_scientific_receivers_after_complete_preflight','round':cfg['round'],
            'expected_records':cfg['count'],'QA_version':cfg['qa'],'launches':rows,'input_sha256':pins,
            'native_math_and_grid_unchanged':True,'new_quality_scores':0})
        all_rows[str(cfg['round'])]=rows
    assert owned(fitter)
    create(A/'pending137to141_receiver_dispatch_v13_20261008.json',{'status':'passed40_idle_replacements_and41_owned_future_steps',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'launches':all_rows,'GPU_fitter_identity':fitter,
        'unchanged137_current_control_reused':True,'training_workers_stopped':0,'new_official_scores':0,'test_labels_read':False})
    print('Fresh11 future five-round pipeline dispatched; original GPU and135136 unchanged.',flush=True)

if __name__=='__main__':
    {'prepare':prepare,'controls':controls,'dispatch':dispatch}[sys.argv[1]]()
