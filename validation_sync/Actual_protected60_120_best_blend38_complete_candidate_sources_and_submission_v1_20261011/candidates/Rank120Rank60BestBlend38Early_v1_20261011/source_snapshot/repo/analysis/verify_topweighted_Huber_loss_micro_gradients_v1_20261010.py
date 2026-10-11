"""CPU-only independent closed-form loss/gradient and correctly normalized microbatch tails."""
from pathlib import Path
import sys,itertools
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A),str(A.parent)]
from run_dependency_queue_v3_20261006 import read,sha,create
def main():
    import numpy as np,torch
    import neural_BF16_medium2048_topweightedhuber010_seed09_e64_native_v1_20261009 as native
    torch.set_num_threads(2);rng=np.random.default_rng(20261010);records=[]
    for n,micro in itertools.product((1,2,7,31,97),(1,3,8,32)):
        target=rng.uniform(-.5,.5,n).astype('f4');target[::5]=np.float32(.4)
        pred=rng.normal(0,.7,n).astype('f4');x=torch.tensor(pred,requires_grad=True);y=torch.tensor(target)
        value=native.weighted_huber_loss(x,y);value.backward();full_grad=x.grad.numpy().copy()
        diff=pred.astype('f8')-target.astype('f8');weights=np.where(target>=np.float32(.4),5.,1.)
        absolute=np.abs(diff);independent_loss=np.sum(weights*np.where(absolute<=.1,.5*diff**2,.1*(absolute-.05)))/weights.sum()
        independent_gradient=(weights*np.clip(diff,-.1,.1)/weights.sum()).astype('f4')
        assert np.isclose(value.item(),independent_loss,atol=2e-8,rtol=2e-6)
        assert np.allclose(full_grad,independent_gradient,atol=2e-8,rtol=2e-6)
        chunk=torch.tensor(pred,requires_grad=True);denominator=torch.tensor(weights.sum(),dtype=torch.float32);sum_loss=0.
        for start in range(0,n,micro):
            part=native.weighted_huber_loss(chunk[start:start+micro],y[start:start+micro],denominator);part.backward();sum_loss+=part.item()
        assert np.isclose(sum_loss,value.item(),atol=2e-8,rtol=2e-6)
        assert np.allclose(chunk.grad.numpy(),full_grad,atol=2e-8,rtol=2e-6)
        records.append({'rows':n,'micro':micro,'loss':value.item(),'independent_loss_gradient_and_global_denominator_micro_tail_passed':True})
    proof=A/'neural_BF16_medium2048_topweightedhuber010_seed09_e64_frontier_v1_20261010.json'
    for p,d in read(proof)['input_sha256'].items():assert sha(p)==d,p
    create(A/'TopWeightedHuber_independent_loss_micro_gradient_controls_v1_20261010.json',{'status':'passed20_actual_CPU_closed_form_loss_gradient_micro_tail_controls','records':records,'input_sha256':{str(p):sha(p) for p in [Path(__file__),Path(native.__file__),proof]},'GPU_used':False,'actual_native_fits':0,'new_quality_scores':0,'own_durable_restart_and_annual_training_full5_native42_still_required':True,'test_labels_read':False})
    print('PASS20 independent CPU loss/gradient/micro-tail controls; no annual fits or quality claims',flush=True)
if __name__=='__main__':main()
