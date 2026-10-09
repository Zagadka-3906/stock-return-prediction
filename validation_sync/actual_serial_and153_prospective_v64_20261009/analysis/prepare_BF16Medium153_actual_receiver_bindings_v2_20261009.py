"""Bind corrected predecessor publication and compare all observed duplicate score metrics."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create

def main():
    oldpub=A/'publish_BF16Medium78_evidence_v1_20261009.py';pub=A/'publish_BF16Medium78_evidence_v2_20261009.py'
    s=oldpub.read_text(encoding='utf8');needle="    closed('BF16Medium78_round153_full_registration_v1_20261009')";assert s.count(needle)==1
    s=s.replace(needle,"    closed('SparseAfter14829_round152_full_registration_v1_20261009')")
    s=s.replace('actual_completed_SparseAfter148_controls_or_scores_before_full153_qualification','actual_completed_medium153_controls_or_scores_before_full153_qualification')
    compile(s,str(pub),'exec')
    with pub.open('x',encoding='utf8') as f:f.write(s)
    oldscore=A/'run_BF16Medium78_official_comparison_v1_20261009.py';score=A/'run_BF16Medium78_official_comparison_v2_20261009.py'
    s=oldscore.read_text(encoding='utf8');needle='    sources=[Path(__file__),';assert s.count(needle)==1
    s=s.replace(needle,"    duplicate_pointer=A/'actual_BF16Medium153_prior_complete_forecast_duplicate_audit_v1_20261009.json'\n    duplicate_proof=Path(read(duplicate_pointer)['output'])/'verification.json'\n    assert sha(duplicate_proof)==read(duplicate_pointer)['verification_sha256']\n    duplicate=read(duplicate_proof);assert duplicate['actual_current_cases']==73\n    duplicate_by_sha={r['numeric_sha256']:r['prior_full_board_matches'] for r in duplicate['records']}\n"+needle)
    needle='    for n,p in parents.items():';assert s.count(needle)==1
    s=s.replace(needle,"    sources += [duplicate_pointer,duplicate_proof]\n"+needle)
    needle="            create(OUT/f'case{index:02d}_official.json',item);records.append(item)";assert s.count(needle)==1
    replacement="""            previous=duplicate_by_sha.get(item['prediction_numeric_bytes_sha256'],[])
            all8=0
            for observed in previous:
                assert all(metrics[k]==v for k,v in observed['metrics'].items()),observed['id']
                if observed['all8_metrics'] is not None:
                    assert metrics==observed['all8_metrics'],observed['id'];all8+=1
            item['observed_prior_complete_forecast_matches']=len(previous)
            item['observed_prior_complete_all8_metric_crosschecks']=all8
"""
    s=s.replace(needle,replacement+needle);compile(s,str(score),'exec')
    with score.open('x',encoding='utf8') as f:f.write(s)
    create(A/'BF16Medium153_actual_receiver_bindings_v2_20261009.json',{
      'status':'prepared_current153_scoring2_publication2_candidate1_sealer1_registration3_before_admission',
      'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in (Path(__file__),oldpub,pub,oldscore,score)},
      'publisher_predecessor_round':152,'current_scoring_source':score.name,'current_publisher_source':pub.name,
      'current_registration_source':'run_BF16Medium78_round153_full_registration_v3_20261009.py',
      'observed_identical_forecast_metric_comparison_in_actual_score_loop':True,'official_quality_admitted':False,'test_labels_read':False})
    print({'scoring_version':2,'publication_version':2,'registration_version':3,'admitted':False},flush=True)

if __name__=='__main__':main()
