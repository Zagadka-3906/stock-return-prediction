"""Fix a future CDF replay report contract before any candidate execution."""
from pathlib import Path
import sys, ast, subprocess, psutil, time, importlib
A=Path(__file__).resolve().parent
sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service

def save(old,new,changes):
    s=(A/old).read_text(encoding='utf-8')
    for before,after in changes:
        assert before in s,(old,before)
        s=s.replace(before,after)
    p=A/new;ast.parse(s)
    if p.exists():assert p.read_text(encoding='utf-8')==s
    else:p.write_text(s,encoding='utf-8',newline='\n')
    return p

def idle_identity(name):
    d=A/'service_owned_workflows_20261006'/name
    identity=read(d/'native_launch.json');assert owned(identity) and not (d/'service_execution.json').exists()
    for _ in range(10):
        dump=subprocess.run([str(A.parent/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'),'dump','--pid',str(identity['owned_worker_pid'])],capture_output=True,text=True,encoding='utf-8',check=True).stdout
        if '(idle)' in dump and 'closed (prepare_protected_tail_pilot76_and_selected_native14_v1_20261010.py:' in dump:break
        time.sleep(1)
    else:raise AssertionError('Preserve non-idle controller '+name)
    assert owned(identity) and not psutil.Process(identity['owned_worker_pid']).children(recursive=True)
    return identity,dump

def main():
    assert allowed()
    prefix='rank60_two_capacity_CDF'
    predictor='predict_'+prefix+'_complete_qualified183_scheme_v1_20261011.py'
    predictor2=predictor.replace('_v1_','_v2_')
    wrong='native_reload_two_independent_decoders_scalar_mix_and_Pandas_protected_tail_bits_exact'
    correct='native_reload_two_independent_decoders_scalar_mix_and_Pandas_CDF_bits_exact'
    stage=A/(prefix+'_after_qualified183_native_stage_v1_20261011.py')
    assert correct in stage.read_text(encoding='utf-8') and wrong not in stage.read_text(encoding='utf-8')
    outputs=[save(predictor,predictor2,[(wrong,correct)])]
    tree=ast.parse(outputs[0].read_text(encoding='utf-8'))
    node=next(n for n in ast.walk(tree) if isinstance(n,ast.Assert) and correct in ast.unparse(n))
    expression=compile(ast.Expression(node.test),str(outputs[0])+'::actual_report_contract','eval')
    for count in (1,3,5):assert eval(expression,{'calls':[{correct:True} for _ in range(count)]})
    assert not eval(expression,{'calls':[{correct:True},{correct:False}]})
    try:eval(expression,{'calls':[{wrong:True}]})
    except KeyError:pass
    else:raise AssertionError('Wrong report contract accepted')
    proofname='capacity_CDF49_future_report_contract_recovery_admission_v2_20261011.json'
    prep='prepare_Rank60TwoCapacityCdf49Early_selected_candidate_v2_20261011.py'
    prep3=prep.replace('_v2_','_v3_')
    outputs.append(save(prep,prep3,[(predictor,predictor2),(Path(predictor).stem,Path(predictor2).stem),("'rank60_two_capacity_CDF49_early_sources_admission_v2_20261011.json'","'rank60_two_capacity_CDF49_early_sources_admission_v2_20261011.json',A/'"+proofname+"'")]))
    runner='run_Rank60TwoCapacityCdf49Early_selected_candidate_feature_cache_v2_20261011.py'
    runner3=runner.replace('_v2_','_v3_')
    outputs.append(save(runner,runner3,[(prep,prep3)]))
    queue='run_rank60_two_capacity_CDF49_early_gaining_candidate_queue_v1_20261011.py'
    queue2=queue.replace('_v1_','_v2_')
    outputs.append(save(queue,queue2,[(runner,runner3),("str(A/'rank60_two_capacity_CDF49_early_sources_admission_v2_20261011.json'):sha(A/'rank60_two_capacity_CDF49_early_sources_admission_v2_20261011.json')","str(A/'rank60_two_capacity_CDF49_early_sources_admission_v2_20261011.json'):sha(A/'rank60_two_capacity_CDF49_early_sources_admission_v2_20261011.json'),str(A/'"+proofname+"'):sha(A/'"+proofname+"')")]))
    oldqueue='actual_rank60_two_capacity_CDF49_early_gaining_candidate_queue_v1_20261011'
    newqueue=oldqueue.replace('_v1_','_v2_')
    publisher='publish_actual_capacity_CDF49_complete_candidate_main_v1_20261011.py'
    publisher2=publisher.replace('_v1_','_v2_')
    outputs.append(save(publisher,publisher2,[(oldqueue,newqueue),("Actual_capacity_CDF49_complete_candidate_sources_and_submission_main_v1_20261011","Actual_capacity_CDF49_complete_candidate_sources_and_submission_main_v2_20261011")]))
    oldmain='actual_capacity_CDF49_complete_candidate_main_v1_20261011';newmain=oldmain.replace('_v1_','_v2_')
    delivery='prepare_verified_capacity_CDF49_alternate_submission_delivery_v1_20261011.py'
    delivery2=delivery.replace('_v1_','_v2_')
    outputs.append(save(delivery,delivery2,[(oldqueue,newqueue),(oldmain,newmain)]))
    olddelivery='actual_verified_capacity_CDF49_alternate_delivery_v1_20261011';newdelivery=olddelivery.replace('_v1_','_v2_')
    old=[]
    for name in (oldqueue,oldmain,olddelivery):old.append((name,*idle_identity(name)))
    assert not (A/'rank60_two_capacity_CDF49_early_gain_decision_v1_20261011.json').exists()
    assert not (A/'Rank60TwoCapacityCdf49Early_selected_release_v1_20261011/inference_ready.json').exists()
    for p in outputs[:3]:importlib.import_module(p.stem)
    paths=[Path(__file__),stage,*outputs,A/predictor,A/prep,A/runner,A/queue,A/publisher,A/delivery]
    create(A/proofname,{'status':'passed_actual_CDF_report_contract_true_false_and_missing_field_refusal_before_future_candidate','input_sha256':{str(p):sha(p) for p in paths},'actual_report_contract_positive_cases':3,'actual_false_report_refused':True,'actual_other_codec_report_refused':True,'actual_new_modules_imported':3,'original_all_native_independent_reload_csv_cold80_assertions_retained':True,'scientific_workers_restarted':0,'new_fits':0,'new_scores':0,'test_labels_read':False,'retired_idle_controller_identities':[{'name':n,'identity':i,'actual_idle_dump':d} for n,i,d in old],'service_alias_updates':{oldqueue:newqueue,oldmain:newmain,olddelivery:newdelivery}})
    for n,i,d in old:
        assert owned(i);psutil.Process(i['owned_worker_pid']).terminate()
    activation=[]
    for n,driver in [(newqueue,queue2),(newmain,publisher2),(newdelivery,delivery2)]:
        assert allowed();activation.append(start_service(n,driver,[],{str(A/driver):sha(A/driver),str(A/proofname):sha(A/proofname)}))
    create(A/'actual_capacity_CDF49_correct_report_contract_routes_v2_20261011.json',{'activations':activation,'service_alias_updates':{oldqueue:newqueue,oldmain:newmain,olddelivery:newdelivery},'new_scientific_execution_claimed':False})
    print('CDF report contract fixed and exercised; 3 idle controllers routed; scientific workers unchanged',flush=True)

if __name__=='__main__':main()
