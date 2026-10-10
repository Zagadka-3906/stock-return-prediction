"""Execute the actual frozen candidate's TRAIN reconstruction code on real panels and one full known winner."""
from pathlib import Path
import sys,ast,textwrap,hashlib,importlib
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create

def main():
    from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
    assert allowed()
    import numpy as np,polars as pl
    from dual_target_daily_rank_consensus_v1_20261010 import transform as consensus
    from cross120_after_complete169_native_stage_v2_20261010 import CODECS
    import budgeted_neural_Top_projection_v1_20261010 as budget
    source=A/'prepare_frontier233171_selected_candidate_v1_20261010.py';text=source.read_text(encoding='utf8')
    start=text.index('        if components:\n            signals=[]');end=text.index('        assert hashlib.sha256',start)
    block=text[start:end];assert block.count('codec.pandas_oracle')==2
    program='def actual_candidate_branch(raw,frame,cfg,components,neural_paths):\n    dates,flags,valid=[frame[k].to_numpy() for k in ("trade_date","flag_limit_up","price_valid")]\n'+textwrap.indent(textwrap.dedent(block),'    ')+'    return selected\n'
    scope={'np':np,'pl':pl,'importlib':importlib};exec(compile(program,str(source)+'::actual_TRAIN_reconstruction','exec'),scope);actual=scope['actual_candidate_branch']
    framepath=A/'connected_validation_20261002/combined_fold_frame.parquet';parentpath=A/'optimization_20261003_r169/selected_validation.npy'
    frame=pl.read_parquet(framepath,columns=['ts_code','trade_date','flag_limit_up','price_valid']);parent=np.load(parentpath,mmap_mode='r')
    assert len(frame)==len(parent)==5635800
    dates,flags,valid=[frame[k].to_numpy() for k in ('trade_date','flag_limit_up','price_valid')]
    recipes=['cross120recent252forward5huber050','cross120recent252rank5huber050'];pointerfiles=['actual_BF16Cross120Recent252Forward5Huber050173_full5_independent_location_v1_20261009.json','actual_BF16Cross120Recent252Rank5Huber050174_full5_independent_location_v1_20261009.json']
    paths=[Path(read(A/n)['output'])/'combined_raw.parquet' for n in pointerfiles]
    real=[pl.read_parquet(p).head(13950) for p in paths]
    assert all(f.select(['ts_code','trade_date']).equals(frame.head(13950).select(['ts_code','trade_date'])) for f in real)
    # Route only the actual saved TRAIN panels; no data creation or future access is needed.
    original_read=pl.read_parquet;fixture_by_path=dict(zip(paths,real));pl.read_parquet=lambda path,*args,**kwargs:fixture_by_path[Path(path)]
    plan=read(A/'dual120_consensus193_predeclared_training_only_selection_plan_v1_20261010.json')['cases']
    probes=[]
    try:
        for mixture in (.25,.5,.75):
            for kind in ('CDF','valid_pool_protection_v1','official_Top_protection_v2'):
                for sign in (1.,-1.):
                    cfg=next(dict(c) for c in plan if c['mean_weight']==mixture and c['kind']==kind and c['sign']==sign)
                    panel=frame.head(13950);raw=parent[:13950];value=actual(raw,panel,cfg,[{},{}],paths)
                    mixed=consensus(*(f['pred_raw'].to_numpy() for f in real),panel['trade_date'].to_numpy(),mixture)
                    codec=importlib.import_module(CODECS[kind]);args=(panel['trade_date'].to_numpy(),panel['flag_limit_up'].to_numpy(),panel['price_valid'].to_numpy(),*((cfg['role'],cfg['weight'],sign) if kind=='CDF' else (cfg['weight'],cfg['protect_fraction'],sign)))
                    expected=codec.transform(raw,mixed,*args);assert np.array_equal(value.view('u8'),expected.view('u8'))
                    original_fixture=dict(fixture_by_path)
                    for n in (4650,9300):
                        fixture_by_path.update({p:f.head(n) for p,f in original_fixture.items()});cold=actual(raw[:n],panel.head(n),cfg,[{},{}],paths);assert np.array_equal(cold.view('u8'),value[:n].view('u8'))
                    fixture_by_path.update(original_fixture);probes.append({'configuration':cfg,'actual_rows':13950,'actual_candidate_code_matches_screen_kernel':True,'cold4650_9300_exact':True})
    finally:pl.read_parquet=original_read
    proofpath=Path('E:/赛题五_本机临时/parent169_causal_Top_stability19_screen_v1_20261010/verification.json');known=read(proofpath)
    budgets=[]
    for row in known['records'][1:]:
        cfg=row['configuration'];value=actual(parent[:13950],frame.head(13950),cfg,[],[])
        expected=budget.transform(parent[:13950],np.asarray(parent[:13950]),dates[:13950],flags[:13950],valid[:13950],1.,cfg['budget_fraction'],cfg['margin'],1.)
        assert np.array_equal(value.view('u8'),expected.view('u8'))
        for n in (4650,9300):assert np.array_equal(actual(parent[:n],frame.head(n),cfg,[],[]).view('u8'),value[:n].view('u8'))
        budgets.append({'configuration':cfg,'actual_rows':13950,'actual_candidate_code_matches_known_kernel':True,'cold4650_9300_exact':True})
    best=known['best'];assert best['case']>0
    value=actual(parent,frame,best['configuration'],[],[])
    digest=hashlib.sha256(memoryview(np.ascontiguousarray(value)).cast('B')).hexdigest();assert digest==best['prediction_numeric_sha256']
    assert len(probes)==len(budgets)==18
    inputs=[Path(__file__),source,framepath,parentpath,proofpath,*paths,*[A/n for n in pointerfiles]]
    create(A/'frontier233171_actual_candidate_TRAIN_reconstruction_CPU_controls_v1_20261010.json',{'status':'passed_actual_generated_candidate_TRAIN_reconstruction18_dual18_budget_and_full5635800_known_budget_winner','input_sha256':{str(p):sha(p) for p in inputs},'dual_actual_CPU_cases':probes,'budget_actual_CPU_cases':budgets,'full_known_budget_winner_numeric_sha256':digest,'full_known_official_score':best['connected_final_score'],'new_quality_scores':0,'actual_GPU_inference_claimed':False,'actual_future_X_read':False,'test_labels_read':False})
    print({'actual_dual_cases':18,'actual_budget_cases':18,'full_known_budget_winner_rows':len(value),'new_quality_scores':0},flush=True)

if __name__=='__main__':main()
