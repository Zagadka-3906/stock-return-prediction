"""Cache byte-identical validation CSV parsing while invoking the unchanged official evaluator."""
from collections import OrderedDict
from pathlib import Path
import json
from identical_official_score_cache_20261003 import digest
ROOT=Path(__file__).resolve().parents[1]
_CACHE=OrderedDict()


def run(ctx,pred,operation):
    import evaluate
    folder=Path(ctx.scoring).resolve()
    assert folder.name=='scoring_validation_only' and folder.is_relative_to(ROOT/'analysis')
    allowed={(folder/name).resolve() for name in ('测试集_X.csv','测试集_Y.csv')}
    original=evaluate.pd;events=[]
    class PandasProxy:
        def __getattr__(self,name):return getattr(original,name)
        def read_csv(self,path,*args,**kwargs):
            if not isinstance(path,(str,Path)) or Path(path).resolve() not in allowed:
                return original.read_csv(path,*args,**kwargs)
            # Hash all bytes on every read; changed labels can never reuse an old frame.
            fingerprint=digest(path)
            key=(fingerprint,json.dumps({'args':args,'kwargs':kwargs},sort_keys=True,default=str))
            hit=key in _CACHE
            if not hit:
                _CACHE[key]=original.read_csv(path,*args,**kwargs)
                while len(_CACHE)>2:_CACHE.popitem(last=False)
            _CACHE.move_to_end(key)
            events.append({'name':Path(path).name,'sha256':fingerprint,'parsed_frame_reused':hit})
            # Give the official merge a private frame; the cached input remains untouched.
            return _CACHE[key].copy(deep=True)
    evaluate.pd=PandasProxy()
    try:return operation(ctx,pred)
    finally:
        evaluate.pd=original
        ctx.last_validation_csv_parse_cache={'validation_only':True,'prediction_csv_always_read_by_official_code':True,
             'events':events,'unchanged_official_evaluator_sha256':digest(ROOT/'evaluate.py'),'adapter_sha256':digest(Path(__file__))}
