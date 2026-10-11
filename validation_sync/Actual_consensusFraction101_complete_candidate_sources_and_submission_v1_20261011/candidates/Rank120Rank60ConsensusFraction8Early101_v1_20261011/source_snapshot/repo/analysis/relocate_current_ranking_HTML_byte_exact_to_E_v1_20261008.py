"""Relocate only current mutable ranking output to E; preserve original pathname and every byte via verified file symlink."""
from pathlib import Path
import sys,ctypes,time,json
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def main():
    assert (A/'round144_connected_API_main_request_v1_20261008.json').exists(), 'Wait until all current HTML publication bytes are already staged and hashed'
    source=ROOT/'results/all_model_rankings_20261003.html'
    base=Path('E:/赛题五_本机临时/current_mutable_ranking_HTML_v1_20261008');target=base/source.name
    assert source.is_file() and not source.is_symlink() and source.resolve()==source
    assert source.resolve().is_relative_to((ROOT/'results').resolve()) and source.resolve().drive.upper()=='D:'
    assert not base.exists();base.mkdir()
    assert target.parent.resolve()==base.resolve() and target.resolve().drive.upper()=='E:' and not target.exists()
    probe=A/'current_ranking_file_link_probe_v1_20261008.bin';assert probe.is_symlink() and probe.read_bytes()==b'actual-byte-exact-file-link-probe'
    # No active scorer directly pins this mutable output. Model/candidate/source/score files remain untouched.
    freezes=[]
    for folder in (A/'ConeRidgeAlpha100_official_comparison_v5_20261008',A/'BF16wide40_official_comparison_v1_20261008'):
        for path in folder.glob('frozen*.json'):
            q=read(path);assert str(source) not in q.get('input_sha256',{}),path;freezes.append(path)
    kernel=ctypes.WinDLL('kernel32',use_last_error=True)
    move=kernel.MoveFileExW;move.argtypes=(ctypes.c_wchar_p,ctypes.c_wchar_p,ctypes.c_uint32);move.restype=ctypes.c_int
    link=kernel.CreateSymbolicLinkW;link.argtypes=(ctypes.c_wchar_p,ctypes.c_wchar_p,ctypes.c_uint32);link.restype=ctypes.c_ubyte
    digest=sha(source);size=source.stat().st_size
    create(A/'current_ranking_HTML_E_relocation_plan_v1_20261008.json',{
        'status':'frozen_exact_single_mutable_output_relocation_with_supported_file_symlink',
        'source':str(source),'E_target':str(target),'sha256':digest,'bytes':size,
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),*freezes]},
        'single_file_absolute_boundaries_checked':True,'no_model_or_scientific_input_relocation':True})
    assert move(str(source),str(target),2),'MoveFileExW failed: '+str(ctypes.get_last_error())
    try:
        assert sha(target)==digest and target.stat().st_size==size
        assert link(str(source),str(target),2),'CreateSymbolicLinkW failed: '+str(ctypes.get_last_error())
        assert source.is_symlink() and source.resolve()==target.resolve() and sha(source)==digest
    except BaseException:
        # Return exact original data if pathname recreation fails; never leave it missing.
        if not source.exists():assert move(str(target),str(source),2)
        raise
    create(A/'current_ranking_HTML_E_relocation_verification_v1_20261008.json',{
        'status':'passed_actual_single_current_ranking_output_moved_byte_exact_to_E_with_original_path_link',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'original_path':str(source),'physical_path':str(target),
        'original_sha256':digest,'relocated_sha256':sha(target),'linked_sha256':sha(source),'bytes_freed_on_D':size,
        'original_builder_write_text_follows_file_link_without_source_changes':True,
        'scientific_sources_scores_models_inputs_candidates_and_immutable_per_round_reports_untouched':True,
        'no_recursive_deletion_no_model_deletion_no_C_drive_storage':True,'new_quality_scores':0})
    print('Current complete ranking HTML moved byte-exactly to E, original path linked; freed %.3f GiB.'%(size/2**30),flush=True)
if __name__=='__main__':main()
