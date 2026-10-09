"""Provide short immutable SHA-verified aliases for parent sources; execute the original nested codecs unchanged."""
from pathlib import Path
from copy import deepcopy
from contextlib import contextmanager
import os,hashlib,shutil
def sha(path):
    with Path(path).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
@contextmanager
def installed(ns,directory):
    directory=Path(directory);assert not directory.exists();directory.mkdir(parents=True)
    original=ns.cohort_saved_models;aliases={};controls=[]
    for key,info in original.items():
        source=Path(info['path']).resolve();assert sha(source)==info['sha256'];target=directory/('native_'+info['sha256']+source.suffix)
        if not target.exists():
            if source.drive.upper()==target.drive.upper():os.link(source,target)
            else:shutil.copyfile(source,target)
        assert sha(target)==info['sha256'];aliases[key]={**deepcopy(info),'path':str(target)}
        controls.append({'key':key,'original_source':str(source),'short_alias':str(target),'sha256':info['sha256'],'source_samefile':os.path.samefile(source,target),'alias_basename_length':len(target.name)})
    ns.cohort_saved_models=aliases
    try:yield {'status':'passed_actual_parent_native_source_aliases_short_before_nested_copy','controls':controls,'only_native_source_filename_aliases_changed':True,'all_original_nested_codec_source_bytes_and_prediction_arithmetic_unchanged':True}
    finally:
        for row in controls:assert sha(row['original_source'])==sha(row['short_alias'])==row['sha256']
        ns.cohort_saved_models=original
