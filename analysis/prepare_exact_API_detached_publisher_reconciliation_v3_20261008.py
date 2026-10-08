from pathlib import Path
A=Path(__file__).resolve().parent
source=A/'reconcile_exact135_144_connected_API_publication_v2_20261008.py';text=source.read_text(encoding='utf8')
old="    old=git('rev-parse','refs/heads/main').decode().strip();assert old==b['parent_commit']\n    git('update-ref','refs/heads/main',commit,old)"
new="    old_head=git('rev-parse','HEAD').decode().strip();assert old_head==b['parent_commit']\n    assert not git('branch','--show-current').strip(), 'Preserve the existing detached publisher checkout'\n    old_branch=git('rev-parse','refs/heads/main').decode().strip();git('merge-base','--is-ancestor',old_branch,commit)\n    git('update-ref','HEAD',commit,old_head)\n    git('update-ref','refs/heads/main',commit,old_branch)"
assert old in text;text=text.replace(old,new).replace('exact135_144_connected_API_reconciliation_v2_20261008.json','exact135_144_connected_API_reconciliation_v3_20261008.json')
target=A/'reconcile_exact135_144_connected_API_publication_v3_20261008.py';assert not target.exists();compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n')
source=A/'prepare135_144_candidates_after_connected_API_v1_20261008.py';text=source.read_text(encoding='utf8')
text=text.replace('publication_reconciliation_v2_20261008','publication_reconciliation_v3_20261008').replace('API_reconciliation_v2_20261008','API_reconciliation_v3_20261008').replace('API_publication_v2_20261008.py','API_publication_v3_20261008.py').replace('prepare135_144_candidates_after_connected_API_v1_20261008.py','prepare135_144_candidates_after_connected_API_v2_20261008.py')
target=A/'prepare135_144_candidates_after_connected_API_v2_20261008.py';assert not target.exists();compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n')
