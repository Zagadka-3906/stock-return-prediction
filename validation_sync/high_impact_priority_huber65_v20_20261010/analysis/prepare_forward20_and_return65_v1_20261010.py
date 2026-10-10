"""Create fresh, inspectable hypotheses; do not mutate frozen Return166 sources."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent
sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import sha,create

def save(name,text):
    p=A/name
    assert not p.exists(),p
    compile(text,str(p),'exec')
    p.write_text(text,encoding='utf8',newline='\n')
    return p

def main():
    screen=(A/'run_TopWeighted_after163_high_impact65_screen_v1_20261010.py').read_text(encoding='utf8')
    screen=screen.replace('TopWeighted','Return').replace('topweightedhuber010','returnhuber050').replace('ReturnHuber010165','ReturnHuber050166')
    screen=screen.replace('actual_new_Huber65','actual_new_Return65').replace('qualified_new_Huber_cumulative163','qualified_new_Return_cumulative163').replace('new_Huber65','new_Return65')
    paths=[save('run_Return_after163_high_impact65_screen_v1_20261010.py',screen)]
    old='neural_BF16_medium2048_returnhuber050_seed09'
    new='neural_BF16_medium2048_forward20huber050_seed09'
    s=(A/(old+'_e64_native_v1_20261009.py')).read_text(encoding='utf8')
    s=s.replace('returnhuber050','forward20huber050').replace("'y_ret_1d'","'y_ret_20mean'")
    s=s.replace("'return_target_scale': 20.","'label_horizon_trading_days': 20, 'return_target_scale': 100.").replace("cfg['return_target_scale']==20.","cfg['return_target_scale']==100.")
    paths.append(save(new+'_e64_native_v1_20261009.py',s))
    s=(A/(old+'_independent_forward_v1_20261009.py')).read_text(encoding='utf8').replace('returnhuber050','forward20huber050')
    # Independent decoder divides by the saved scale; require the new frozen constant.
    paths.append(save(new+'_independent_forward_v1_20261009.py',s))
    s=(A/'verify_medium_return_Huber050_targets_and_loss_v1_20261010.py').read_text(encoding='utf8').replace('returnhuber050','forward20huber050').replace('ReturnHuber050','Forward20Huber050').replace('*20.','*100.')
    start=s.index("    plan=A/")
    end=s.index("    create(A/",start)
    s=s[:start]+"    plan=A/'forward20_model_target_plan_v1_20261010.json'\n    for p,d in read(plan)['input_sha256'].items():assert sha(p)==d,p\n"+s[end:]
    paths.append(save('verify_medium_forward20_Huber050_targets_and_loss_v1_20261010.py',s))
    create(A/'forward20_model_target_plan_v1_20261010.json',{
        'status':'frozen_new20day_mean_training_return_target_before_own_GPU_training',
        'target':'mean of provided training y_ret_1d over20 consecutive trading sessions',
        'label_end':'stock session t+20 must be strictly before the fold cutoff',
        'return_target_scale':100.,'epochs':64,'selection_metric':'official connected one-day-return S only',
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),*paths[1:],A/'forward20_mature_training_labels_v1_20261010.py',A/'forward20_mature_training_labels_actual_CPU_controls_v1_20261010.json']},
        'actual_native_fits':0,'new_quality_scores':0,'test_labels_read':False})
    print('PASS fresh Return65 screen and frozen forward20 model/decoder/CPU controls; no new training claimed',flush=True)

if __name__=='__main__':main()
