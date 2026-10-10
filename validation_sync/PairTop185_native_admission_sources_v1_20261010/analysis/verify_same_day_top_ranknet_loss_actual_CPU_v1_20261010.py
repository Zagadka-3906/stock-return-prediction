from pathlib import Path
import sys,math
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import create,sha
def main():
    import numpy as np,torch
    import same_day_top_ranknet_loss_v1_20261010 as native
    from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
    assert allowed()
    p=torch.tensor([-.7,.2,0.,.4,40.,-40.],dtype=torch.float64,requires_grad=True)
    q=torch.tensor([.3,-.4,.1,.4,-40.,40.],dtype=torch.float64,requires_grad=True)
    y=torch.tensor([-.5,.5,.1,.1,.5,-.5],dtype=torch.float64)
    z=torch.tensor([.5,-.5,.1,-.1,-.5,.5],dtype=torch.float64)
    records=[]
    for temp in (.05,.1,.2):
        result=native.loss(p,q,y,z,temp,.1,.1)
        gp,gq=torch.autograd.grad(result,(p,q))
        expected=0.;ep=[];eq=[]
        for a,b,c,d in zip(p.detach().tolist(),q.detach().tolist(),y.tolist(),z.tolist()):
            gap=c-d;sign=0. if gap==0 else math.copysign(1.,gap)
            v=-sign*(a-b)/temp
            soft=max(v,0.)+math.log1p(math.exp(-abs(v)))
            sigmoid=1./(1.+math.exp(-v)) if v>=0 else math.exp(v)/(1.+math.exp(v))
            error=a-c;h=.5*error*error if abs(error)<=.1 else .1*(abs(error)-.05)
            emphasis=10. if max(c,d)>.4 else 1.
            expected+=(emphasis*abs(gap)*soft+.1*h)/len(y)
            pairgrad=-emphasis*abs(gap)*sign*sigmoid/temp/len(y)
            ep.append(pairgrad+.1*max(-.1,min(.1,error))/len(y));eq.append(-pairgrad)
        assert math.isclose(float(result.detach()),expected,rel_tol=1e-12,abs_tol=1e-12)
        assert np.allclose(gp.numpy(),ep,rtol=1e-12,atol=1e-12)
        assert np.allclose(gq.numpy(),eq,rtol=1e-12,atol=1e-12)
        records.append({'temperature':temp,'independent_scalar_value_and_both_gradients_exact_tolerance':True})
    dates=np.array([20200102]*3+[20200103]*4+[20200106],dtype=np.int32)
    starts,sizes=native.date_groups(dates)
    assert starts.tolist()==[0,0,0,3,3,3,3,7] and sizes.tolist()==[3,3,3,4,4,4,4,1]
    rng=np.random.default_rng(20261010)
    for _ in range(100):
        partners=starts+(rng.random(len(dates))*sizes).astype(np.int64)
        assert np.array_equal(dates,dates[partners])
    rejected=0
    for bad in (dates[::-1],dates.astype(float),np.array([],dtype=np.int32)):
        try:native.date_groups(bad)
        except AssertionError:rejected+=1
    assert rejected==3
    create(A/'same_day_top_ranknet_loss_actual_CPU_controls_v1_20261010.json',{'status':'passed_independent_top_decile_weighted_scalar_loss_both_gradients_and_date_local_pairing_CPU','input_sha256':{str(x):sha(x) for x in (Path(__file__),Path(native.__file__))},'loss_controls':records,'actual_date_local_pair_draws':800,'invalid_date_inputs_rejected':3,'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})
    print('Independent pair-loss and both gradients, extreme logits, ties and800 date-local draws passed.',flush=True)
if __name__=='__main__':main()
