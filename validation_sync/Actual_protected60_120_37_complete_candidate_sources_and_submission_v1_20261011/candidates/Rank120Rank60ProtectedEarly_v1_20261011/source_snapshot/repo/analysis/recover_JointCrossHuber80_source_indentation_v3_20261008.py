"""Reuse completed35-state audit and finish the not-yet-created native80 receiver with its actual one-space indentation."""
from pathlib import Path
import sys,textwrap
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
def main():
 original=A/'prepare_JointCrossHuber35_reused_evidence_and_native80_v2_20261008.py'
 pointer=A/'actual_JointCrossHuber35_existing_native_location_v1_20261008.json';out=Path(read(pointer)['output'])
 proof=read(out/'verification.json');assert proof['actual_saved_model_count']==35 and not proof['new_native_replay_claimed']
 for p,d in proof['input_sha256'].items():assert sha(p)==d,p
 create(A/'JointCrossHuber35_factory2_partial_completion_preserved_v3_20261008.json',{
  'status':'actual35_state_audit_passed_factory2_then_failed_before_native80_creation_on_indentation_needle',
  'completed_verification':str(out/'verification.json'),'verification_sha256':sha(out/'verification.json'),
  'original_factory_sha256':sha(original),'actual_native80_controls_started':0,'new_quality_scores':0})
 text=original.read_text(encoding='utf8');body=text[text.index(" old=A/'verify_JointCrossHuber80_native_historical_calendar_v1_20261008.py'"):text.index("if __name__=='__main__':")]
 body=body.replace("needle='    for r in plan", "needle=' for r in plan")
 body=body.replace(' s=s.replace(needle,extra+needle)'," extra=textwrap.indent(textwrap.dedent(extra),' ')\n s=s.replace(needle,extra+needle)")
 body=body.replace('JointCrossHuber80_native_source_scope_recovery_v2_20261008.json','JointCrossHuber80_native_source_scope_recovery_v3_20261008.json')
 compile('def finish():\n'+body,'<fresh80 source recovery>','exec')
 namespace={**globals(),'pointer':pointer,'out':out};exec(compile('def finish():\n'+body,str(Path(__file__)),'exec'),namespace);namespace['finish']()
if __name__=='__main__':main()
