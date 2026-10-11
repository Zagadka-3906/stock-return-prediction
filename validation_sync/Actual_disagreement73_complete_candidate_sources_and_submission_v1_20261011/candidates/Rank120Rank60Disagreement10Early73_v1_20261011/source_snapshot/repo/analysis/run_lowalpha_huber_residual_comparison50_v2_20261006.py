"""Keep the fixed50-case search and use the actual complete-registration recovery."""
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
SOURCE=A/'run_lowalpha_huber_residual_comparison50_20261006.py'


def main():
    text=SOURCE.read_text(encoding='utf-8')
    before='service_owned_workflows_20261006/simplex_residual47_round106_full_registration_v3'
    assert text.count(before)==1
    text=text.replace(before,'service_owned_workflows_20261006/simplex_residual47_round106_full_registration_v5')
    before='    evidence=[Path(__file__),SOURCE,';assert text.count(before)==1
    text=text.replace(before,"    evidence=[ORIGINAL_LOWALPHA_SOURCE, A/'lowalpha_huber_residual50_source_construction_preflight_20261006.json', Path(__file__),SOURCE,")
    ns={'__file__':__file__,'__name__':'actual_lowalpha_comparison50_after_complete_registration',
        'ORIGINAL_LOWALPHA_SOURCE':SOURCE}
    exec(compile(text,str(SOURCE),'exec'),ns);ns['main']()


if __name__=='__main__':main()
