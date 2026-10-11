"""Prepare a checkpoint-preserving continuation that releases unused read-only mappings."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
def main():
    old=A/'train_nonflag_residual_RFF128Low_bank10_v1_20261007.py';new=A/'train_nonflag_residual_RFF128Low_bank10_v2_20261007.py';assert not new.exists()
    text=old.read_text(encoding='utf8')
    needle="out=A/'nonflag_residual_RFF128Low_bank10_20261007'; assert not out.exists(); out.mkdir()";assert text.count(needle)==1
    text=text.replace(needle,"out=A/'nonflag_residual_RFF128Low_bank10_20261007'; assert out.is_dir()\n    resume_path=A/'RFF128Low_checkpoint_resume_snapshot_20261007.json';resume=read(resume_path)\n    assert resume['status']=='verified_owned_idle_bank_saved_complete_years_before_memory_release_resume'\n    for p,d in resume['immutable_saved_file_sha256'].items():assert sha(p)==d,p")
    text=text.replace("paths=[Path(p) for p in proof['input_sha256']]","paths=[Path(p) for p in proof['input_sha256']]\n    paths += [Path(__file__),resume_path,*[Path(p) for p in resume['immutable_saved_file_sha256']]]")
    text=text.replace("out/'frozen_before_actual_training.json'","out/'frozen_before_actual_resume_v2.json'")
    text=text.replace("'actual_declared_native_fits':10,","'actual_declared_native_fits':10,'reused_saved_native_fits':resume['saved_native_fit_count'],")
    needle='        eligible=np.isfinite(y)&valid; del labels; gc.collect()';assert text.count(needle)==1
    text=text.replace(needle,needle+"\n        raw._mmap.close();raw=None;gc.collect()")
    needle="            (out/name).mkdir(); outputs[name]=np.lib.format.open_memmap(out/name/'nonflag_oof_predictions.npy',mode='w+',dtype=np.float64,shape=(len(full),)); outputs[name][:]=0.; outputs[name].flush()";assert text.count(needle)==1
    text=text.replace(needle,"            assert (out/name).is_dir()\n            outputs[name]=np.lib.format.open_memmap(out/name/'nonflag_oof_predictions.npy',mode='r+')\n            assert outputs[name].shape==(len(full),) and outputs[name].dtype==np.float64\n            assert numeric_sha(outputs[name][:resume['preserved_prefix_rows']])==resume['oof_prefix_numeric_sha256'][name]")
    needle="        for year in plan['native_fit_years']:\n            cutoff=";assert text.count(needle)==1
    text=text.replace(needle,"""        for year in plan['native_fit_years']:
            saved=[out/name/f'info_{year}.json' for name in plan['configurations']]
            if all(p.exists() for p in saved):
                for p in saved:
                    record=read(p)
                    assert record['native_reload_independent_all_prediction_bits_exact']
                    assert sha(record['native_model_path'])==record['native_model_sha256']
                    assert sha(record['independent_random_fourier_linear_state_path'])==record['independent_random_fourier_linear_state_sha256']
                    records.append(record)
                continue
            assert not any(p.exists() for p in saved),'Only complete saved annual pairs are admitted by this continuation'
            cutoff=""")
    needle="            window=np.load(cache/f'mature_training_features64_{year}.npy',mmap_mode='r')";assert text.count(needle)==1
    text=text.replace(needle,"            assert raw is None\n            raw=np.load(raw_path,mmap_mode='r')\n"+needle)
    needle="            else: test=np.asarray(window[:1000]).copy()";assert text.count(needle)==1
    text=text.replace(needle,needle+"\n            assert not np.shares_memory(bx,window) and not np.shares_memory(test,window) and not np.shares_memory(test,raw)\n            raw._mmap.close();raw=None\n            window._mmap.close();window=None;gc.collect()")
    needle="        for name,array in outputs.items():";assert text.count(needle)==1
    text=text.replace(needle,needle+"\n            assert numeric_sha(array[:resume['preserved_prefix_rows']])==resume['oof_prefix_numeric_sha256'][name]")
    text=text.replace("'actual_native_fits':10,'elapsed_seconds':", "'actual_native_fits':10,'reused_saved_native_fits':resume['saved_native_fit_count'],'actual_new_native_fits_by_resume':10-resume['saved_native_fit_count'],'elapsed_seconds_scope':'remaining_fits_and_controls_after_resume','elapsed_seconds':")
    compile(text,str(new),'exec');new.write_text(text,encoding='utf8',newline='\n')
    old_hook=A/'run_nonflag_residual_RFF128Low_hook6_after_bank_20261007.py'
    old_transform=A/'verify_nonflag_residual_RFF128Low73_transform_20261007.py'
    old_controller=A/'run_nonflag_RFF128Low_actual_controls_20261007.py'
    pairs=[(old_hook,A/'run_nonflag_residual_RFF128Low_hook6_after_bank_v2_20261007.py'),
      (old_transform,A/'verify_nonflag_residual_RFF128Low73_transform_v2_20261007.py'),
      (old_controller,A/'run_nonflag_RFF128Low_actual_controls_v2_20261007.py')]
    generated=[new]
    for before,after in pairs:
        assert not after.exists();source=before.read_text(encoding='utf8')
        source=source.replace("nonflag_residual_RFF128Low_native_bank10'","nonflag_residual_RFF128Low_native_bank10_v2'")
        source=source.replace('run_nonflag_residual_RFF128Low_hook6_after_bank_20261007','run_nonflag_residual_RFF128Low_hook6_after_bank_v2_20261007')
        source=source.replace('verify_nonflag_residual_RFF128Low73_transform_20261007','verify_nonflag_residual_RFF128Low73_transform_v2_20261007')
        compile(source,str(after),'exec');after.write_text(source,encoding='utf8',newline='\n');generated.append(after)
    pins={str(p):sha(p) for p in [Path(__file__),old,old_hook,old_transform,old_controller,*generated]}
    create(A/'RFF128Low_memory_release_resume_source_preparation_20261007.json',
      {'status':'compiled_saved_annual_pair_resume_and_readonly_mapping_release_before_execution','input_sha256':pins,
       'model_parameters_labels_preprocessing_and_inference_recipe_unchanged':True,'actual_new_fits_by_preparation':0})
if __name__=='__main__':main()
