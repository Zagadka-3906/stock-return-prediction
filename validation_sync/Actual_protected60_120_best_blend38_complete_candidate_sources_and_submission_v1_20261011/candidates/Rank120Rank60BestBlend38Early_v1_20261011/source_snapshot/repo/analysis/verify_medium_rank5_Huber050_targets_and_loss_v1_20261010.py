"""CPU-only independent target quantiles, clipping, loss/gradient, and microbatch tail controls."""
from pathlib import Path
import sys,itertools
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A),str(A.parent)]
from run_dependency_queue_v3_20261006 import read,sha,create
def main():
    import numpy as np,torch
    import neural_BF16_medium2048_recent252rank5huber050_seed09_e64_native_v1_20261009 as native
    torch.set_num_threads(2);rng=np.random.default_rng(20261010);records=[]
    for n in (1,2,7,31,97):
        y=rng.uniform(0.,1.,n).astype('f8');y[0]=0.
        if n>1:y[-1]=1.
        transformed,bounds=native.prepare_return_targets(y,native.CONFIG)
        ordered=sorted(map(float,y))
        def independent_quantile(q):
            index=(n-1)*q;left=int(index);right=min(left+1,n-1);fraction=index-left
            # Explicit linear interpolation in real arithmetic; verify actual rounded target bits.
            return ordered[left]+fraction*(ordered[right]-ordered[left])
        lower,upper=[independent_quantile(q) for q in (.005,.995)]
        assert np.allclose(bounds,[lower,upper],atol=1e-15,rtol=1e-14)
        manual=np.array([min(max(float(v),lower),upper)*1. for v in y],dtype='f4')
        assert np.array_equal(manual.view('u4'),transformed.view('u4'))
        for micro in (1,3,8,32):
            pred=rng.normal(0,1,n).astype('f4');x=torch.tensor(pred,requires_grad=True);target=torch.tensor(transformed)
            full=torch.nn.functional.huber_loss(x,target,delta=.5);full.backward();gradient=x.grad.numpy().copy()
            difference=pred.astype('f8')-transformed.astype('f8');absolute=np.abs(difference)
            expected=np.mean(np.where(absolute<=.5,.5*difference**2,.5*(absolute-.25)))
            derivative=(np.clip(difference,-.5,.5)/n).astype('f4')
            assert np.isclose(full.item(),expected,atol=2e-7,rtol=2e-6) and np.allclose(gradient,derivative,atol=2e-8,rtol=2e-6)
            chunk=torch.tensor(pred,requires_grad=True);total=0.
            for left in range(0,n,micro):
                part=chunk[left:left+micro];loss=torch.nn.functional.huber_loss(part,target[left:left+micro],delta=.5)*(len(part)/n)
                loss.backward();total+=loss.item()
            assert np.isclose(total,full.item(),atol=2e-7,rtol=2e-6) and np.allclose(chunk.grad.numpy(),gradient,atol=2e-8,rtol=2e-6)
            records.append({'rows':n,'micro':micro,'bounds':bounds,'target_float32_bits_exact':True,'independent_loss_gradient_micro_tail_passed':True})
    for bad in (np.array([]),np.array([np.nan]),np.array([np.inf]),np.array([-.001]),np.array([1.001])):
        try:native.prepare_return_targets(bad,native.CONFIG)
        except AssertionError:pass
        else:raise AssertionError('Invalid target accepted')
    plan=A/'rank5_model_target_plan_v1_20261010.json'
    for p,d in read(plan)['input_sha256'].items():assert sha(p)==d,p
    create(A/'Rank5Huber050_independent_targets_loss_gradient_controls_v1_20261010.json',{'status':'passed20_CPU_independent_quantile_target_bits_loss_gradient_micro_tail_and_invalid_target_rejections','records':records,'input_sha256':{str(p):sha(p) for p in [Path(__file__),Path(native.__file__),plan]},'GPU_used':False,'actual_native_fits':0,'new_quality_scores':0,'own_durable_restart_and_six_full_models_not_yet_claimed':True,'test_labels_read':False})
    print('PASS20 direct-return target, independent loss, gradient and micro-tail controls',flush=True)
if __name__=='__main__':main()
