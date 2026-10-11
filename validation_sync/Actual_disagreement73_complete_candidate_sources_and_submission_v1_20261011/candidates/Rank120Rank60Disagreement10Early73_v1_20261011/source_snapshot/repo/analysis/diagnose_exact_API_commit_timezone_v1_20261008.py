import pathlib,json,datetime,hashlib,itertools
E=pathlib.Path('E:/赛题五_本机临时/exact135_144_scores_connected_API_v1_20261008');r=json.loads((E/'actual_connected_API_responses.json').read_text(encoding='utf8'));c=json.loads(r['raw_commit']['structuredContent']['content'])
def identity(v):return f"{v['name']} <{v['email']}> {int(datetime.datetime.fromisoformat(v['date'].replace('Z','+00:00')).timestamp())} "
tz=[('+' if m>=0 else '-')+f'{abs(m)//60:02d}{abs(m)%60:02d}' for m in range(-12*60,14*60+1,15)]
prefix='tree '+c['tree']['sha']+'\n'+''.join('parent '+p['sha']+'\n' for p in c['parents'])
matches=[]
for at,ct,end,enc in itertools.product(tz,tz,('','\n'),('','encoding UTF-8\n')):
    raw=(prefix+'author '+identity(c['author'])+at+'\ncommitter '+identity(c['committer'])+ct+'\n'+enc+'\n'+c['message']+end).encode('utf8')
    if hashlib.sha1(b'commit '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==c['sha']:
        matches.append({'author_timezone':at,'committer_timezone':ct,'end':end,'encoding_header':enc});(E/'actual_verified_raw_commit.bin').write_bytes(raw)
print(json.dumps({'commit':c['sha'],'matches':matches},ensure_ascii=False))
