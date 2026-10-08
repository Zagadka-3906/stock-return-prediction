"""Repair preflight call literals, preserving frozen100 scientific receivers and generated source bytes."""
from pathlib import Path
import sys,time,ast
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def main():
    source=A/'verify_ConeRidgeAlpha100_prospective_routes_v2_20261008.py'
    text=source.read_text(encoding='utf8')
    changes={"'collect(143, 68, 54)'":"'collect(144, 100, 55)'",
        '"namespace[\'snapshot\'](143)"':'"namespace[\'snapshot\'](144)"',
        '"== full[\'scored_records\'] == 68"':'"== full[\'scored_records\'] == 100"',
        "scope['collect'](144,100,54)":"scope['collect'](144,100,55)",
        '(142,100,54),(144,55,100),(144,99,55)':'(143,100,55),(144,55,100),(144,99,55)'}
    for before,after in changes.items():assert text.count(before)==1,(before,text.count(before));text=text.replace(before,after)
    target=A/'verify_ConeRidgeAlpha100_prospective_routes_v3_20261008.py';assert not target.exists()
    compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n')
    create(A/'ConeRidgeAlpha144_prospective_literal_recovery_v2_20261008.json',{
        'status':'frozen_exact_preflight_literal_changes_before_actual144_quality',
        'input_sha256':{str(p):sha(p) for p in (Path(__file__),source,target)},'literal_changes':changes,
        'original_failed_preflight_source_preserved':True,'scientific_receiver_sources_unchanged':True,
        'new_quality_scores':0,'test_labels_read':False})
    from verify_ConeRidgeAlpha100_prospective_routes_v3_20261008 import main as prospective
    prospective()
if __name__=='__main__':main()
