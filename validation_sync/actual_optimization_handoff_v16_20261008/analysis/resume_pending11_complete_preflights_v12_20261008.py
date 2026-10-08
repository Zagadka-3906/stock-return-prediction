"""Retain completed137 and failed138; verify138 against actual D1 records, then remaining routes."""
from pathlib import Path
import ast,hashlib,importlib,sys,time
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def main():
    import recover_pending137to141_registration_contracts_v11_20261008 as h
    h.initialize();old=A/'verify_BF16reverse40_prospective_routes_v11_20261008.py';target=A/'verify_BF16reverse40_prospective_routes_actual_D1_v12_20261008.py'
    assert not target.exists();text=old.read_text(encoding='utf8');patches={
      'verify_BF16reverse138_D_scoring_scope_v2_20261008':'verify_BF16reverse138_D_scoring_scope_v1_20261008',
      'BF16reverse138_D_scoring_scope_v2_20261008.json':'BF16reverse138_D_scoring_scope_v1_20261008.json',
      ",A/'actual_BF16reverse138_complete_dependency_recovery_v5_20261008.json'":"",
      ",A/'actual_BF16reverse138_D_scoring_receiver_recovery_v4_20261008.json'":"",
      'transfer_probe_v11':'transfer_probe_v12','cross_volume_byte_probe_v11':'cross_volume_byte_probe_v12'}
    for before,after in patches.items():text=text.replace(before,after)
    # The actual source12 and failed source11 are both explicit, immutable provenance.
    text=text.replace("names=[scorer,Path(__file__),", "names=[scorer,Path(__file__),A/'verify_BF16reverse40_prospective_routes_v11_20261008.py',")
    compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n')
    create(A/'pending11_reverse138_missing_alias_recovery_v12_20261008.json',{
      'status':'prepared_actual_D1_binding_after_missing_D2_alias_failure','input_sha256':{str(p):sha(p) for p in [Path(__file__),old,target,A/'BF16reverse138_D_scoring_scope_v1_20261008.json']},
      'patches':patches,'failed_source11_and_probe_bytes_preserved':True,'cache_gates_and_mathematics_unchanged':True,'new_official_scores':0})
    records=[];proofs=[]
    for cfg in h.CONFIG:
        module=importlib.import_module(h.version11(cfg['generator']))
        for parent in cfg['parents']:
            generated=module.generate(parent);fn=next(x for x in ast.parse(next(t for n,t in generated.items() if n.startswith('collect_full_'))).body if isinstance(x,ast.FunctionDef) and x.name=='collect')
            forwarded=[];scope={'namespace':{'collect':lambda *args:forwarded.append(args)}}
            exec(compile(ast.fix_missing_locations(ast.Module(body=[fn],type_ignores=[])),'<actual-complete-collector-contract>','exec'),scope)
            scope['collect'](cfg['round'],cfg['qa'],cfg['count']);assert forwarded==[(cfg['round'],cfg['qa'],cfg['count'])]
            records.append({'round':cfg['round'],'parent':parent,'actual_argument_contract_passed':True})
        if cfg['round']==137:
            proof=A/'Huber52_prospective_routes_v11_20261008.json';assert read(proof)['prospective_sources']==24
            for path,digest in read(proof)['input_sha256'].items():assert sha(path)==digest,path
        elif cfg['round']==138:
            importlib.import_module(target.stem).main();proof=A/'BF16reverse40_prospective_routes_v11_20261008.json'
        else:
            importlib.import_module(h.version11(cfg['prospective'])).main()
            prefix={139:'HuberCrossFamily112',140:'SpectralGram52',141:'KrylovGram52'}[cfg['round']]
            proof=A/(prefix+'_prospective_routes_v11_20261008.json')
        proofs.append(proof);print('Actual preflight complete for round'+str(cfg['round']),flush=True)
    create(A/'pending137to141_collector_controls_v11_20261008.json',{
      'status':'passed_all15_collectors_and_five_complete_prospective_preflights','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
      'input_sha256':{str(p):sha(p) for p in [Path(__file__),target,*proofs]},'records':records,
      'failed11_missing_D2_refs_preserved_and_actual_D1_checked':True,'new_quality_scores':0,'new_inference_calls':0,'test_labels_read':False})
if __name__=='__main__':main()
