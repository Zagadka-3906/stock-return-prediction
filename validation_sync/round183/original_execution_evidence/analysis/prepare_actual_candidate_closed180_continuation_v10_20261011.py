"""Admit omitted180 candidate routing and fresh downstream dependency helpers; preserve every failed source."""
from pathlib import Path
import sys,importlib,subprocess,psutil,time,ast
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service,retire

DESCRIPTORS=[
 (181,'prepare_StockRankWide32Embedding181_complete48_pipeline_v2_20261010','actual_stock_rank_wide32_embedding48_after180_normalization_queue_v6_20261010','StockRankWide32Embedding48_selected_native14_v6_20261010','StockRankWide32Embedding181_complete48_family_v7_20261010'),
 (182,'prepare_StockRank20Complement182_complete63_pipeline_v1_20261010','actual_stock_rank20_embedding63_after181_normalization_queue_v5_20261010','StockRank20Embedding63_selected_native14_v5_20261010','StockRank20Embedding182_complete63_family_v6_20261010'),
 (183,'prepare_StockRank20Tiny183_complete85_pipeline_v1_20261010','actual_stock_rank20_embedding85_after182_normalization_queue_v5_20261010','StockRank20Embedding85_selected_native14_v5_20261010','StockRank20Embedding183_complete85_family_v6_20261010'),
 (184,'prepare_StockPairRankEmbedding184_complete48_pipeline_v4_20261010','actual_stock_pairrank_embedding48_after183_normalization_queue_v8_20261010','StockPairRankEmbedding48_selected_native14_v8_20261010','StockPairRankEmbedding184_complete48_family_v9_20261010'),
 (185,'prepare_StockTopPairEmbedding185_complete48_pipeline_v1_20261010','actual_stock_toppair_embedding48_after184_normalization_queue_v8_20261010','StockTopPairEmbedding48_selected_native14_v8_20261010','StockTopPairEmbedding185_complete48_family_v9_20261010'),
 (186,'prepare_StockRank20Seed10Embedding186_complete48_pipeline_v2_20261011','actual_stock_rank20seed10_embedding48_after185_normalization_queue_v1_20261011','StockRank20Seed10Embedding48_selected_native14_v1_20261011','StockRank20Seed10Embedding186_complete48_family_v2_20261011'),
 (187,'prepare_Rank20TwoSeed187_complete88_pipeline_v2_20261011','actual_rank20_two_seed88_after186_normalization_v1_20261011','actual_rank20_two_seed88_selected_native14_v1_20261011','Rank20TwoSeed187_complete88_family_v2_20261011'),
 (188,'prepare_StockRank20LongEmbedding188_complete48_pipeline_v1_20261011','actual_stock_rank20long_embedding48_after187_normalization_queue_v1_20261011','StockRank20LongEmbedding48_selected_native14_v1_20261011','StockRank20LongEmbedding188_complete48_family_v1_20261011')]

def save(name,text):
    p=A/name;assert not p.exists(),p;compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p

def main():
    assert allowed()
    proofs=[A/'Dual25_verified_recovery_exact_dependency_aliases_v7_20261010.json',A/'actual_PairRank_native42_admission_routes_v8_20261010.json',A/'PairTop184185_complete_reference_routes_v9_20261010.json',A/'long188_actual_scientific_queue_routes_v2_20261011.json']
    previous_aliases={}
    for proof in proofs:previous_aliases.update(read(proof)['service_aliases'])
    failure=A/'service_owned_workflows_20261006/StockRank20Embedding180_selected_candidate_preparation_v1_20261010/service_execution.json'
    assert read(failure)['status']=='failed' and read(failure)['failure']=='AssertionError: StockRank20Embedding48_selected_native14_v5_20261010'
    failedfamily=previous_aliases['StockRank20Embedding180_complete48_family_v6_20261010']
    assert read(A/'service_owned_workflows_20261006'/failedfamily/'service_execution.json')['status']=='failed'
    from stock_rank20_embedding180_storage_v2_20261010 import OUTPUTS,empty
    for logical,physical in OUTPUTS.items():assert logical.resolve()==physical.resolve();empty(logical)
    oldcache=Path('E:/赛题五_本机临时/第180轮_20261010/selected_feature_cache_runtime_v5')
    assert sorted(p.name for p in oldcache.iterdir())==['frozen_before_actual_selected_dispatch.json']
    assert not (A/'StockRank20Embedding180_selected_release_v1_20261010/inference_ready.json').exists()
    source=A/'run_StockRank20Embedding180_selected_candidate_feature_cache_v6_20261010.py'
    text=source.read_text(encoding='utf8');old='selected_feature_cache_runtime_v5';assert text.count(old)==1
    fresh=save('run_StockRank20Embedding180_selected_candidate_feature_cache_actual_gate_v10_20261011.py',text.replace(old,'selected_feature_cache_runtime_actual_gate_v10_20261011'))
    aliases={};wrappers={};tasks=[];pinsources=[Path(__file__),*proofs,failure,source,fresh,
        A/'route_actual_candidate_closed_and180_continuation_v10_20261011.py',A/'resume180_after_actual_native_candidate_gate_v10_20261011.py']
    factories=['prepare_StockRank20Embedding180_complete48_pipeline_v1_20261010']
    idle=[];terminal=[]
    def alias(original,actual):
        aliases[original]=actual
        for name in previous_aliases:
            if name==original or name.startswith(original[:-len('_20261010')]+'_' if original.endswith('_20261010') else original+'_'):aliases[name]=actual
        if original in previous_aliases:aliases[previous_aliases[original]]=actual
    def wrapper(driver):
        if driver not in wrappers:
            target=Path(driver).stem+'_actual_candidate_closed_routes_v10.py'
            p=save(target,"from pathlib import Path\nimport sys\nA=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]\nfrom route_actual_candidate_closed_and180_continuation_v10_20261011 import execute\nif __name__=='__main__':execute("+repr(driver)+")\n")
            wrappers[driver]=target;pinsources.extend([A/driver,p])
        return wrappers[driver]
    rootfamily='StockRank20Embedding180_complete48_family_v6_20261010'
    rootactual='StockRank20Embedding180_complete48_family_actual_resume_v10_20261011'
    alias(rootfamily,rootactual)
    for name in ['StockRank20Embedding180_selected_candidate_preparation_v1_20261010','StockRank20Embedding180_selected_candidate_sealing_v1_20261010','StockRank20Embedding180_round180_full_registration_v1_20261010']:
        alias(name,name.replace('_v1_20261010','_actual_native_gate_v10_20261011'))
    for driver in ['prepare_StockRank20Embedding180_selected_candidate_v5_20261010.py',fresh.name,'seal_StockRank20Embedding180_selected_candidate_v2_20261010.py','run_StockRank20Embedding180_full_registration_v5_20261010.py']:wrapper(driver)
    wrappers[source.name]=wrapper(fresh.name)
    tasks.append((rootactual,'resume180_after_actual_native_candidate_gate_v10_20261011.py'))
    spy=ROOT/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'
    for number,factoryname,norm,qual,family in DESCRIPTORS:
        factory=importlib.import_module(factoryname);factories.append(factoryname)
        for driver in [*factory.EXTRAS[:2],*factory.EXTRAS[3:9]]:wrapper(driver)
        for canonical,driver in [(norm,factory.EXTRAS[0]),(qual,factory.EXTRAS[1]),(family,factory.EXTRAS[5])]:
            actual=canonical+'_actual_candidate_closed_v10_20261011'
            alias(canonical,actual);tasks.append((actual,wrapper(driver)))
            current=previous_aliases.get(canonical,canonical)
            folder=A/'service_owned_workflows_20261006'/current
            launch=read(folder/'native_launch.json');execution=read(folder/'service_execution.json') if (folder/'service_execution.json').exists() else {}
            if owned(launch):
                assert not psutil.Process(launch['owned_worker_pid']).children(),current
                for attempt in range(10):
                    assert allowed()
                    stack=subprocess.run([str(spy),'dump','--pid',str(launch['owned_worker_pid'])],capture_output=True,text=True,encoding='utf8',check=True).stdout
                    if '(idle)' in stack and Path(driver).stem+'.py:' in stack:break
                    # Wrapped188 dispatcher actually waits in the original family source.
                    if '(idle)' in stack and number==188 and canonical==family and 'run_StockRank20LongEmbedding188_complete_family_v1_20261011.py:' in stack:break
                    time.sleep(2)
                else:raise RuntimeError('Dependent helper not verified idle: '+current)
                idle.append({'canonical':canonical,'actual_previous':current,'identity':launch,'stack':stack})
            else:
                assert execution.get('status')=='failed',(current,execution)
                terminal.append({'canonical':canonical,'actual_previous':current,'identity':launch,'execution':execution})
            # These dependent helpers have not reached any scientific output directory.
            if canonical==norm or canonical==qual:
                module=importlib.import_module(Path(driver).stem);assert not module.OUT.exists(),(current,module.OUT)
            else:
                storage=importlib.import_module(Path(factory.EXTRAS[2]).stem)
                assert all(not p.exists() and not q.exists() for p,q in storage.OUTPUTS.items()),number
    aliases.update(read(proofs[-1])['dependency_aliases'])
    # Replace every canonical/previous exact child driver in newly dispatched workers; preserve old science sources.
    proof=A/'actual_candidate_closed180_continuation_routes_v10_20261011.json'
    input_hashes={str(p):sha(p) for p in dict.fromkeys(pinsources)}
    create(proof,{'status':'verified_omitted180_candidate_closed_callback_and_exact_downstream_unstarted_continuations',
        'input_sha256':input_hashes,'service_aliases':aliases,'driver_wrappers':wrappers,'source_factories':factories,
        'original_failed180_candidate':read(failure),'terminal_failed_dependency_helpers':terminal,'verified_idle_helpers':idle,
        'remaining_tasks':tasks,'original180_six_output_junctions_verified_empty':True,
        'original_failed_feature_cache_freeze_preserved':str(oldcache/'frozen_before_actual_selected_dispatch.json'),
        'new_model_fits':0,'new_quality_scores':0,'actual_future_X_read':False,'test_labels_read':False,
        'scientific_workers_stopped_or_restarted':0})
    # Only exact childless idle dependency dispatchers are retired; scientific workers remain running.
    for record in idle:
        assert allowed();retire(record['identity'],'Verified idle downstream dependency helper rerouted after omitted180 candidate closed callback; no scientific output had begun')
    for name,driver in tasks:
        assert allowed();row=start_service(name,driver,[],{str(A/driver):sha(A/driver),str(proof):sha(proof)})
        create(A/(name+'_activation.json'),row)
    print({'actual180_and_downstream_dependency_continuations_started':len(tasks),'idle_dependency_helpers_retired':len(idle),
        'failed_services_preserved':len(terminal)+2,'scientific_workers_stopped_or_restarted':0},flush=True)

if __name__=='__main__':main()
