from pathlib import Path
from collections import defaultdict
import sys,json,re,gzip
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,create,sha
OUT=Path('E:/赛题五_本机临时/仓库清理140_20261011')
inventory=read(OUT/'tracked_inventory.json');rows=inventory['files']
protected=['validation_sync/Actual_consensusFraction101_complete_candidate_sources_and_submission_v1_20261011/','validation_sync/Actual_fraction101_complete_bundle_catalog_v7_and_discarded_weights_cleanup137_20261011/','validation_sync/Actual_project_documentation138_refresh_20261011/','validation_sync/round189/','validation_sync/round191/']
def keep(p):return not p.startswith('validation_sync/') or any(p.startswith(prefix) for prefix in protected)
generated={}
for path,oid,size in rows:
    match=re.match(r'validation_sync/round(\d+)/complete_ranking_display/',path)
    if match and int(match[1])<191 and int(match[1])!=189 and (path.endswith('complete_rankings_lossless.html') or re.search(r'/full_report_reconstructed_for_publication\.json\.gz(?:\.part\d+)?$',path)):
        assert not keep(path);generated[path]=(oid,size)
objects=defaultdict(list)
for path,oid,size in rows:
    if path not in generated:objects[oid].append((path,size))
removed=[]
for oid,entries in objects.items():
    if len(entries)<2:continue
    canonical=min(entries,key=lambda x:(not keep(x[0]),x[0].startswith('validation_sync/'),len(x[0]),x[0]))[0]
    for path,size in entries:
        if path==canonical or keep(path) or Path(path).suffix not in ['.py','.json','.gz']:continue
        removed.append({'removed_path':path,'reason':'byte_identical_historical_export_copy','git_blob_oid':oid,'bytes':size,'retained_path':canonical})
for path,(oid,size) in generated.items():removed.append({'removed_path':path,'reason':'obsolete_generated_cumulative_ranking_display','git_blob_oid':oid,'bytes':size,'latest_cumulative_display':'validation_sync/round191/complete_ranking_display/lossless_ranking_display_v2_20261006/round191/complete_rankings_lossless.html'})
removed.sort(key=lambda x:x['removed_path']);deleted={r['removed_path'] for r in removed};assert len(deleted)==len(removed)
for row in removed:
    assert not keep(row['removed_path'])
    if 'retained_path' in row:assert row['retained_path'] not in deleted
    row['historical_commit']=inventory['head'];row['historical_url']='https://github.com/Zagadka-3906/stock-return-prediction/blob/'+inventory['head']+'/'+row['removed_path']
archive=OUT/'deletion_plan.jsonl.gz'
with archive.open('xb') as raw:
    with gzip.GzipFile(fileobj=raw,mode='wb',mtime=0) as stream:
        for row in removed:stream.write((json.dumps(row,ensure_ascii=False,separators=(',',':'))+'\n').encode('utf8'))
create(OUT/'plan_verification.json',{'status':'predeclared_only_duplicate_export_paths_and_obsolete_generated_views','previous_main':inventory['head'],'tracked_files_before':len(rows),'planned_deletions':len(removed),'planned_logical_bytes':sum(r['bytes'] for r in removed),'generated_display_files':len(generated),'duplicate_export_files':len(removed)-len(generated),'protected_prefixes':protected,'plan_sha256':sha(archive),'local_model_data_submission_and_resume_dependencies_not_in_scope':True,'unique_scientific_blobs_not_deleted':True,'Git_history_not_rewritten':True,'new_training':0,'new_scoring':0,'new_inference':0})
print(read(OUT/'plan_verification.json'),flush=True)
