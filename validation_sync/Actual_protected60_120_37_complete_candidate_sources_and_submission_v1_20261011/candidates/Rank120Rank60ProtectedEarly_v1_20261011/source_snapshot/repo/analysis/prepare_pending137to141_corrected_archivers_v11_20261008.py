"""Archive only successfully closed temporary CSVs from the actual fresh11 scientific services."""
from pathlib import Path
import sys,re
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import sha,create,read
def main():
    import recover_pending137to141_registration_contracts_v11_20261008 as h
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    jobs=[('Huber137',3),('BF16reverse138',1),('HuberCrossFamily139',1),('SpectralGram140',1),('KrylovGram141',2)]
    rows={};sources=[Path(__file__),A/'pending137to141_receiver_dispatch_v11_20261008.json']
    for family,version in jobs:
        old=A/f'archive_{family}_completed_scoring_CSV_v{version}_20261008.py'
        text=h.remap(old.read_text(encoding='utf8'))
        text=re.sub(r'(scoring_CSV_archive)_v\d+_20261008',r'\1_v11_20261008',text)
        target=A/f'archive_{family}_completed_scoring_CSV_v11_20261008.py';assert not target.exists();compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n')
        sources.extend((old,target))
        name=family+'_completed_scoring_CSV_archivist_v11_20261008'
        rows[name]=start(name,target.name,[],{str(target):sha(target),str(sources[1]):sha(sources[1])})
    create(A/'pending137to141_corrected_archivers_hidden_launches_v11_20261008.json',{
        'status':'started_five_closed_only_CSV_archivers_following_fresh11_services','launches':rows,
        'input_sha256':{str(p):sha(p) for p in sources},'scientific_inputs_or_models_deleted':0,'training_workers_stopped':0})
if __name__=='__main__':main()
