"""Freeze eight previously uncovered signed alpha heads and dispatch real probes, bank and causal controls."""
from pathlib import Path
import ast,importlib,io,sys,time,tokenize
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
ALPHAS=(.001,.003,.03,.3)
def counts(text,mapping):
    tokens=list(tokenize.generate_tokens(io.StringIO(text).readline))
    return tokenize.untokenize([t._replace(string=mapping[t.string]) if t.type==tokenize.NUMBER and t.string in mapping else t for t in tokens])
def save(name,text):
    path=A/name;assert not path.exists();compile(text,str(path),'exec');path.write_text(text,encoding='utf8',newline='\n');return path
def main():
    old=A/'nonflag_ConeRidge64_streamed_v1_20261008.py';text=old.read_text(encoding='utf8')
    assert text.count('for alpha in (.01,.1)')==1;text=text.replace('for alpha in (.01,.1)','for alpha in '+repr(ALPHAS))
    native=save('nonflag_ConeRidgeAlpha8_64_streamed_v1_20261008.py',text)
    # Full solver, class, export kind and all numerical checks remain identical; only declared alpha tuple changes.
    before=ast.parse(old.read_text(encoding='utf8'));after=ast.parse(text)
    generators=[n for n in ast.walk(before) if isinstance(n,ast.comprehension) and isinstance(n.target,ast.Name) and n.target.id=='alpha'];assert len(generators)==1
    generators[0].iter=ast.Tuple(elts=[ast.Constant(v) for v in ALPHAS],ctx=ast.Load());assert ast.dump(before)==ast.dump(after)
    module=importlib.import_module(native.stem);assert len(module.CONFIGS)==8
    import nonflag_ConeRidge64_streamed_v1_20261008 as previous
    assert not set(module.CONFIGS)&set(previous.CONFIGS)
    source_small=A/'verify_nonflag_ConeRidge64_small_v2_20261008.py'
    small=source_small.read_text(encoding='utf8').replace('ConeRidge64','ConeRidgeAlpha8_64').replace('_v2_20261008','_v1_20261008')
    small=counts(small,{'12':'24','72':'144'}).replace('actual12','actual24').replace('and72','and144').replace('Twelve constrained','Twenty-four constrained').replace('and72 saved','and144 saved')
    small_path=save('verify_nonflag_ConeRidgeAlpha8_64_small_v1_20261008.py',small)
    source_probe=A/'verify_nonflag_ConeRidge64_actual200k_v2_20261008.py'
    probe=source_probe.read_text(encoding='utf8').replace('ConeRidge64','ConeRidgeAlpha8_64').replace('_v2_20261008','_v1_20261008')
    probe=counts(probe,{'4':'8','12':'24','24':'48'}).replace('actual4_','actual8_').replace('and24_prefix','and48_prefix')
    probe_path=save('verify_nonflag_ConeRidgeAlpha8_64_actual200k_v1_20261008.py',probe)
    source_bank=A/'train_nonflag_ConeRidge64_bank20_v1_20261008.py'
    bank=source_bank.read_text(encoding='utf8').replace('ConeRidge64','ConeRidgeAlpha8_64').replace('bank20','bank40')
    bank=bank.replace('actual200k_location_v2','actual200k_location_v1')
    bank=counts(bank,{'20':'40','4':'8'}).replace('actual20','actual40').replace('actual4_','actual8_').replace('and24_prefix','and48_prefix').replace('/20:', '/40:').replace('Twenty CPU2','Forty CPU2').replace('frozen_before_actual20','frozen_before_actual40')
    bank_path=save('train_nonflag_ConeRidgeAlpha8_64_bank40_v1_20261008.py',bank)
    source_causal=A/'verify_ConeRidge20_causal_refit_v1_20261008.py'
    causal=source_causal.read_text(encoding='utf8').replace('ConeRidge64','ConeRidgeAlpha8_64').replace('ConeRidge20','ConeRidgeAlpha40').replace('bank20','bank40')
    causal=counts(causal,{'20':'40','4':'8'}).replace('actual20','actual40').replace('and20_','and40_').replace('all20 heads','all40 heads').replace('four saved','eight saved')
    causal_path=save('verify_ConeRidgeAlpha40_causal_refit_v1_20261008.py',causal)
    sources=[Path(__file__),old,native,source_small,small_path,source_probe,probe_path,source_bank,bank_path,source_causal,causal_path,
        A/'nonflag_SpectralGram64_streamed_v1_20261008.py',A/'nonflag_HuberIRLS64_own_window_v1_20261008.py',
        A/'nonflag_residual_HGB_preprocessing_20261007.py',A/'memory_bounded_numeric_preparation_20261007.py',A/'nonflag_residual_Ridge_codec_20261007.py']
    old_plan=read(A/'nonflag_ConeRidge64_bank20_plan_v1_20261008.json');plan=dict(old_plan)
    plan.update(status='frozen_before_actual40_new_alpha_own_mature_fits_and_any_quality',at_local=time.strftime('%Y-%m-%dT%H:%M:%S'),
        input_sha256={str(p):sha(p) for p in sources},configurations=module.CONFIGS,actual_declared_native_fits=40,
        alpha_values=list(ALPHAS),native_solver_and_export_kind_unmodified_except_declared_alpha_tuple=True,
        solver_AST_parameter_only_change_verified=True,previous_native_source_sha256=sha(old),
        prior_alpha_values=[.01,.1],no_previous_configuration_duplicates=True,
        own_actual200k_and_independent_BVLS_required_before_bank=True,
        complete_current_comparison_freeze_and_official_scoring_candidate_full_replay_and_board_main_still_required=True,
        actual_official_scores=0,test_labels_read=False,global_exhaustion_claimed=False)
    plan_path=A/'nonflag_ConeRidgeAlpha8_64_bank40_plan_v1_20261008.json';create(plan_path,plan)
    driver=f'''"""Serial real alpha probes and40 own-window bank fits, before any candidate quality."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha
def main():
    plan=read(A/'{plan_path.name}')
    for path,digest in plan['input_sha256'].items():assert sha(path)==digest,path
    from {small_path.stem} import main as small
    from {probe_path.stem} import main as probe
    from {bank_path.stem} import main as bank
    small();probe();bank()
if __name__=='__main__':main()
'''
    pipeline=save('run_ConeRidgeAlpha8_actual_admission_bank_v1_20261008.py',driver)
    # The causal driver waits on this real combined service name, not an unlaunched bank-only service.
    launch_name='nonflag_ConeRidgeAlpha8_64_bank40_v1_20261008'
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    pins={str(p):sha(p) for p in [*sources,plan_path,pipeline]}
    rows={launch_name:start(launch_name,pipeline.name,[],pins)}
    causal_name='ConeRidgeAlpha40_causal_refit_v1_20261008';rows[causal_name]=start(causal_name,causal_path.name,[],pins)
    create(A/'ConeRidgeAlpha8_actual_controls_hidden_launches_v1_20261008.json',{
        'status':'started_eight_uncovered_alpha_actual_small200k40_annual_fits_and40_causal_refits',
        'input_sha256':pins,'launches':rows,'CPU_threads_per_worker':2,'large_outputs_on_E':True,
        'prior143_and_neural_and135141_workers_changed':0,'new_official_scores':0,'test_labels_read':False})
    print('Eight new alpha heads frozen; real synthetic/200k admission then40 own-window fits and40 causal refits started consoleless.',flush=True)
if __name__=='__main__':main()
