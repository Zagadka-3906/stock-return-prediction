"""Versioned matched Fourier capacity, penalty andseed controls before scoring."""
from pathlib import Path
import ast
import hashlib
import json
ROOT=Path(__file__).resolve().parents[1]
HERE=ROOT/'analysis'


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    assert not (HERE/'fourier_tuning_bank_20261004/protocol.json').exists()
    assert not (HERE/'fourier_tuning_preflight_20261004/verification.json').exists()
    source=HERE/'train_fourier_ridge_bank_20261004.py'
    text=source.read_text(encoding='utf-8').replace('fourier_ridge','fourier_tuning')
    start=text.index('CONFIGS={');end=text.index('engine.OUT=OUT',start)
    text=text[:start]+"""VARIANTS=(('c256_mass128',256,.1,20261004),('c512_mass128',512,.1,20261004),
          ('c128_l0001',128,.001,20261004),('c128_l1',128,1.,20261004),
          ('c128_seed20261005',128,.1,20261005))
CONFIGS={f'{label}_fourier_tuning_{suffix}':{'kind':'ridge_fourier','target':target,'ridge_lambda':penalty,
          'chunk_rows':32768,'clip_z':8.,'lengthscale':1.,'random_components':components,'seed':seed,
          'fixed_fourier_mass':128.,'reserve_available_ram_GiB':8.,'return_quantiles':[.005,.995]}
         for label,target in (('rank','y_rank'),('return','y_ret_1d'))
         for suffix,components,penalty,seed in VARIANTS}
"""+text[end:]
    text=text.replace("'kind':'ridge_fourier_tuning'","'kind':'ridge_fourier'")
    marker='random=np.sqrt(2.)*np.cos(projected[:len(z)]+phase)';assert marker in text
    text=text.replace(marker,"random=np.sqrt(2.*cfg['fixed_fourier_mass']/cfg['random_components'])*np.cos(projected[:len(z)]+phase)")
    text=text.replace("Append128 fixed seeded cosine features sqrt(2)*cos(z@W+phase), total191 columns.","Append128/256/512 fixed seeded cosine features sqrt(2*128/components)*cos(z@W+phase), total191/319/575 columns. Fixed mass128 preserves the Fourier component kernel scale across capacity variants.")
    text=text.replace('Fourier amplitudes equal sqrt128 times standard RBFSampler output.','All Fourier amplitudes equal sqrt128 times standard RBFSampler output, independent of feature count.')
    text=text.replace("'expected_annual_fits':30","'expected_annual_fits':50")
    text=text.replace('Six raw-plus-Fourier ridge configurations frozen','Ten matched Fourier capacity/penalty/seed controls frozen')
    text=text.replace("gate=ROOT/'analysis/additive_ridge_future_pipelines_qa_20261004/verification.json'","gate=ROOT/'analysis/nonlinear_stacking_future_pipelines_qa_20261004/verification.json'")
    text=text.replace("'models_trained':30","'models_trained':50").replace('All30 Fourier ridge fold models','All50 matched Fourier tuning fold models')
    marker='sources=[Path(__file__),SOURCE,';assert marker in text
    text=text.replace(marker,"sources=[Path(__file__),ROOT/'analysis/prepare_fourier_tuning_bank_20261004.py',ROOT/'analysis/fourier_tuning_sources_prepared_20261004.json',ROOT/'analysis/train_fourier_ridge_bank_20261004.py',SOURCE,")
    target=HERE/'train_fourier_tuning_bank_20261004.py';ast.parse(text);target.write_text(text,encoding='utf-8',newline='\n')
    router=(HERE/'fourier_ridge_model_sources_20261004.py').read_text(encoding='utf-8')
    router=router.replace('additive_ridge_model_sources_20261004','nonlinear_stacking_model_sources_20261004').replace('fourier_ridge','fourier_tuning')
    router=router.replace("if bundle['kind']=='ridge_fourier':","if 'fixed_fourier_mass' in bundle.get('config',{}):")
    path=HERE/'fourier_tuning_model_sources_20261004.py';ast.parse(router);path.write_text(router,encoding='utf-8',newline='\n')
    verifier=(HERE/'verify_fourier_ridge_bank_20261004.py').read_text(encoding='utf-8').replace('fourier_ridge','fourier_tuning')
    verifier=verifier.replace("sampler.transform(z)*np.sqrt(cfg['random_components'])","sampler.transform(z)*np.sqrt(cfg['fixed_fourier_mass'])")
    verifier=verifier.replace("'random_features':128,'basis_columns':191,'seed':20261004,","'random_features':[128,256,512],'basis_columns':[191,319,575],'seeds':[20261004,20261005],'fixed_fourier_mass':128.,")
    marker="    bank.dump(folder/'verification.json'";assert marker in verifier
    verifier=verifier.replace(marker,"""    import train_fourier_ridge_bank_20261004 as baseline
    baseline_controls=[]
    for label,target_name in (('rank','y_rank'),('return','y_ret_1d')):
        cfg={**baseline.CONFIGS[f'{label}_fourier128_s1'],'fixed_fourier_mass':128.}
        labels=rank if target_name=='y_rank' else returns
        a=baseline.fit_arrays(x,labels,baseline.CONFIGS[f'{label}_fourier128_s1']);b=bank.fit_arrays(x,labels,cfg)
        assert a['intercept']==b['intercept']
        for field in ('mean','scale','coefficients','random_weights','random_phase'):assert np.array_equal(a[field],b[field])
        assert np.array_equal(baseline.predict_arrays(a,x),bank.predict_arrays(b,x))
        baseline_controls.append({'target':target_name,'original128_mass_and_fit_bit_identical':True})
"""+marker)
    verifier=verifier.replace("'random_projection_does_not_use_feature_values_or_targets':True,'controls':proofs,","'random_projection_does_not_use_feature_values_or_targets':True,'controls':proofs,'baseline_controls':baseline_controls,")
    verifier=verifier.replace('All six Fourier ridge','All ten matched Fourier tuning')
    path2=HERE/'verify_fourier_tuning_bank_20261004.py';ast.parse(verifier);path2.write_text(verifier,encoding='utf-8',newline='\n')
    record={'status':'sources_prepared_before_fit_and_scoring','new_configurations':10,'expected_annual_fits':50,
        'capacity_features':[256,512],'capacity_fixed_fourier_mass':128.,'penalty_controls':[.001,1.],
        'seed_control':20261005,'target_controls':['supplied one-day rank','one-day return'],
        'all_other_settings_match_original128_s1':True,'source_template_sha256':sha(source),
        'generated_source_sha256':{str(p.resolve()):sha(p) for p in (target,path,path2)},'test_data_read':False}
    (HERE/'fourier_tuning_sources_prepared_20261004.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(record,ensure_ascii=False))


if __name__=='__main__':main()
