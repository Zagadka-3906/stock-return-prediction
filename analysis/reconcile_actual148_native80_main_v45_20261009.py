"""Verify the completed301-blob push after an administrative receipt-name collision; never republish or rerun80 controls."""
from pathlib import Path
import hashlib,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
def main():
    folder=Path('E:/赛题五_本机临时/actual148_native80_main_v44_20261009')
    receipt=read(folder/'receipt.json');frozen=read(folder/'frozen_before_main_publication.json')
    failed=A/'service_owned_workflows_20261006/actual148_native80_main_publication_v44_20261009'
    assert not owned(read(failed/'native_launch.json')) and 'FileExistsError' in read(failed/'service_execution.json')['failure']
    assert receipt['status']=='pushed_and_remote_head_verified' and receipt['branch']=='main'
    import publish_classifier_consensus_workflows_20261006 as helpers
    from verified_TLS_Git_retry_runtime_v2_20261008 import installed
    expected={r['published_path']:r['raw_sha256'] for r in frozen['files'].values()}
    with installed(A/'actual148_native80_receipt_reconciliation_file_IO_v45_20261009'):
        helpers.verify_main(receipt['commit'])
        assert helpers.blob_hashes(receipt['commit'],expected)==expected
        prefix='validation_sync/actual148_native80_v44_20261009'
        attributes={prefix+'/.gitattributes':hashlib.sha256(b'* -text\n').hexdigest()}
        assert helpers.blob_hashes(receipt['commit'],attributes)==attributes
    pointer=A/'actual_AdaptiveJointCrossHuber80_native_calendar_location_v3_20261008.json'
    proof=Path(read(pointer)['output'])/'verification.json';assert sha(proof)==read(pointer)['verification_sha256']
    v=read(proof);assert (v['actual_historical_cases'],v['actual_calendar_cases'],v['actual_cold_cases'])==(60,20,80)
    value={**receipt,'reconciled_at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'status':'pushed_and_remote_head_verified','actual_data_blobs_reverified':len(expected),
        'administrative_old44_receipt_collision_after_successful_push_preserved':True,
        'original43_44_failure_statuses_not_rewritten':True,'new_pushes_by_reconciliation':0,'new_native_replays':0,
        'actual_native_controls':[60,20,80],'source_existing_E_receipt_sha256':sha(folder/'receipt.json'),
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),folder/'receipt.json',folder/'frozen_before_main_publication.json',proof,failed/'service_execution.json']}}
    create(A/'actual148_native80_main_reconciled_receipt_v45_20261009.json',value)
    print(value,flush=True)
if __name__=='__main__':main()
