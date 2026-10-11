from pathlib import Path
from contextlib import contextmanager
import sys,os,runpy
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from scoped_user_cleanup_package134_runtime_v1_20261011 import install
gates=install()
from run_dependency_queue_v3_20261006 import read,sha,create
gates.closed('Rank120Rank60ConsensusFraction8Early101_selected_candidate_preparation_v1_20261011')
import rank120_rank60_consensusFraction8_early101_storage_v1_20261011 as storage
candidate=A.parent/'candidates/Rank120Rank60ConsensusFraction8Early101_v1_20261011'
assert not (candidate/'manifest.json').exists()
original_context=storage.installed_transfer;events=[]
@contextmanager
def resume_transfer():
    with original_context():
        transfer=os.link
        def exact_resume(source,destination,*args,**kwargs):
            source,destination=Path(source),Path(destination)
            if destination.exists():
                assert not args and not kwargs and destination.resolve().is_relative_to(candidate.resolve()) and sha(source)==sha(destination)
                events.append(str(destination));return
            return transfer(source,destination,*args,**kwargs)
        os.link=exact_resume
        try:yield
        finally:os.link=transfer
storage.installed_transfer=resume_transfer
try:runpy.run_path(str(A/'seal_Rank120Rank60ConsensusFraction8Early101_selected_candidate_v2_20261011.py'),run_name='__main__')
finally:storage.installed_transfer=original_context
create(A/'actual_fraction101_scoped_seal134_verification_v1_20261011.json',{'status':'passed_original_sealer_all_source_manifest_checks_existing_exact_partial_links_reused','existing_same_bytes_links_reused':len(events),'manifest_sha256':sha(candidate/'manifest.json'),'no_new_inference':True,'no_new_training':True,'no_new_scoring':True,'test_labels_read':False})
print('candidate101 sealed',flush=True)
