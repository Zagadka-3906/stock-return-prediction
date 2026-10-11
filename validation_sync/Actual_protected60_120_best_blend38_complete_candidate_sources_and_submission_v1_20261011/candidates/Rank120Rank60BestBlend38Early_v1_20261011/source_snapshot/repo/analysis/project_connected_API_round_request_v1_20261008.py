from pathlib import Path
import argparse,json,hashlib
def main(number):
    out=Path(f'E:/赛题五_本机临时/round{number}_connected_API_main_v1_20261008');data=(out/'bundle.json').read_bytes();b=json.loads(data.decode('utf-8-sig'));target=out/'api_request_projection.json';assert not target.exists()
    projected={k:b[k] for k in ('repository_full_name','round','parent_commit','parent_tree','expected_exact_tree_sha','tree_elements','binary_new_blobs','message')};projected['original_bundle_sha256']=hashlib.sha256(data).hexdigest()
    target.write_text(json.dumps(projected,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf8')
    print(json.dumps({'path':str(target),'bytes':target.stat().st_size,'tree_entries':len(b['tree_elements']),'new_binary_blobs':len(b['binary_new_blobs']),'binary_bytes':sum(x['bytes'] for x in b['binary_new_blobs'])},ensure_ascii=False))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--round',type=int,required=True,choices=(135,144));main(p.parse_args().round)
