"""Execute the real candidate's selected transform on5635800 TRAIN rows; no future arrays."""
from pathlib import Path
import sys,ast,hashlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
def main():
    assert allowed();closed('actual_stock_embedding_after170_fast17_screen_v2_20261010')
    import numpy as np,polars as pl,importlib
    import stock_embedding_after_complete_qualified_parent_native_stage_v1_20261010 as stage
    source=A/'prepare_StockEmbedding173_selected_candidate_v1_20261010.py';tree=ast.parse(source.read_text(encoding='utf8'))
    assignments=[node for node in ast.walk(tree) if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='selected' for t in node.targets)]
    assert len(assignments)==1
    code=compile(ast.fix_missing_locations(ast.Module(body=assignments,type_ignores=[])),str(source)+'::actual_selected_TRAIN_transform','exec')
    screen=Path('E:/赛题五_本机临时/StockEmbeddingSmall512_after170_high_impact17_screen_v1_20261010');proof=read(screen/'verification.json')
    assert len(proof['records'])==17
    own=Path(read(A/'actual_StockEmbeddingSmall512_full5_independent_location_v1_20261009.json')['output'])
    framepath=A/'connected_validation_20261002/combined_fold_frame.parquet';parentpath=A/'optimization_20261003_r170/selected_validation.npy'
    frame=pl.read_parquet(framepath,columns=['ts_code','trade_date','flag_limit_up','price_valid']);rf=pl.read_parquet(own/'combined_raw.parquet')
    assert rf.select(['ts_code','trade_date']).equals(frame.select(['ts_code','trade_date']))
    parent=np.load(parentpath,mmap_mode='r');signal=rf['pred_raw'].to_numpy();dates,flags,valid=[frame[c].to_numpy() for c in ('trade_date','flag_limit_up','price_valid')]
    pins={str(p):sha(p) for p in [Path(__file__),source,Path(stage.__file__),screen/'verification.json',own/'verification.json',own/'combined_raw.parquet',framepath,parentpath]};records=[]
    #Three distinct actual codecs and both signs, taken from the original
    #declared cases; full5,635,800 winner reconstruction independently checked.
    for codec in stage.CODECS:
        for sign in (1.,-1.) if codec=='CDF' else (1.,):
            row=next(r for r in proof['records'] if r['configuration']['kind']==codec and r['configuration']['sign']==sign and r['configuration']['weight']==.016)
            cfg={**row['configuration'],'codec':codec};module=importlib.import_module(stage.CODECS[codec]);n=13950
            scope={'cfg':cfg,'transform':module.transform,'raw':np.asarray(parent[:n]),'neural':signal[:n],'dates':dates[:n],'flags':flags[:n],'valid':valid[:n]};exec(code,scope)
            args=(cfg['role'],cfg['weight'],cfg['sign']) if codec=='CDF' else (cfg['weight'],cfg['protect_fraction'],cfg['sign'])
            oracle=module.pandas_oracle(parent[:n],signal[:n],dates[:n],flags[:n],valid[:n],*args)
            assert np.array_equal(scope['selected'].view('u8'),oracle.view('u8'))
            records.append({'codec':codec,'sign':sign,'rows':n,'actual_candidate_statement_and_Pandas_oracle_bits_exact':True})
    best=proof['best'];cfg={**best['configuration'],'codec':best['configuration']['kind']};module=importlib.import_module(stage.CODECS[cfg['codec']])
    scope={'cfg':cfg,'transform':module.transform,'raw':parent,'neural':signal,'dates':dates,'flags':flags,'valid':valid};exec(code,scope);selected=scope['selected']
    numeric=hashlib.sha256(memoryview(np.ascontiguousarray(selected)).cast('B')).hexdigest();assert numeric==best['prediction_numeric_sha256']
    control=screen/f"case{best['case']:03d}_controls.json";assert sha(control)==best['control_sha256'] and read(control)['numeric_sha256']==numeric
    pins[str(control)]=sha(control)
    for p,d in pins.items():assert sha(p)==d,p
    create(A/'stock_embedding173_actual_candidate_TRAIN_reconstruction_CPU_controls_v1_20261010.json',{'status':'passed_actual_candidate_statement_four_real13950_TRAIN_cases_and_full5635800_stock_winner_numeric_bits','input_sha256':pins,'records':records,'full_winner_numeric_sha256':numeric,'known_completed_screen_best':best,'full_selected_future_pipeline_not_claimed':True,'all_arrays_from_TRAIN_only':True,'new_quality_scores':0,'test_labels_read':False})
    print('PASS actual candidate transform4 real13950 TRAIN cases and full5635800 winner numeric bits; actual173 future pipeline pending',flush=True)
if __name__=='__main__':main()
