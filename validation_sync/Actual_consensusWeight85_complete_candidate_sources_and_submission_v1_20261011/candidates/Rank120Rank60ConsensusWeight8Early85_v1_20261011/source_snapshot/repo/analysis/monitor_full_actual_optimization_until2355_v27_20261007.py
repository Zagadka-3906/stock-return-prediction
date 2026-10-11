"""Report actual post-resume evidence; numerical completion requires proof and actual main receipt."""
from pathlib import Path
import re,sys,time
import psutil
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,owned
from atomic_optimization_observer_writes_20261005 import write

def snapshot():
    rounds={};closed=[]
    for number,family,expected in [(127,'nonflag_RFF128Hi76',76),(128,'nonflag_RidgeFine52',52),(129,'nonflag_RFF128StreamMid76',76),(130,'nonflag_EmpiricalBayes40',40)]:
        folder=A/f'{family}_official_comparison_v1_20261007'
        rows=[read(p) for p in folder.glob('case*_official.json')]
        full=A/f'optimization_20261003_r{number}/full_registration_execution.json'
        receipt=A/f'github_validation_sync_main_20261005/round{number}_receipt.json'
        qualified=full.is_file() and receipt.is_file() and read(full)['status']=='passed' and read(receipt)['status']=='pushed_and_remote_head_verified'
        rounds[str(number)]={'family':family,'actual_completed_official_comparisons':len(rows),'expected_comparisons':expected,
          'best_scored_so_far':max([r['connected_final_score'] for r in rows],default=None),
          'actual_full_board_and_main_closed':qualified,'stage':read(folder/'actual_stage.json') if (folder/'actual_stage.json').exists() else None}
        if qualified:closed.append(number)
    best_number=121;best=read(A/'optimization_20261003_r121/selection.json')['winner']['metrics']['final_score']
    for number in closed:
        score=read(A/f'optimization_20261003_r{number}/selection.json')['winner']['metrics']['final_score']
        if score>best:best_number,best=number,score
    log=A/'service_owned_workflows_20261006/neural16384_annual/stdout.log'
    text=log.read_text(encoding='utf8',errors='replace')[-25000:]
    epoch=re.findall(r'\[([^]]+)\] MLP y_rank epoch(\d+)/(\d+)',text)
    storage=read(A/'neural16384_full_storage_20261005.json')
    complete_years=sorted(read(p)['year'] for p in Path(storage['output_directory']).glob('*/info_202[0-5].json'))
    return {'status':'actual_user_authorized_foreground_optimization_until_fixed2355_stop',
      'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'actual_user_reply':'现在继续至23:55',
      'stop_at_local':'2026-10-07T23:55:00+08:00','automatic_morning_resume_enabled':False,
      'best_fully_qualified_round':best_number,'best_fully_qualified_score':best,'rounds':rounds,
      'latest_fully_qualified_round':max([126,*closed]),'available_RAM_GiB':psutil.virtual_memory().available/2**30,
      'neural_completed_saved_years':complete_years,'neural_latest_logged_epoch':epoch[-1] if epoch else None,
      'intra_annual_checkpoint_supported_by_original_running_fitter':False,
      'shutdown_guard':read(A/'shutdown_ready_stop_until_manual_continue_20261007/guardian_status.json'),
      'global_optimization_boundary_proven':False,'test_labels_read':False}

def main():
    while True:
        write(A/'single_host_optimization_full_live_status_v27_20261007.json',snapshot())
        time.sleep(15)

if __name__=='__main__':main()
