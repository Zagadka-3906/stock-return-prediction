"""Persist concrete owned workflows and remaining135 work; do not mark pending validation complete."""
from pathlib import Path
from datetime import datetime
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,owned
from atomic_optimization_observer_writes_20261005 import write


def main():
    names=['actual_neural_BF16_micro8192_bank6_v2_20261008',
           'BF16_independent_full5_GPU_controls_v2_20261008',
           'BF16_rank_CDF_actual_full37_controls_v1_20261008',
           'BF16_complete_parent_actual_historical_native_hook3_v1_20261008',
           'nonflag_ReverseBayesFine40_round134_full_registration_v1',
           'actual_BF16_independent_rank_controls_main_publication_v1_20261008']
    services={}
    for name in names:
        folder=A/'service_owned_workflows_20261006'/name;row=read(folder/'native_launch.json')
        value={'identity':row,'actually_owned_live':owned(row)}
        if (folder/'service_execution.json').exists():value['terminal']=read(folder/'service_execution.json')
        services[name]=value
    paths=[Path(__file__),A/'BF16wide40_round135_plan_v1_20261008.json',
           A/'BF16_complete_parent_rank_CDF_v1_20261008.py',
           A/'BF16_complete_parent_native_stage_v1_20261008.py',
           A/'predict_BF16_complete_parent_rank_scheme_v1_20261008.py',
           A/'verify_BF16_complete_parent_native_hook3_v1_20261008.py',
           A/'actual_BF16_remaining_bank_runtime_estimate_v1_20261008.json',
           A/'actual_user_submission_deadline_and_priority_20261008.json']
    write(A/'actual_optimization_handoff_20261008.json',{
        'status':'active_optimization_with_owned_running_and_ordered_lazy_workflows',
        'at_local':datetime.now().isoformat(timespec='seconds'),'services':services,
        'input_sha256':{str(p):sha(p) for p in paths},
        'deadline_local':read(paths[-1])['deadline_local'],
        'progress_snapshot':read(A/'actual_manual_resume_progress_20261008.json'),
        'remaining135_required_work':[
            'Wait actual6 own-mature fixed32 BF16 fits; never start a duplicate live fitter.',
            'Require full5 GPU tensor oracle then full37 CDF/111 prefixes then actual3 historical native hooks.',
            'Prepare fresh complete135 scorer, source generator, prospective schema/status/paths/graphs/baselines admission and all8 receivers before first135 quality score.',
            'Preserve whole current qualified134 parent including existing signed two-head Bayes stage; add new BF16 stage afterward.',
            'Use explicitly admitted fixed8192 FP32 BF16-native inference; old16384 routing uses original32768 and is inappropriate for this new recipe.',
            'Select highest actual official continuous S, freeze complete graph/calibration/source bytes before actual future X, run two complete/native/independent/cold80 selected replays or prove exact anchor reuse.',
            'Complete all original six-view45-second full board QA and actual remote main-only publication.',
            'Reassess other feasible model/ensemble/postprocessing directions using remaining deadline and measured resources; do not equate the finite grid with global exhaustion.'
        ],
        'round135_quality_pipeline_not_yet_dispatched':True,'new_quality_scores_by_handoff':0,
        'old_20261007_stop_guard_and_queues_not_restarted':True,'goal_not_paused_or_marked_complete':True,
        'scientific_workers_not_stopped_by_handoff':True,'test_labels_read':False})
    print('Active actual workflow identities and remaining135 source/admission/inference/QA/main work recorded.',flush=True)


if __name__=='__main__':main()
