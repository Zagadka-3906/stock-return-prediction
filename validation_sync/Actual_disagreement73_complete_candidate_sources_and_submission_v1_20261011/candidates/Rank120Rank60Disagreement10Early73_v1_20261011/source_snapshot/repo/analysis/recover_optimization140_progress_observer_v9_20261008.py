"""Recover the progress Markdown writer; retain the failed8 observer and running archivist."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start

def main():
    folder=A/'service_owned_workflows_20261006/actual_optimization135_to140_live_progress_v8_20261008'
    assert not owned(read(folder/'native_launch.json')) and read(folder/'service_execution.json')['status']=='failed'
    source=A/'monitor_actual_optimization135_to140_v8_20261008.py';target=A/'monitor_actual_optimization135_to140_v9_20261008.py'
    text=source.read_text(encoding='utf8').replace('observer_version=8','observer_version=9').replace('progress_v8_20261008','progress_v9_20261008')
    before="        write(A/'actual_optimization135_to140_progress_v9_20261008.md','\\n'.join(lines))"
    assert text.count(before)==1
    text=text.replace(before,"        target=A/'actual_optimization135_to140_progress_v9_20261008.md';temporary=target.with_suffix('.md.part')\n        assert target.resolve().is_relative_to(A.resolve())\n        temporary.write_text('\\n'.join(lines)+'\\n',encoding='utf8',newline='\\n');temporary.replace(target)")
    assert not target.exists();compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n')
    files=[Path(__file__),source,target,folder/'native_launch.json',folder/'service_execution.json',folder/'stderr.log',A/'SpectralGram140_complete_hidden_launches_v4_20261008.json',A/'SpectralGram52_prospective_routes_v2_20261008.json']
    pins={str(p):sha(p) for p in files}
    archive=read(A/'actual_SpectralGram140_completed_CSV_archivist_hidden_launch_v1_20261008.json');assert owned(archive)
    observer=start('actual_optimization135_to140_live_progress_v9_20261008',target.name,[],pins)
    assert owned(observer)
    create(A/'actual_optimization135_to140_progress_hidden_launch_v9_20261008.json',observer)
    create(A/'SpectralGram140_archive_and_observer_preparation_v2_20261008.json',{
        'status':'passed_preserved_exact140_archivist_and_fresh_six_pipeline_observer9_started',
        'input_sha256':pins,'archivist':archive,'observer':observer,'new_quality_scores':0,'test_labels_read':False})
    print('Observer9 writes actual JSON and Markdown atomically; original archivist remains live.',flush=True)

if __name__=='__main__':main()
