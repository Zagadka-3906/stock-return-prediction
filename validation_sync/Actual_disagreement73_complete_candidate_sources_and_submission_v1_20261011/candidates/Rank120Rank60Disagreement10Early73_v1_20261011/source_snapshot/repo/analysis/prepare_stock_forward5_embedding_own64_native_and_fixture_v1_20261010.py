"""Prepare a distinct stock-identity five-day-return recipe and actual mature input controls."""
from pathlib import Path
import sys,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service
def save(name,text):
    p=A/name;assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p
def main():
    assert allowed();source=A/'stock_embedding_small512_BF16_native_v1_20261010.py'
    text=source.read_text(encoding='utf8').replace("'target': 'y_ret_1d'","'target': 'y_ret_5mean'").replace("cfg['target'] == 'y_ret_1d'","cfg['target'] == 'y_ret_5mean'").replace("'epochs': 24","'epochs': 64").replace("'training_calendar_window':252","'label_horizon_trading_days':5,'training_calendar_window':252").replace('own_mature_stock_embedding16_cross120_return1d_recent252_small512_BF16_e24_v1_20261010','own_mature_stock_forward5_embedding16_cross120_return5mean_recent252_small512_BF16_e64_v1_20261010')
    native=save('stock_forward5_embedding_small512_BF16_native_v1_20261010.py',text)
    decoder_source=A/'stock_embedding_saved_tensor_decoder_v1_20261010.py'
    decoder=save('stock_forward5_embedding_saved_tensor_decoder_v1_20261010.py',decoder_source.read_text(encoding='utf8').replace('own_mature_stock_embedding16_cross120_return1d_recent252_small512_BF16_e24_v1_20261010','own_mature_stock_forward5_embedding16_cross120_return5mean_recent252_small512_BF16_e64_v1_20261010'))
    cfg=importlib.import_module(native.stem).CONFIG
    assert cfg['target']=='y_ret_5mean' and cfg['epochs']==64 and cfg['label_horizon_trading_days']==5 and cfg['return_target_scale']==20.
    plan=A/'stock_forward5_embedding_own64_native_sources_preparation_v1_20261010.json'
    create(plan,{'status':'prospective_distinct_stock_identity_forward5_mean_return_Huber_e64_native_sources_actual_fixture_pending','input_sha256':{str(p):sha(p) for p in [Path(__file__),source,decoder_source,native,decoder,A/'recent252_forward5_mature_training_population_v1_20261010.py',A/'recent252_forward5_mature_population_actual_CPU_controls_v1_20261010.json',A/'forward5_mature_training_labels_v1_20261010.py']},'configuration':cfg,'reason':'Uncovered identity-embedding five-day return magnitude target; contrast with five-day rank target, without repeating prior recipe; official annual excess and turnover determine actual merit','new_fits':0,'new_quality_scores':0,'actual_future_X_read':False,'test_labels_read':False})
    original=A/'verify_stock_rank5_embedding_actual_mature_fixture_v1_20261010.py';text=original.read_text(encoding='utf8')
    text=text.replace('stock_rank5_embedding','stock_forward5_embedding').replace('recent252_rank5_mature','recent252_forward5_mature').replace('Cross120Recent252Rank5Huber050','Cross120Recent252Forward5Huber050').replace('y_rank_5mean','y_ret_5mean').replace('cross120_rank5_real49153_mature_fixture_alignment_actual_CPU_controls_v1_20261010.json','recent252_forward5_mature_population_actual_CPU_controls_v1_20261010.json').replace('past_rank5_targets','past_forward5_targets')
    # A verified forward5 peer fixture already independently proves raw features and return labels.
    text=text.replace("A/'cross120_rank5_real49153_mature_fixture_alignment_actual_CPU_controls_v1_20261010.json'","A/'recent252_forward5_mature_population_actual_CPU_controls_v1_20261010.json'")
    start=text.index('    target,bounds=native.prepare_rank_targets');end=text.index('    unknown=architecture.attach',start)
    text=text[:start]+"    target,bounds=native.prepare_return_targets(y,native.CONFIG);lo,hi=np.quantile(y,[.005,.995]);oracle=(np.minimum(np.maximum(y,lo),hi)*20.).astype(np.float32)\n    assert np.array_equal(target.view('u4'),oracle.view('u4')) and bounds==[float(lo),float(hi)]\n    refusal=[]\n    for bad in (np.array([np.nan,.5]),np.array([np.inf,.5]),np.array([])):\n        try:native.prepare_return_targets(bad,native.CONFIG)\n        except AssertionError:refusal.append(True)\n        else:raise AssertionError('Invalid forward5 return target accepted')\n"+text[end:]
    text=text.replace('passed_actual49153_rank5_mature_targets_raw120_bits_stock_vocab_IDS_and_exact_once_centering_CPU','passed_actual49153_forward5_mature_returns_raw120_bits_stock_vocab_IDS_and_exact_Huber_target_scaling_CPU').replace('rank5_centered_once_and_winsorized_bits_exact','forward5_return_winsor_scaled20_bits_exact').replace('raw_rank5_target_sha256','raw_forward5_return_target_sha256').replace('actual_mature_rank5_rows','actual_mature_forward5_rows').replace("'target_centered_once':True","'return_target_scaled20_bits_exact':True")
    driver=save('verify_stock_forward5_embedding_actual_mature_fixture_v1_20261010.py',text)
    row=start_service('StockForward5Embedding_actual_mature_fixture_CPU_v1_20261010',driver.name,[],{str(driver):sha(driver),str(plan):sha(plan)});create(A/'actual_stock_forward5_embedding_mature_fixture_CPU_activation_v1_20261010.json',row)
    print({'new_forward5_return_native_e64_prepared':True,'actual_mature_CPU_fixture_started':True,'new_fits':0,'new_quality_scores':0},flush=True)
if __name__=='__main__':main()
