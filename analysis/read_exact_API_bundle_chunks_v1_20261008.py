import argparse,json,pathlib
p=argparse.ArgumentParser();p.add_argument('--offset',type=int,required=True);p.add_argument('--count',type=int,required=True);a=p.parse_args()
s=pathlib.Path('E:/赛题五_本机临时/exact135_144_scores_connected_API_v1_20261008/bundle.json').read_text(encoding='utf-8-sig')
print(json.dumps({'offset':a.offset,'total':len(s),'chunk':s[a.offset:a.offset+a.count]},ensure_ascii=True))
