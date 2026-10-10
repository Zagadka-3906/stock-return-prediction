"""Predeclare a genuinely new 504-origin Rank20 bank, with an independently verified new fixture."""
from pathlib import Path
import sys,re,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service
def route(text):
    text=text.replace('stock_rank20_embedding','stock_rank20long_embedding').replace('StockRank20Embedding','StockRank20LongEmbedding')
    text=text.replace('recent252_rank20_mature_training_population_v1_20261010','recent504_rank20_mature_training_population_v1_20261011')
    text=text.replace('recent252_rank20_mature_population_actual_CPU_controls_v1_20261010','recent504_rank20_mature_population_actual_CPU_controls_v1_20261011')
    text=text.replace('recent252','recent504').replace('rolling252','rolling504')
    return re.sub(r'\b252\b','504',text)
def save(name,text):
    p=A/name;assert not p.exists(),p;compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p
def main():
    assert allowed();cpu=A/'recent504_rank20_population_preparation_v1_20261011.json'
    assert read(cpu)['actual504_truncation_exercised']
    originals=[
        'stock_rank20_embedding_small512_BF16_native_v1_20261010.py','stock_rank20_embedding_saved_tensor_decoder_v1_20261010.py',
        'verify_stock_rank20_embedding_small512_restart_v1_20261010.py','verify_stock_rank20_embedding_small512_small_CPU_v1_20261010.py',
        'train_stock_rank20_embedding_small512_BF16_bank6_own64_v1_20261010.py','verify_stock_rank20_embedding_small512_full5_independent_v1_20261010.py',
        'stock_rank20_embedding_after_complete_qualified_parent_native_stage_v1_20261010.py','verify_stock_rank20_embedding_six_state_native42_v1_20261010.py']
    inputs=[A/n for n in originals];outputs=[]
    for p in inputs:
        text=route(p.read_text(encoding='utf8'))
        if p.name.startswith('train_'):
            text=text.replace('while psutil.virtual_memory().available < 11 * 2**30: time.sleep(15)',
                'while psutil.virtual_memory().available < 13 * 2**30:\n            assert __import__("prepare_protected_tail_pilot76_and_selected_native14_v1_20261010").allowed(); time.sleep(15)')
        outputs.append(save(route(p.name),text))
    for kind in ('fast17','large_allocation29'):
        p=A/f'run_stock_rank20_embedding_after173_{kind}_screen_v1_20261010.py';inputs.append(p)
        text=route(p.read_text(encoding='utf8'))
        text=text.replace("closed('StockEmbedding173_complete36_family_v3_20261010')","closed('StockTop10Embedding175_selected_candidate_sealing_recovery_v2_20261010')")
        text=text.replace("release['scored_records']==36","release['scored_records']==47").replace('173','175')
        if kind=='fast17':text=text.replace('(.00025,.001,.004,.016)','(.00015625,.0003125,.00125,.004)')
        outputs.append(save(f'run_stock_rank20long_embedding_after175_{kind}_screen_v1_20261010.py',text))
    modules=[importlib.import_module(p.stem) for p in outputs];native=modules[0]
    assert native.CONFIG['epochs']==64 and native.CONFIG['training_calendar_window']==504 and native.CONFIG['target']=='y_rank_20mean'
    assert len(modules[-2].cases())==17 and len(modules[-1].cases())==29
    fixture=A/'verify_stock_rank20long_embedding_actual_mature_fixture_v1_20261010.py'
    prep=A/'stock_rank20long_embedding_own64_native_sources_preparation_v1_20261010.json'
    create(prep,{'status':'compiled_long504_rank20_own64_sources_before_new_fixture_GPU_and_official_scores',
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),*inputs,*outputs,fixture,cpu,A/'recent504_rank20_mature_training_population_v1_20261011.py',A/'recent504_rank20_mature_population_actual_CPU_controls_v1_20261011.json']},
        'configuration':native.CONFIG,'baseline_round':175,'new_native_fits':0,'new_quality_scores':0,
        'actual_future_X_read':False,'test_labels_read':False,'long_window_synthetic504_truncation_verified':True})
    admission=A/'stock_rank20long_embedding_native_stage_and_fast17_sources_admission_v1_20261010.json'
    create(admission,read(prep));assert sha(admission)==sha(prep)
    tasks=[('actual_stock_rank20long_embedding_small512_restart_v1_20261010',outputs[2].name),
        ('StockRank20LongEmbeddingSmall512_independent_small_CPU_v1_20261009',outputs[3].name),
        ('actual_stock_rank20long_embedding_small512_bank6_v1_20261010',outputs[4].name),
        ('StockRank20LongEmbeddingSmall512_independent_full5_GPU_controls_v1_20261009',outputs[5].name),
        ('actual_stock_rank20long_embedding_six_state_native42_v1_20261010',outputs[7].name),
        ('actual_stock_rank20long_embedding_after175_fast17_screen_v1_20261010',outputs[8].name),
        ('actual_stock_rank20long_embedding_after175_large_allocation29_screen_v1_20261010',outputs[9].name)]
    queue='''from pathlib import Path
import sys,time
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
from handoff_ready_goss_full_execution_20261006 import start_service
def main():
    assert allowed();closed('StockRank20LongEmbedding_actual_mature_fixture_CPU_v1_20261010')
    closed('actual_rank20_two_seed_native84_v1_20261010')
    proof=A/PROOF
    for p,d in read(proof)['input_sha256'].items():assert sha(p)==d,p
    for name,driver in TASKS:
        assert allowed();p=A/driver;row=start_service(name,driver,[],{str(p):sha(p),str(proof):sha(proof)})
        create(A/(name+'_activation.json'),row)
        while owned(row):assert allowed();time.sleep(15)
        assert read(A/'service_owned_workflows_20261006'/name/'service_execution.json')['status']=='passed',name
if __name__=='__main__':main()
'''.replace('PROOF',repr(prep.name)).replace('TASKS',repr(tasks))
    driver=save('run_stock_rank20long_embedding_504_own64_controls46_queue_v1_20261011.py',queue)
    for name,p in [('StockRank20LongEmbedding_actual_mature_fixture_CPU_v1_20261010',fixture),('actual_stock_rank20long_embedding_504_own64_controls46_queue_v1_20261011',driver)]:
        assert allowed();row=start_service(name,p.name,[],{str(p):sha(p),str(prep):sha(prep)})
        create(A/(name+'_activation.json'),row)
    print({'planned_long504_own_fits':6,'planned_official_cases':46,'new_actual_fixture_required':True,'GPU_waits_actual_two_seed_native84':True},flush=True)
if __name__=='__main__':main()
