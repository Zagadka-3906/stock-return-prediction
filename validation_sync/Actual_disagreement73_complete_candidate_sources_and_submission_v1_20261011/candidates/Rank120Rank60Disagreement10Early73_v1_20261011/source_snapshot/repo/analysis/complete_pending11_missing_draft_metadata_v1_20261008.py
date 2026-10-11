"""Supply absent declared draft metadata, then retry unchanged controls11; no source rewrites."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def main():
    import recover_pending137to141_registration_contracts_v11_20261008 as helper
    helper.initialize();outputs=[]
    for old,new in helper.MAPPING.items():
        source=A/(old+'.json');target=A/(new+'.json')
        if 'receiver_drafts' in old and source.is_file() and not target.exists():
            create(target,{'status':'prepared_declared_receiver11_drafts_before_prospective_checks',
                'original_source':str(source),'original_sha256':sha(source),'input_sha256':{str(Path(__file__)):sha(__file__)},
                'fresh11_sources':read(A/'pending137to141_receiver_preparation_v11_20261008.json')['input_sha256'],
                'actual_prospective_checks_required':True,'new_official_scores':0,'test_labels_read':False})
            outputs.append(target)
    create(A/'pending137to141_control11_missing_draft_recovery_v1_20261008.json',{
        'status':'supplied_missing_draft_inputs_without_modifying_frozen11_sources',
        'previous_failure':'137 source_paths future subset rejected absent receiver_drafts11 before any prospective output',
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),*outputs]},'new_official_scores':0,'training_workers_stopped':0})
    helper.controls()
if __name__=='__main__':main()
