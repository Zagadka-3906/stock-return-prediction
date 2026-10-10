"""Create a versioned67-child stacking experiment from frozen55-child code."""
from pathlib import Path
import ast
import hashlib
import json
ROOT=Path(__file__).resolve().parents[1]
HERE=ROOT/'analysis'


def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    assert not (HERE/'nonlinear_stacking_bank_20261004/protocol.json').exists()
    assert not (HERE/'nonlinear_stacking_preflight_20261004/verification.json').exists()
    originals={};generated={}
    for source_name in ('train_expanded_stacking_bank_20261004.py','expanded_stacking_model_sources_20261004.py','verify_expanded_stacking_20261004.py'):
        source=HERE/source_name;originals[str(source.resolve())]=digest(source)
        text=source.read_text(encoding='utf-8')
        text=text.replace('expanded_stacking','nonlinear_stacking')
        text=text.replace('catboost_tuning_model_sources_20261004','fourier_ridge_model_sources_20261004')
        text=text.replace('expanded_oof_','nonlinear_oof_')
        for old,new in (('55-parent','67-parent'),('all55','all67'),('all55','all67'),('all45','all55'),
                        ('55-child','67-child'),('55 children','67 children'),('55 child','67 child'),
                        ('55-column','67-column'),('55-member','67-member'),('55 mature','67 mature'),
                        ('all55 mature','all67 mature'),('len(MEMBERS)==55','len(MEMBERS)==67'),
                        ("'members':55","'members':67"),("'members':55","'members':67"),
                        ('fold{year},55','fold{year},67'),('all55_actual_children','all67_actual_children'),
                        ('frozen45 existing','frozen55 existing'),('the10 new columns','the12 new columns'),
                        ("'reused_frozen_columns':45","'reused_frozen_columns':55"),("'new_columns':10","'new_columns':12")):
            text=text.replace(old,new)
        if source_name.startswith('train_'):
            text=text.replace("OLD=ROOT/'analysis/oof_stacking_bank_20261004'","OLD=ROOT/'analysis/expanded_stacking_bank_20261004'")
            text=text.replace("OLD/'input_routing_recovery_protocol.json',",'')
            marker="    old_names=tuple(old_audit['members']);old_matrix=np.load(OLD/'oof_features.npy',mmap_mode='r')"
            assert marker in text
            text=text.replace(marker,marker+"\n    assert len(old_names)==55 and set(old_names).issubset(MEMBERS) and len(set(MEMBERS)-set(old_names))==12")
            marker="    verify();cfg=CONFIGS[name]"
            assert marker in text
            text=text.replace(marker,"    if year==2025:wait_for_fit_reserve()\n"+marker)
            marker="sources=[Path(__file__),SOURCE,"
            assert marker in text
            text=text.replace(marker,"sources=[Path(__file__),ROOT/'analysis/prepare_nonlinear_stacking_bank_20261004.py',ROOT/'analysis/nonlinear_stacking_sources_prepared_20261004.json',SOURCE,")
            marker='    freeze();build_features();frame=load_oof_frame();matrix=np.load(OUT/\'oof_features.npy\',mmap_mode=\'r\')'
            assert marker in text
            text=text.replace(marker,"    wait_for_fit_reserve();"+marker.strip())
            marker="if __name__=='__main__':"
            assert marker in text
            text=text.replace(marker,"def wait_for_fit_reserve():\n    import psutil\n    while psutil.virtual_memory().available<8*2**30:\n        log('Waiting for chosen8GiB free-RAM reserve; no physical exhaustion inferred');time.sleep(10)\n\n\n"+marker)
        if source_name.endswith('model_sources_20261004.py'):
            marker="bundle.get('config',{}).get('first_fold_policy') in ('ridge','uniform')"
            assert marker in text
            text=text.replace(marker,"tuple(bundle.get('config',{}).get('members',()))==bank.MEMBERS")
        target=HERE/source_name.replace('expanded_stacking','nonlinear_stacking')
        ast.parse(text,filename=str(target))
        target.write_text(text,encoding='utf-8',newline='\n');generated[str(target.resolve())]=digest(target)
    record={'status':'sources_prepared_before_fit_and_scoring','member_count':67,'new_scheme_configurations':12,
        'new_annual_fits_planned':24,'paired_later_fold_reuses_planned':24,'annual_artifacts_planned':60,
        'reused_fixed_feature_columns':55,'new_feature_columns':12,'new_child_annual_fits':0,
        'first_year_policies':['matching frozen raw63 ridge','fixed equal-weight67-child daily-rank mean'],
        'training_only':True,'test_data_read':False,'source_templates_sha256':originals,'generated_source_sha256':generated}
    destination=HERE/'nonlinear_stacking_sources_prepared_20261004.json'
    destination.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(record,ensure_ascii=False))


if __name__=='__main__':main()
