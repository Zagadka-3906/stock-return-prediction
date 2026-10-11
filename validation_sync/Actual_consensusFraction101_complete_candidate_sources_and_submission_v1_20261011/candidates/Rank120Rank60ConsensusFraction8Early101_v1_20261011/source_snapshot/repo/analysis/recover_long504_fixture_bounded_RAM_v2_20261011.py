"""Replace only two idle helpers; reduce the small CPU fixture's inherited annual-fit RAM guard."""
from pathlib import Path
import sys,subprocess,psutil
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service,retire
def verify_idle(name,expected):
    row=read(A/'service_owned_workflows_20261006'/name/'native_launch.json')
    assert not psutil.Process(row['owned_worker_pid']).children()
    spy=A.parent/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'
    stack=subprocess.run([str(spy),'dump','--pid',str(row['owned_worker_pid'])],capture_output=True,text=True,encoding='utf8',check=True).stdout
    assert '(idle)' in stack and expected in stack
    return row,stack
def main():
    assert allowed()
    oldfixture='StockRank20LongEmbedding_actual_mature_fixture_CPU_v1_20261010'
    oldqueue='actual_stock_rank20long_embedding_504_own64_controls46_queue_v1_20261011'
    rows=[verify_idle(oldfixture,'main (verify_stock_rank20long_embedding_actual_mature_fixture_v1_20261010.py:10)'),
        verify_idle(oldqueue,'closed (prepare_protected_tail_pilot76_and_selected_native14_v1_20261010.py:')]
    source=A/'verify_stock_rank20long_embedding_actual_mature_fixture_v1_20261010.py'
    assert not Path('E:/赛题五_本机临时/stock_rank20long_embedding_mature_fixture_v1_20261010').exists()
    import polars as pl
    from run import FEATURE_FILE
    import recent504_rank20_mature_training_population_v1_20261011 as population
    cfg=read(A/'stock_rank20long_embedding_own64_native_sources_preparation_v1_20261010.json')['configuration']
    query=population.training_frame(pl.scan_parquet(FEATURE_FILE),20191231,cfg).select('ts_code','trade_date','label_end_20d','y_ret_20mean','y_rank_20mean')
    plan=query.explain(optimized=True)
    stats=pl.scan_parquet(FEATURE_FILE).filter(pl.col('is_train')&(pl.col('trade_date')<20191231)).select(pl.len().alias('rows'),pl.col('trade_date').n_unique().alias('dates')).collect().row(0,named=True)
    # Conservative host array allowance: 8 copies of 128 bytes for every past row,
    # 8 copies of the actual complete 13-day peer120 fixture, plus 1 GiB for imports.
    array_bound=stats['rows']*128*8+13*4650*120*4*8+2**30
    assert array_bound<4*2**30 and stats['dates']==486
    text=source.read_text(encoding='utf8');old='while psutil.virtual_memory().available<11*2**30:'
    assert text.count(old)==1
    text=text.replace(old,'while psutil.virtual_memory().available<5*2**30:')
    assert text.replace('<5*2**30:','<11*2**30:')==source.read_text(encoding='utf8')
    driver=A/'verify_stock_rank20long_embedding_actual_mature_fixture_bounded_RAM_v2_20261011.py'
    assert not driver.exists();compile(text,str(driver),'exec');driver.write_text(text,encoding='utf8',newline='\n')
    queue_source=A/'run_stock_rank20long_embedding_504_own64_controls46_queue_v1_20261011.py'
    queue_text=queue_source.read_text(encoding='utf8').replace(oldfixture,'StockRank20LongEmbedding_actual_mature_fixture_CPU_bounded_RAM_v2_20261011')
    queue=A/'run_stock_rank20long_embedding_504_own64_controls46_queue_v2_20261011.py'
    assert not queue.exists();compile(queue_text,str(queue),'exec');queue.write_text(queue_text,encoding='utf8',newline='\n')
    proof=A/'long504_fixture_bounded_RAM_actual_source_and_idle_controls_v2_20261011.json'
    create(proof,{'status':'verified_exact_idle_helpers_and_only_CPU_fixture_guard_change_before_any_fixture_output',
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),source,driver,queue_source,queue,FEATURE_FILE]},
        'actual_past_population':stats,'optimized_projection_plan':plan,'conservative_host_array_allowance_bytes':array_bound,
        'new_RAM_guard_GiB':5,'old_guard_GiB':11,'annual_fit_RAM_guard_GiB_unchanged':13,
        'CPU_fixture_mathematics_byte_identical_except_wait_guard':True,'idle_evidence':[{'identity':r,'stack':s} for r,s in rows],
        'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})
    for row,stack in rows:retire(row,'Verified childless idle helper; small CPU fixture inherited an 11GiB annual-fit guard. Only fixture wait guard changes to5GiB; annual fit retains13GiB.')
    for name,p in [('StockRank20LongEmbedding_actual_mature_fixture_CPU_bounded_RAM_v2_20261011',driver),('actual_stock_rank20long_embedding_504_own64_controls46_queue_v2_20261011',queue)]:
        assert allowed();row=start_service(name,p.name,[],{str(p):sha(p),str(proof):sha(proof)})
        create(A/(name+'_activation.json'),row)
    print({'actual_small_fixture_recovery2_started':True,'conservative_host_allowance_GiB':array_bound/2**30,'mathematics_unchanged':True},flush=True)
if __name__=='__main__':main()
