"""Audit actual fixed-batch controls, including failed and unattempted cases."""
from pathlib import Path
from datetime import datetime
from collections import Counter
import hashlib
import json

ROOT=Path(__file__).resolve().parents[1]
BANK=ROOT/'analysis/neural_width_frontier_20261004'
OUT=ROOT/'analysis/neural_width_frontier_scope_audit_20261004.json'

def read(path):return json.loads(path.read_text(encoding='utf-8-sig'))
def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda:stream.read(8*1024*1024),b''):h.update(block)
    return h.hexdigest()

def main():
    if OUT.exists():
        for path,digest in read(OUT)['input_sha256'].items():assert sha(Path(path))==digest,path
        print('Frozen GPU frontier scope verified',flush=True);return
    import numpy as np
    import polars as pl
    import train_diverse_backbones_20261003 as engine
    sources=[Path(__file__),BANK/'protocol.json',BANK/'verification.json',
        BANK/'mature_training_batch.npz',BANK/'mature_training_batch_keys.parquet',
        ROOT/'analysis/neural_width_frontier_prepared_plan_20261004.json',
        ROOT/'analysis/neural_width_capacity_20261004/protocol.json']
    protocol=read(sources[1]);proof=read(sources[2]);plan=read(sources[5]);baseline=read(sources[6])
    assert proof['status'] in ('passed','failed') and proof['protocol_sha256']==sha(sources[1])
    for frozen in (plan,protocol):
        for path,digest in frozen['input_sha256'].items():assert sha(Path(path))==digest,path
    assert protocol['widths']==plan['widths']==[16384,32768,65536]
    assert protocol['actual_batch_rows']==32768 and protocol['common_configuration']==baseline['common_configuration']
    assert protocol['training_matrix_sha256']==baseline['training_matrix_sha256']
    assert protocol['training_target_sha256']==baseline['training_target_sha256']
    assert protocol['training_keys_sha256']==baseline['training_keys_sha256']
    assert protocol['minimum_available_host_bytes_before_launch']==20*2**30
    assert protocol['stop_owned_child_if_available_host_bytes_below']==4*2**30
    assert protocol['maximum_seconds_per_width']==180
    assert sha(sources[3])==protocol['actual_batch_sha256'] and sha(sources[4])==protocol['training_keys_sha256']
    cfg=protocol['common_configuration'];features=engine.feature_names();cutoff=engine.fold_cutoff(2020)
    assert cfg['epochs']==1 and cfg['batch_size']==32768 and features==protocol['features'] and len(features)==63
    assert cutoff==protocol['cutoff_exclusive']
    batch=engine.training_frame(pl.scan_parquet(engine.FEATURE_FILE),cutoff,cfg).select(engine.KEYS+features+['y_rank']).sort('trade_date','ts_code').head(32768).collect()
    assert int(batch['trade_date'].max())<cutoff and batch.select(engine.KEYS).equals(pl.read_parquet(sources[4]))
    with np.load(sources[3]) as saved:
        assert np.array_equal(saved['x'],engine.to_matrix(batch,features),equal_nan=True)
        assert np.array_equal(saved['y'],batch['y_rank'].to_numpy(),equal_nan=True)
        assert engine.array_hash(saved['x'])==protocol['training_matrix_sha256']
        assert engine.array_hash(saved['y'])==protocol['training_target_sha256']
    controls=proof['execution_controls'];assert controls
    assert [r['width'] for r in controls]==protocol['widths'][:len(controls)]
    records=[];successful=[];oom=[]
    for index,control in enumerate(controls):
        width=control['width'];result=BANK/f'width{width}_result.json'
        assert read(result)==control;sources.append(result)
        status=control['status']
        if status=='not_launched_for_current_memory_budget':
            assert control['available_host_bytes_at_launch']<20*2**30 and index==len(controls)-1
            records.append({'width':width,'execution_status':status,'actual_training_step_status':None,
                'available_host_GiB_at_launch':control['available_host_bytes_at_launch']/2**30,
                'actual_training_step_completed':False,'physical_exhaustion_proved':False})
            continue
        assert status in ('completed','stopped_at_declared_control_boundary','failed')
        sample=BANK/f'width{width}_samples.jsonl';stdout=BANK/f'width{width}.stdout.log';stderr=BANK/f'width{width}.stderr.log'
        for path,key in ((sample,'resource_samples_sha256'),(stdout,'stdout_sha256'),(stderr,'stderr_sha256')):
            assert sha(path)==control[key];sources.append(path)
        rows=[json.loads(line) for line in sample.read_text(encoding='utf-8').splitlines()]
        assert rows and len(rows)==control['samples']
        assert min(r['available_host_bytes'] for r in rows)==control['minimum_available_host_bytes_sampled']
        child=control['child_result'];child_path=BANK/f'width{width}_child_result.json'
        if child is not None:
            assert read(child_path)==child and sha(child_path)==control['child_result_sha256'];sources.append(child_path)
            assert child['configuration']=={**cfg,'hidden':[width,width//2,width//4]}
            assert child['training_rows']==32768 and child['actual_batch_sha256']==protocol['actual_batch_sha256']
            assert child['status'] in ('one_step_completed','actual_CUDA_out_of_memory')
            if child['status']=='one_step_completed':
                assert len(child['training_losses'])==1 and np.isfinite(child['training_losses']).all()
                assert child['all_returned_weights_finite']
            else:
                assert child['exception_type']=='OutOfMemoryError' and child['exception_message']
        else:assert control['child_result_sha256'] is None and not child_path.exists()
        if status=='completed':
            assert control['exit_code']==0 and control['stop_reason'] is None and child is not None
            (successful if child['status']=='one_step_completed' else oom).append(width)
        elif status=='stopped_at_declared_control_boundary':
            reason=control['stop_reason'];assert reason in ('sampled_host_memory_floor','declared_wall_time_budget')
            assert any(r['available_host_bytes']<4*2**30 for r in rows) if reason=='sampled_host_memory_floor' else any(r['elapsed_seconds']>180 for r in rows)
        else:assert control['stop_reason'] is None and (control['exit_code']!=0 or child is None)
        if status!='completed' or (child and child['status']=='actual_CUDA_out_of_memory'):
            assert index==len(controls)-1
        records.append({'width':width,'execution_status':status,'actual_training_step_status':child['status'] if child else None,
            'actual_training_step_completed':status=='completed' and child['status']=='one_step_completed',
            'stop_reason':control['stop_reason'],'exit_code':control['exit_code'],
            'total_fit_seconds':child['total_fit_seconds'] if child else None,
            'own_tensor_allocation_peak_GiB':child['peak_own_tensor_allocated_bytes']/2**30 if child else None,
            'own_allocator_reservation_peak_GiB':child['peak_own_allocator_reserved_bytes']/2**30 if child else None,
            'reported_device_total_GiB':child['device_total_bytes']/2**30 if child else None,
            'minimum_available_host_GiB_sampled':control['minimum_available_host_bytes_sampled']/2**30,
            'actual_background_official_worker_count_samples':dict(Counter(str(len(r['background'].get('actual_official_worker_pids',[]))) for r in rows)),
            'global_physical_exhaustion_proved':False})
    assert successful==proof['successful_one_step_widths'] and oom==proof['actual_CUDA_OOM_widths']
    assert proof['unattempted_widths']==protocol['widths'][len(controls):]
    assert proof['status']==('failed' if any(r['status']=='failed' for r in controls) else 'passed')
    output={'status':'passed','actual_resource_control_status':proof['status'],'at_local':datetime.now().isoformat(timespec='seconds'),
        'actual_original_mature_training_batch_reconstructed_exactly':True,'batch_matches_earlier_successful_control':True,
        'controls':records,'actual_CUDA_OOM_widths':oom,'unattempted_widths':proof['unattempted_widths'],
        'own_allocated_andreserved_statistics_are_not_dedicated_resident_VRAM_measurements':True,
        'guards_timeouts_andunexpected_failures_not_called_hardware_maxima':True,
        'CUDA_OOM_is_only_the_observed_layout_batch_allocator_andbackground_boundary':True,
        'full_fold_feasibility_andglobal_resource_exhaustion_not_established':True,
        'scope_audit_pass_does_not_turn_failed_orunattempted_workloads_into_successes':True,
        'new_quality_scores':0,'test_labels_read':False,
        'input_sha256':{str(p.resolve()):sha(p) for p in dict.fromkeys(sources)}}
    with OUT.open('x',encoding='utf-8') as stream:json.dump(output,stream,ensure_ascii=False,indent=2)
    print(json.dumps({'status':'passed','actual_resource_control_status':proof['status'],'controls':len(records),'actual_CUDA_OOM_widths':oom}),flush=True)

if __name__=='__main__':main()
