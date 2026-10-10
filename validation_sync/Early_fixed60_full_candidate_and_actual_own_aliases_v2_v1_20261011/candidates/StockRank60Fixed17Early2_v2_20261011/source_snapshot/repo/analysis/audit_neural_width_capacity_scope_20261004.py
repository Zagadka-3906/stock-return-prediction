"""Validate actual resource controls without inferring full-fold or physical maxima."""
from pathlib import Path
from datetime import datetime
import hashlib
import json

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'analysis/neural_width_capacity_20261004'
def read(path):return json.loads(path.read_text(encoding='utf-8-sig'))
def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda:stream.read(8*1024*1024),b''):h.update(block)
    return h.hexdigest()

def main():
    import numpy as np
    import polars as pl
    import train_diverse_backbones_20261003 as engine
    protocol=read(OUT/'protocol.json');proof=read(OUT/'verification.json')
    assert proof['status']=='passed' and proof['protocol_sha256']==sha(OUT/'protocol.json')
    for p,digest in protocol['input_sha256'].items():assert sha(Path(p))==digest,p
    assert sha(OUT/'mature_training_batch.npz')==protocol['actual_batch_sha256']
    assert sha(OUT/'mature_training_batch_keys.parquet')==protocol['training_keys_sha256']
    cfg=protocol['common_configuration'];cutoff=engine.fold_cutoff(2020)
    assert cutoff==protocol['cutoff_exclusive'] and cfg['epochs']==1
    features=engine.feature_names();assert features==protocol['features'] and len(features)==63
    batch=engine.training_frame(pl.scan_parquet(engine.FEATURE_FILE),cutoff,cfg).select(engine.KEYS+features+['y_rank']).sort('trade_date','ts_code').head(protocol['actual_batch_rows']).collect()
    assert int(batch['trade_date'].max())<cutoff
    assert batch.select(engine.KEYS).equals(pl.read_parquet(OUT/'mature_training_batch_keys.parquet'))
    with np.load(OUT/'mature_training_batch.npz') as saved:
        assert np.array_equal(saved['x'],engine.to_matrix(batch,features),equal_nan=True)
        assert np.array_equal(saved['y'],batch['y_rank'].to_numpy(),equal_nan=True)
        assert engine.array_hash(saved['x'])==protocol['training_matrix_sha256']
        assert engine.array_hash(saved['y'])==protocol['training_target_sha256']
    controls=[]
    for control in proof['execution_controls']:
        width=control['width'];assert read(OUT/f'width{width}_result.json')==control
        if control['status']=='not_launched_for_current_memory_budget':continue
        child_path=OUT/f'width{width}_child_result.json'
        if control['child_result']:
            assert sha(child_path)==control['child_result_sha256'] and read(child_path)==control['child_result']
            c=control['child_result'];assert c['configuration']=={**cfg,'hidden':[width,width//2,width//4]}
            assert c['actual_batch_sha256']==protocol['actual_batch_sha256'] and c['training_rows']==protocol['actual_batch_rows']
            if c['status']=='one_step_completed':
                assert len(c['training_losses'])==1 and np.isfinite(c['training_losses']).all()
                assert c['all_returned_weights_finite']
            elif c['status']=='actual_CUDA_out_of_memory':assert c['exception_type']=='OutOfMemoryError'
            else:raise AssertionError(c['status'])
        for name,key in (('stdout.log','stdout_sha256'),('stderr.log','stderr_sha256'),('samples.jsonl','resource_samples_sha256')):
            assert sha(OUT/f'width{width}_{name}' if name=='samples.jsonl' else OUT/f'width{width}.{name}')==control[key]
        samples=[json.loads(line) for line in (OUT/f'width{width}_samples.jsonl').read_text(encoding='utf-8').splitlines()]
        assert len(samples)==control['samples'] and min(s['available_host_bytes'] for s in samples)==control['minimum_available_host_bytes_sampled']
        c=control['child_result'] or {}
        controls.append({'width':width,'training_step_status':c.get('status'),'total_fit_seconds':c.get('total_fit_seconds'),
            'own_tensor_allocation_peak_GiB':c.get('peak_own_tensor_allocated_bytes',0)/2**30,
            'own_allocator_reservation_peak_GiB':c.get('peak_own_allocator_reserved_bytes',0)/2**30,
            'reported_device_total_GiB':c.get('device_total_bytes',0)/2**30,
            'reservation_peak_exceeds_reported_device_total':c.get('peak_own_allocator_reserved_bytes',0)>c.get('device_total_bytes',0),
            'minimum_available_host_GiB_sampled':control['minimum_available_host_bytes_sampled']/2**30})
    output={'status':'passed','at_local':datetime.now().isoformat(timespec='seconds'),
        'actual_original_mature_training_batch_reconstructed_exactly':True,'controls':controls,
        'actual_CUDA_OOM_widths':proof['actual_CUDA_OOM_widths'],
        'own_allocated_andreserved_statistics_are_not_dedicated_resident_VRAM_measurements':True,
        'no_unmeasured_Windows_shared_memory_mechanism_asserted':True,
        'full_training_resident_inputs_andmulti_step_optimizer_lifetime_unmeasured':True,
        'no_hardware_maximum_orfull_fold_feasibility_inferred':True,
        'new_quality_scores':0,'test_labels_read':False,
        'input_sha256':{str(p.resolve()):sha(p) for p in (Path(__file__),OUT/'protocol.json',OUT/'verification.json')}}
    with (ROOT/'analysis/neural_width_capacity_scope_audit_20261004.json').open('x',encoding='utf-8') as stream:json.dump(output,stream,ensure_ascii=False,indent=2)
    print(json.dumps({'status':'passed','controls':controls,'actual_CUDA_OOM_widths':proof['actual_CUDA_OOM_widths']},ensure_ascii=False))

if __name__=='__main__':main()
