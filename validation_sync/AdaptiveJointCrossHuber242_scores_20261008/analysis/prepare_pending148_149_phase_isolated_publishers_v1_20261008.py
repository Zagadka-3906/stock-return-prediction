"""Prevent the observed147 phase-directory collision before pending148/149 quality admission."""
from pathlib import Path
import importlib
import sys
import time

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_JointCrossHuber147_core_receivers_v1_20261008 import save
META=A/'pending148_149_phase_isolation_preparation_v1_20261008.json'
FAMILIES={
    148:{'generator':'prepare_AdaptiveJointCrossHuber242_round148_sources_v2_20261008',
        'prior':'recover_Adaptive148_own_full_service_identity_v4_20261008',
        'admission_old':'verify_AdaptiveJointCrossHuber242_round148_sources_v2_20261008.py',
        'admission_current':'verify_AdaptiveJointCrossHuber242_round148_sources_v4_20261008.py',
        'admission_new':'verify_AdaptiveJointCrossHuber242_round148_sources_v5_20261008.py',
        'publisher_old':'publish_AdaptiveJointCrossHuber242_evidence_v2_20261008.py',
        'publisher_current':'publish_AdaptiveJointCrossHuber242_evidence_v4_20261008.py',
        'publisher_new':'publish_AdaptiveJointCrossHuber242_evidence_v5_20261008.py',
        'dispatcher_current':'dispatch_AdaptiveJointCrossHuber148_complete_pipeline_v4_20261008.py',
        'dispatcher_new':'dispatch_AdaptiveJointCrossHuber148_complete_pipeline_v5_20261008.py',
        'old_service':'AdaptiveJointCrossHuber148_complete_chronological_dispatch_v4_20261008',
        'new_service':'AdaptiveJointCrossHuber148_complete_chronological_dispatch_v5_20261008'},
    149:{'generator':'prepare_PureRFFHuber128_round149_sources_v2_20261008',
        'prior':'prepare_Pure149_duplicate_bound_receivers_v3_20261008',
        'admission_old':'verify_PureRFFHuber128_round149_sources_v2_20261008.py',
        'admission_current':'verify_PureRFFHuber128_round149_sources_v3_20261008.py',
        'admission_new':'verify_PureRFFHuber128_round149_sources_v4_20261008.py',
        'publisher_old':'publish_PureRFFHuber128_evidence_v2_20261008.py',
        'publisher_current':'publish_PureRFFHuber128_evidence_v3_20261008.py',
        'publisher_new':'publish_PureRFFHuber128_evidence_v4_20261008.py',
        'dispatcher_current':'dispatch_PureRFFHuber149_complete_pipeline_v3_20261008.py',
        'dispatcher_new':'dispatch_PureRFFHuber149_complete_pipeline_v4_20261008.py',
        'old_service':'PureRFFHuber149_complete_chronological_dispatch_v3_20261008',
        'new_service':'PureRFFHuber149_complete_chronological_dispatch_v4_20261008'}}


def execute(number,original,phase=None):
    for path,digest in read(META)['input_sha256'].items():assert sha(path)==digest,path
    settings=FAMILIES[number]
    generator=importlib.import_module(settings['generator'])
    previous=generator.source_paths
    extras=[Path(__file__),META,A/'isolated_publisher_phase_runtime_v1_20261008.py',
        A/'verify_isolated_publisher_phase_runtime_v1_20261008.py',A/'actual_isolated_publisher_phase_preflight_v1_20261008.json',
        *[A/row[key] for row in FAMILIES.values() for key in ('admission_new','publisher_new','dispatcher_new')]]
    generator.source_paths=lambda:list(dict.fromkeys([*previous(),*extras]))
    prior=importlib.import_module(settings['prior'])
    if phase is None:prior.execute(original)
    else:
        from isolated_publisher_phase_runtime_v1_20261008 import installed_phase
        with installed_phase(phase):prior.execute(original,phase)


def main():
    pointer=A/'actual_isolated_publisher_phase_preflight_v1_20261008.json'
    proof=Path(read(pointer)['output'])/'verification.json'
    assert sha(proof)==read(pointer)['verification_sha256']
    assert read(proof)['actual_fresh_native_processes']==2
    products=[];originals=[]
    for number,row in FAMILIES.items():
        for kind in ('admission','publisher'):
            old=row[kind+'_old'];new=row[kind+'_new']
            source="from pathlib import Path\nimport sys\nROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]\nfrom prepare_pending148_149_phase_isolated_publishers_v1_20261008 import execute\n"
            if kind=='publisher':
                source+=f"if __name__=='__main__':\n import argparse\n parser=argparse.ArgumentParser();parser.add_argument('phase',choices=('controls','scores'));execute({number},{old!r},parser.parse_args().phase)\n"
            else:source+=f"if __name__=='__main__':execute({number},{old!r})\n"
            products.append(save(new,source));originals.append(A/old)
        dispatcher=A/row['dispatcher_current'];originals.append(dispatcher)
        source=dispatcher.read_text(encoding='utf8')
        for kind in ('admission','publisher'):
            assert row[kind+'_current'] in source
            source=source.replace(row[kind+'_current'],row[kind+'_new'])
        version=5 if number==148 else 4
        source=source.replace('complete_hidden_launches_v'+str(version-1),'complete_hidden_launches_v'+str(version))
        needle="pins={str(Path(__file__)):sha(__file__),str(p):sha(p)};rows={}"
        assert source.count(needle)==1
        source=source.replace(needle,"from prepare_pending148_149_phase_isolated_publishers_v1_20261008 import META\n pins={str(Path(__file__)):sha(__file__),str(p):sha(p),str(META):sha(META)};rows={}")
        products.append(save(row['dispatcher_new'],source))
    pins={str(path):sha(path) for path in [Path(__file__),pointer,proof,A/'isolated_publisher_phase_runtime_v1_20261008.py',
        *[A/row['prior'].__add__('.py') for row in FAMILIES.values()],*originals,*products]}
    create(META,{'status':'prospectively_prepared_phase_isolated148_and149_publishers_and_source_admission_before_any_quality',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,
        'actual_two_hidden_Git_process_regression_proof':str(proof),'old_receivers_preserved':True,
        'original242_and128_numeric_grids_selection_all32_generated_sources_and_prospective_graphs_unchanged':True,
        'actual148_149_native_full_and_duplicate_workers_not_restarted':True,'new_quality_scores':0,'test_labels_read':False})
    from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
    retired=[]
    for number,row in FAMILIES.items():
        launch=read(A/'service_owned_workflows_20261006'/row['old_service']/'native_launch.json')
        assert owned(launch)
        parent,worker,idle=suspended_idle(launch,'    closed ('+row['dispatcher_current']+':')
        try:
            assert not worker.children()
            worker.terminate();worker.wait(timeout=10)
            parent.terminate();parent.wait(timeout=10)
        finally:
            for process in (parent,worker):
                if process.is_running():process.resume()
        retired.append({'round':number,'launch':launch,'idle_stack':idle,'scientific_workers_stopped':0})
    create(A/'pending148_149_proved_idle_dispatchers_retired_for_phase_isolation_v1_20261008.json',retired)
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    launches={}
    for number,row in FAMILIES.items():
        launches[str(number)]=start(row['new_service'],row['dispatcher_new'],[],{**pins,str(META):sha(META)})
    create(A/'pending148_149_phase_isolated_hidden_launches_v1_20261008.json',launches)
    print({'started_pending_dispatchers':{key:row['owned_worker_pid'] for key,row in launches.items()}},flush=True)


if __name__=='__main__':main()
