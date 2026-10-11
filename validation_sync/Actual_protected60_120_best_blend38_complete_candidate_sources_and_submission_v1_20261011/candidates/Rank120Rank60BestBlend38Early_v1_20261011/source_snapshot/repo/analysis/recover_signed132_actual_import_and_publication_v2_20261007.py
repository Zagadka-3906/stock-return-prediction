"""Preserve published V1; finalize signed132 executor imports before any scoring."""
from pathlib import Path
import ast,sys,time,psutil
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start

def fresh(old,new,changes):
    source=A/old;target=A/new;text=source.read_text(encoding='utf8')
    for before,after,count in changes:
        assert text.count(before)==count,(old,before,text.count(before))
        text=text.replace(before,after)
    compile(text,str(target),'exec');assert not target.exists()
    target.write_text(text,encoding='utf8',newline='\n');return source,target

def main():
    proof=A/'signed132_actual_import_and_publication_recovery_v2_20261007.json'
    admitted='run_nonflag_ReverseBayes40_admitted_comparison_v2_20261007.py'
    admission='verify_nonflag_ReverseBayes40_round132_sources_v2_20261007.py'
    publisher='publish_nonflag_ReverseBayes40_evidence_v2_20261007.py'
    queue='queue_nonflag_ReverseBayes132_after_actual131_v2_20261007.py'
    paths=[Path(__file__)]
    paths+=fresh('run_nonflag_ReverseBayes40_admitted_comparison_v1_20261007.py',admitted,[
      ('from run_nonflag_ReverseBayes40_official_comparison_v4_20261007 import main as actual','from run_nonflag_ReverseBayes40_official_comparison_v1_20261007 import main as actual',1),
      ("'nonflag_ReverseBayes40_round132_source_admission_v1'","'nonflag_ReverseBayes40_round132_source_admission_v2'",1)])
    extra="    sources += [A/"+repr(admitted)+",A/"+repr(admission)+",A/"+repr(publisher)+",A/"+repr(queue)+",A/"+repr(Path(__file__).name)+",A/"+repr(proof.name)+"]\n"
    paths+=fresh('verify_nonflag_ReverseBayes40_round132_sources_v1_20261007.py',admission,[('    for p in sources:\n',extra+'    for p in sources:\n',1)])
    paths+=fresh('publish_nonflag_ReverseBayes40_evidence_v1_20261007.py',publisher,[
      ('    if phase==\'scores\':\n',extra+"    if phase=='scores':\n",1),
      ("'actual_cold_prefix_cases':147","'actual_cold_prefix_cases':111",1),
      ('非涨停残差Ridge：两组样本数归一化L2及等权集成，各12幅度，加三个合格锚点及消融，共40项。实际10年度成熟模型；49全量、147冷前缀和3历史原生核对。完整130候选须冻结、重放及QA43。仅main。','第132轮反向经验贝叶斯残差融合：标量先验、对角先验及等权均值，各12权重，加三个合格锚点及消融，共40项。复用实际10年度成熟模型；37全量、111冷前缀和3历史原生核对。完整132候选须冻结、重放及QA43。仅main。',1),
      ('上传非涨停残差Ridge的','上传反向经验贝叶斯残差融合的',1)])
    paths+=fresh('queue_nonflag_ReverseBayes132_after_actual131_20261007.py',queue,[
      ("'nonflag_ReverseBayes40_round132_source_admission_v1'","'nonflag_ReverseBayes40_round132_source_admission_v2'",1),
      ('verify_nonflag_ReverseBayes40_round132_sources_v1_20261007.py',admission,1),
      ('run_nonflag_ReverseBayes40_admitted_comparison_v1_20261007.py',admitted,1),
      ('publish_nonflag_ReverseBayes40_evidence_v1_20261007.py',publisher,2),
      ('    for p,d in pins.items():assert sha(p)==d,p',"    recovery=A/"+repr(proof.name)+"\n    pins.update({**read(recovery)['input_sha256'],str(recovery):sha(recovery)})\n    for p,d in pins.items():assert sha(p)==d,p",1)])
    # Resolve every signed-family executor import. Compile alone cannot prove this.
    controls=[]
    for path in sorted(A.glob('*ReverseBayes*20261007.py')):
        if path.name=='run_nonflag_ReverseBayes40_admitted_comparison_v1_20261007.py':continue
        for node in ast.walk(ast.parse(path.read_text(encoding='utf8'))):
            modules=[node.module] if isinstance(node,ast.ImportFrom) else [n.name for n in node.names] if isinstance(node,ast.Import) else []
            for module in modules:
                if module and 'ReverseBayes' in module:
                    resolved=A/(module+'.py');assert resolved.is_file(),(path,module)
                    controls.append({'source':str(path),'module':module,'resolved_sha256':sha(resolved)})
    assert not (A/'nonflag_ReverseBayes40_official_comparison_v1_20261007').exists()
    assert not any((A/'service_owned_workflows_20261006'/n).exists() for n in ['nonflag_ReverseBayes40_round132_source_admission_v1','nonflag_ReverseBayes40_round132_source_admission_v2','nonflag_ReverseBayes40_official_comparison_v1'])
    folder=A/'service_owned_workflows_20261006/nonflag_ReverseBayes40_actual132_after131_dependency_queue'
    row=read(folder/'native_launch.json');assert owned(row);identities=[]
    for key,birth in [('owned_worker_pid','owned_worker_creation_time'),('pid','owned_parent_creation_time')]:
        proc=psutil.Process(row[key]);assert abs(proc.create_time()-row[birth])<.03
        assert 'run_service_owned_windows_workflow_20261006.py' in ' '.join(proc.cmdline())
        identities.append({'pid':proc.pid,'creation_time':proc.create_time(),'cmdline':proc.cmdline()})
    for item in identities:psutil.Process(item['pid']).terminate()
    for item in identities:
        try:psutil.Process(item['pid']).wait(timeout=10)
        except psutil.NoSuchProcess:pass
    assert not owned(row)
    paths += [*folder.glob('*.json'),*folder.glob('*.log')]
    create(proof,{'status':'resolved_actual_signed132_executor_import_and_publication_metadata_before_any_scores',
      'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in paths},
      'actual_signed_executor_import_controls':controls,'original_published_V1_bytes_retained':True,
      'administratively_superseded_waiting_controller':identities,'only_waiting_controller_terminated':True,
      'actual_native_controls_unchanged':True,'numerical_scorer_original_V1_bytes_unchanged':True,
      'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})
    pins={**read(proof)['input_sha256'],str(proof):sha(proof)}
    launch=start('nonflag_ReverseBayes40_actual132_after131_dependency_queue_v2',queue,[],pins)
    create(A/'signed132_recovered_actual_hidden_queue_launch_v2_20261007.json',{'status':'started_corrected_waiting_signed132_queue_with_fixed2312_cutoff','identity':launch,'input_sha256':pins})
    print('PASS signed132 actual import correction; original scorer and published V1 retained',flush=True)

if __name__=='__main__':main()
