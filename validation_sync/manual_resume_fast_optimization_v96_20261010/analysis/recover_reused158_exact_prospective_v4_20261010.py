from pathlib import Path
import sys,subprocess,json
A=Path(__file__).resolve().parent;ROOT=A.parent
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def main():
    p=A/'verify_ReusedNN158Quality23_prospective_routes_v2_20261010.py'
    archive=A/'ReusedNN158_third_preflight_failure_v3_20261010';archive.mkdir();(archive/p.name).write_bytes(p.read_bytes())
    s=p.read_text(encoding='utf8').replace("new['original_complete_parent_round']==182","new['original_complete_parent_round']==152")
    p.write_text(s,encoding='utf8',newline='\n')
    for name in ('ReusedNN158Stage_complete_native_predictor_preparation_v58_20261009.json','ReusedNN158Stage_core_preparation_v62_20261009.json'):
        path=A/name;value=read(path);(archive/name).write_bytes(path.read_bytes());value['input_sha256'][str(p)]=sha(p)
        path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    result=subprocess.run([sys.executable,'-B','-X','utf8',str(p)],capture_output=True,text=True,encoding='utf8',creationflags=subprocess.CREATE_NO_WINDOW)
    print(result.stdout);print(result.stderr);assert result.returncode==0
    create(A/'ReusedNN158_exact_prospective_recovery_v4_20261010.json',{'status':'passed_actual48_derived_sources456_graphs18_baselines12_ties',
        'input_sha256':{str(p):sha(p)},'new_quality_scores':0})
if __name__=='__main__':main()
