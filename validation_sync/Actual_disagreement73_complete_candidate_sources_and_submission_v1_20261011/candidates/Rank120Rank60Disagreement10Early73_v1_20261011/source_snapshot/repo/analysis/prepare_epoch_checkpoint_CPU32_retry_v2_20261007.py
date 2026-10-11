"""Preserve the real Windows read-handle fsync failure and retry with a write-capable handle."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create

def main():
    failure=A/'epoch_durable_neural_checkpoint_CPU32_preflight_20261007/actual_first7_failure_preserved.json'
    assert 'Bad file descriptor' in read(failure)['exception']
    old=A/'epoch_durable_neural_checkpoint_adapter_20261007.py'
    adapter=A/'epoch_durable_neural_checkpoint_adapter_v2_20261007.py';assert not adapter.exists()
    text=old.read_text(encoding='utf8');needle="with temporary.open('rb') as stream:os.fsync(stream.fileno())";assert text.count(needle)==1
    text=text.replace(needle,"with temporary.open('r+b') as stream:os.fsync(stream.fileno())")
    compile(text,str(adapter),'exec');adapter.write_text(text,encoding='utf8',newline='\n')
    oldtest=A/'verify_epoch_durable_neural_checkpoint_CPU32_20261007.py'
    test=A/'verify_epoch_durable_neural_checkpoint_CPU32_v2_20261007.py';assert not test.exists()
    text=oldtest.read_text(encoding='utf8').replace('epoch_durable_neural_checkpoint_adapter_20261007',
      'epoch_durable_neural_checkpoint_adapter_v2_20261007').replace('epoch_durable_CPU32_20261007','epoch_durable_CPU32_v2_20261007').replace(
      'epoch_durable_neural_checkpoint_CPU32_preflight_20261007','epoch_durable_neural_checkpoint_CPU32_preflight_v2_20261007')
    text=text.replace('timeout=300,check=True)','timeout=300,check=False)')
    needle="            phases.append({'phase':mode";assert text.count(needle)==1
    text=text.replace(needle,"            assert result.returncode==0, result.stderr\n"+needle)
    compile(text,str(test),'exec');test.write_text(text,encoding='utf8',newline='\n')
    create(A/'epoch_checkpoint_CPU32_v2_retry_admission_20261007.json',{
      'status':'prepared_fresh_v2_write_capable_flush_after_actual_preserved_Windows_failure',
      'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in [Path(__file__),failure,old,oldtest,adapter,test]},
      'new_native_annual_fits':0,'new_quality_scores':0,'test_labels_read':False})

if __name__=='__main__':main()
