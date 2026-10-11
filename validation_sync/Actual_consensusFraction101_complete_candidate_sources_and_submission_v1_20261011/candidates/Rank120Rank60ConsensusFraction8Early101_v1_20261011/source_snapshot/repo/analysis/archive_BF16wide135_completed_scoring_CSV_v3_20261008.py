"""After scoring exits, move only its generated scratch CSV to verified E archive; retain every score/input."""
from pathlib import Path
import ctypes,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned


def closed(name):
    folder=A/'service_owned_workflows_20261006'/name
    while not (folder/'native_launch.json').exists() or owned(read(folder/'native_launch.json')):time.sleep(.5)
    assert read(folder/'service_execution.json')['status']=='passed',name


def main():
    out=A/'BF16wide135_completed_scoring_CSV_archive_v3_20261008.json';assert not out.exists()
    archive=Path('E:/赛题五_本机临时/第135轮_20261008/completed_scoring_CSV')
    assert archive.resolve().is_relative_to(Path('E:/赛题五_本机临时/第135轮_20261008').resolve())
    archive.mkdir()
    move=ctypes.WinDLL('kernel32',use_last_error=True).MoveFileExW
    move.argtypes=(ctypes.c_wchar_p,ctypes.c_wchar_p,ctypes.c_uint32);move.restype=ctypes.c_int
    records=[]
    for phase,service in (('comparison','BF16wide40_official_comparison_v3_20261008'),
                          ('selected','BF16wide40_selected_candidate_preparation_v3_20261008')):
        closed(service)
        source=A/'BF16wide135_D_scoring_v2_20261008'/phase/'scoring_validation_only/submission.csv'
        target=archive/(phase+'_submission.csv')
        assert source.resolve()==(ROOT/'analysis/BF16wide135_D_scoring_v2_20261008'/phase/'scoring_validation_only/submission.csv')
        assert source.resolve().is_relative_to(ROOT/'analysis/BF16wide135_D_scoring_v2_20261008')
        assert target.parent.resolve()==archive.resolve() and target.resolve().drive.upper()=='E:'
        if not source.exists():
            assert phase=='selected' and not read(A/'BF16wide40_selected_release_v1_20261008/inference_ready.json')['new_inference_claimed']
            records.append({'phase':phase,'no_scratch_CSV_created_for_exact_anchor_reuse':True});continue
        assert source.is_file() and not target.exists();digest=sha(source);size=source.stat().st_size
        assert move(str(source),str(target),2),'MoveFileExW COPY_ALLOWED failed: '+str(ctypes.get_last_error())
        assert not source.exists() and sha(target)==digest
        record={'phase':phase,'original_path':str(source),'archived_path':str(target),'raw_sha256':digest,'bytes':size,
            'scoring_service_closed_passed_before_move':True,'source_and_destination_absolute_boundaries_checked':True,
            'all_scientific_input_and_official_capsule_paths_untouched':True}
        records.append(record)
        create(A/f'BF16wide135_{phase}_scoring_CSV_archive_v3_20261008.json',record)
        print(f'Completed {phase} scoring scratch CSV archived byte-identically on E; inputs and capsules retained.',flush=True)
    create(out,{'status':'archived_only_closed_generated_scoring_CSVs_byte_identically_on_E','records':records,
        'input_sha256':{str(Path(__file__)):sha(__file__)},'new_quality_scores':0,'test_labels_read':False})


if __name__=='__main__':main()
