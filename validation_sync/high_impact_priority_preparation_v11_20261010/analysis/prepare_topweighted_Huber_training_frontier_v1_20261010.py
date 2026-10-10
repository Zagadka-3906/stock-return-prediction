"""Prepare a new training loss; no annual fit or quality gain is claimed here."""
from pathlib import Path
import sys,time
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected162_candidate_sources_v2_20261010 import change
def main():
    names=['neural_BF16_medium2048_huber010_seed09_e64_native_v1_20261009.py','neural_BF16_medium2048_huber010_seed09_independent_forward_v1_20261009.py','train_neural_BF16_medium2048_huber010_seed09_e64_bank6_v1_20261009.py']
    outputs={}
    for name in names:
        text=(A/name).read_text(encoding='utf8');text=text.replace('huber010','topweightedhuber010')
        if 'native_' in name:
            text=change(text,"'loss': 'Huber', 'huber_delta': .1,","'loss': 'TopWeightedHuber', 'huber_delta': .1, 'top_rank_threshold': .9, 'top_sample_weight': 5.,")
            text=change(text,"assert cfg['loss']=='Huber' and cfg['huber_delta']==.1","assert cfg['loss']=='TopWeightedHuber' and cfg['huber_delta']==.1 and cfg['top_rank_threshold']==.9 and cfg['top_sample_weight']==5.")
            text=change(text,"            optimizer.zero_grad(set_to_none=True)","            optimizer.zero_grad(set_to_none=True)\n            batch_weights=1.+(cfg['top_sample_weight']-1.)*(yt[index]>=cfg['top_rank_threshold']-.5).float()\n            denominator=batch_weights.sum()")
            text=change(text,"loss = torch.nn.functional.huber_loss(pred.float(), yt[part], delta=cfg['huber_delta']) * (len(part) / len(index))","loss = weighted_huber_loss(pred.float(),yt[part],denominator)")
            text+='''

def weighted_huber_loss(pred,target,denominator=None):
    import torch
    pred=pred.float();target=target.float()
    weights=1.+4.*(target>=.4).float()
    total=weights.sum() if denominator is None else denominator
    assert total>0
    return (torch.nn.functional.huber_loss(pred,target,delta=.1,reduction='none')*weights).sum()/total
'''
        outputs[name.replace('huber010','topweightedhuber010')]=text
    for name,text in outputs.items():assert not (A/name).exists();compile(text,str(A/name),'exec')
    for name,text in outputs.items():(A/name).write_text(text,encoding='utf8',newline='\n')
    import neural_BF16_medium2048_topweightedhuber010_seed09_e64_native_v1_20261009 as native
    inputpaths=[Path(__file__),ROOT/'后续选模标准.md',*(A/n for n in names),*(A/n for n in outputs),Path('E:/赛题五_本机临时/Huber010_high_impact65_screen_v1_20261010/verification.json')]
    create(A/'neural_BF16_medium2048_topweightedhuber010_seed09_e64_frontier_v1_20261010.json',{'status':'frozen_new_training_only_TopWeightedHuber_loss_before_any_fit_or_score','configuration':native.CONFIG,'input_sha256':{str(p):sha(p) for p in inputpaths},'only_new_training_change':'Huber loss weights mature training top rank samples5 versus other samples1, normalized by full actual minibatch weight sum','reason':'Existing broad Huber can raise Top annual excess but loses to turnover; test a genuinely different fitted signal rather than only mixing weights','planned_own_mature_saved_states':list(range(2020,2026)),'own_loss_formula_micro_tail_gradients_restart_and_full5_native42_required_before_scoring':True,'GPU_fitting_not_started':True,'actual_native_fits':0,'new_quality_scores':0,'test_labels_read':False,'at_local':time.strftime('%Y-%m-%dT%H:%M:%S')})
    print('Compiled new TopWeightedHuber recipe; annual fitting and actual quality pending',flush=True)
if __name__=='__main__':main()
