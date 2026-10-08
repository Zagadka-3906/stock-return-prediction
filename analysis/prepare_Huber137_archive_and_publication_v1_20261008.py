"""Prepare the closed-scratch archivist and publish the actual137 receiver preflight and8 live dependencies."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_Huber137_complete_receivers_v1_20261008 import adapt
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start


def main():
    source=A/'archive_CrossFamily136_completed_scoring_CSV_v1_20261008.py'
    text=adapt(source.read_text(encoding='utf8')).replace('CrossFamily136','Huber137').replace('completed136','completed137')
    target=A/'archive_Huber137_completed_scoring_CSV_v1_20261008.py';assert not target.exists();compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n')
    pins={str(p):sha(p) for p in (Path(__file__),source,target)}
    row=start('Huber137_completed_scoring_CSV_archivist_v1_20261008',target.name,[],pins)
    create(A/'actual_Huber137_completed_CSV_archivist_hidden_launch_v1_20261008.json',{
        'status':'started_only_closed_generated137_CSV_archive_on_E','identity':row,'input_sha256':pins,
        'all_models_inputs_and_capsules_retained':True,'new_quality_scores':0})
    from prepare_Huber52_round137_sources_v1_20261008 import source_paths
    names=[Path(__file__),A/'publish_Huber137_receiver_preflight_v1_20261008.py',
        A/'Huber52_prospective_routes_v1_20261008.json',A/'Huber137_complete_hidden_launches_v1_20261008.json']
    pins={str(p):sha(p) for p in names}
    row=start('Huber137_receiver_preflight_main_publication_v1_20261008','publish_Huber137_receiver_preflight_v1_20261008.py',[],pins)
    create(A/'actual_Huber137_receiver_preflight_publication_hidden_launch_v1_20261008.json',{
        'status':'started_main_publication_of_actual24_receivers588_graphs_and7_new_plus1_reused_jobs','identity':row,
        'input_sha256':pins,'actual_quality_scores':0})


if __name__=='__main__':main()
