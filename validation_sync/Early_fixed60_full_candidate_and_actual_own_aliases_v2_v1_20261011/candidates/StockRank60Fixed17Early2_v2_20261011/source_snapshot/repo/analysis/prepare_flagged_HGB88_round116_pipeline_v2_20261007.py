"""Retain the failed prototype; fix generated quoting before any workflow admission."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create

def main():
    source=A/'prepare_flagged_HGB88_round116_pipeline_20261007.py'
    text=source.read_text(encoding='utf8')
    lines=text.splitlines(keepends=True)
    matches=[i for i,line in enumerate(lines) if "text=text.replace('preserved_scheme_training_parent_round=106,'" in line]
    assert len(matches)==1
    lines[matches[0]]='            text=text.replace("preserved_scheme_training_parent_round=106,", "preserved_scheme_training_parent_round=106, actual_scheme_base_round=pilot[\'actual_scheme_base_round\'],")\n'
    text=''.join(lines)
    # This wrapper is the sole preparation authority, while the prototype is retained.
    namespace={'__file__':str(Path(__file__)),'__name__':'prospective_pipeline_preparation_v2'}
    exec(compile(text,str(source),'exec'),namespace)
    namespace['main']()
    create(A/'flagged_HGB88_round116_pipeline_preparation_prototype_failure_20261007.json',{'status':'prototype_compile_failure_preserved_before_any_generated_file_or_workflow_launch',
        'prototype_sha256':sha(source),'recovery_source_sha256':sha(Path(__file__)),'failure':'nested generated string quoting SyntaxError','canonical116_sources_written':0,'new_quality_scores':0})

if __name__=='__main__':main()
