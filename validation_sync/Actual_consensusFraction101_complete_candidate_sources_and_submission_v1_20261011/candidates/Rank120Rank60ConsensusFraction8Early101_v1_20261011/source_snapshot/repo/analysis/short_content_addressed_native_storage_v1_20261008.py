"""Only shorten copied native basenames; all native SHA/model keys and prediction arithmetic remain exact."""
from pathlib import Path
from contextlib import contextmanager
import hashlib
@contextmanager
def installed():
    import predict_cohort_calibrated_scheme_20261006 as original
    source=Path(original.__file__);text=source.read_text(encoding='utf8')
    old="            name = hashlib.sha256(key.encode('utf-8')).hexdigest()[:16] + '__' + source.name"
    new="            name = 'native_' + info['sha256'] + source.suffix"
    assert text.count(old)==1
    patched=text.replace(old,new);ns={'__file__':str(source),'__name__':'exact_cohort_predict_with_short_content_addressed_native_basenames'}
    exec(compile(patched,str(source),'exec'),ns);saved=original.predict;original.predict=ns['predict']
    try:yield {'original_source_sha256':hashlib.sha256(text.encode()).hexdigest(),'patched_source_sha256':hashlib.sha256(patched.encode()).hexdigest(),'only_native_filename_assignment_changed':True}
    finally:original.predict=saved
