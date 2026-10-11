from pathlib import Path
import sys,hashlib,gzip,json,time,gc
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
 assert allowed();import psutil
 from verified_shared_publication_board_loader_v1_20261011 import SharedBoard,bind_namespace
 from exact_native_pretty_JSON_archive_20261007 import pieces
 import verified_shared_publication_board_loader_v1_20261011 as runtime
 proof=A/'shared_immutable_ranking_loader_actual_complete180_benchmark_v1_20261011.json';old=read(proof);assert old['status']=='passed_actual_complete180_shared_loader_all_native_bytes_exact'
 for p,d in old['input_sha256'].items():assert sha(p)==d,p
 path=A/'lossless_ranking_display_v2_20261006/round180/full_report_reconstructed_for_publication.json.gz';folder=path.parent;paths=[Path(__file__),Path(runtime.__file__),proof,path,folder/'complete_rankings_lossless.html',folder/'verification.json',folder/'full_report_publication_snapshot_verification.json'];pins={str(p):sha(p) for p in paths};before=psutil.Process().memory_info().rss;started=time.perf_counter()
 namespace={'PUBLICATION_FULL_REPORT':path,'json':json,'gzip':gzip,'sha':lambda b:hashlib.sha256(b).hexdigest()};state,restore=bind_namespace(namespace)
 marker=namespace['gzip'].decompress(path.read_bytes());report=namespace['json'].loads(marker.decode('utf-8-sig'));digest=namespace['sha'](marker);assert report is state['owner'].report and len(report['connected'])==17062 and digest==old['original_native_sha256']
 assert namespace['sha'](namespace['gzip'].decompress(path.read_bytes()))==digest
 # All other JSON/gzip/hash operations must retain their actual library semantics.
 for obj in [{'a':1,'floats':[0.,-0.,1e-7,None,True],'中文':'rank\\n'},[1,2,3]]:
  raw=json.dumps(obj,ensure_ascii=False).encode('utf8');compressed=gzip.compress(raw,mtime=0);assert namespace['gzip'].decompress(compressed)==raw and namespace['json'].loads(raw)==obj and namespace['sha'](raw)==hashlib.sha256(raw).hexdigest()
 h=hashlib.sha256();count=0
 for block in pieces(report):h.update(block);count+=len(block)
 assert h.hexdigest()==digest and count==old['original_native_bytes'];state['owner'].reverify();restore();assert namespace['json'] is json and namespace['gzip'] is gzip
 for p,d in pins.items():assert sha(p)==d,p
 create(A/'verified_shared_publication_board_loader_actual_complete180_controls_v1_20261011.json',{'status':'passed_actual_complete180_shared_board_publication_read_stage_and_full_native_bytes_exact','input_sha256':pins,'original_native_sha256':digest,'original_native_bytes':count,'connected_records':17062,'actual_read_and_final_hash_calls':state['avoided_full_decompression_calls'],'snapshot_read_stage_same_report_values_types_order_and_float_spellings_verified':True,'all_other_JSON_gzip_SHA_calls_unchanged':True,'namespace_restored':True,'elapsed_seconds':time.perf_counter()-started,'before_RSS_bytes':before,'actual_decoded_RSS_bytes':psutil.Process().memory_info().rss,'scientific_runtime_adoption_not_performed_by_control':True,'new_fits':0,'new_scores':0,'test_labels_read':False});print({'actual_full_report_180_reader_controls_passed':True,'native_bytes':count},flush=True)
if __name__=='__main__':main()
