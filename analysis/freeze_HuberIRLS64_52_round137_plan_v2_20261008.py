"""Verify the bounded plan frozen by recovery2; preserve both versions and never rewrite a plan."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create


def main():
    path=A/'HuberIRLS64_52_round137_plan_v2_20261008.json';plan=read(path)
    expected=[{'group':group,'amplitude':weight} for group in range(6) for weight in (.0025,.005,.01,.025,.05,.075,.085,.1)]
    assert plan['new_cases']==expected and plan['new_case_count']==48 and plan['total_cases']==52
    assert plan['anchors']==[134,135,136] and plan['identity_cases']==1 and plan['maximum_amplitude']==.1
    assert plan['new_quality_scores']==0 and plan['native_model_bank_unchanged']
    for source,digest in plan['input_sha256'].items():assert sha(source)==digest,source
    native=A/'HuberIRLS64_complete_parent_native_stage_v2_20261008.py';text=native.read_text(encoding='utf8')
    assert "assert 0.<spec['amplitude']<=.1" in text
    cdf=A/'CrossFamily_complete_parent_CDF_v1_20261008.py';text=cdf.read_text(encoding='utf8')
    assert '0. <= amplitude <= .1' in text
    create(A/'HuberIRLS64_bounded_plan_recheck_v2_20261008.json',{
        'status':'passed_actual48_bounded_cases_three_anchors_identity_and_unchanged_CDF_guard',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'actual_plan_writer':'recover_HuberIRLS64_amplitude_cap_receivers_v2_20261008.py',
        'plan_sha256':sha(path),'native_stage_sha256':sha(native),'original_CDF_sha256':sha(cdf),
        'plan_or_model_bytes_rewritten':False,'actual_quality_scores':0})


if __name__=='__main__':main()
