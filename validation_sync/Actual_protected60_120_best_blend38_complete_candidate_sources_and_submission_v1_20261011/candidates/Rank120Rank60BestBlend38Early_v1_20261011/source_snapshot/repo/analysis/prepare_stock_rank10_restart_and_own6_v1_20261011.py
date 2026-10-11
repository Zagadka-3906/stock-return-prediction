"""Admit new true mean10 targets, fresh-process restart and six independent annual64 fits."""
from pathlib import Path
import sys,re,importlib
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
PROOF='stock_rank10_embedding_actual_restart_and_own6_sources_admission_v1_20261011.json'
MAP={
 'verify_stock_rank5_embedding_small512_restart_v1_20261010.py':'verify_stock_rank10_embedding_small512_restart_v1_20261011.py',
 'verify_stock_rank5_embedding_small512_small_CPU_v1_20261010.py':'verify_stock_rank10_embedding_small512_small_CPU_v1_20261011.py',
 'train_stock_rank5_embedding_small512_BF16_bank6_own64_v1_20261010.py':'train_stock_rank10_embedding_small512_BF16_bank6_own64_v1_20261011.py',
 'verify_stock_rank5_embedding_small512_full5_independent_v1_20261010.py':'verify_stock_rank10_embedding_small512_full5_independent_v1_20261011.py',
 'stock_rank5_embedding_small512_BF16_native_v1_20261010.py':'stock_rank10_embedding_small512_BF16_native_v1_20261011.py',
 'stock_rank5_embedding_saved_tensor_decoder_v1_20261010.py':'stock_rank10_embedding_saved_tensor_decoder_v1_20261011.py',
 'recent252_rank5_mature_training_population_v1_20261010.py':'recent252_rank10_mature_training_population_v2_20261011.py',
 'forward5_mature_training_labels_v1_20261010.py':'forward10_mature_training_labels_v2_20261011.py',
 'recent252_rank5_mature_population_actual_CPU_controls_v1_20261010.json':'recent252_rank10_mature_population_actual_CPU_controls_v2_20261011.json',
 'stock_rank5_embedding_own64_native_sources_preparation_v1_20261010.json':'stock_rank10_embedding_own64_native_sources_preparation_v1_20261011.json',
}

def route(text):
    mapping={**MAP,**{Path(k).stem:Path(v).stem for k,v in MAP.items() if k.endswith('.py')}}
    placeholders={k:'__RANK10_'+str(i)+'__' for i,k in enumerate(mapping)}
    pattern=re.compile('|'.join(re.escape(k) for k in sorted(mapping,key=len,reverse=True)))
    text=pattern.sub(lambda m:placeholders[m.group()],text)
    text=text.replace('stock_rank5','stock_rank10').replace('StockRank5','StockRank10').replace('y_rank_5mean','y_rank_10mean').replace('label_end_5d','label_end_10d').replace('past_rank5_targets','past_rank10_targets').replace('mean5_tied','mean10_tied').replace('five_day','ten_day').replace('five-day','ten-day')
    # Only new Rank10 identifiers receive new dates; shared runtime imports retain their actual dates.
    text=re.sub(r'[^\s\'"/]*[Rr]ank10[^\s\'"/]*',lambda m:m.group().replace('_v1_20261010','_v1_20261011').replace('_v1_20261009','_v1_20261011'),text)
    for k,v in placeholders.items():text=text.replace(v,mapping[k])
    text=text.replace("native.CONFIG['label_horizon_trading_days']==5","native.CONFIG['label_horizon_trading_days']==10").replace("'label_horizon_trading_days':5","'label_horizon_trading_days':10")
    return text

def main():
    assert allowed()
    control=A/'recent252_rank10_mature_population_actual_CPU_controls_v2_20261011.json'
    assert read(control)['status']=='passed7_independent_mean10_tied_daily_rank_and_recent252_maturity_CPU_controls'
    originals=list(MAP)[:4];outputs=[]
    for name in originals:
        p=A/name;text=route(p.read_text(encoding='utf8'))
        if name.startswith('train_'):
            text=text.replace('label_end <= cutoff','label_end < cutoff')
            begin=text.index('            #193 normalization+main gates');end=text.index('            boundary=completed+8',begin)
            text=text[:begin]+text[end:]
        target=A/MAP[name];assert not target.exists();compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n');outputs.append(target)
    for target in outputs:
        text=target.read_text(encoding='utf8');assert 'y_rank_5mean' not in text and 'stock_rank5' not in text
        if target.name.startswith('train_'):
            assert 'label_end_10d' in text and 'recent252_rank10_mature_training_population_v2_20261011' in text
            assert "assert native.CONFIG['label_horizon_trading_days']==10" in text
        for line in text.splitlines():
            if line.startswith('from ') or line.startswith('import '):
                if 'stock_rank10' in line:
                    module=line.split()[1];assert (A/(module+'.py')).is_file(),(target,module)
    sources=[Path(__file__),*[A/n for n in originals],*outputs,control,
             A/'stock_rank10_embedding_own64_native_sources_preparation_v1_20261011.json',
             A/'verify_stock_rank10_embedding_actual_mature_fixture_v1_20261011.py']
    create(A/PROOF,{'status':'compiled_new_rank10_real_fixture_restart_smallCPU_own6_64epochs_and_independentfull5_sources',
           'input_sha256':{str(p):sha(p) for p in sources},'label_horizon_trading_days':10,'fixed_epochs':64,
           'actual_annual_years':[2020,2021,2022,2023,2024,2025],'new_native_fits':0,'new_quality_scores':0,
           'actual_fits_and_independent_full5_not_yet_complete':True,'GPU_priority':'actual183_candidate_preparation_and_sealing_before_new_restart_and_training','test_labels_read':False})
    tasks=[('actual_stock_rank10_embedding_small512_restart_v1_20261011',outputs[0].name),
           ('StockRank10EmbeddingSmall512_independent_small_CPU_v1_20261011',outputs[1].name),
           ('actual_stock_rank10_embedding_small512_bank6_v1_20261011',outputs[2].name),
           ('StockRank10EmbeddingSmall512_independent_full5_GPU_controls_v1_20261011',outputs[3].name)]
    driver=A/'run_stock_rank10_embedding_own_training_and_full5_queue_v1_20261011.py'
    text="""from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
from start_fast_completed_owned_service_v1_20261011 import start_service
def main():
    assert allowed();closed('StockRank10Embedding_actual_mature_fixture_CPU_v1_20261011')
    closed('recovery14_StockRank20Embedding183_selected_candidate_preparation_v1_20261010')
    closed('recovery14_StockRank20Embedding183_selected_candidate_sealing_v1_20261010')
    proof=A/'PROOF'
    for p,d in read(proof)['input_sha256'].items():assert sha(p)==d,p
    for name,driver in TASKS:
        assert allowed();p=A/driver;r=start_service(name,driver,[],{str(p):sha(p),str(proof):sha(proof)})
        create(A/(name+'_activation.json'),r);closed(name)
    print({'actual_rank10_own6_and_independentfull5_complete':True},flush=True)
if __name__=='__main__':main()
""".replace("'PROOF'",repr(PROOF)).replace('TASKS',repr(tasks))
    assert not driver.exists();compile(text,str(driver),'exec');driver.write_text(text,encoding='utf8',newline='\n')
    assert allowed();name='actual_stock_rank10_embedding_own_training_and_full5_queue_v1_20261011'
    row=start_service(name,driver.name,[],{str(driver):sha(driver),str(A/PROOF):sha(A/PROOF)})
    create(A/(name+'_activation.json'),row)
    print({'actual_rank10_restart_own6_full5_queue_dispatched':True,'actual_fits_pending_fixture_and183_GPU':True},flush=True)

if __name__=='__main__':main()
