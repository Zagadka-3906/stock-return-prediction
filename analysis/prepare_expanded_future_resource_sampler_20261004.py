"""Create a separate sampler for the actual full-fit and future-inference jobs."""
from pathlib import Path
import ast
import json
ROOT=Path(__file__).resolve().parents[1]
HERE=ROOT/'analysis'


def main():
    full=json.loads((HERE/'expanded_stacking_fulltraining_run_20261004.json').read_text(encoding='utf-8-sig'))
    queues=json.loads((HERE/'expanded_stacking_queues_20261004.json').read_text(encoding='utf-8-sig'))
    run={'pid':full['warm_pid'],'qa_pid':full['qa_pid'],'script':full['warm_script']}
    (HERE/'expanded_future_resource_input_20261004.json').write_text(json.dumps(run,indent=2)+'\n',encoding='utf-8')
    (HERE/'expanded_future_resource_queue_20261004.json').write_text(json.dumps({'active_run_registry':queues['active_run_registry']},indent=2)+'\n',encoding='utf-8')
    text=(HERE/'observe_expanded_stacking_resources_20261004.py').read_text(encoding='utf-8')
    text=text.replace('expanded_stacking_resource_observations_20261004','expanded_future_resource_observations_20261004')
    text=text.replace('expanded_stacking_run_20261004.json','expanded_future_resource_input_20261004.json').replace('expanded_stacking_queues_20261004.json','expanded_future_resource_queue_20261004.json')
    text=text.replace("entries+[run]","entries+[run,{'pid':run['qa_pid']}]")
    text=text.replace("ROOT/'analysis/expanded_stacking_bank_20261004/oof_audit.json'","ROOT/'analysis/expanded_stacking_future_pipelines_qa_20261004/verification.json'")
    text=text.replace("if not psutil.pid_exists(run['pid']):failure='training process ended before OOF audit';break", "if not any(psutil.pid_exists(pid) for pid in (run['pid'],run['qa_pid'])):failure='both full-fit/inference jobs ended before future verification';break")
    text=text.replace('Observed combined training plus active scoring resources from sampler start. Samples miss earlier fits and between-sample peaks. No claim of global resource exhaustion.',
                      'Observed full-training and future-inference jobs plus active scoring from sampler start. Earlier annual/meta fits and full-fit peaks before sampler start are not covered. No global resource-exhaustion claim.')
    text=text.replace('observed_training_scoring_coexistence','observed_full_pipeline_scoring_coexistence')
    path=HERE/'observe_expanded_future_resources_20261004.py';ast.parse(text,filename=str(path))
    if path.exists():assert path.read_text(encoding='utf-8')==text
    else:path.write_text(text,encoding='utf-8',newline='\n')
    print('Full-fit/inference resource sampler prepared; scope starts now.')


if __name__=='__main__':main()
