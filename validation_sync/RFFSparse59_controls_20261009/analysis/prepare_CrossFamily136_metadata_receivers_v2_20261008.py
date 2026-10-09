"""Fresh2 fixes two old descriptive metadata labels; retains all immutable1 proofs and unchanged numeric recipes."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute


def main():
    stems=('prepare_CrossFamily94_round136_sources','run_CrossFamily94_official_comparison','prepare_CrossFamily94_selected_candidate',
        'seal_CrossFamily94_selected_candidate','run_CrossFamily94_round136_full_registration','verify_CrossFamily94_round136_sources',
        'publish_CrossFamily94_evidence','queue_CrossFamily136_complete_pipeline','verify_CrossFamily94_prospective_routes')
    mapping={stem+'_v1_20261008':stem+'_v2_20261008' for stem in stems}
    for stem in ('CrossFamily94_round136_source_admission','CrossFamily94_round136_source_preparation','CrossFamily94_prospective_routes',
        'CrossFamily136_receiver_preparation','CrossFamily136_complete_dependency_plan','CrossFamily136_complete_hidden_launches',
        'CrossFamily94_controls_main_publication','CrossFamily94_scores_main_publication','CrossFamily94_official_comparison',
        'CrossFamily94_selected_candidate_preparation','CrossFamily94_selected_candidate_sealing','CrossFamily94_round136_full_registration'):
        mapping[stem+'_v1_20261008']=stem+'_v2_20261008'
    outputs={}
    for stem in stems:
        source=A/(stem+'_v1_20261008.py');target=A/(stem+'_v2_20261008.py')
        assert not target.exists()
        text=substitute(source.read_text(encoding='utf8'),mapping)
        # Services and source receivers are fresh2, while exact physical comparison/release/receipt folders stay1.
        text=text.replace("OUT=A/'CrossFamily94_official_comparison_v2_20261008'","OUT=A/'CrossFamily94_official_comparison_v1_20261008'")
        text=text.replace("folder=A/'CrossFamily94_official_comparison_v2_20261008';proof=","folder=A/'CrossFamily94_official_comparison_v1_20261008';proof=")
        text=text.replace('CrossFamily94_official_comparison_v2_20261008/verification.json','CrossFamily94_official_comparison_v1_20261008/verification.json')
        text=text.replace('CrossFamily94_official_comparison_v2_20261008/frozen_before','CrossFamily94_official_comparison_v1_20261008/frozen_before')
        if stem=='prepare_CrossFamily94_round136_sources':
            text=text.replace("A/'CrossFamily94_official_comparison_v2_20261008'):","A/'CrossFamily94_official_comparison_v1_20261008'):")
            text=text.replace("names=[Path(__file__).name,","names=[Path(__file__).name,'prepare_CrossFamily136_metadata_receivers_v2_20261008.py','CrossFamily136_metadata_receiver_preparation_v2_20261008.json',")
        if stem=='publish_CrossFamily94_evidence':
            assert "'round':135" in text
            text=text.replace("'round':135","'round':136").replace('actual_completed_BF16_controls_or_scores_before_full136_qualification','actual_completed_CrossFamily_controls_or_scores_before_full136_qualification')
        if stem=='prepare_CrossFamily94_selected_candidate':
            assert 'selected_by_all40_actual_official_scores' in text
            text=text.replace('selected_by_all40_actual_official_scores','selected_by_all94_actual_official_scores')
        if stem=='run_CrossFamily94_round136_full_registration':
            text=text.replace('Register40 actual complete-parent neural comparisons','Register94 actual complete-parent cross-family comparisons')
            text=text.replace('CrossFamily94_round136_actual_registration_v1_20261008','CrossFamily94_round136_actual_registration_v2_20261008')
            text=text.replace('run_CrossFamily94_round136_full_registration_v1_file_IO_20261008','run_CrossFamily94_round136_full_registration_v2_file_IO_20261008')
        if stem=='verify_CrossFamily94_prospective_routes':
            text=text.replace('CrossFamily136_transfer_probe_v1_20261008.bin','CrossFamily136_transfer_probe_v2_20261008.bin').replace('/transfer_probe_v1.bin','/transfer_probe_v2.bin')
            marker='    scope=read('
            assert text.count(marker)==1
            text=text.replace(marker,"    manifest=next(node for node in ast.walk(ast.parse(producer)) if isinstance(node,ast.Dict) and any(isinstance(key,ast.Constant) and key.value=='actual_existing_native_head_audits' for key in node.keys))\n    actual_fields={key.value:value for key,value in zip(manifest.keys,manifest.values) if isinstance(key,ast.Constant)}\n    assert actual_fields['round'].value==136\n    selected_text=(A/'prepare_CrossFamily94_selected_candidate_v2_20261008.py').read_text(encoding='utf8')\n    assert 'selected_by_all94_actual_official_scores' in strings(selected_text) and 'selected_by_all40_actual_official_scores' not in selected_text\n"+marker)
        compile(text,str(target),'exec');outputs[target]=text
    for path,text in outputs.items():path.write_text(text,encoding='utf8',newline='\n')
    create(A/'CrossFamily136_metadata_receiver_preparation_v2_20261008.json',{'status':'prepared_fresh2_correct_round136_and_all94_labels_before_any_quality',
        'input_sha256':{str(path):sha(path) for path in [Path(__file__),*[A/(stem+'_v1_20261008.py') for stem in stems],*outputs]},
        'old_prospective1_and_all_original_sources_retained':True,'scientific_math_and94_case_grid_unchanged':True,
        'new_quality_scores':0,'actual_future_X_calls':0,'fresh24_prospective2_checks_required':True})
    print('Fresh2 corrects round136 and all94 metadata labels; original1 proofs/source bytes retained.',flush=True)


if __name__=='__main__':main()
