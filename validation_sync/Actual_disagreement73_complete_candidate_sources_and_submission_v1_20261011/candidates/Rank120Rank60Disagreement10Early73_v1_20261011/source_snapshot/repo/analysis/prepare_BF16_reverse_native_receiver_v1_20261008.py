"""Prepare the exact original neural native stage with explicit valid-row reversal and fixed-year admission."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create


def main():
    source=A/'BF16_complete_parent_native_stage_v1_20261008.py';target=A/'BF16_reverse_complete_parent_native_stage_v1_20261008.py'
    text=source.read_text(encoding='utf8').replace("GRAPH_KEY='BF16_complete_parent_rank_CDF'","GRAPH_KEY='BF16_reverse_complete_parent_rank_CDF'")
    text=text.replace('from BF16_complete_parent_rank_CDF_v1_20261008 import','from BF16_reverse_complete_parent_rank_CDF_v1_20261008 import')
    needle="    info=component['training_info'];meta=info['training_meta']";assert text.count(needle)==1
    text=text.replace(needle,needle+"\n    assert spec['signal_sign_on_valid_rows']==-1. and spec['invalid_signal_bits_preserved']\n    years=np.unique(context.dates//10000);fit_year=int(info['year'])\n    assert len(years)>0 and int(years.min())>=fit_year\n    assert len(years)==1 and int(years[0])==fit_year or fit_year==2025")
    text=text.replace("report={'rows':len(parent),","report={'rows':len(parent),'saved_fit_year':fit_year,'prediction_calendar_years':[int(y) for y in years],\n            'negative_only_valid_neural_values_invalid_sentinel_bits_preserved':True,")
    assert not target.exists();compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n')
    from predict_BF16_reverse_complete_parent_scheme_v1_20261008 import BACKENDS,prepared_backend
    controls=[];paths=[Path(__file__),source,target,A/'predict_BF16_reverse_complete_parent_scheme_v1_20261008.py',
        A/'BF16_reverse_complete_parent_rank_CDF_v1_20261008.py']
    for backend,(filename,module,has_teacher) in BACKENDS.items():
        path=A/filename;paths.append(path);prepared=prepared_backend(path.read_text(encoding='utf8'),backend);compile(prepared,str(path),'exec')
        controls.append({'parent_backend':backend,'single_scoped_stage_import_replaced':True,
            'actual_complete_parent_and_future_inference_not_yet_claimed':True})
    create(A/'BF16_reverse_native_receiver_preparation_v1_20261008.json',{
        'status':'prepared_reverse_native_stage_and_compiled4_preserved_parent_backend_adapters',
        'input_sha256':{str(p):sha(p) for p in paths},'controls':controls,'new_fits':0,'actual_quality_scores':0,
        'historical_native_hooks_full_future_controls_and_complete138_admission_still_required':True,'test_labels_read':False})
    print('Reverse neural native stage and four complete-parent adapters prepared; compilation is not future qualification.',flush=True)


if __name__=='__main__':main()
