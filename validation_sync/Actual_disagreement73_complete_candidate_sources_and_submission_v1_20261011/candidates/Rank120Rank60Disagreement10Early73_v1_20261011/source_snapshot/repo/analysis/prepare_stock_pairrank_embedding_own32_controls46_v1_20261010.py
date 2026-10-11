"""New date-local pairwise objective with stock identity and cross120; own32 fixed epochs."""
from pathlib import Path
import sys,importlib
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service

def route(text):
    text=text.replace('stock_rank_embedding','stock_pairrank_embedding').replace('StockRankEmbeddingSmall512','StockPairRankEmbeddingSmall512')
    text=text.replace('stock_pairrank_embedding_mature_population','stock_rank_embedding_mature_population').replace('stock_pairrank_embedding_mature_fixture','stock_rank_embedding_mature_fixture')
    text=text.replace('embedding16_cross120_rank1d_recent252_small512_BF16_e24','embedding16_cross120_pairrank1d_recent252_small512_BF16_e32')
    text=text.replace("'epochs': 24","'epochs': 32").replace("len(bundle['training_losses']) == 24","len(bundle['training_losses']) == 32").replace("len(original['training_losses'])==24","len(original['training_losses'])==32").replace('24 fixed epochs','32 fixed epochs')
    return text

def save(name,text):
    p=A/name;assert not p.exists(),p
    compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p

def once(text,old,new):
    assert text.count(old)==1,(old,text.count(old));return text.replace(old,new)

def main():
    assert allowed()
    assert read(A/'same_day_ranknet_loss_actual_CPU_controls_v1_20261010.json')['status'].startswith('passed_')
    inputs=[];outputs=[]
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
        if name.startswith('stock_rank_embedding_small512_BF16_native'):
            text=text.replace("'loss': 'Huber'","'loss': 'same_day_pair_ranknet_Huber_aux', 'pair_temperature': .1, 'pair_aux_weight': .1")
            text=text.replace("assert cfg['loss']=='Huber'","assert cfg['loss']=='same_day_pair_ranknet_Huber_aux' and cfg['pair_temperature']==.1 and cfg['pair_aux_weight']==.1")
            text=text.replace('def fit_arrays(x, y, cfg, checkpoint_path=None, stop_after_epoch=None):','def fit_arrays(x, y, cfg, checkpoint_path=None, stop_after_epoch=None, *, training_dates):')
            text=once(text,'    identity = identity_for(x, y, cfg)',"    from same_day_ranknet_loss_v1_20261010 import date_groups,loss as pair_loss\n    assert len(training_dates)==len(y)\n    group_starts,group_sizes=date_groups(training_dates)\n    identity = identity_for(x, y, cfg)\n    identity['training_dates_sha256']=array_sha(training_dates)\n    identity['pair_loss_source_sha256']=hashlib.sha256((ROOT/'analysis/same_day_ranknet_loss_v1_20261010.py').read_bytes()).hexdigest()")
            text=once(text,'    del clean, target',"    gt=torch.from_numpy(group_starts).cuda();nt=torch.from_numpy(group_sizes).cuda()\n    del clean, target, group_starts, group_sizes")
            text=once(text,"                with torch.autocast('cuda', dtype=torch.bfloat16):\n                    pred = model(xt[part]).squeeze(-1)\n                loss = torch.nn.functional.huber_loss(pred.float(), yt[part], delta=cfg['huber_delta']) * (len(part) / len(index))", "                partner=gt[part]+(torch.rand(len(part),device='cuda')*nt[part]).long()\n                with torch.autocast('cuda', dtype=torch.bfloat16):\n                    pred = model(xt[part]).squeeze(-1)\n                    partner_pred=model(xt[partner]).squeeze(-1)\n                loss = pair_loss(pred.float(),partner_pred.float(),yt[part],yt[partner],cfg['pair_temperature'],cfg['pair_aux_weight'],cfg['huber_delta']) * (len(part) / len(index))")
            text=text.replace('del xt, yt, model, optimizer','del xt, yt, gt, nt, model, optimizer')
        if 'restart' in name:
            text=text.replace('return x, np.clip(rng.normal(0.,.03,1024),-.1,.1).astype(np.float64)','return x, np.clip(rng.normal(0.,.03,1024),-.1,.1).astype(np.float64),np.repeat(np.arange(20200101,20200117,dtype=np.int32),64)')
            text=text.replace("np.load(Path(read(A/'actual_stock_rank_embedding_mature_fixture_location_v1_20261010.json')['output'])/'past_rank_targets.npy')", "np.load(Path(read(A/'actual_stock_rank_embedding_mature_fixture_location_v1_20261010.json')['output'])/'past_rank_targets.npy'),np.load(Path(read(A/'actual_stock_pairrank_training_dates_fixture_location_v1_20261010.json')['output'])/'past_training_dates.npy')")
            text=text.replace('x, y = inputs(case)','x, y, training_dates = inputs(case)')
            text=text.replace('native.fit_arrays(x, y, cfg)','native.fit_arrays(x, y, cfg,training_dates=training_dates)').replace('stop_after_epoch=stop)','stop_after_epoch=stop,training_dates=training_dates)')
            text=text.replace("native.fit_arrays(x, y, cfg, folder / 'checkpoint.joblib')","native.fit_arrays(x, y, cfg, folder / 'checkpoint.joblib',training_dates=training_dates)")
            text=text.replace("native.fit_arrays(poisoned, y, config(case), folder / 'checkpoint.joblib')","native.fit_arrays(poisoned, y, config(case), folder / 'checkpoint.joblib',training_dates=training_dates)")
            text=text.replace('    pins = {str(p): sha(p) for p in paths}',"    dates_fixture=Path(read(A/'actual_stock_pairrank_training_dates_fixture_location_v1_20261010.json')['output'])\n    paths += [dates_fixture/'past_training_dates.npy',dates_fixture/'verification.json',A/'same_day_ranknet_loss_v1_20261010.py',A/'same_day_ranknet_loss_actual_CPU_controls_v1_20261010.json']\n    pins = {str(p): sha(p) for p in paths}")
        if name.startswith('train_'):
            text=text.replace("        y = train['y_rank'].to_numpy();","        training_dates=train['trade_date'].to_numpy()\n        y = train['y_rank'].to_numpy();")
            text=text.replace("'training_target_sha256': native.array_sha(y),","'training_target_sha256': native.array_sha(y),'training_dates_sha256':native.array_sha(training_dates),'pair_partners_within_same_date_only':True,")
            text=text.replace('stop_after_epoch=stop)','stop_after_epoch=stop,training_dates=training_dates)')
            text=text.replace("Path(population.__file__), A/'recent252", "Path(population.__file__), A/'same_day_ranknet_loss_v1_20261010.py',A/'same_day_ranknet_loss_actual_CPU_controls_v1_20261010.json', A/'recent252")
            text=text.replace('del x, y','del x, y, training_dates')
        if 'native_stage' in name:text=text.replace('(169,170,171,172,173)','(169,170,171,172,173,174,175,176,177,178,179,180,181,182,183)')
        outputs.append(save(route(name),text))
    for kind in ('fast17','large_allocation29'):
        p=A/f'run_stock_rank20_embedding_after173_{kind}_screen_v1_20261010.py';inputs.append(p)
        text=p.read_text(encoding='utf8').replace('stock_rank20_embedding','stock_rank_embedding').replace('StockRank20EmbeddingSmall512','StockRankEmbeddingSmall512').replace('rank20mean','rank1d').replace('own_rank20_mean_Huber','own_pair_ranknet_Huber_aux')
        text=text.replace('embedding16_cross120_rank1d_recent252_small512_BF16_e64','embedding16_cross120_rank1d_recent252_small512_BF16_e24')
        text=route(text).replace('StockEmbedding173_complete36_family_v3_20261010','StockRankDual174_verified_candidate_registration_recovery_v3_20261010').replace("release['scored_records']==36","release['scored_records']==44").replace('173','174')
        outputs.append(save(f'run_stock_pairrank_embedding_after174_{kind}_screen_v1_20261010.py',text))
    import numpy as np,polars as pl
    from run import FEATURE_FILE
    import stock_rank_embedding_mature_population_v1_20261010 as population
    native=importlib.import_module(outputs[0].stem)
    frame=population.training_frame(pl.scan_parquet(FEATURE_FILE),20191231,native.CONFIG).select('ts_code','trade_date','y_ret_1d','y_rank').limit(49153).collect()
    rank_fixture=Path(read(A/'actual_stock_rank_embedding_mature_fixture_location_v1_20261010.json')['output'])
    return_fixture=Path(read(A/'actual_Cross120RecentReturn252Huber050_past_fixture_location_v1_20261010.json')['output'])
    assert np.array_equal(frame['y_rank'].to_numpy(),np.load(rank_fixture/'past_rank_targets.npy'))
    assert np.array_equal(frame['y_ret_1d'].to_numpy().view('u4'),np.load(return_fixture/'past_return_targets.npy').view('u4'))
    dates=frame['trade_date'].to_numpy()
    import same_day_ranknet_loss_v1_20261010 as loss_module
    loss_module.date_groups(dates)
    out=Path('E:/赛题五_本机临时/stock_pairrank_training_dates_fixture_v1_20261010');out.mkdir(exist_ok=False)
    np.save(out/'past_training_dates.npy',dates,allow_pickle=False)
    create(out/'verification.json',{'status':'passed_actual49153_training_dates_exact_existing_centered_rank_and_return_fixture_alignment','rows':len(dates),'last':int(dates.max()),'dates_sha256':sha(out/'past_training_dates.npy'),'dates_used_only_in_training_pair_selection':True,'test_labels_read':False,'new_quality_scores':0})
    create(A/'actual_stock_pairrank_training_dates_fixture_location_v1_20261010.json',{'output':str(out),'verification_sha256':sha(out/'verification.json')})
    for p in outputs:importlib.import_module(p.stem)
    assert len(importlib.import_module(outputs[-2].stem).cases())==17 and len(importlib.import_module(outputs[-1].stem).cases())==29
    proof=A/'stock_pairrank_embedding_own32_controls46_sources_admission_v1_20261010.json'
    create(proof,{'status':'compiled_frozen_new_same_day_pairrank_ID16_cross120_recent252_own32_sources_actual_GPU_and_scores_pending','input_sha256':{str(p):sha(p) for p in [Path(__file__),*inputs,*outputs,Path(loss_module.__file__),A/'same_day_ranknet_loss_actual_CPU_controls_v1_20261010.json',out/'verification.json',out/'past_training_dates.npy']},'configuration':native.CONFIG,'new_quality_scores':0,'new_native_fits':0,'test_labels_read':False,'actual_future_X_read':False,'existing_raw63_pairwise_models_are_distinct':True})
    tasks=[('actual_stock_pairrank_embedding_small512_restart_v1_20261010',outputs[2].name),('StockPairRankEmbeddingSmall512_independent_small_CPU_v1_20261009',outputs[3].name),('actual_stock_pairrank_embedding_small512_bank6_v1_20261010',outputs[4].name),('StockPairRankEmbeddingSmall512_independent_full5_GPU_controls_v1_20261009',outputs[5].name),('actual_stock_pairrank_embedding_six_state_native42_v1_20261010',outputs[7].name),('actual_stock_pairrank_embedding_after174_fast17_screen_v1_20261010',outputs[8].name),('actual_stock_pairrank_embedding_after174_large_allocation29_screen_v1_20261010',outputs[9].name)]
    queue='''from pathlib import Path
import sys,time
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_ready_goss_full_execution_20261006 import start_service
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
def main():
    assert allowed()
    closed('StockTop10Embedding175_selected_candidate_sealing_recovery_v2_20261010')
    closed('actual_stock_rank_wide32_embedding_after174_large_allocation29_screen_v1_20261010')
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
    driver=save('run_stock_pairrank_embedding_own32_controls46_queue_v1_20261010.py',queue)
    assert allowed()
    name='actual_stock_pairrank_embedding_own32_controls46_queue_v1_20261010'
    row=start_service(name,driver.name,[],{str(driver):sha(driver),str(proof):sha(proof)})
    create(A/(name+'_activation.json'),row)
    print({'pairrank_own32_queue':row,'actual_date_fixture_rows':len(dates),'scores_pending':True},flush=True)
if __name__=='__main__':main()
