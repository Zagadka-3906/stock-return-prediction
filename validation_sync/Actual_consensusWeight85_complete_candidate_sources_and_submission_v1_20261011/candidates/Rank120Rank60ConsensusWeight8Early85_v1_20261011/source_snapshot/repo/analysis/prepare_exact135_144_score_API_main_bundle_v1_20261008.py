"""Prepare exact completed score files for connected GitHub Git-data API; local tree equals remote proposed tree."""
from pathlib import Path
import sys,time,gzip,hashlib,json,subprocess,base64
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
PARENT='fc1d74adc97e42c3c2a35ccf0e082c53b3736a0d'
OUT=Path('E:/赛题五_本机临时/exact135_144_scores_connected_API_v1_20261008')
def main():
    import publish_classifier_consensus_workflows_20261006 as helpers
    from file_backed_hidden_git_runtime_20261007 import installed
    assert not OUT.exists();OUT.mkdir()
    payload={};bindings={};phases={}
    for number,folder,freeze,prefix,count in (
        (135,'BF16wide40_official_comparison_v1_20261008','BF16wide40_scores_github_v2_20261008','BF16wide40_scores_20261008',40),
        (144,'ConeRidgeAlpha100_official_comparison_v5_20261008','ConeRidgeAlpha100_scores_github_v1_20261008','ConeRidgeAlpha100_scores_20261008',100)):
        q=read(A/folder/'verification.json');assert len(q['records'])==count and q['status'].startswith('passed')
        frozen=read(A/freeze/'frozen_before_main_publication.json');pins=frozen['input_sha256']
        sources=[Path(p) for p in pins]
        for p,d in pins.items():assert sha(p)==d,p
        base=Path('validation_sync')/prefix;entries={}
        for source in sources:
            data=source.read_bytes();assert not helpers.sync.SECRET.search(data),source
            digest=hashlib.sha256(data).hexdigest();relative=source.relative_to(ROOT) if source.is_relative_to(ROOT) else Path('external_metadata')/(digest+'_'+source.name)
            target=(base/relative).as_posix();raw_size=len(data)
            if len(data)>=5*1024**2:data=gzip.compress(data,mtime=0);target+='.gz';assert hashlib.sha256(gzip.decompress(data)).hexdigest()==digest
            assert target not in payload;payload[target]=data;entries[str(source)]={'published_path':target,'raw_sha256':digest,'original_bytes':raw_size}
        for row in q['records']:
            capsule=Path(row['official_score_cache']['official_metrics_source'])
            assert sha(capsule)==row['official_metric_capsule_sha256'] and read(capsule)['metrics']==row['metrics']
            assert str(capsule) in entries
        payload[(base/'.gitattributes').as_posix()]=b'* -text\n'
        payload[(base/'manifest.json').as_posix()]=helpers.sync.encoded({
            'status':'actual_complete_official_scores_uploaded_via_connected_GitHub_API_after_preserved_TLS_failure',
            'at_local':helpers.sync.now(),'round':number,'actual_score_records':count,'files':entries,'actual_best':q['best'],
            'candidate_and_complete_QA_main_still_required':True,'new_quality_scores_by_publication':0,'main_only':True,'test_labels_read':False})
        phases[str(number)]={'prefix':base.as_posix(),'official_score_records':count,'actual_best':q['best'],'files':entries}
    extra=Path('validation_sync/exact135_144_scores_API_transport_v1_20261008')
    for source in (Path(__file__),A/'recover_BF16wide135_after_TLS_publication_v6_20261008.py',
                   A/'BF16wide135_TLS_publication_receiver_recovery_v5_20261008.json'):
        payload[(extra/source.relative_to(ROOT)).as_posix()]=source.read_bytes()
    payload[(extra/'.gitattributes').as_posix()]=b'* -text\n'
    with installed(OUT/'local_git_file_IO'):
        sync=helpers.sync;assert sync.git('rev-parse','HEAD')==PARENT and not sync.git('status','--porcelain')
        sync.git('config','--local','core.longpaths','true')
        existing=set(sync.git('ls-tree','-r','--format=%(objectname)',PARENT).splitlines())
        elements=[];binary=[];files={}
        for name,data in payload.items():
            oid=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
            files[name]={'sha256':hashlib.sha256(data).hexdigest(),'git_blob_sha':oid,'bytes':len(data)}
            item={'path':name,'mode':'100644','type':'blob'}
            if oid in existing:item['sha']=oid
            else:
                try:item['content']=data.decode('utf8')
                except UnicodeDecodeError:
                    file=OUT/(oid+'.blob');file.write_bytes(data);binary.append({'git_blob_sha':oid,'path':str(file),'bytes':len(data)});item['sha']=oid
            elements.append(item);sync.atomic(sync.WORKTREE/name,data)
        names=sorted(payload)
        for start in range(0,len(names),50):sync.git('add','-f','--',*names[start:start+50])
        assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())==set(names)
        tree=sync.git('write-tree');parent_tree=sync.git('rev-parse',PARENT+'^{tree}')
        bundle={'repository_full_name':'Zagadka-3906/stock-return-prediction','parent_commit':PARENT,'parent_tree':parent_tree,
            'expected_exact_tree_sha':tree,'tree_elements':elements,'binary_new_blobs':list({b['git_blob_sha']:b for b in binary}.values()),
            'files':files,'phases':phases,'local_worktree':str(sync.WORKTREE),'new_quality_scores':0,
            'only_main_fast_forward_with_expected_parent_lease':True,'all_prior_failed_publishers_preserved':True}
        create(OUT/'bundle.json',bundle)
        create(A/'exact135_144_scores_API_bundle_location_v1_20261008.json',{
            'status':'frozen_exact_local_git_tree_for_two_complete_score_sets_before_connected_API_publication',
            'output':str(OUT),'bundle_sha256':sha(OUT/'bundle.json'),'expected_tree_sha':tree,'parent':PARENT,
            'actual_scored_records':140,'published_files_planned':len(files),'binary_new_blobs':len(bundle['binary_new_blobs']),
            'bundle_bytes':(OUT/'bundle.json').stat().st_size,'source_weights_or_large_arrays_uploaded':False})
        print({'expected_tree':tree,'files':len(files),'new_binary_blobs':len(bundle['binary_new_blobs']),
               'bundle_bytes':(OUT/'bundle.json').stat().st_size,'new_inline_UTF8_blobs':sum('content' in e for e in elements)},flush=True)
if __name__=='__main__':main()
