"""Check saved-score provenance and the local ranking report's interactions."""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import tempfile

ROOT=Path(__file__).resolve().parents[1]
QA=ROOT/'analysis/all_model_ranking_qa'
REPORT=ROOT/'results/all_model_rankings_20261003.json'
HTML=ROOT/'results/all_model_rankings_20261003.html'


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    report=json.loads(REPORT.read_text(encoding='utf-8'))
    sources={}
    for item in report['source_manifest']:
        assert digest(item['path'])==item['sha256'],item['path']
        if Path(item['path']).suffix=='.json':
            sources[item['path']]=json.loads(Path(item['path']).read_text(encoding='utf-8-sig'))
    pointers=0
    for view in ('representative','connected','mlp_bounds','historical','csv_test','legacy_annual'):
        for row in report[view]:
            value=sources[row['source']]
            for token in row['source_pointer'].lstrip('/').split('/'):
                token=token.replace('~1','/').replace('~0','~')
                value=value[int(token)] if isinstance(value,list) else value[token]
            pointers+=1
            if view=='connected':assert value['connected_final_score']==row['score'],row['id']
        scored=[r['score'] for r in report[view] if r['score'] is not None and (view!='historical' or r['rank'] is not None)]
        assert scored==sorted(scored,reverse=True),view
    weighted_records=report['summary'].get('weighted_wave62_64_records',0)
    role_records=report['summary'].get('role_wave65_67_records',0)
    priority_records=report['summary'].get('retention_priority_wave68_70_records',0)
    multi_records=report['summary'].get('multi_method_wave71_76_records',0)
    independent_records=report['summary'].get('independent_membership_wave77_80_records',0)
    later_records=report['summary'].get('later_round_records',{})
    new_records=independent_records or multi_records or priority_records or role_records or weighted_records
    assert report['summary']['connected_exact_records']==1191+weighted_records+role_records+priority_records+multi_records+independent_records+sum(later_records.values())
    assert report['summary']['repaired_wave59_61_records']==35
    latest='r12' if independent_records else ('r11' if multi_records else ('r10' if priority_records else ('r9' if role_records else ('r8' if weighted_records else 'r7'))))
    if later_records:
        number=max(map(int,later_records));latest=f'r{number}';new_records=later_records[str(number)]
    selection=json.loads((ROOT/f'analysis/optimization_20261003_{latest}/selection.json').read_text(encoding='utf-8'))
    assert report['connected'][0]['score']==selection['winner']['connected_final_score']
    r6=next(r for r in report['representative'] if r['name'].endswith('（R6）'))
    assert r6['wave'] in ('56','57','58') and r6['known_restriction']
    repair=json.loads((ROOT/'analysis/optimization_20261003_r7/repair_amendment.json').read_text(encoding='utf-8'))
    for path,expected in repair['source_sha256'].items():assert digest(path)==expected,path
    candidate=ROOT/f'candidates/optimization_20261003_{latest}'
    manifest=json.loads((candidate/'manifest.json').read_text(encoding='utf-8'))
    for name,metadata in manifest['files'].items():assert digest(candidate/name)==metadata['sha256'],name
    check_script=r'''
<script>
try {
 const check=(condition,label)=>{if(!condition)throw new Error(label)};
 check(document.querySelectorAll('#body tr').length>10,'initial rows');
 check(document.querySelector('#body tr').textContent.includes(report.connected[0].score.toFixed(9)),'repaired leader');
 document.querySelector('#tabs button[data-id=connected]').click();
 const count=(n)=>document.getElementById('count').textContent.includes(n.toLocaleString('en-US'));
 check(count(report.connected.filter(r=>!r.known_restriction).length),'known restrictions hidden');
 document.getElementById('hide').click();check(count(report.connected.length),'all connected records');
 document.getElementById('pageSize').value='10000';document.getElementById('pageSize').dispatchEvent(new Event('input'));
 check(document.querySelectorAll('#body tr').length===report.connected.length,'all rows rendered');
 document.getElementById('search').value='pruned_member_excluded';document.getElementById('search').dispatchEvent(new Event('input'));
 check(document.querySelectorAll('#body tr').length>=1,'new ensemble search');
 document.querySelector('#body tr button').click();check(document.getElementById('detail').open,'details');
 check(document.getElementById('detailText').textContent.includes('source_pointer'),'source provenance');document.getElementById('close').click();
 document.getElementById('search').value='';document.getElementById('search').dispatchEvent(new Event('input'));
 document.querySelector('#tabs button[data-id=mlp_bounds]').click();check(document.querySelectorAll('#body tr').length===2,'MLP intervals');
 check(document.querySelector('#body tr').textContent.includes('～'),'interval display');
 document.querySelector('#tabs button[data-id=historical]').click();check(document.querySelectorAll('#body tr').length===396,'historical statuses');
 document.getElementById('hide').click();check(document.querySelectorAll('#body tr').length===370,'historical restricted records');
 document.querySelector('#tabs button[data-id=csv_test]').click();check(document.querySelectorAll('#body tr').length===7,'actual CSV scores');
 check(document.querySelector('#body tr').textContent.includes('0.417099224'),'CSV leader');
 document.getElementById('sort').click();check(document.querySelector('#body tr').textContent.includes('0.386058058'),'ascending sort');
 document.querySelector('#tabs button[data-id=legacy_annual]').click();check(document.querySelectorAll('#body tr').length===15,'annual diagnostics');
 const result=document.createElement('pre');result.id='qa-result';result.textContent='PASS: six views, new leader, restrictions, all records, search, provenance, intervals, historical statuses, CSV scores, sorting';document.body.append(result);
} catch(error) {const result=document.createElement('pre');result.id='qa-result';result.textContent='FAIL: '+error.stack;document.body.append(result)}
</script>
'''
    QA.mkdir(parents=True,exist_ok=True)
    interaction=QA/'interaction_check.html'
    interaction.write_text(HTML.read_text(encoding='utf-8')+check_script,encoding='utf-8')
    chrome=Path('C:/Program Files/Google/Chrome/Application/chrome.exe')
    def render(path,screenshot=None):
        args=[str(chrome),'--headless=new','--disable-gpu','--no-first-run','--disable-background-networking',
              '--user-data-dir='+tempfile.mkdtemp(prefix='codex-model-ranking-qa-'),
              '--virtual-time-budget=1500','--window-size=1500,2100','--dump-dom']
        if screenshot:args.append('--screenshot='+str(screenshot))
        result=subprocess.run(args+[path.as_uri()],capture_output=True,encoding='utf-8',errors='replace',
                              timeout=45,creationflags=subprocess.CREATE_NO_WINDOW)
        assert result.returncode==0,result.stderr[-2000:]
        return result.stdout
    dom=render(HTML,QA/'ranking_report.png');(QA/'rendered_dom.html').write_text(dom,encoding='utf-8')
    assert f"{selection['winner']['connected_final_score']:.9f}" in dom and '验证来源勘误' in dom
    dom=render(interaction)
    result=re.search(r'<pre id="qa-result">(.*?)</pre>',dom,re.S)
    assert result and result.group(1).startswith('PASS:'),result.group(1) if result else 'No interaction result'
    summary={'status':'passed','source_hashes':len(report['source_manifest']),'resolved_source_pointers':pointers,
             'connected_records':len(report['connected']),'new_round_records':new_records,
             'candidate_manifest_files':len(manifest['files']),'interaction':result.group(1)}
    (QA/'interaction_result.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary,ensure_ascii=False,indent=2))


if __name__=='__main__':main()
