"""Replace an unadmitted historical-recovery draft with the current clean registration contract."""
from pathlib import Path
import sys,re,io,tokenize,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create

def main():
    old=A/'run_SparseAfter14829_round152_full_registration_v2_20261009.py';new=A/'run_BF16Medium78_round153_full_registration_v2_20261009.py'
    s=old.read_text(encoding='utf8')
    s=s.replace('RFFSparse59_round151_full_registration_v1_20261009','SparseAfter14829_round152_full_registration_v1_20261009')
    for a,b in [('SparseAfter14829','BF16Medium78'),('SparseAfter148152','BF16Medium153'),('round152','round153'),
      ('full152','full153'),('actual152','actual153'),('_r152','_r153'),('第152轮','第153轮'),('qa63','qa64'),('QA63','QA64')]:s=s.replace(a,b)
    # The chronological predecessor must stay152, independent of the new target153.
    s=s.replace("'BF16Medium78_round153_full_registration_v1_20261009'", "'SparseAfter14829_round152_full_registration_v1_20261009'",1)
    s=s.replace('(148,148,149,150,151)','(148,149,150,151,152)')
    nums={'152':'153','63':'64','29':'78'}
    s=tokenize.untokenize([t._replace(string=nums.get(t.string,t.string)) if t.type==tokenize.NUMBER else t for t in tokenize.generate_tokens(io.StringIO(s).readline)])
    s=s.replace('预定29项：四个合格锚点、120项细权重重调、零权重恒等对照','预定78项：五个合格锚点、72项正负神经排序融合、零权重恒等对照')
    s=s.replace('完整父方案跨模型细权重重调','新中型神经网络在完整148方案后的正负排序融合')
    s=s.replace('actual_registration_v1_20261009','actual_registration_v2_20261009')
    compile(s,str(new),'exec')
    assert 'recover_exact138' not in s and 'prepare_actual153_candidate_registration_after_TLS15' not in s
    assert "'SparseAfter14829_round152_full_registration_v1_20261009'" in s
    with new.open('x',encoding='utf8') as f:f.write(s)
    create(A/'BF16Medium153_clean_registration_draft_v2_20261009.json',{
      'status':'prepared_unadmitted_clean153_registration_without_historical138_recovery_dependencies',
      'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in (Path(__file__),old,new,A/'run_BF16Medium78_round153_full_registration_v1_20261009.py')},
      'superseded_unadmitted_draft':'run_BF16Medium78_round153_full_registration_v1_20261009.py',
      'new_candidate_and_source_generator_and_full_prospective_admission_still_required':True,
      'actual_quality_scores':0,'actual_future_X_read':False,'test_labels_read':False})
    print({'new_clean_registration_draft':new.name,'admitted':False},flush=True)

if __name__=='__main__':main()
