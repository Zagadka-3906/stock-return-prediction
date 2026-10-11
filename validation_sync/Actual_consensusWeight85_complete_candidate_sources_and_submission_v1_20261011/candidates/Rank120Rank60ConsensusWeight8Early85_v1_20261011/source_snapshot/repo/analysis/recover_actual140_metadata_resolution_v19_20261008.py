"""Close already scored140 using the real immutable version2 metadata, without recreating eight sources."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def install():
    import prepare_SpectralGram52_round140_sources_v18_20261008 as g
    original=g.source_paths
    missing=A/'SpectralGram140_truthful_metadata_receiver_preparation_v18_20261008.json'
    actual=A/'SpectralGram140_truthful_metadata_receiver_preparation_v2_20261008.json'
    assert not missing.exists() and actual.is_file()
    proof=A/'SpectralGram140_actual_metadata_resolution_v19_20261008.json'
    def paths():
        return list(dict.fromkeys([*(actual if p==missing else p for p in original()),Path(__file__),proof,A/'run_SpectralGram52_round140_full_registration_v19_20261008.py']))
    def existing():
        p=A/'SpectralGram52_round140_source_preparation_v18_20261008.json';prep=read(p)
        assert prep['status']=='passed_actual52_sealed_candidate_and_admitted_full140_QA51_sources'
        for f,d in prep['input_sha256'].items():assert sha(f)==d,f
        generated=g.generate(prep['actual_comparison_parent_round'])
        import hashlib
        for n,s in generated.items():assert sha(A/n)==hashlib.sha256(s.encode()).hexdigest(),n
    existing()
    if not proof.exists():
        create(proof,{'status':'resolved_only_missing_administrative_metadata_to_actual_immutable_version2_before_registration',
            'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'expected_nonexistent_path':str(missing),'actual_path':str(actual),
            'actual_metadata_sha256':sha(actual),'existing_eight_sources_unchanged_and_reverified':True,
            'old_failure_preserved':True,'new_quality_scores':0,'new_inference':0,'test_labels_read':False})
    g.source_paths=paths;g.main=existing
    assert all(p.is_file() for p in paths())
    return g
def main():
    old=A/'run_SpectralGram52_round140_full_registration_v18_20261008.py';target=A/'run_SpectralGram52_round140_full_registration_v19_20261008.py'
    s=old.read_text(encoding='utf-8-sig').replace('actual_registration_v18_20261008','actual_registration_v19_20261008').replace('full_registration_v18_file_IO_20261008','full_registration_v19_file_IO_20261008')
    needle='    import psutil\n';assert s.count(needle)==1
    s=s.replace(needle,'    from recover_actual140_metadata_resolution_v19_20261008 import install as recover\n    recover()\n'+needle)
    compile(s,str(target),'exec')
    with target.open('x',encoding='utf8',newline='') as stream:stream.write(s)
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    row=start('SpectralGram52_round140_full_registration_v19_20261008',target.name,[],{str(p):sha(p) for p in [Path(__file__),old,target]})
    create(A/'actual140_metadata_recovery_hidden_launch_v19_20261008.json',row)
    print(row['owned_worker_pid'],flush=True)
if __name__=='__main__':main()
