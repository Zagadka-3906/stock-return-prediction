import argparse,pathlib,json,base64
p=argparse.ArgumentParser();p.add_argument('--file',required=True);p.add_argument('--offset',type=int,required=True);p.add_argument('--count',type=int,required=True);a=p.parse_args()
path=pathlib.Path(a.file);assert path.resolve().is_relative_to(pathlib.Path('E:/赛题五_本机临时').resolve());assert a.offset>=0 and a.offset%4==0 and a.count>0 and a.count%4==0
size=path.stat().st_size;total=((size+2)//3)*4
with path.open('rb') as f:f.seek(a.offset//4*3);chunk=base64.b64encode(f.read(a.count//4*3)).decode('ascii')
assert len(chunk)<=a.count
print(json.dumps({'offset':a.offset,'total':total,'chunk':chunk},ensure_ascii=True))
