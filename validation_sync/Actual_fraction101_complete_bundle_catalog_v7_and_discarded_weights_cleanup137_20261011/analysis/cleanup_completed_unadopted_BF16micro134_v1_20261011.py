from pathlib import Path
import sys,shutil
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from scoped_user_cleanup_package134_runtime_v1_20261011 import install
gates=install()
from run_dependency_queue_v3_20261006 import read,sha,create
used=set();preserved={}
for name in ['Rank120Rank60ConsensusWeight8Early85_v1_20261011','Rank120Rank60ConsensusFraction8Early101_v1_20261011']:
    p=A.parent/'candidates'/name/'verification.json';proof=read(p);assert proof['status']=='passed'
    for m in proof['models'].values():
        assert sha(m['path'])==m['sha256'];used.add(m['sha256']);preserved[m['path']]=m['sha256']
    preserved[str(p)]=sha(p)
selection=A/'optimization_20261003_r135/selection.json';s=read(selection)
assert s['actual_expected_unique_native_models']==18 and s['chosen_postprocessor']['model']=='nonflag_residual_empirical_bayes64_equal_mean_two'
preserved[str(selection)]=sha(selection)
base=Path('E:/赛题五_本机临时');bank=base/'neural_BF16_micro8192_bank6_v2_20261008'
assert bank.resolve().parent==base.resolve()
proof=bank/'verification.json';assert read(proof)['actual_native_fits']==6;preserved[str(proof)]=sha(proof)
rows=[]
for year in range(2020,2026):
    info=bank/str(year)/'info.json';meta=read(info);assert meta['status']=='passed_actual_complete_mature_BF16_micro_annual_model' and meta['model_sha256'] not in used
    model=bank/str(year)/'model.joblib';assert sha(model)==meta['model_sha256']
    for p in (model,bank/str(year)/'checkpoint.joblib'):
        assert p.is_file() and not p.is_symlink() and p.resolve().is_relative_to(bank.resolve())
        rows.append({'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size})
    for p in (info,bank/str(year)/'frozen_training_inputs.json'):preserved[str(p)]=sha(p)
create(A/'actual_unadopted_BF16micro134_cleanup_plan_v1_20261011.json',{'status':'user_authorized_completed_tested_micro_model_bank_not_in_selected37_models','delete_only':rows,'preserved_sha256':preserved,'selection_evidence':str(selection),'current37_model_SHA_set':sorted(used)})
before=shutil.disk_usage('E:/').free
for r in rows:
    assert gates.allowed();p=Path(r['path']);assert sha(p)==r['sha256'];p.unlink()
for p,d in preserved.items():assert sha(p)==d
result={'status':'passed_unused_complete_micro8192_six_annual_weights_and_six_resume_caches_deleted_scores_and_configuration_preserved_current37_models_rehashed','deleted_files':len(rows),'logical_deleted_bytes':sum(r['bytes'] for r in rows),'E_free_before':before,'E_free_after':shutil.disk_usage('E:/').free,'preserved_sha256':preserved,'test_labels_read':False}
create(A/'actual_unadopted_BF16micro134_cleanup_verification_v1_20261011.json',result)
print({k:result[k] for k in ('status','deleted_files','logical_deleted_bytes','E_free_before','E_free_after')},flush=True)
