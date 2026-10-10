"""New rank1d capacity hypothesis; immutable own fits, independent controls and TRAIN screens."""
from pathlib import Path
import sys, importlib
A=Path(__file__).resolve().parent
sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import create,sha
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service

def route(text):
    text=text.replace('stock_rank_embedding','stock_rank_wide_embedding').replace('StockRankEmbeddingSmall512','StockRankWideEmbedding1024').replace('small512','wide1024')
    # The mature target population and verified input fixture are reused exactly.
    text=text.replace('stock_rank_wide_embedding_mature_population','stock_rank_embedding_mature_population').replace('stock_rank_wide_embedding_mature_fixture','stock_rank_embedding_mature_fixture')
    text=text.replace('embedding16_cross120_rank1d_recent252_wide1024_BF16_e24','embedding32_cross120_rank1d_recent252_wide1024_BF16_e64')
    text=text.replace('[512, 256, 128]','[1024, 512, 256]').replace("'epochs': 24","'epochs': 64").replace("'stock_embedding_dim':16","'stock_embedding_dim':32").replace('(4651,16)','(4651,32)')
    text=text.replace("len(bundle['training_losses']) == 24","len(bundle['training_losses']) == 64").replace("len(original['training_losses'])==24","len(original['training_losses'])==64").replace('24 fixed epochs','64 fixed epochs')
    return text

def save(name,text):
    p=A/name;assert not p.exists(),p
    compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p

def main():
    assert allowed(); inputs=[]; outputs=[]
    originals=[
      'stock_rank_embedding_small512_BF16_native_v1_20261010.py',
      'stock_rank_embedding_saved_tensor_decoder_v1_20261010.py',
      'verify_stock_rank_embedding_small512_restart_v1_20261010.py',
      'verify_stock_rank_embedding_small512_small_CPU_v1_20261010.py',
      'train_stock_rank_embedding_small512_BF16_bank6_checkpoint_yield_priority173_v2_20261010.py',
      'verify_stock_rank_embedding_small512_full5_independent_v1_20261010.py',
      'stock_rank_embedding_after_complete_qualified_parent_native_stage_v1_20261010.py',
      'verify_stock_rank_embedding_six_state_native42_v1_20261010.py']
    for name in originals:
        p=A/name;inputs.append(p);text=route(p.read_text(encoding='utf8'))
        if 'native_stage' in name:text=text.replace('(169,170,171,172,173)','(169,170,171,172,173,174,175,176,177,178,179,180)')
        outputs.append(save(route(name),text))
    for kind in ('fast17','large_allocation29'):
        p=A/f'run_stock_rank20_embedding_after173_{kind}_screen_v1_20261010.py';inputs.append(p)
        text=p.read_text(encoding='utf8').replace('stock_rank20_embedding','stock_rank_embedding').replace('StockRank20EmbeddingSmall512','StockRankEmbeddingSmall512').replace('rank20mean','rank1d').replace('own_rank20_mean_Huber','own_rank1d_Huber')
        text=text.replace('embedding16_cross120_rank1d_recent252_small512_BF16_e64','embedding16_cross120_rank1d_recent252_small512_BF16_e24')
        text=route(text).replace('StockEmbedding173_complete36_family_v3_20261010','StockRankDual174_verified_candidate_registration_recovery_v3_20261010').replace("release['scored_records']==36","release['scored_records']==44").replace('173','174')
        outputs.append(save(f'run_stock_rank_wide_embedding_after174_{kind}_screen_v1_20261010.py',text))
    native=importlib.import_module(outputs[0].stem)
    assert native.CONFIG['hidden']==[1024,512,256] and native.CONFIG['stock_embedding_dim']==32 and native.CONFIG['epochs']==64 and native.CONFIG['target']=='y_rank'
    for p in outputs:importlib.import_module(p.stem)
    assert len(importlib.import_module(outputs[-2].stem).cases())==17 and len(importlib.import_module(outputs[-1].stem).cases())==29
    proof=A/'stock_rank_wide_embedding_native_stage_and_fast17_sources_admission_v1_20261010.json'
    create(proof,{'status':'compiled_frozen_rank1d_ID32_wide1024_own64_sources_actual_controls_and_scores_pending','input_sha256':{str(p):sha(p) for p in [Path(__file__),*inputs,*outputs]},'configuration':native.CONFIG,'baseline_round':174,'all_model_fits_start_from_own_seed':True,'reused_centered_target_fixture_no_second_centering':True,'new_quality_scores':0,'test_labels_read':False,'actual_future_X_read':False})
    tasks=[
      ('actual_stock_rank_wide_embedding_wide1024_restart_v1_20261010',outputs[2].name),
      ('StockRankWideEmbedding1024_independent_small_CPU_v1_20261009',outputs[3].name),
      ('actual_stock_rank_wide_embedding_wide1024_bank6_v1_20261010',outputs[4].name),
      ('StockRankWideEmbedding1024_independent_full5_GPU_controls_v1_20261009',outputs[5].name),
      ('actual_stock_rank_wide_embedding_six_state_native42_v1_20261010',outputs[7].name),
      ('actual_stock_rank_wide_embedding_after174_fast17_screen_v1_20261010',outputs[8].name),
      ('actual_stock_rank_wide_embedding_after174_large_allocation29_screen_v1_20261010',outputs[9].name)]
    queue='''from pathlib import Path
import sys,time
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_ready_goss_full_execution_20261006 import start_service
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
def main():
    assert allowed()
    closed('actual_stock_rank20_embedding_six_state_native42_v1_20261010')
    proof=A/PROOF
    for p,d in read(proof)['input_sha256'].items():assert sha(p)==d,p
    for name,driver in TASKS:
        assert allowed();p=A/driver
        row=start_service(name,driver,[],{str(p):sha(p),str(proof):sha(proof)})
        create(A/(name+'_activation.json'),row)
        while owned(row):
            assert allowed();time.sleep(15)
        assert read(A/'service_owned_workflows_20261006'/name/'service_execution.json')['status']=='passed',name
if __name__=='__main__':main()
'''.replace('PROOF',repr(proof.name)).replace('TASKS',repr(tasks))
    driver=save('run_stock_rank_wide_embedding1024_ID32_own64_controls46_queue_v1_20261010.py',queue)
    assert allowed()
    name='actual_stock_rank_wide_embedding1024_ID32_own64_controls46_queue_v1_20261010'
    row=start_service(name,driver.name,[],{str(driver):sha(driver),str(proof):sha(proof)})
    create(A/(name+'_activation.json'),row)
    print({'distinct_rank1d_ID32_1024_512_256_own64_fits_queued':True,'records':46,'quality_pending':True},flush=True)
if __name__=='__main__':main()
