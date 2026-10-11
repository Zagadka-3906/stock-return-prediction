"""Actual forty saved artifacts, idempotent fit accounting and Windows lock-retry controls."""
from pathlib import Path
import ctypes,hashlib,json,os,sys,threading,time
import psutil
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
OUT=ROOT/'analysis/linear_leaf_ensemble_cost_inventory_qa_20261005'
def read(path):return json.loads(Path(path).read_text(encoding='utf-8-sig'))
def sha(path):
    with Path(path).open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()
def create(path,value):
    with Path(path).open('x',encoding='utf-8') as stream:json.dump(value,stream,ensure_ascii=False,indent=2)
def main():
    import refresh_linear_leaf_ensemble_cost_evidence_20261005 as cost
    from atomic_optimization_observer_writes_20261005 import write as atomic
    storage=read(ROOT/'analysis/linear_leaf_ensemble_storage_20261005.json');bank=Path(storage['output_directory'])
    plan=read(ROOT/'analysis/linear_leaf_ensemble_complete_search_plan_20261005.json');configs=plan['model_configurations']
    assert read(bank/'oof_audit.json')['actual_virtual_annual_outputs']==40
    OUT.mkdir(exist_ok=True)
    sources=[Path(__file__),Path(cost.__file__),ROOT/'analysis/atomic_optimization_observer_writes_20261005.py',bank/'oof_audit.json',bank/'construction_execution_scope.json',ROOT/'analysis/linear_leaf_ensemble_complete_search_plan_20261005.json']+list(bank.glob('*/info_202[0-4].json'))
    bindings={str(p):sha(p) for p in sources}
    create(OUT/'frozen_before_controls.json',{'status':'frozen_before_real_artifact_and_native_OS_controls','source_sha256':bindings,'test_labels_read':False})
    run=read(ROOT/'analysis/actual_optimization_monitor_run_v7_20261005.json')
    parent=psutil.Process(run['pid']);assert run['script'] in parent.cmdline()
    workers=[p for p in parent.children(recursive=True) if p.cmdline()[1:]==parent.cmdline()[1:]]
    assert len(workers)==1
    suspended=[]
    try:
        for p in (workers[0],parent):p.suspend();suspended.append(p)
        first=None
        for attempt in range(2):
            cost.main();ledger=read(ROOT/'analysis/optimization_fit_cost_evidence_20261004.json')
            byname={row['model']:row for row in ledger['models']}
            assert all(byname[name]['annual_artifacts']==5 and byname[name]['new_annual_fits']==0 and byname[name]['fit_seconds_total']==0. for name in configs)
            snapshot={key:ledger[key] for key in ('configurations','total_actual_new_annual_fits','native_child_annual_fits','linear_leaf_actual_annual_fits','linear_leaf_ensemble_declared_configurations','linear_leaf_ensemble_actual_virtual_annual_outputs','linear_leaf_ensemble_actual_new_annual_fits')}
            assert snapshot['configurations']==168 and snapshot['linear_leaf_actual_annual_fits']==30 and snapshot['linear_leaf_ensemble_actual_virtual_annual_outputs']==40
            assert snapshot['total_actual_new_annual_fits']==667
            if first is None:first=snapshot
            else:assert snapshot==first
        checks=[]
        for name in configs:
            for year in range(2020,2025):
                folder=bank/name;info=read(folder/f'info_{year}.json')
                assert info['new_model_fits']==0 and info['model_reload_bit_identical'] and info['actual80_day_native_composite_prefix_bit_identical']
                assert sha(folder/f'model_{year}.joblib')==info['model_sha256']
                assert sha(folder/f'raw_{year}.parquet')==info['prediction_sha256']
                checks.append({'model':name,'year':year,'actual_new_fits':0,'model_and_raw_SHA256_verified':True})
        target=OUT/'actual_lock_target.json';atomic(target,{'generation':'old'})
        kernel=ctypes.WinDLL('kernel32',use_last_error=True)
        kernel.CreateFileW.argtypes=[ctypes.c_wchar_p,ctypes.c_uint32,ctypes.c_uint32,ctypes.c_void_p,ctypes.c_uint32,ctypes.c_uint32,ctypes.c_void_p]
        kernel.CreateFileW.restype=ctypes.c_void_p;kernel.CloseHandle.argtypes=[ctypes.c_void_p]
        handle=kernel.CreateFileW(str(target),0x80000000,1,None,3,0,None)
        assert handle not in (None,ctypes.c_void_p(-1).value)
        errors=[];finished=threading.Event()
        def writer():
            try:atomic(target,{'generation':'new','payload':list(range(10000))})
            except BaseException as error:errors.append(repr(error))
            finally:finished.set()
        thread=threading.Thread(target=writer);thread.start()
        try:
            time.sleep(.3);assert not finished.is_set() and read(target)=={'generation':'old'}
        finally:assert kernel.CloseHandle(handle)
        thread.join(10);assert finished.is_set() and not errors
        assert read(target)=={'generation':'new','payload':list(range(10000))}
        assert not target.with_name(target.name+f'.observer-{os.getpid()}.tmp').exists()
        for source,digest in bindings.items():assert sha(source)==digest,source
        create(OUT/'verification.json',{'status':'passed_actual_saved_artifact_counts_idempotence_and_Windows_lock_retry','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'source_sha256':bindings,'central_counts':first,'actual_artifacts_verified':checks,'real_OS_exclusive_delete_lock_held_then_released':True,'old_JSON_remained_complete_until_atomic_replace':True,'parent_actual_annual_fits_counted_once':30,'new_ensemble_model_fits':0,'new_quality_scores':0,'test_labels_read':False})
        print(json.dumps({'status':'passed','central_counts':first,'actual_artifacts_verified':len(checks),'actual_OS_lock_retry':True},ensure_ascii=False),flush=True)
    finally:
        for p in reversed(suspended):
            if p.is_running():p.resume()
if __name__=='__main__':main()
