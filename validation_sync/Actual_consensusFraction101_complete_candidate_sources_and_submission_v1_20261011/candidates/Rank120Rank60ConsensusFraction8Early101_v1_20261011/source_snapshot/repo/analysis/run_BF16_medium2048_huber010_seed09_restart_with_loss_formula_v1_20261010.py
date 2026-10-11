from pathlib import Path
from datetime import datetime,timezone,timedelta
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def main():
    control=read(A/'current_user_runtime_control_20261010.json')
    assert control['status']=='optimization_active_after_explicit_manual_resume'
    assert datetime.now(timezone(timedelta(hours=8)))<datetime.fromisoformat(control['stop_at_local'])
    import torch
    import neural_BF16_medium2048_huber010_seed09_e64_native_v1_20261009 as native
    residual=torch.tensor([-1.,-.1001,-.1,-.0999,0.,.0999,.1,.1001,1.],dtype=torch.float64,requires_grad=True)
    observed=torch.nn.functional.huber_loss(residual,torch.zeros_like(residual),delta=.1,reduction='none')
    expected=torch.where(residual.abs()<=.1,.5*residual.square(),.1*(residual.abs()-.05))
    assert torch.equal(observed,expected)
    observed.sum().backward();expected_gradient=torch.clamp(residual.detach(),-.1,.1)
    assert torch.equal(residual.grad,expected_gradient)
    losses=[]
    for left in range(0,len(residual),4):
        part=residual.detach()[left:left+4]
        losses.append(torch.nn.functional.huber_loss(part,torch.zeros_like(part),delta=.1)*(len(part)/len(residual)))
    assert torch.allclose(torch.stack(losses).sum(),observed.detach().mean(),rtol=0,atol=1e-17)
    create(A/'BF16_medium2048_huber010_loss_formula_controls_v1_20261010.json',{'status':'passed_actual_loss_formula_gradient_tail_and_weighted_microbatch_controls','source_sha256':{str(Path(__file__)):sha(__file__),str(Path(native.__file__)):sha(native.__file__)},'actual_loss_values':observed.detach().tolist(),'actual_gradients':residual.grad.tolist(),'new_quality_scores':0,'test_labels_read':False})
    import verify_neural_BF16_medium2048_huber010_seed09_restart_v1_20261009 as restart
    restart.main()
if __name__=='__main__':main()
