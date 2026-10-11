"""Compare all optimized codec nodes and exact embedded bytes with original full180 evidence."""
from pathlib import Path
from datetime import datetime
import sys,json,re,time,os,psutil
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
import identity_memoized_original_lossless_report_codec_v1_20261011 as optimized

def main():
 assert allowed()
 import build_lossless_ranking_display_v2_20261006 as original
 shared={'nested':[None,True,False,0,1,0.,-0.,1e-7,'中文</script>🚀']}
 fixtures=[{},shared,{'a':shared,'b':shared},[shared,shared,{'equal':dict(shared)}],{'long':'中文</script>'*600,'again':'中文</script>'*600},{'types':[False,0,True,1,0.,-0.,1.,1e20]}]
 for fixture in fixtures:
  before=json.dumps(fixture,ensure_ascii=False,allow_nan=False)
  a=optimized.pack_report(fixture);b=original.pack_report(fixture)
  assert json.dumps(a,ensure_ascii=False,separators=(',',':'),allow_nan=False)==json.dumps(b,ensure_ascii=False,separators=(',',':'),allow_nan=False)
  assert json.dumps(fixture,ensure_ascii=False,allow_nan=False)==before
  assert original.unpack_report(a)==fixture
 print('Actual6 original codec node/byte/type/alias/long-string/input-immutability fixtures passed',flush=True)
 OUT=Path('E:/赛题五_本机临时/原始完整榜共享节点身份复用实测_v1_20261011');OUT.mkdir(exist_ok=False)
 while psutil.virtual_memory().available<2*2**30:assert allowed();time.sleep(10)
 folder=A/'lossless_ranking_display_v2_20261006/round180';page=folder/'complete_rankings_lossless.html'
 paths=[Path(__file__),Path(optimized.__file__),Path(original.__file__),page,folder/'verification.json',folder/'full_report_publication_snapshot_verification.json']
 pins={str(p):sha(p) for p in paths};create(OUT/'frozen_before_full180_codec_controls.json',{'input_sha256':pins,'expected_connected_records':17062,'original_node_layout_and_all_fields_required':True,'new_scores':0,'test_labels_read':False})
 text=page.read_text(encoding='utf-8');match=re.search(r'<script\s+id="data"\s+type="application/json">(.*?)</script>',text,re.S);assert match is not None
 expected=json.loads(match.group(1));report=original.unpack_report(expected);assert len(report['connected'])==17062
 started=time.perf_counter();actual=optimized.pack_report(report);elapsed=time.perf_counter()-started
 expected_bytes=json.dumps(expected,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode('utf-8');actual_bytes=json.dumps(actual,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode('utf-8')
 assert actual_bytes==expected_bytes
 assert json.dumps(actual,ensure_ascii=False,separators=(',',':'),allow_nan=False).replace('</','<\\/')==match.group(1)
 for view in ('representative','connected','mlp_bounds','historical','csv_test','legacy_annual'):assert original.unpack_report(actual)[view]==report[view]
 for p,d in pins.items():assert sha(p)==d,p
 create(OUT/'verification.json',{'status':'passed_actual_complete180_original_every_codec_node_and_embedded_JSON_byte_identity_memoized_input_containers','at_local':datetime.now().isoformat(),'input_sha256':pins,'connected_records':17062,'all_original_codec_nodes':len(expected['nodes']),'encoded_payload_bytes':len(actual_bytes),'actual_memoized_pack_seconds':elapsed,'actual_process_RSS_bytes':psutil.Process().memory_info().rss,'actual6_original_codec_fixtures':6,'all_original_six_views_exact':True,'original_float_bool_int_string_keys_and_node_order_preserved':True,'new_fits':0,'new_scores':0,'test_labels_read':False,'scientific_workers_unchanged':True,'runtime_not_yet_adopted':True})
 create(A/'actual_identity_memoized_lossless_codec_full180_location_v1_20261011.json',{'output':str(OUT),'verification_sha256':sha(OUT/'verification.json')})
 print({'actual_full180_all_nodes_and_embedded_bytes_exact':True,'pack_seconds':elapsed,'nodes':len(expected['nodes']),'runtime_not_yet_adopted':True},flush=True)

if __name__=='__main__':main()
