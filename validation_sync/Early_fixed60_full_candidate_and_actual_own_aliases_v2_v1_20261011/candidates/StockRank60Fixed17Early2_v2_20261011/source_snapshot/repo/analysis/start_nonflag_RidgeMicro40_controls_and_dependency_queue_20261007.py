"""Start proven-source micro controls and actual131 dependent queue without consoles."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start

def main():
    prep=A/'nonflag_RidgeMicro40_science_route_preparation_v1_20261007.json';pros=A/'nonflag_RidgeMicro40_prospective_routes_v2_20261007.json'
    proof=read(pros);assert proof['status']=='passed_actual24_prospective_sources_and12_graph_controls' and not proof['issues']
    pins={**read(prep)['input_sha256'],**proof['input_sha256'],**{str(p):sha(p) for p in [Path(__file__),prep,pros,A/'queue_nonflag_RidgeMicro131_after_actual130_20261007.py']}}
    for p,d in pins.items():assert sha(p)==d,p
    rows={}
    rows['controls']=start('nonflag_residual_RidgeMicro37_transform_preflight','verify_nonflag_residual_RidgeMicro37_transform_20261007.py',[],pins)
    rows['queue']=start('nonflag_RidgeMicro40_actual131_after130_dependency_queue','queue_nonflag_RidgeMicro131_after_actual130_20261007.py',[],pins)
    create(A/'nonflag_RidgeMicro40_actual_controls_and_dependency_queue_hidden_launch_20261007.json',{
      'status':'started_actual37_controls_and_after130_actual131_dependency_queue_without_consoles','launches':rows,'input_sha256':pins,
      'new_quality_scores':0,'test_labels_read':False})

if __name__=='__main__':main()
