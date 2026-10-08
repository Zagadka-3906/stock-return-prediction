"""Prepare a fresh same-recipe later-TRAIN-label poisoning control for all20 signed heads."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create

def main():
    old=A/'verify_KrylovGram20_causal_refit_v2_20261008.py';text=old.read_text(encoding='utf8')
    for before,after in (
        ('nonflag_KrylovGram64_bank20_v3_20261008','nonflag_ConeRidge64_bank20_v1_20261008'),
        ('actual_nonflag_KrylovGram64_bank20_location_v3_20261008','actual_nonflag_ConeRidge64_bank20_location_v1_20261008'),
        ('nonflag_KrylovGram64_streamed_v2_20261008','nonflag_ConeRidge64_streamed_v1_20261008'),
        ('KrylovGram20_causal_refit_v2_20261008','ConeRidge20_causal_refit_v1_20261008'),
        ('actual_KrylovGram20_causal_refit_location_v2_20261008','actual_ConeRidge20_causal_refit_location_v1_20261008'),
        ('ReorthogonalizedCG','Coefficient-constrained ridge'),('reorthogonalizedCG','constrained_ridge')):text=text.replace(before,after)
    old_check="                assert model.actual_iterations_==saved['model'].actual_iterations_"
    new_check="""                assert np.array_equal(model.nonnegative_parameters_.view('u8'),saved['model'].nonnegative_parameters_.view('u8'))
                assert np.all(model.nonnegative_parameters_>=0.) and metadata['actual_relative_KKT_violation']<1e-10"""
    assert text.count(old_check)==1;text=text.replace(old_check,new_check)
    target=A/'verify_ConeRidge20_causal_refit_v1_20261008.py'
    assert not target.exists();compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n')
    sources=[Path(__file__),old,target,A/'nonflag_ConeRidge64_streamed_v1_20261008.py']
    pins={str(p):sha(p) for p in sources}
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    row=start('ConeRidge20_causal_refit_controls_v1_20261008',target.name,[],pins)
    create(A/'actual_ConeRidge20_causal_refit_hidden_launch_v1_20261008.json',{'identity':row,'input_sha256':pins,
        'status':'queued20_same_configuration_controls_after_native_bank_not_additional_candidates','new_official_scores':0})

if __name__=='__main__':main()
