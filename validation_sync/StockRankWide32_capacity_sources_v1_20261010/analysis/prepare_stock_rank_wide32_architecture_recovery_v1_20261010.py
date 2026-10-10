"""Preserve the refused16-dimensional architecture trial; dispatch fresh explicit32 architecture."""
from pathlib import Path
import sys,runpy
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import create,read,sha
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
def main():
    assert allowed()
    service=A/'service_owned_workflows_20261006/actual_stock_rank_wide_embedding1024_ID32_own64_controls46_queue_v1_20261010'
    assert read(service/'service_execution.json')['status']=='failed'
    original=A/'stock_identity_embedding_network_v1_20261010.py'
    architecture=A/'stock_identity_embedding32_network_v1_20261010.py'
    text=original.read_text(encoding='utf8').replace("cfg['stock_embedding_dim']==16","cfg['stock_embedding_dim']==32").replace('Embedding(4651,16','Embedding(4651,32').replace('width=120+16','width=120+32')
    assert not architecture.exists();compile(text,str(architecture),'exec');architecture.write_text(text,encoding='utf8',newline='\n')
    source=A/'prepare_stock_rank_wide_embedding1024_ID32_own64_v1_20261010.py'
    driver=A/'prepare_stock_rank_wide32_embedding1024_ID32_own64_v1_20261010.py'
    text=source.read_text(encoding='utf8').replace('stock_rank_wide_embedding','stock_rank_wide32_embedding').replace('StockRankWideEmbedding1024','StockRankWide32Embedding1024')
    text=text.replace('    return text',"    text=text.replace('stock_identity_embedding_network_v1_20261010','stock_identity_embedding32_network_v1_20261010')\n    return text")
    assert not driver.exists();compile(text,str(driver),'exec');driver.write_text(text,encoding='utf8',newline='\n')
    create(A/'stock_rank_wide32_explicit_architecture_recovery_v1_20261010.json',{'status':'preserved_actual_old16_dimension_architecture_refusal_fresh32_dimension_namespace','input_sha256':{str(p):sha(p) for p in [Path(__file__),source,driver,original,architecture,service/'service_execution.json']},'original_failed_trial_preserved':True,'own32_architecture_gpu_controls_pending':True,'new_quality_scores':0})
    runpy.run_path(str(driver),run_name='__main__')
if __name__=='__main__':main()
