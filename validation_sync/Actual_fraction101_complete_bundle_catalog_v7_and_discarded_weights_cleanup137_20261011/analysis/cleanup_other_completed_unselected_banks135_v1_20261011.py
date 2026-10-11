from pathlib import Path
import sys,csv,shutil
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from scoped_user_cleanup_package134_runtime_v1_20261011 import install
gates=install()
from run_dependency_queue_v3_20261006 import read,sha,create
used=set();preserved={};keep=[]
for name in ['Rank120Rank60ConsensusWeight8Early85_v1_20261011','Rank120Rank60ConsensusFraction8Early101_v1_20261011','optimization_20261003_r189']:
    p=A.parent/'candidates'/name/'verification.json';proof=read(p);assert proof['status']=='passed'
    for m in proof['models'].values():
        assert sha(m['path'])==m['sha256'];used.add(m['sha256']);preserved[m['path']]=m['sha256']
catalog=Path('E:/赛题五_本机临时/完整191轮与新增已完成TRAIN评分明细榜_v5_20261011/全部训练验证分数明细.csv')
with catalog.open(encoding='utf-8-sig',newline='') as f:records=list(csv.DictReader(f))
proofs={}
for folder in {Path(r['source']).parent for r in records if r['row_id'].startswith('raw/')}:
    p=folder/'verification.json'
    if p.is_file():
        v=read(p)
        if v.get('status','').startswith('passed'):proofs[p]=p.read_text(encoding='utf8')
for year in range(135,192):
    folder=A/f'optimization_20261003_r{year}';terminal=folder/'full_registration_execution.json';p=folder/'protocol.json'
    if terminal.is_file() and read(terminal)['status']=='passed' and p.is_file():proofs[p]=p.read_text(encoding='utf8')
base=Path('E:/赛题五_本机临时');rows=[];banks=[]
for bank in sorted(base.glob('*bank6*')):
    proof=bank/'verification.json';infos=[bank/str(y)/'info.json' for y in range(2020,2026)]
    if not proof.is_file() or not all(p.is_file() for p in infos):continue
    metadata=[read(p) for p in infos]
    if not all(m.get('status','').startswith('passed') and m.get('model_sha256') for m in metadata):continue
    if any(m.get('model_sha256') in used for m in metadata):keep.append(str(bank));continue
    evidence=next((p for p,t in proofs.items() if bank.name in t),None)
    if evidence is None:continue
    existing=[bank/str(y)/n for y in range(2020,2026) for n in ('model.joblib','checkpoint.joblib') if (bank/str(y)/n).is_file()]
    if not existing:continue
    assert bank.resolve().parent==base.resolve() and all((bank/str(y)/'raw.parquet').is_file() for y in range(2020,2025))
    assert all(m.get('status','').startswith('passed') and m.get('model_sha256') for m in metadata)
    for p in infos:
        model=p.parent/'model.joblib';assert model.is_file() and sha(model)==read(p)['model_sha256'];preserved[str(p)]=sha(p)
    for p in (proof,evidence):preserved[str(p)]=sha(p)
    for p in existing:
        assert not p.is_symlink() and p.resolve().is_relative_to(bank.resolve())
        digest=sha(p);assert digest not in used
        rows.append({'path':str(p),'sha256':digest,'bytes':p.stat().st_size})
    banks.append({'bank':str(bank),'completed_TRAIN_evidence':str(evidence),'six_annual_models_not_in_current_or_fallback_SHA_sets':True})
create(A/'actual_unselected_banks135_cleanup_plan_v1_20261011.json',{'status':'user_authorized_predeclared_only_completed_TRAIN_tested_banks_excluded_from_current37_and_formal189','banks':banks,'delete_only':rows,'preserved_sha256':preserved,'kept_selected_banks':keep})
before=shutil.disk_usage('E:/').free
for r in rows:
    assert gates.allowed();p=Path(r['path']);assert sha(p)==r['sha256'];p.unlink()
for p,d in preserved.items():assert sha(p)==d
result={'status':'passed_unused_completed_TRAIN_model_weights_and_resume_caches_deleted_scores_configs_validation_metadata_and_selected_native_models_preserved','banks':len(banks),'deleted_files':len(rows),'logical_deleted_bytes':sum(r['bytes'] for r in rows),'E_free_before':before,'E_free_after':shutil.disk_usage('E:/').free,'preserved_sha256':preserved,'test_labels_read':False}
create(A/'actual_unselected_banks135_cleanup_verification_v1_20261011.json',result)
print({k:result[k] for k in ('status','banks','deleted_files','logical_deleted_bytes','E_free_before','E_free_after')},flush=True)
