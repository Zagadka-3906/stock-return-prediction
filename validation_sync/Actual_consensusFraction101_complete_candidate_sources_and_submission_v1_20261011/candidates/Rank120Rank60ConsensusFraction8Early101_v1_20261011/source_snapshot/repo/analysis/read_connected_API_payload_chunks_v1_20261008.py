import argparse,json,pathlib,base64
p=argparse.ArgumentParser();p.add_argument('--file',required=True);p.add_argument('--offset',type=int,required=True);p.add_argument('--count',type=int,required=True);p.add_argument('--base64',action='store_true');a=p.parse_args()
path=pathlib.Path(a.file);assert path.resolve().is_relative_to(pathlib.Path('E:/赛题五_本机临时').resolve())
s=base64.b64encode(path.read_bytes()).decode('ascii') if a.base64 else path.read_text(encoding='utf-8-sig')
print(json.dumps({'offset':a.offset,'total':len(s),'chunk':s[a.offset:a.offset+a.count]},ensure_ascii=True))
