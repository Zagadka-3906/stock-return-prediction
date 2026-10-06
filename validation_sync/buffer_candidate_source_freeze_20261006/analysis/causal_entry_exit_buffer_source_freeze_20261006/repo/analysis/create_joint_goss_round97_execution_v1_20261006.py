"""Add full round97 scoring, qualification, lossless QA and main export routes."""
from pathlib import Path

A=Path(__file__).resolve().parent

def put(name,text):
    compile(text,str(A/name),'exec')
    with (A/name).open('x',encoding='utf-8',newline='\n') as f:f.write(text)

def derived(old,new,replacements):
    text=(A/old).read_text(encoding='utf-8')
    for before,after in replacements:
        assert before in text,before
        text=text.replace(before,after)
    put(new,text)

def main():
    derived('build_lossless_ranking_display_v5_20261006.py','build_lossless_ranking_display_v6_20261006.py',[
        ('assert number in (95,96)','assert number == 97')])
    derived('verify_lossless_ranking_display_v6_20261006.py','verify_lossless_ranking_display_v7_20261006.py',[
        ('lossless_ranking_display_qa_v6_20261006','lossless_ranking_display_qa_v7_20261006'),
        ('ranking_display_qa_v6_20261006','ranking_display_qa_v7_20261006'),
        ('build_lossless_ranking_display_v4_20261006.py','build_lossless_ranking_display_v6_20261006.py')])
    derived('lossless_ranking_runtime_adapter_v4_20261006.py','lossless_ranking_runtime_adapter_v5_20261006.py',[
        ('assert number in (95, 96)','assert number == 97'),
        ('build_lossless_ranking_display_v5_20261006','build_lossless_ranking_display_v6_20261006'),
        ('verify_lossless_ranking_display_v6_20261006','verify_lossless_ranking_display_v7_20261006'),
        ('lossless_ranking_display_qa_v6_20261006','lossless_ranking_display_qa_v7_20261006')])
    derived('run_goss_reference_quality_qualified_workflow_20261006.py','run_joint_goss_quality_qualified_workflow_v1_20261006.py',[
        ('assert number in (95, 96)','assert number == 97'),
        ('lossless_ranking_runtime_adapter_v4_20261006','lossless_ranking_runtime_adapter_v5_20261006'),
        ('build_lossless_ranking_display_v5_20261006','build_lossless_ranking_display_v6_20261006'),
        ('verify_lossless_ranking_display_v6_20261006','verify_lossless_ranking_display_v7_20261006')])
    derived('run_goss_reference_quality_with_exact_rank_cache_20261006.py','run_joint_goss_quality_with_exact_rank_cache_v1_20261006.py',[
        ("assert run['round'] in (95,96)","assert run['round'] == 97"),
        ('run_goss_reference_quality_qualified_workflow_20261006.py','run_joint_goss_quality_qualified_workflow_v1_20261006.py')])
    derived('goss_reference_lossless_publication_adapter_20261006.py','joint_goss_lossless_publication_adapter_v1_20261006.py',[
        ('if number not in (95, 96):','if number != 97:'),
        ('expected = 124 if number == 95 else 138','expected = 151'),
        ('collect(number, 6, expected)','collect(number, 7, expected)'),
        ('lossless_ranking_display_qa_v6_20261006','lossless_ranking_display_qa_v7_20261006'),
        ("manifest['actual_complete_QA_version'] = 6","manifest['actual_complete_QA_version'] = 7")])
    derived('watch_validations_main_v6_20261006.py','watch_validations_main_v7_20261006.py',[
        ('    goss(sync)','    goss(sync)\n    from joint_goss_lossless_publication_adapter_v1_20261006 import install as joint\n    joint(sync)'),
        ('state_v6_20261006.json','state_v7_20261006.json')])
    print('Created full original ranking QA and exact-cache qualified execution routes for97.',flush=True)

if __name__=='__main__':main()
