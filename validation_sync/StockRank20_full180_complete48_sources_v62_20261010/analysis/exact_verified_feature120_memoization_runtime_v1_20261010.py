"""Scoped byte-keyed feature memoization; first input executes native AND independent oracle."""
from contextlib import contextmanager
from pathlib import Path
from collections import OrderedDict
import hashlib,json,time

@contextmanager
def installed(max_bytes=1024**3):
    import numpy as np
    import daily_cross_sectional_feature_encoder120_v1_20261010 as encoder
    assert not getattr(encoder,'_exact_verified_cache_active',False)
    native,oracle=encoder.encode,encoder.pandas_oracle
    source=Path(encoder.__file__);source_sha=hashlib.file_digest(source.open('rb'),'sha256').hexdigest()
    entries=OrderedDict();retained=0
    stats={'status':'active_scoped_verified_feature120_cache','native_calls':0,'oracle_calls':0,'hits':0,'misses':0,'actual_independent_full_pairs':[],'max_retained_bytes':0,'configured_max_bytes':max_bytes,'no_labels_or_model_predictions_in_key':True}
    def key_for(raw,dates,names):
        a=np.asarray(raw);d=np.asarray(dates)
        if a.dtype!=np.float32 or a.ndim!=2 or a.shape[1]!=63 or d.ndim!=1 or len(d)!=len(a) or d.dtype.kind not in 'iu':return None
        encoder.names(names)
        assert hashlib.file_digest(source.open('rb'),'sha256').hexdigest()==source_sha
        h=hashlib.sha256(json.dumps([source_sha,list(names),a.shape,a.dtype.str,d.shape,d.dtype.str],ensure_ascii=False,separators=(',',':')).encode('utf8'))
        h.update(memoryview(np.ascontiguousarray(a)).cast('B'));h.update(memoryview(np.ascontiguousarray(d)).cast('B'))
        return h.hexdigest()
    def value_for(raw,dates,names,backend):
        nonlocal retained
        stats[backend+'_calls']+=1
        key=key_for(raw,dates,names)
        if key is None:return (native if backend=='native' else oracle)(raw,dates,names)
        if key in entries:
            stats['hits']+=1;entries.move_to_end(key)
            # Caller mutation cannot corrupt a verified cache entry.
            return entries[key].copy()
        stats['misses']+=1;started=time.perf_counter()
        primary=native(raw,dates,names);independent=oracle(raw,dates,names)
        assert primary.dtype==independent.dtype==np.float32 and primary.shape==independent.shape==(len(raw),120)
        assert np.array_equal(primary.view('u4'),independent.view('u4'))
        row={'rows':len(raw),'input_sha256':key,'numeric_output_sha256':hashlib.sha256(memoryview(np.ascontiguousarray(primary)).cast('B')).hexdigest(),'native_and_independent_Pandas_bits_exact':True,'uncached_pair_seconds':time.perf_counter()-started}
        stats['actual_independent_full_pairs'].append(row)
        del independent
        if primary.nbytes<=max_bytes:
            while entries and retained+primary.nbytes>max_bytes:
                _,old=entries.popitem(last=False);retained-=old.nbytes
            primary.setflags(write=False);entries[key]=primary;retained+=primary.nbytes
            stats['max_retained_bytes']=max(stats['max_retained_bytes'],retained)
            return primary.copy()
        return primary
    def encode(raw,dates,raw_names):return value_for(raw,dates,raw_names,'native')
    def pandas_oracle(raw,dates,raw_names):return value_for(raw,dates,raw_names,'oracle')
    encoder._exact_verified_cache_active=True;encoder.encode=encode;encoder.pandas_oracle=pandas_oracle
    try:yield stats
    finally:
        assert encoder.encode is encode and encoder.pandas_oracle is pandas_oracle
        encoder.encode=native;encoder.pandas_oracle=oracle;encoder._exact_verified_cache_active=False
        entries.clear();stats['status']='closed_original_encoder_and_oracle_restored';stats['retained_bytes_after_close']=0
