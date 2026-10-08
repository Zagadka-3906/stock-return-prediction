"""Fresh independent oracle controls; preserve the failed strict-bound check and native recipe."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create

def main():
    native=A/'nonflag_ConeRidge64_streamed_v1_20261008.py'
    small1=A/'verify_nonflag_ConeRidge64_small_v1_20261008.py'
    probe1=A/'verify_nonflag_ConeRidge64_actual200k_v1_20261008.py'
    diagnostic=Path('E:/赛题五_本机临时/ConeRidge64_dense_BVLS_bound_diagnostic_v1_20261008/verification.json')
    d=read(diagnostic)
    assert d['status']=='recorded_actual_dense_BVLS_bound_diagnostic_not_an_admitted_model'
    native_before=sha(native)
    old="    assert result.success and np.all(result.x>=0.),result.message\n    coef=cfg['feature_sign']*result.x\n    return coef,float(mean-center@coef),{'dense_BVLS_success':True,'iterations':int(result.nit),'optimality':float(result.optimality)}"
    new="""    raw_min=float(np.min(result.x));boundary_tolerance=2e-12
    assert result.success and np.isfinite(result.x).all() and raw_min>=-boundary_tolerance,(result.message,raw_min)
    # BVLS can return roundoff below its lower bound; validate before projecting that oracle value.
    positive=np.maximum(result.x,0.)
    gradient=augmented.T@(augmented@positive-target);rhs=augmented.T@target
    active=positive>boundary_tolerance
    active_violation=float(np.max(np.abs(gradient[active]))) if active.any() else 0.
    inactive_violation=float(np.max(np.maximum(-gradient[~active],0.))) if (~active).any() else 0.
    relative_kkt=max(active_violation,inactive_violation)/max(1.,float(np.max(np.abs(rhs))))
    assert relative_kkt<1e-10,relative_kkt
    coef=cfg['feature_sign']*positive
    return coef,float(mean-center@coef),{'dense_BVLS_success':True,'iterations':int(result.nit),
        'optimality':float(result.optimality),'raw_minimum_parameter':raw_min,'allowed_boundary_roundoff':boundary_tolerance,
        'projected_negative_parameters':int(np.count_nonzero(result.x<0.)),
        'maximum_boundary_projection':float(np.max(np.abs(positive-result.x))),
        'independent_dense_relative_KKT_violation':relative_kkt,'native_solver_and_comparison_tolerances_unchanged':True}"""
    s=small1.read_text(encoding='utf8');assert s.count(old)==1;s=s.replace(old,new)
    s=s.replace('nonflag_ConeRidge64_small_v1_20261008','nonflag_ConeRidge64_small_v2_20261008')
    s=s.replace('actual_nonflag_ConeRidge64_small_location_v1_20261008','actual_nonflag_ConeRidge64_small_location_v2_20261008')
    p=probe1.read_text(encoding='utf8')
    for old_name,new_name in (
        ('nonflag_ConeRidge64_actual200k_v1_20261008','nonflag_ConeRidge64_actual200k_v2_20261008'),
        ('verify_nonflag_ConeRidge64_small_v1_20261008','verify_nonflag_ConeRidge64_small_v2_20261008'),
        ('actual_nonflag_ConeRidge64_small_location_v1_20261008','actual_nonflag_ConeRidge64_small_location_v2_20261008'),
        ('actual_nonflag_ConeRidge64_actual200k_location_v1_20261008','actual_nonflag_ConeRidge64_actual200k_location_v2_20261008'),
        ('mature_krylov200k_probe','mature_constrained_ridge200k_probe')):p=p.replace(old_name,new_name)
    paths=[A/'verify_nonflag_ConeRidge64_small_v2_20261008.py',A/'verify_nonflag_ConeRidge64_actual200k_v2_20261008.py']
    for path,source in zip(paths,(s,p)):
        assert not path.exists();compile(source,str(path),'exec');path.write_text(source,encoding='utf8',newline='\n')
    assert sha(native)==native_before
    create(A/'ConeRidge64_BVLS_oracle_recovery_v2_20261008.json',{
        'status':'prepared_fresh_independent_BVLS_boundary_roundoff_controls_not_yet_run',
        'input_sha256':{str(q):sha(q) for q in [Path(__file__),native,small1,probe1,diagnostic,*paths]},
        'frozen_native_solver_bytes_unchanged':True,'failed_actual200k_v1_preserved':True,
        'independent_oracle_boundary_tolerance':2e-12,'independent_KKT_relative_tolerance':1e-10,
        'native_coefficient_and_intercept_comparison_rtol':2e-8,'native_comparison_atol':2e-10,
        'new_official_scores':0,'future_X_and_Y_read':False})
    print('Fresh oracle2 created; native1 and failed actual200k1 preserved.',flush=True)

if __name__=='__main__':main()
