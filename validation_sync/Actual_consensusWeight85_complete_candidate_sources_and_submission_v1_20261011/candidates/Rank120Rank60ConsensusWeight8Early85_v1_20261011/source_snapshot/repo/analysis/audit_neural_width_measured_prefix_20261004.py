"""Actual completed model internals andtraining cost; snapshot live resource samples."""
from pathlib import Path
import hashlib
import json
import gc
import time
ROOT=Path(__file__).resolve().parents[1]
BANK=ROOT/'analysis/neural_width_bank_20261004'
BASE=ROOT/'analysis/neural_regularization_bank_20261003/rank512_drop000_e32'
OBS=ROOT/'analysis/neural_width_resource_observations_20261004'

def read(path):return json.loads(path.read_text(encoding='utf-8-sig'))
def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda:stream.read(8*1024*1024),b''):h.update(block)
    return h.hexdigest()
def create(path,value):
    with path.open('x',encoding='utf-8') as stream:json.dump(value,stream,ensure_ascii=False,indent=2)

def main():
    infos=sorted(BANK.glob('*/info_202[0-4].json'));count=len(infos)
    assert 0<count<=20
    OUT=ROOT/f'analysis/neural_width_measured_prefix{count}_20261004';OUT.mkdir(exist_ok=True)
    assert not (OUT/'verification.json').exists()
    import numpy as np
    import joblib
    import torch
    sources=[Path(__file__),BANK/'protocol.json',OBS/'protocol.json',ROOT/'后续选模标准.md']
    records=[]
    for path in infos:
        info=read(path);name=info['model'];year=info['year'];cfg=info['configuration']
        reference=BASE/f'info_{year}.json';control=read(reference)
        assert info['status']=='passed' and info['training_meta']==control['training_meta']
        assert all(cfg[k]==control['configuration'][k] for k in cfg if k!='hidden')
        assert info['training_meta']['last_label_end']<=info['training_meta']['cutoff_exclusive']<year*10000+101
        model=path.with_name(f'model_{year}.joblib');baseline=BASE/f'model_{year}.joblib'
        assert sha(model)==info['model_sha256'] and sha(baseline)==control['model_sha256']
        actual=joblib.load(model);old=joblib.load(baseline)
        assert actual['config']==cfg and np.array_equal(actual['mean'],old['mean']) and np.array_equal(actual['scale'],old['scale'])
        assert actual['target_bounds']==old['target_bounds'] and actual['target_scale']==old['target_scale']
        assert all(t.device.type=='cpu' and torch.isfinite(t).all() for t in actual['state'].values())
        parameters=sum(t.numel() for t in actual['state'].values());weight_bytes=sum(t.numel()*t.element_size() for t in actual['state'].values())
        raw=path.with_name(f'raw_{year}.parquet');prefix=BANK/f'prefix_control_{name}_{year}.json'
        assert sha(raw)==info['prediction_sha256'] and info['model_reload_bit_identical']
        assert read(prefix)['status']=='passed'
        sources.extend([path,reference,model,baseline,raw,prefix])
        records.append({'model':name,'width':cfg['hidden'][0],'year':year,'mature_training_rows':info['training_meta']['rows'],
            'actual_past_normalizer_andtarget_bounds_bit_identical_to_control':True,
            'saved_weights_all_finite_CPU_tensors':True,'parameter_count':parameters,'state_tensor_bytes':weight_bytes,
            'pure_fitter_seconds':info['fit_seconds'],'artifact_elapsed_seconds':info['elapsed_seconds'],
            'same_year_512_control_historical_fitter_seconds':control['fit_seconds'],
            'background_workload_not_matched_between_width_fits_or_historical_control':True,
            'actual_saved_raw_andprefix_source_hashes_verified':True})
        del actual,old;gc.collect()
    assert not torch.cuda.is_initialized(),'Inspector must not perform GPU work'
    data=(OBS/'samples.jsonl').read_bytes();lines=data.splitlines(keepends=True)
    ignored_partial_tail=bool(lines and not lines[-1].endswith(b'\n'))
    if ignored_partial_tail:lines.pop()
    assert lines
    snapshot=OUT/'resource_samples_prefix_snapshot.jsonl'
    with snapshot.open('xb') as stream:stream.write(b''.join(lines))
    rows=[json.loads(line) for line in lines];assert rows[0]['actual_completed_annual_fits']==0
    assert max(r['actual_completed_annual_fits'] for r in rows)>=count
    gpu=[r['gpu_last_sample'] for r in rows if (r.get('gpu_last_sample') or {}).get('query_status')=='passed']
    assert gpu
    sources=list(dict.fromkeys(sources));inputs={str(p.resolve()):sha(p) for p in sources}
    create(OUT/'verification.json',{'status':'passed','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'completed_models_inspected':count,'completed_width_year_records':records,
        'source_hashes_currently_verified':True,'all_actual_past_normalizers_andtargets_match_corresponding_frozen_512_controls':True,
        'source_training_data_keys_andlabels_identical_to_corresponding_control':True,
        'inspection_performed_no_GPU_work':True,'resource_snapshot_sha256':sha(snapshot),
        'resource_snapshot_source_mutable_andnot_frozen_as_input':str(OBS/'samples.jsonl'),
        'ignored_incomplete_tail_line':ignored_partial_tail,
        'observed_samples':len(rows),'sampling_first_completed_fits':rows[0]['actual_completed_annual_fits'],
        'sampling_last_completed_fits':rows[-1]['actual_completed_annual_fits'],
        'snapshot_can_include_partial_following_fit':True,
        'minimum_available_host_GiB_sampled':min(r['available_ram_bytes'] for r in rows)/2**30,
        'maximum_all_gpu_memory_used_mib_sampled':max(r['memory_used_mib'] for r in gpu),
        'gpu_measurement_includes_other_background_GPU_work':True,
        'timing_scope':'Actual immutable fitter timings. Inputs andoptimizer matched; historical environment andbackground load not matched. No speedup ratio orquality ranking inferred.',
        'memory_scope':'Entire sampled prefix, including input controls, inference, other background jobs andpossible next partial fit. Not an isolated per-model tensor peak orfullfuture peak.',
        'new_quality_scores':0,'test_labels_read':False,'physical_resource_boundary_established':False,
        'all20_width_annual_fits_proven_complete':count==20,'input_sha256':inputs})
    print(json.dumps({'status':'passed','models_inspected':count,'samples':len(rows),'all_gpu_max_mib':max(r['memory_used_mib'] for r in gpu),
        'first_year_fitter_seconds':{str(r['width']):r['pure_fitter_seconds'] for r in records if r['year']==2020}}),flush=True)

if __name__=='__main__':main()
