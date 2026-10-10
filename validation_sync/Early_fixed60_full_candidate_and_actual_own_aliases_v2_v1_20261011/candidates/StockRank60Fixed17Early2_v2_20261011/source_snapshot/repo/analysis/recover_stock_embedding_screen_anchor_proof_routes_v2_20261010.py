"""Retain the169 fixture compatibility proof; bind actual170/172 release scores separately."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_ready_goss_full_execution_20261006 import start_service,retire
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def save(name,text):
    p=A/name;assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p
def main():
    assert allowed()
    failed=A/'service_owned_workflows_20261006/actual_stock_embedding_after170_fast17_screen_v1_20261010/service_execution.json'
    assert read(failed)['status']=='failed' and 'exact_E_TRAIN_validation_actual_anchor170' in read(failed)['failure']
    proof=A/'exact_E_TRAIN_validation_actual_anchor169_all8_compatibility_v1_20261010.json';assert proof.is_file()
    inputs=[];tasks=[]
    for number in (170,172):
        name='run_stock_embedding_after170_fast17_screen_v1_20261010.py' if number==170 else 'run_stock_embedding_after172_high_impact17_screen_v1_20261010.py'
        original=A/name;inputs.append(original);text=original.read_text(encoding='utf8')
        bad=f'exact_E_TRAIN_validation_actual_anchor{number}_all8_compatibility_v1_20261010.json'
        assert text.count(bad)==1;text=text.replace(bad,proof.name)
        source=save(name.replace('_v1_','_v2_'),text)
        assert not Path(f'E:/赛题五_本机临时/StockEmbeddingSmall512_after{number}_high_impact17_screen_v1_20261010').exists()
        tasks.append((number,source))
    #The172 dispatcher is waiting for the existing172 complete family and has
    #never allocated its exclusive score output; retire that idle helper only.
    old='actual_stock_embedding_after172_high_impact17_screen_v1_20261010'
    row=read(A/'service_owned_workflows_20261006'/old/'native_launch.json');assert owned(row)
    retire(row,'Correct fixture-proof169 pin independently from future172 actual baseline; no stock score/output has started, successor172v2 preserves the original17 cases.')
    oldpub='actual_stock_embedding17_completion_main_v49_20261010';row=read(A/'service_owned_workflows_20261006'/oldpub/'native_launch.json')
    if owned(row):retire(row,'Idle publisher49 replaced by actual172v2 completion publisher52; no Git mutation or scientific score performed.')
    launched=[]
    for number,source in tasks:
        name='actual_stock_embedding_after170_fast17_screen_v2_20261010' if number==170 else 'actual_stock_embedding_after172_high_impact17_screen_v2_20261010'
        assert allowed();row=start_service(name,source.name,[],{str(source):sha(source),str(proof):sha(proof)})
        create(A/f'actual_stock_embedding_after{number}_screen_activation_v2_20261010.json',row);launched.append(source)
        proto=A/('publish_stock_embedding_after170_fast17_completion_v51_20261010.py' if number==170 else 'publish_stock_embedding17_completion_v49_20261010.py')
        text=proto.read_text(encoding='utf8')
        oldservice='actual_stock_embedding_after170_fast17_screen_v1_20261010' if number==170 else 'actual_stock_embedding_after172_high_impact17_screen_v1_20261010'
        text=text.replace(oldservice,name).replace(inputs[0 if number==170 else 1].name,source.name)
        version=53 if number==170 else 52;oldversion=51 if number==170 else 49
        #Replace only publisher artifact namespaces, preserving every existing
        #prototype path and frozen source pin in its inherited inventory.
        for token in (f'completion_v{oldversion}',f'completion_main_v{oldversion}',f'completion_main_receipt_v{oldversion}'):
            text=text.replace(token,token.replace(f'v{oldversion}',f'v{version}'))
        publisher=save(f'publish_stock_embedding_after{number}_completion_v{version}_20261010.py',text)
        pname=f'actual_stock_embedding_after{number}_completion_main_v{version}_20261010'
        assert allowed();row=start_service(pname,publisher.name,[],{str(publisher):sha(publisher)})
        create(A/f'actual_stock_embedding_after{number}_completion_main_activation_v{version}_20261010.json',row);launched.append(publisher)
    create(A/'stock_embedding_score_original_fixture169_and_actual170172_baseline_route_recovery_v2_20261010.json',{'status':'compiled_original_fixture169_proof_and_independent_actual_170172_baselines','input_sha256':{str(p):sha(p) for p in [Path(__file__),failed,proof,*inputs,*launched]},'failed_fast170_attempt_before_output_and_quality_scores':True,'original17_cases_and_kernels_unchanged':True,'no_blind_reuse_of_existing_exclusive_score_output':True,'new_quality_scores':0})
    print('Actual fast170v2 and later172v2 screens53/52 publishers launched; original169 compatibility fixture remains honestly169',flush=True)
if __name__=='__main__':main()
