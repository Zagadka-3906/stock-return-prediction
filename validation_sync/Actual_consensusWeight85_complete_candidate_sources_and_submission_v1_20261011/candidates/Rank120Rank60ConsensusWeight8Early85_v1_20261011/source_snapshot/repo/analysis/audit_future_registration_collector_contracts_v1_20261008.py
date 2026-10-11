"""Execute generated collector forwarding contracts without any ranking or inference."""
from pathlib import Path
import ast, importlib, sys, time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
SPECS=[(135,40,46,'prepare_BF16wide40_round135_sources_v4_20261008',134),
 (136,94,47,'prepare_CrossFamily94_round136_sources_v4_20261008',134),
 (137,52,48,'prepare_Huber52_round137_sources_v3_20261008',134),
 (138,40,49,'prepare_BF16reverse40_round138_sources_v1_20261008',134),
 (139,112,50,'prepare_HuberCrossFamily112_round139_sources_v1_20261008',134),
 (140,52,51,'prepare_SpectralGram52_round140_sources_v2_20261008',137),
 (141,52,52,'prepare_KrylovGram52_round141_sources_v3_20261008',138)]
def main():
    records=[];sources=[Path(__file__)]
    for number,count,qav,mod,parent in SPECS:
        module=importlib.import_module(mod);sources.append(Path(module.__file__))
        generated=module.generate(parent)
        name=next(n for n in generated if n.startswith('collect_full_'));tree=ast.parse(generated[name])
        function=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='collect')
        publisher=ast.parse(generated[next(n for n in generated if n.startswith('publish_'))])
        call=next(n for n in ast.walk(publisher) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='collect')
        args=tuple(ast.literal_eval(n) for n in call.args);forwarded=[]
        def forwarded_collect(*values):forwarded.append(values);return {}
        scope={'namespace':{'collect':forwarded_collect}}
        exec(compile(ast.fix_missing_locations(ast.Module(body=[function],type_ignores=[])),name,'exec'),scope)
        try:scope['collect'](*args);error=None
        except Exception as exception:error=type(exception).__name__+': '+str(exception)
        passed=error is None and forwarded==[(number,qav,count)]
        qa=generated[next(n for n in generated if n.startswith('verify_lossless_'))]
        row={'round':number,'expected_records':count,'QA_version':qav,'collector_name':name,
          'caller_args':args,'formal_args':[n.arg for n in function.args.args],
          'guard_source':ast.unparse(function.body[0]),'forwarded_args':forwarded,'contract_passed':passed,'error':error,
          'own_round_QA_chronology_patch_present':'number=REQUESTED_ROUND;' in qa,
          'generated_source_sha256':{n:__import__('hashlib').sha256(t.encode()).hexdigest() for n,t in generated.items()}}
        records.append(row);print(row['round'],row['contract_passed'],row['caller_args'],row['guard_source'],flush=True)
    create(A/'future_registration_collector_contract_audit_v1_20261008.json',{
      'status':'executed_all_seven_actual_generated_call_signatures_with_failures_preserved',
      'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in sources},
      'records':records,'new_official_scores':0,'new_inference_calls':0,'test_labels_read':False})
if __name__=='__main__':main()
