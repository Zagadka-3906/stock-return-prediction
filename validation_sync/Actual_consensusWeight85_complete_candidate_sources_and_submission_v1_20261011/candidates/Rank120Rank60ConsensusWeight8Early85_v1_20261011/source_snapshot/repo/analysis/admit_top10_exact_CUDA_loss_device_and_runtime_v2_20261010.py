"""Bind new BCE positive weight to CUDA and verify its real expression/gradient on CPU."""
from pathlib import Path
import sys,ast,copy,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service,retire
def save(name,text):
    p=A/name;assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p
def main():
    assert allowed()
    source=A/'stock_top10_embedding_small512_BF16_native_v1_20261010.py';text=source.read_text(encoding='utf8')
    assert text.count("dtype=torch.float32,device=device")==1
    native=save('stock_top10_embedding_small512_BF16_native_v2_20261010.py',text.replace("dtype=torch.float32,device=device","dtype=torch.float32,device='cuda'"))
    import numpy as np,torch
    module=importlib.import_module(native.stem)
    tree=ast.parse(native.read_text(encoding='utf8'));fit=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='fit_arrays')
    nodes=[n for n in ast.walk(fit) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='loss' for t in n.targets)];assert len(nodes)==1
    expression=compile(ast.fix_missing_locations(ast.Expression(nodes[0].value)),str(native)+'::actual_BCE_loss_expression','eval')
    pred=torch.tensor([-20.,-1.,0.,1.,20.],dtype=torch.float32,requires_grad=True);yt=torch.tensor([0.,1.,0.,1.,1.],dtype=torch.float32);part=np.arange(5);index=np.arange(13)
    original_tensor=torch.tensor;calls=[]
    def CPU_tensor(*args,**kwargs):
        assert kwargs['device']=='cuda' and kwargs['dtype']==torch.float32 and args[0]==9.;calls.append('exact_CUDA_weight_binding_verified_CPU_adapter_only');kwargs['device']='cpu';return original_tensor(*args,**kwargs)
    torch.tensor=CPU_tensor
    try:loss=eval(expression,{'torch':torch,'pred':pred,'yt':yt,'part':part,'index':index,'cfg':module.CONFIG})
    finally:torch.tensor=original_tensor
    loss.backward();values=pred.detach().numpy().astype(np.float64);labels=yt.numpy();weights=np.where(labels==1.,9.,1.)
    expected=np.mean(np.where(labels==1.,9.*np.logaddexp(0.,-values),np.logaddexp(0.,values)))*5./13.
    expected_gradient=(1./(1.+np.exp(-values))-labels)*weights/13.
    assert calls==['exact_CUDA_weight_binding_verified_CPU_adapter_only'] and np.isclose(loss.item(),expected,rtol=1e-6,atol=1e-7) and np.allclose(pred.grad.numpy(),expected_gradient,rtol=1e-5,atol=1e-7)
    replacements={'stock_top10_embedding_small512_BF16_native_v1_20261010':'stock_top10_embedding_small512_BF16_native_v2_20261010','stock_top10_embedding_after_complete_qualified_parent_native_stage_v1_20261010':'stock_top10_embedding_after_complete_qualified_parent_native_stage_v2_20261010','stock_top10_embedding_stage_and_after174_fast17_sources_admission_v1_20261010':'stock_top10_embedding_stage_and_after174_fast17_sources_admission_v2_20261010'}
    templates=[('verify_stock_top10_embedding_small512_restart_priority174_v1_20261010.py','verify_stock_top10_embedding_small512_restart_priority174_v2_20261010.py'),('train_stock_top10_embedding_small512_BF16_bank6_checkpoint_yield_priority174_v1_20261010.py','train_stock_top10_embedding_small512_BF16_bank6_checkpoint_yield_priority174_v2_20261010.py'),('verify_stock_top10_embedding_small512_small_CPU_v1_20261010.py','verify_stock_top10_embedding_small512_small_CPU_v2_20261010.py'),('verify_stock_top10_embedding_small512_full5_independent_v1_20261010.py','verify_stock_top10_embedding_small512_full5_independent_v2_20261010.py'),('stock_top10_embedding_after_complete_qualified_parent_native_stage_v1_20261010.py','stock_top10_embedding_after_complete_qualified_parent_native_stage_v2_20261010.py'),('verify_stock_top10_embedding_six_state_native42_v1_20261010.py','verify_stock_top10_embedding_six_state_native42_v2_20261010.py')]
    inputs=[Path(__file__),source];outputs=[native]
    for old,new in templates:
        p=A/old;inputs.append(p);text=p.read_text(encoding='utf8')
        for left,right in replacements.items():text=text.replace(left,right)
        outputs.append(save(new,text))
    own=copy.deepcopy(read(A/'stock_top10_embedding_own_sources_admission_v1_20261010.json'));own['status']='passed_actual_BCE_loss_expression_CPU_adapter_CUDA_weight_binding_and_gradient_real_target_conversion_GPU_phases_pending';own['actual_loss_CPU_controls']={'expected_loss':float(expected),'actual_loss':float(loss.item()),'actual_gradient_matches_analytic':True,'does_not_claim_GPU_training':True}
    own['input_sha256']={str(p):sha(p) for p in [*inputs,*outputs]}
    create(A/'stock_top10_embedding_own_sources_admission_v2_20261010.json',own)
    stage=copy.deepcopy(read(A/'stock_top10_embedding_stage_and_after174_fast17_sources_admission_v1_20261010.json'));stage['status']='compiled_actual_v2_CUDA_weight_bound_native42_and_original_predeclared17_cases_unchanged';stage['input_sha256']={str(p):sha(p) for p in [*inputs,*outputs,A/'stock_top10_embedding_own_sources_admission_v2_20261010.json']}
    create(A/'stock_top10_embedding_stage_and_after174_fast17_sources_admission_v2_20261010.json',stage)
    queue=A/'run_stock_top10_embedding_own_training_queue_v1_20261010.py';text=queue.read_text(encoding='utf8').replace('stock_top10_embedding_own_sources_admission_v1_20261010.json','stock_top10_embedding_own_sources_admission_v2_20261010.json')
    for old,new in templates[:4]:text=text.replace(old,new)
    own_queue=save('run_stock_top10_embedding_own_training_queue_v2_20261010.py',text)
    queue=A/'run_stock_top10_embedding_native42_and_after174_fast17_queue_v1_20261010.py';text=queue.read_text(encoding='utf8').replace('actual_stock_top10_embedding_own_training_queue_v1_20261010','actual_stock_top10_embedding_own_training_queue_v2_20261010').replace('stock_top10_embedding_stage_and_after174_fast17_sources_admission_v1_20261010.json','stock_top10_embedding_stage_and_after174_fast17_sources_admission_v2_20261010.json').replace('verify_stock_top10_embedding_six_state_native42_v1_20261010.py','verify_stock_top10_embedding_six_state_native42_v2_20261010.py')
    native_queue=save('run_stock_top10_embedding_native42_and_after174_fast17_queue_v2_20261010.py',text)
    assert not (A/'service_owned_workflows_20261006/actual_stock_top10_embedding_small512_restart_v1_20261010').exists()
    for name in ('actual_stock_top10_embedding_own_training_queue_v1_20261010','actual_stock_top10_embedding_native42_and_after174_fast17_queue_v1_20261010'):
        retire(read(A/'service_owned_workflows_20261006'/name/'native_launch.json'),'Verified childless before174 seal; actual v2 binds BCE pos_weight CUDA explicitly and passes analytic CPU loss/gradient. No GPU control/training/scoring output was created.')
    rows=[]
    for name,driver in [('actual_stock_top10_embedding_own_training_queue_v2_20261010',own_queue),('actual_stock_top10_embedding_native42_and_after174_fast17_queue_v2_20261010',native_queue)]:
        row=start_service(name,driver.name,[],{str(driver):sha(driver)});create(A/(name+'_activation.json'),row);rows.append(row)
    create(A/'stock_top10_actual_CUDA_weight_loss_CPU_and_runtime_admission_v2_20261010.json',{'status':'passed_actual_loss_expression_CUDA_weight_binding_CPU_value_and_gradient_fresh_v2_GPU_routes_queued_before_any_fit','actual_services':rows,'input_sha256':{str(p):sha(p) for p in [Path(__file__),native,own_queue,native_queue,A/'stock_top10_embedding_own_sources_admission_v2_20261010.json',A/'stock_top10_embedding_stage_and_after174_fast17_sources_admission_v2_20261010.json']},'new_fits':0,'new_quality_scores':0,'test_labels_read':False})
    print({'actual_BCE_loss_and_gradient_CPU_passed':True,'actual_classifier_queues_version':2,'GPU_phases_pending':True},flush=True)
if __name__=='__main__':main()
