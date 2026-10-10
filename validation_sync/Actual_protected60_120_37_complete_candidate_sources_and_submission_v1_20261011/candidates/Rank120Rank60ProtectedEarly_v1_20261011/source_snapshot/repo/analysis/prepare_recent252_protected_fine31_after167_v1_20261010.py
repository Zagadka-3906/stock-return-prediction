"""Targeted TRAIN-only refinement around the qualified recent252 protected optimum; no refits."""
from pathlib import Path
import sys,io,tokenize
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import create,sha
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed

def main():
    assert allowed()
    original=A/'run_RecentReturn252_after167_high_impact65_screen_v1_20261010.py'
    text=original.read_text(encoding='utf8').replace('RecentReturn252_after167_high_impact65','RecentReturn252_after167_protected_fine31')
    a=text.index('def cases():');b=text.index('\ndef main():',a)
    text=text[:a]+'''def cases():
    rows=[{'kind':'anchor168','role':None,'weight':0.,'sign':1.,'protect_fraction':None}]
    for fraction in (.1,.125,.15,.175,.2,.225):
        for weight in (.008,.012,.016,.024,.032):
            rows.append({'kind':'valid_pool_protection_v1','role':'nonflag_valid','weight':weight,'sign':1.,'protect_fraction':fraction})
    assert len(rows)==31;return rows

''' +text[b:]
    needle='    assert allowed()\n';assert needle in text
    text=text.replace(needle,needle+"    closed('RecentReturn252Protected168_round168_full_registration_v1_20261010')\n    receipt=read(A/'github_validation_sync_main_20261005/round168_receipt.json')\n    assert receipt['status']=='pushed_and_remote_head_verified' and receipt['scored_records']==67\n",1)
    needle="A/'optimization_20261003_r167/selected_validation.npy',A/'optimization_20261003_r167/calibrated_csv_official.json'"
    assert text.count(needle)==1
    text=text.replace(needle,needle+",A/'optimization_20261003_r168/selected_validation.npy',A/'optimization_20261003_r168/calibrated_csv_official.json',A/'github_validation_sync_main_20261005/round168_receipt.json'")
    old="scoring=A/'RecentReturn252_after167_protected_fine31_D_scoring_v1_20261010/scoring_validation_only'"
    assert text.count(old)==1;text=text.replace(old,"scoring=OUT/'scoring_validation_only'")
    old="for name in ('测试集_X.csv','测试集_Y.csv'):os.link(A/'optimization_20261003_r95/scoring_validation_only'/name,scoring/name)"
    assert text.count(old)==1
    text=text.replace(old,"for name in ('测试集_X.csv','测试集_Y.csv'):\n        import shutil\n        source=A/'optimization_20261003_r95/scoring_validation_only'/name\n        shutil.copyfile(source,scoring/name);assert sha(source)==sha(scoring/name)")
    text=text.replace("baseline=read(A/'optimization_20261003_r167/calibrated_csv_official.json')['metrics'];", "anchor168=np.load(A/'optimization_20261003_r168/selected_validation.npy',mmap_mode='r')\n    baseline=read(A/'optimization_20261003_r168/calibrated_csv_official.json')['metrics'];")
    text=text.replace("if c['kind']=='anchor167':return np.asarray(parent[:n])","if c['kind']=='anchor168':return np.asarray(anchor168[:n])")
    text=text.replace("'parent_round':167,","'parent_round':168,'actual_scheme_base_round':167,")
    text=text.replace('Return65','RecentReturn252_fine31').replace('passed65_','passed31_')
    text=tokenize.untokenize([t._replace(string={'65':'31','64':'30','192':'90'}.get(t.string,t.string)) if t.type==tokenize.NUMBER else t for t in tokenize.generate_tokens(io.StringIO(text).readline)])
    filename='run_RecentReturn252_after167_protected_fine31_screen_v1_20261010.py'
    assert not (A/filename).exists();compile(text,str(A/filename),'exec');(A/filename).write_text(text,encoding='utf8',newline='\n')
    create(A/'RecentReturn252_after167_protected_fine31_source_admission_v1_20261010.json',{'status':'compiled31_training_only_predeclared_local_weight_and_protected_fraction_refinements_waiting_full168','input_sha256':{str(p):sha(p) for p in [Path(__file__),original,A/filename]},'new_native_fits':0,'new_quality_scores':0,'hypotheses':31,'test_X_read':False,'test_labels_read':False,'large_scoring_files_volume':'E','current_exact016_015_configuration_included':True})
    from handoff_ready_goss_full_execution_20261006 import start_service
    assert allowed()
    row=start_service('actual_RecentReturn252_after167_protected_fine31_screen_v1_20261010',filename,[],{str(A/filename):sha(A/filename)})
    create(A/'actual_RecentReturn252_after167_protected_fine31_screen_activation_v1_20261010.json',row)
    print({'worker':row['owned_worker_pid'],'predeclared_local_cases':31,'new_native_fits':0,'score_CSV_volume':'E'},flush=True)
if __name__=='__main__':main()
