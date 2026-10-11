"""Derive complete156 receivers from the exercised155 route before any new quality."""
from pathlib import Path
import sys,io,tokenize,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
from prepare_BF16Drop05_156_scientific_controls_v1_20261009 import route as scientific_route

def transform(source):
    s=scientific_route(source)
    for old,new in [('round155','round156'),('full155','full156'),('actual155','actual156'),('_r155','_r156'),('第155轮','第156轮'),
        ('QA66','QA67'),('actual80','actual81'),('all80','all81'),('anchor80','anchor81'),('80项','81项')]:s=s.replace(old,new)
    s=s.replace('BF16Drop05_156_actual_full73_training_v2_20261009','BF16Drop05_156_actual_full73_training_v1_20261009')
    s=s.replace('BF16Drop05_81_round156_proposal_v1_20261009','BF16Drop05_81_round156_proposal_v2_20261009')
    numbers={'155':'156','80':'81','66':'67'}
    return tokenize.untokenize([t._replace(string=numbers.get(t.string,t.string)) if t.type==tokenize.NUMBER else t for t in tokenize.generate_tokens(io.StringIO(s).readline)])

def main():
    sources=[Path(__file__)];drafts=[]
    pairs=[('publish_BF16Seed10_80_evidence_v1_20261009.py','publish_BF16Drop05_81_evidence_v1_20261009.py'),
        ('verify_BF16Seed10_155_prior_complete_forecast_duplicate_audit_v1_20261009.py','verify_BF16Drop05_156_prior_complete_forecast_duplicate_audit_v1_20261009.py'),
        ('verify_BF16Seed10_80_prospective_routes_v1_20261009.py','verify_BF16Drop05_81_prospective_routes_v1_20261009.py')]
    for old,new in pairs:
        src,dst=A/old,A/new;s=transform(src.read_text(encoding='utf8'))
        s=s.replace('BF16TwoSeed79_round154_full_registration_v1_20261009','BF16Seed10_80_round155_full_registration_v1_20261009')
        if old.startswith('publish_'):
            needle="    with safe(log),serial(log/'serial_mutex.json'):main(phase)";assert s.count(needle)==1
            s=s.replace(needle,"    from verified_TLS_Git_retry_runtime_v2_20261008 import installed as git_io\n    with safe(log),serial(log/'serial_mutex.json'),git_io(log/'file_backed_git'):main(phase)")
        elif 'duplicate_audit' in old:
            s=s.replace('round154','round155').replace('_r154','_r155')
        else:
            s=s.replace('[148,149,150,151,152,153,154]','[148,149,150,151,152,153,154,155]')
            s=s.replace('len(outputs)==7','len(outputs)==8').replace('==56','==64').replace('==2100','==2400').replace('==21','==24').replace('==14','==16')
            for x,y in [("'prospective_sources':56","'prospective_sources':64"),("'graph_controls':2100","'graph_controls':2400"),
                ("'baselines':21","'baselines':24"),("'physical_model_ties':14","'physical_model_ties':16"),
                ('actual56_drop05_156_prospective_sources2100_graphs21_baselines14','actual64_drop05_156_prospective_sources2400_graphs24_baselines16')]:s=s.replace(x,y)
            s=s.replace("missing={p for p in g.source_paths() if not p.is_file()}",
                "allowed.update({A/'actual_BF16Drop05_156_native42_calendar_location_v1_20261009.json',A/'actual_BF16Drop05_156_full5_independent_location_v1_20261009.json',A/'actual_BF16_medium2048_drop05_seed09_e64_bank6_location_v1_20261009.json'})\n    missing={p for p in g.source_paths() if not p.is_file()}")
        compile(s,str(dst),'exec');assert not dst.exists();drafts.append((src,dst,s))
    for src,dst,s in drafts:dst.write_text(s,encoding='utf8');sources.extend((src,dst))
    sources.extend(A/n for n in ('run_BF16Drop05_81_official_comparison_v1_20261009.py','prepare_BF16Drop05_81_selected_candidate_v1_20261009.py',
        'seal_BF16Drop05_81_selected_candidate_v1_20261009.py','run_BF16Drop05_81_round156_full_registration_v1_20261009.py'))
    create(A/'BF16Drop05_156_actual_receiver_bindings_v1_20261009.json',{'status':'prepared_complete156_receivers_before64_route_prospective_and_admission',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in sources},
        'publisher_predecessor_round':155,'ordered_physical_native_components':1,'own_seed':20261009,'own_dropout':.05,
        'official_quality_admitted':False,'test_labels_read':False})
    print({'prospective_sources_expected':64,'graphs_expected':2400,'quality_admitted':False},flush=True)
if __name__=='__main__':main()
