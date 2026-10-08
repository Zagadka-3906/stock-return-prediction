"""Use each declared eligible parent; preserve audit1's pre-proof assertion failure."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
def main():
    source=A/'audit_future_registration_collector_contracts_v1_20261008.py'
    text=source.read_text(encoding='utf8')
    text=text.replace("'prepare_BF16reverse40_round138_sources_v1_20261008',134)","'prepare_BF16reverse40_round138_sources_v1_20261008',135)")
    text=text.replace("'prepare_HuberCrossFamily112_round139_sources_v1_20261008',134)","'prepare_HuberCrossFamily112_round139_sources_v1_20261008',136)")
    text=text.replace('future_registration_collector_contract_audit_v1_20261008.json','future_registration_collector_contract_audit_v2_20261008.json')
    namespace={'__file__':str(Path(__file__)),'__name__':'audit_actual_eligible_future_registration_contracts'}
    exec(compile(text,str(source),'exec'),namespace);namespace['main']()
    create(A/'future_registration_collector_audit1_failure_preserved_20261008.json',{
      'status':'failed_assertion_before_complete_audit1_proof',
      'source_sha256':sha(source),'failure':'Audit1 used undeclared parent134 for round138; actual135/136 contracts passed and137 failed before this assertion.',
      'recovery_source_sha256':sha(__file__),'new_official_scores':0,'new_inference_calls':0})
if __name__=='__main__':main()
