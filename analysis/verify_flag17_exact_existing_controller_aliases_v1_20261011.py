"""Resolve copied historical score namespace to the actual new17 stream, preserving all frozen sources."""
from pathlib import Path
import sys,ctypes
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed

def main():
 assert allowed()
 proof=A/'rank60_flag17_best17_full_candidate_sources_admission_v1_20261011.json'
 data=read(proof)
 for p,d in data['input_sha256'].items():assert sha(p)==d,p
 base=A/'service_owned_workflows_20261006'
 service=base/'actual_stock_rank60_embedding_after183_direct_allocation17_v1_20261011'
 actual=base/'actual_stock_rank60_flag17_after183_direct17_v1_20261011'
 source=Path('E:/赛题五_本机临时/StockRank60EmbeddingSmall512_after183_direct_allocation17_screen_v1_20261011')
 target=Path('E:/赛题五_本机临时/StockRank60FlagOnly_after183_direct17_screen_v1_20261011')
 assert actual.exists() and not service.exists() and not source.exists()
 probe=A/'current_ranking_file_link_probe_v1_20261008.bin';assert probe.is_symlink()
 kernel=ctypes.WinDLL('kernel32',use_last_error=True);link=kernel.CreateSymbolicLinkW;link.argtypes=(ctypes.c_wchar_p,ctypes.c_wchar_p,ctypes.c_uint32);link.restype=ctypes.c_ubyte
 for logical,physical,root in [(service,actual,base),(source,target,Path('E:/赛题五_本机临时'))]:
  assert logical.parent.resolve()==root.resolve() and physical.parent.resolve()==root.resolve()
  assert link(str(logical),str(physical),3),ctypes.get_last_error()
  assert logical.is_symlink() and logical.resolve()==physical.resolve()
 assert sha(service/'native_launch.json')==sha(actual/'native_launch.json')
 bank=read(Path('E:/赛题五_本机临时/stock_rank60_embedding_small512_BF16_bank6_v1_20261011/protocol.json'))
 assert bank['configuration']['hidden']==[512,256,128]
 create(A/'flag17_exact_existing_controller_aliases_admission_v1_20261011.json',{'status':'passed_actual_new17_service_and_scoring_output_directory_aliases_frozen_scientific_sources_unchanged','input_sha256':{str(proof):sha(proof),str(Path(__file__)):sha(__file__),str(actual/'native_launch.json'):sha(actual/'native_launch.json')},'aliases':{str(service):str(actual),str(source):str(target)},'new_scores':0,'new_fits':0,'candidate_inference_not_started':True,'actual_model_hidden':[512,256,128],'inherited_model_string_is_only_historical_identifier_not_architecture':'rank_MLP2048_StockRank60Medium_ID16_Cross120_seed20261009_e64','all_native_configuration_and_weight_SHA_assertions_retained':True})
 print('Actual flag17 namespaces resolved with original source SHA unchanged; existing real512 capacity documented',flush=True)

if __name__=='__main__':main()
