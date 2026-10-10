from pathlib import Path
import sys,json,subprocess
A=Path(__file__).resolve().parent;ROOT=A.parent
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def main():
    p=A/'prepare_ReusedNN158Stage_core_v62_20261009.py';s=p.read_text(encoding='utf8')
    archive=A/'ReusedNN158_initial_preflight_failure_v1_20261010';archive.mkdir()
    (archive/p.name).write_bytes(p.read_bytes())
    for old,new in [("'80':'22'","'80':'23'"),("'155':'157'","'155':'158'"),("'66':'68'","'66':'69'"),("'438':'440'","'438':'441'")]:s=s.replace(old,new)
    p.write_text(s,encoding='utf8',newline='\n')
    for name in ('ReusedNN158Stage_complete_native_predictor_preparation_v58_20261009.json','ReusedNN158Stage_core_preparation_v62_20261009.json'):
        path=A/name;value=read(path);(archive/name).write_bytes(path.read_bytes())
        value['input_sha256'][str(p)]=sha(p);path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    path=A/'verify_ReusedNN158Quality23_prospective_routes_v2_20261010.py'
    result=subprocess.run([sys.executable,'-B','-X','utf8',str(path)],capture_output=True,text=True,encoding='utf8',creationflags=subprocess.CREATE_NO_WINDOW)
    print(result.stdout);print(result.stderr);assert result.returncode==0
    create(A/'ReusedNN158_route_constant_recovery_v2_20261010.json',{'status':'passed_derived158_route_counts_after_preserved_unadmitted_preflight_failure',
        'input_sha256':{str(p):sha(p),str(path):sha(path)},'new_quality_scores':0})
if __name__=='__main__':main()
