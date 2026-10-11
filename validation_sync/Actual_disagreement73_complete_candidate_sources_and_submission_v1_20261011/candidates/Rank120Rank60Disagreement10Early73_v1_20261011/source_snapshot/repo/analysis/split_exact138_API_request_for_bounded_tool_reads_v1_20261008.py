from pathlib import Path
import json,sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def main():
    out=Path('E:/赛题五_本机临时/exact138_scores_connected_API_v1_20261008');request=read(out/'create_tree_request.json')
    chunks=[];current=[];size=0
    for entry in request['tree_elements']:
        length=len(json.dumps(entry,ensure_ascii=False))
        if current and size+length>180000:chunks.append(current);current=[];size=0
        current.append(entry);size+=length
    if current:chunks.append(current)
    paths=[]
    for i,entries in enumerate(chunks):
        path=out/f'tool_read_chunk{i}.json';create(path,{'tree_elements':entries});paths.append({'path':str(path),'entries':len(entries),'sha256':sha(path),'bytes':path.stat().st_size})
    create(out/'bounded_tool_read_manifest.json',{'repository_full_name':request['repository_full_name'],'base_tree_sha':request['base_tree_sha'],'chunks':paths,'total_entries':sum(r['entries'] for r in paths),'original_request_sha256':sha(out/'create_tree_request.json')})
    print(json.dumps({'chunks':len(paths),'max_bytes':max(r['bytes'] for r in paths),'entries':sum(r['entries'] for r in paths)}))
if __name__=='__main__':main()
