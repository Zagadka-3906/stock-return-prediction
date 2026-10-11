"""Prepare actual new sparse residual native and full CDF controls; no official scoring."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start

def save(original,fresh,changes=()):
    old=A/original;new=A/fresh;text=old.read_text(encoding='utf8')
    text=text.replace('EmpiricalBayes64','SparseGram64').replace('EmpiricalBayes37','SparseGram37').replace('nonflag_empirical_Bayes64_codec','nonflag_sparse_Gram64_codec')
    for before,after,count in changes:
        assert text.count(before)==count,(original,before,text.count(before));text=text.replace(before,after)
    compile(text,str(new),'exec');assert not new.exists();new.write_text(text,encoding='utf8',newline='\n');return [old,new]

def main():
    bankplan=A/'nonflag_residual_SparseGram6410_plan_20261007.json';plan=read(bankplan);heads=list(plan['configurations'])
    controlplan=A/'nonflag_SparseGram64_residual_precheck_plan_20261007.json'
    create(controlplan,{'status':'frozen_native_and_transform_controls_before_execution_not_official_comparison',
      'single_native_heads':heads,'ensembles':{'nonflag_residual_sparseGram64_equal_mean_two':heads},
      'weights':[.0003125,.000625,.00125,.0025,.005,.0075,.01,.015,.02,.03,.04,.05],
      'universe':'all_current_raw_forecasts','residual_sign':1,'reference_round':106,'complete_flag_parent_round':112,
      'expected_native_hook_cases':3,'expected_full_cases':37,'expected_cold_cases':111,
      'new_quality_scores':0,'real_future_candidate_inference_not_claimed':True,'test_labels_read':False})
    paths=[Path(__file__),bankplan,controlplan]
    paths+=save('nonflag_residual_EmpiricalBayes64_native_stage_20261007.py','nonflag_residual_SparseGram64_native_stage_20261007.py',[
      ("'empirical_bayes_centered_Gram64'","'own_centered_Gram64_cyclic_coordinate_descent'",1),
      ("native['model'].alpha==info['parameters']['alpha']","native['model'].alpha_==info['parameters']['alpha']",1),
      ('nonflag_cpu_empirical_bayes64_','nonflag_cpu_sparse_gram64_',1)])
    paths+=save('run_nonflag_residual_EmpiricalBayes64_hook3_after_bank_v2_20261007.py','run_nonflag_residual_SparseGram64_hook3_after_bank_20261007.py')
    paths+=save('verify_nonflag_residual_EmpiricalBayes37_transform_v3_20261007.py','verify_nonflag_residual_SparseGram37_transform_20261007.py',[
      ('nonflag_EmpiricalBayes40_plan_20261007.json',controlplan.name,1),
      ('passed_actual37_full5635800_nonflag_residual_Ridge_independent_CDF_and111_cold_controls','passed_actual37_full5635800_nonflag_SparseGram64_independent_CDF_and111_cold_controls',1),
      ("'official40_comparisons_and_round130_candidate_QA41_not_claimed'","'official_scores_and_actual_future_candidate_not_claimed'",1),
      ("'full_cases':49,'cold_controls':147","'full_cases':37,'cold_controls':111",1)])
    proof=A/'nonflag_SparseGram64_actual_native_and_transform_source_preparation_20261007.json'
    create(proof,{'status':'compiled_actual_sparse_native3_and_full37_cold111_routes','input_sha256':{str(p):sha(p) for p in paths},
      'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'new_native_fits':0,'new_quality_scores':0})
    driver=A/'run_nonflag_SparseGram64_actual_native_and_full37_controls_20261007.py';assert driver.is_file()
    row=start('nonflag_SparseGram64_actual_native3_full37_controls',driver.name,[],{**read(proof)['input_sha256'],str(proof):sha(proof),str(driver):sha(driver)})
    create(A/'nonflag_SparseGram64_actual_controls_hidden_launch_20261007.json',{'status':'started_actual_sparse_controls_after_native_bank','identity':row})

if __name__=='__main__':main()
