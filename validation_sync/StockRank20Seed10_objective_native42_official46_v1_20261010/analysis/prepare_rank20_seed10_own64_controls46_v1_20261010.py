"""Predeclare a truly independent Rank20 seed bank using the verified unchanged population."""
from pathlib import Path
import sys, importlib, json
A=Path(__file__).resolve().parent; ROOT=A.parent
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service

def route(text):
    text=text.replace('stock_rank20_embedding','stock_rank20seed10_embedding').replace('StockRank20Embedding','StockRank20Seed10Embedding')
    # The target and mature cohort are exactly unchanged: reuse their real controls.
    text=text.replace('actual_stock_rank20seed10_embedding_mature_fixture_location','actual_stock_rank20_embedding_mature_fixture_location')
    return text.replace("'seed': 20261009", "'seed': 20261010")

def save(name,text):
    p=A/name; assert not p.exists(),p
    compile(text,str(p),'exec'); p.write_text(text,encoding='utf8',newline='\n'); return p

def main():
    assert allowed()
    originals=[
        'stock_rank20_embedding_small512_BF16_native_v1_20261010.py',
        'stock_rank20_embedding_saved_tensor_decoder_v1_20261010.py',
        'verify_stock_rank20_embedding_small512_restart_v1_20261010.py',
        'verify_stock_rank20_embedding_small512_small_CPU_v1_20261010.py',
        'train_stock_rank20_embedding_small512_BF16_bank6_own64_v1_20261010.py',
        'verify_stock_rank20_embedding_small512_full5_independent_v1_20261010.py',
        'stock_rank20_embedding_after_complete_qualified_parent_native_stage_v1_20261010.py',
        'verify_stock_rank20_embedding_six_state_native42_v1_20261010.py']
    inputs=[A/n for n in originals]; outputs=[]
    for p in inputs:
        text=route(p.read_text(encoding='utf8'))
        if p.name.startswith('train_'):
            # Memory and deadline waits must also honor the current user stop.
            text=text.replace('while psutil.virtual_memory().available < 11 * 2**30: time.sleep(15)',
                'while psutil.virtual_memory().available < 11 * 2**30:\n            assert __import__("prepare_protected_tail_pilot76_and_selected_native14_v1_20261010").allowed(); time.sleep(15)')
        outputs.append(save(route(p.name),text))
    for kind in ('fast17','large_allocation29'):
        p=A/f'run_stock_rank20_embedding_after173_{kind}_screen_v1_20261010.py'; inputs.append(p)
        text=route(p.read_text(encoding='utf8'))
        text=text.replace("closed('StockEmbedding173_complete36_family_v3_20261010')",
            "closed('StockTop10Embedding175_selected_candidate_sealing_recovery_v2_20261010')")
        text=text.replace("release['scored_records']==36","release['scored_records']==47").replace('173','175')
        if kind=='fast17':
            # Allocate half the initial comparisons to the observed useful negative tiny-CDF region.
            text=text.replace('for sign in (1.,-1.):\n        for weight in (.00025,.001,.004,.016):',
                'for sign in (1.,-1.):\n        for weight in (.00015625,.0003125,.000625,.00125):')
        outputs.append(save(f'run_stock_rank20seed10_embedding_after175_{kind}_screen_v1_20261010.py',text))
    modules=[importlib.import_module(p.stem) for p in outputs]
    native=modules[0]
    old=importlib.import_module('stock_rank20_embedding_small512_BF16_native_v1_20261010')
    before=dict(old.CONFIG); after=dict(native.CONFIG)
    for k in ('seed','recipe'): before.pop(k); after.pop(k)
    assert before==after and native.CONFIG['seed']==20261010 and native.CONFIG['epochs']==64
    assert list(modules[6].BACKENDS)==['stock_rank20seed10_embedding16_cross120_rank20mean_recent252_small512_BF16_e64']
    assert len(modules[-2].cases())==17 and len(modules[-1].cases())==29
    shared=[A/'recent252_rank20_mature_population_actual_CPU_controls_v1_20261010.json',
        A/'recent252_rank20_mature_training_population_v1_20261010.py',
        A/'forward20_mature_training_labels_v1_20261010.py',
        A/'actual_stock_rank20_embedding_mature_fixture_location_v1_20261010.json']
    fixture=Path(read(shared[-1])['output']); shared += [fixture/'verification.json',fixture/'past_features121.npy',fixture/'past_rank20_targets.npy']
    assert read(shared[0])['status'].startswith('passed7_')
    assert read(fixture/'verification.json')['last_label_end']<20191231
    proof=A/'stock_rank20seed10_embedding_own64_controls46_sources_admission_v1_20261010.json'
    create(proof,{'status':'compiled_and_API_checked_actual_independent_seed10_bank_training_pending',
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),*inputs,*outputs,*shared]},
        'configuration':native.CONFIG,'baseline_round':175,'new_quality_scores':0,'new_native_fits':0,
        'unchanged_population_and_fixture_reused_explicitly':True,
        'independent_seed_not_loaded_parent_weights':True,'actual_future_X_read':False,'test_labels_read':False,
        'hypothesis':'independent initialization of the strongest observed long-horizon rank complement; TRAIN adaptive hypothesis, no claimed blind validation'})
    admission=A/'stock_rank20seed10_embedding_native_stage_and_fast17_sources_admission_v1_20261010.json'
    create(admission,read(proof)); assert sha(admission)==sha(proof)
    tasks=[('actual_stock_rank20seed10_embedding_small512_restart_v1_20261010',outputs[2].name),
        ('StockRank20Seed10EmbeddingSmall512_independent_small_CPU_v1_20261009',outputs[3].name),
        ('actual_stock_rank20seed10_embedding_small512_bank6_v1_20261010',outputs[4].name),
        ('StockRank20Seed10EmbeddingSmall512_independent_full5_GPU_controls_v1_20261009',outputs[5].name),
        ('actual_stock_rank20seed10_embedding_six_state_native42_v1_20261010',outputs[7].name),
        ('actual_stock_rank20seed10_embedding_after175_fast17_screen_v1_20261010',outputs[8].name),
        ('actual_stock_rank20seed10_embedding_after175_large_allocation29_screen_v1_20261010',outputs[9].name)]
    queue='''from pathlib import Path
import sys,time
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_ready_goss_full_execution_20261006 import start_service
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
def main():
    assert allowed()
    closed('actual_stock_toppair_embedding_six_state_native42_v1_20261010')
    proof=A/PROOF
    for p,d in read(proof)['input_sha256'].items():assert sha(p)==d,p
    for name,driver in TASKS:
        assert allowed();p=A/driver
        row=start_service(name,driver,[],{str(p):sha(p),str(proof):sha(proof)})
        create(A/(name+'_activation.json'),row)
        while owned(row): assert allowed();time.sleep(15)
        assert read(A/'service_owned_workflows_20261006'/name/'service_execution.json')['status']=='passed',name
if __name__=='__main__':main()
'''.replace('PROOF',repr(proof.name)).replace('TASKS',repr(tasks))
    driver=save('run_stock_rank20seed10_embedding_own64_controls46_queue_v1_20261010.py',queue)
    # Actual GPU restart and new six fits are required; no old seed proof is relabeled.
    assert allowed()
    row=start_service('actual_stock_rank20seed10_embedding_own64_controls46_queue_v1_20261010',driver.name,[],{str(driver):sha(driver),str(proof):sha(proof)})
    create(A/'actual_stock_rank20seed10_embedding_own64_controls46_queue_v1_20261010_activation.json',row)
    print({'new_seed':20261010,'planned_own_fits':6,'planned_TRAIN_cases':46,'new_scores_completed':0},flush=True)
if __name__=='__main__':main()
