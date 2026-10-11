"""Preserve existing controls and derive fresh own TopWeighted state/restart/decoder controls."""
from pathlib import Path
import sys,time
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import create,sha,read
def main():
    originals=['verify_neural_BF16_medium2048_huber010_seed09_restart_v1_20261009.py','verify_BF16Huber010161_independent_small_CPU_v1_20261009.py','verify_BF16Huber010161_full5_independent_GPU_v1_20261009.py','BF16Huber010161_complete_parent_native_stage_v1_20261009.py','verify_BF16Huber010161_native42_calendar_v1_20261009.py']
    def route(s):return s.replace('huber010','topweightedhuber010').replace('Huber010161','TopWeightedHuber010165')
    outputs={route(n):route((A/n).read_text(encoding='utf8')) for n in originals}
    source=A/'build_reused_neural_frontier_v9_20261010.py'
    outputs['build_reused_topweighted_neural_frontier_v10_20261010.py']=route(source.read_text(encoding='utf8'))
    for name,text in outputs.items():assert not (A/name).exists();compile(text,str(A/name),'exec')
    for name,text in outputs.items():(A/name).write_text(text,encoding='utf8',newline='\n')
    create(A/'TopWeightedHuber_own_bank_controls_source_admission_v1_20261010.json',{'status':'passed_compiled_own_restart_small_CPU_full5_native42_and_dedicated_frontier_sources','input_sha256':{str(p):sha(p) for p in [Path(__file__),*[A/n for n in originals],source,*[A/n for n in outputs],A/'TopWeightedHuber_independent_loss_micro_gradient_controls_v1_20261010.json',A/'neural_BF16_medium2048_topweightedhuber010_seed09_e64_frontier_v1_20261010.json']},'actual_annual_fits':0,'GPU_controls_and_own_model_training_pending':True,'new_quality_scores':0,'test_labels_read':False})
    print('Compiled own TopWeighted restart/full5/native42 routes and dedicated future round builder',flush=True)
if __name__=='__main__':main()
