"""Freeze the exact unpublished tree and hold only the idle main publisher for API transport."""
from pathlib import Path
import sys,subprocess,json,hashlib
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
import publish_classifier_consensus_workflows_20261006 as helpers
OUT=A/'sparse_main_API_transport_recovery_20261007'

def main():
    sync=helpers.sync;commit='04c65d0c967c206575a5b4b72dd194e1a3eb45c5';parent='d3f72d82dcb337e5436824b5c32412db364e2a41'
    assert sync.git('rev-parse','HEAD')==commit and not sync.git('status','--porcelain')
    assert not OUT.exists();OUT.mkdir();entries=[]
    for line in sync.git('diff-tree','--no-commit-id','--name-only','-r',commit).splitlines():
        assert line.startswith('validation_sync/actual_sparse_and_isolated_scoring_controls_20261007/')
        path=sync.WORKTREE/line;data=path.read_bytes();assert not sync.SECRET.search(data)
        blob=hashlib.sha1(('blob '+str(len(data))+'\0').encode()+data).hexdigest()
        assert sync.git('rev-parse',commit+':'+line)==blob
        entry={'path':line,'mode':'100644','type':'blob','expected_blob_sha':blob,'raw_sha256':hashlib.sha256(data).hexdigest()}
        try:entry['content']=data.decode('utf8')
        except UnicodeDecodeError:
            import base64
            entry['binary_base64']=base64.b64encode(data).decode('ascii')
        entries.append(entry)
    packets=[];current=[];size=0
    for entry in entries:
        amount=len(json.dumps(entry,ensure_ascii=False).encode('utf8'))
        if current and size+amount>45000:packets.append(current);current=[];size=0
        current.append(entry);size+=amount
    if current:packets.append(current)
    for index,packet in enumerate(packets):create(OUT/f'packet{index:03d}.json',{'entries':packet})
    create(OUT/'frozen_exact_API_tree_payload.json',{'status':'frozen_exact_original_unpublished_commit_tree_for_standard_API_transport',
      'original_local_commit':commit,'expected_remote_parent':parent,'base_tree_sha':sync.git('show','-s','--format=%T',parent),
      'expected_tree_sha':sync.git('show','-s','--format=%T',commit),'files':len(entries),'packets':len(packets),
      'maximum_packet_bytes':max((OUT/f'packet{i:03d}.json').stat().st_size for i in range(len(packets))),
      'binary_files':sum('binary_base64' in entry for entry in entries),'packet_sha256':{str(OUT/f'packet{i:03d}.json'):sha(OUT/f'packet{i:03d}.json') for i in range(len(packets))},
      'branch':'main','force_update_authorized_or_used':False,'scientific_source_and_all_parameter_bytes_unchanged':True,'new_quality_scores':0})
    driver=A/'hold_idle_main_publisher_for_API_tree_recovery_20261007.py'
    row=start('main_publication_API_tree_recovery_lease',driver.name,[],{str(driver):sha(driver),str(OUT/'frozen_exact_API_tree_payload.json'):sha(OUT/'frozen_exact_API_tree_payload.json')})
    create(OUT/'actual_hidden_main_lease_launch.json',{'identity':row,'new_quality_scores':0})
    print(json.dumps({'files':len(entries),'packets':len(packets),'binary_files':sum('binary_base64' in entry for entry in entries),'max_packet_bytes':max((OUT/f'packet{i:03d}.json').stat().st_size for i in range(len(packets)))}),flush=True)

if __name__=='__main__':main()
