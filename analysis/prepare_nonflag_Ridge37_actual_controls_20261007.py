"""Launch the already-fitted residual bank's full numerical controls only."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]; A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create

def main():
    text=(A/'verify_nonflag_residual_HGB37_transform_20261007.py').read_text(encoding='utf8')
    for old,new in [('nonflag_residual_HGB10_training','nonflag_residual_Ridge_native_bank10'),
        ('nonflag_residual_HGB_bank10_20261007','nonflag_residual_Ridge_bank10_20261007'),
        ('nonflag_residual_HGB37_transform_preflight','nonflag_residual_Ridge37_transform_preflight'),
        ('nonflag_residual_HGB10_plan_20261007','nonflag_Ridge40_plan_20261007'),
        ('passed_actual10_nonflag_residual_HGB','passed_actual10_nonflag_residual_Ridge'),
        ('passed_actual37_full5635800_nonflag_residual_HGB','passed_actual37_full5635800_nonflag_residual_Ridge'),
        ('remove_nonflag_HGB','remove_nonflag_Ridge'),("plan['configurations']","plan['single_native_heads']"),
        ("plan['later_weights']","plan['weights']"),('official40_comparisons_and_round120_candidate_QA31','official40_comparisons_and_round121_candidate_QA32')]:text=text.replace(old,new)
    p=A/'verify_nonflag_residual_Ridge37_transform_20261007.py'; assert not p.exists(); compile(text,str(p),'exec')
    with p.open('x',encoding='utf8',newline='\n') as f:f.write(text)
    pins={str(q):sha(q) for q in [Path(__file__),p,A/'nonflag_Ridge40_plan_20261007.json',A/'nonflag_residual_Ridge_bank10_20261007/verification.json',A/'nonflag_residual_HGB_CDF_transform_20261007.py']}
    from handoff_ready_goss_full_execution_20261006 import start_service
    row=start_service('nonflag_residual_Ridge37_transform_preflight',p.name,[],pins)
    create(A/'nonflag_Ridge37_actual_hidden_launch_20261007.json',{'status':'started_actual37_full_and111_cold_controls','row':row,'input_sha256':pins,'new_quality_scores':0})
    print({'worker':row['owned_worker_pid']},flush=True)
if __name__=='__main__':main()
