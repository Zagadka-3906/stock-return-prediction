"""Verify a longer-history alternative independently before any new annual model fitting."""
from pathlib import Path
import sys,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def save(name,text):
    path=A/name;assert not path.exists();compile(text,str(path),'exec');path.write_text(text,encoding='utf8',newline='\n');return path
def main():
    assert allowed()
    source=A/'recent252_rank20_mature_training_population_v1_20261010.py'
    population=save('recent504_rank20_mature_training_population_v1_20261011.py',source.read_text(encoding='utf8').replace('252','504'))
    original=A/'verify_recent252_rank20_mature_population_v1_20261010.py'
    text=original.read_text(encoding='utf8').replace('recent252_rank20_mature_training_population_v1_20261010','recent504_rank20_mature_training_population_v1_20261011')
    text=text.replace("range(1,421)","range(1,841)").replace('(44,111,276)','(44,111,276,533,711)')
    text=text.replace("'training_calendar_window':252","'training_calendar_window':504").replace('calendar[-252:]','calendar[-504:]')
    text=text.replace('(1,19,20,21,253,301,401)','(1,19,20,21,505,601,801)')
    text=text.replace('recent252_rank20_mature_population_actual_CPU_controls_v1_20261010','recent504_rank20_mature_population_actual_CPU_controls_v1_20261011')
    text=text.replace('recent252_maturity_CPU_controls','recent504_maturity_CPU_controls')
    # Explicitly prove this larger fixture exercises a real 504-origin truncation.
    marker="    assert controls[-1]['tied_rank_rows']>0";assert text.count(marker)==1
    text=text.replace(marker,marker+"\n    trimmed=population.training_frame(frame.lazy(),801,cfg).collect()\n    assert trimmed['trade_date'].min()==297 and trimmed['trade_date'].max()<801\n    assert sorted({r['trade_date'] for r in rows if r['is_train'] and r['trade_date']<801})[-504]==297")
    control=save('verify_recent504_rank20_mature_population_v1_20261011.py',text)
    importlib.import_module(control.stem).main()
    proof=A/'recent504_rank20_population_preparation_v1_20261011.json'
    create(proof,{'status':'passed_actual7_independent_long_window_scalar_rank_mean_maturity_and_future_poison_controls_before_training',
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),source,original,population,control,A/'recent504_rank20_mature_population_actual_CPU_controls_v1_20261011.json',A/'forward20_mature_training_labels_v1_20261010.py']},
        'calendar_fixture_dates':840,'training_calendar_window':504,'label_horizon':20,
        'actual504_truncation_exercised':True,'new_native_fits':0,'new_quality_scores':0,
        'actual_future_X_read':False,'test_labels_read':False})
    print({'long_window_CPU_cases_passed':7,'actual_504_origin_truncation_verified':True,'annual_training_not_started':True},flush=True)
if __name__=='__main__':main()
