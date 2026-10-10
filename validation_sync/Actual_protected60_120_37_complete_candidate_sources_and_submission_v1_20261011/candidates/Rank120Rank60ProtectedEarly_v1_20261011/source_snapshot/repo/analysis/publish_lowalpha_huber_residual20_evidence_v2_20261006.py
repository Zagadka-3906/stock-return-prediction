"""Retain the failed TLS publication and publish the actual20-fit bank on main."""
from pathlib import Path
import sys
import time

ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,create,owned
SOURCE=A/'publish_lowalpha_huber_residual20_evidence_20261006.py'


def main():
    preceding=A/'service_owned_workflows_20261006/simplex_residual47_round106_full_registration_v5'
    identity=read(preceding/'native_launch.json')
    while owned(identity):time.sleep(15)
    assert read(preceding/'service_execution.json')['status']=='passed'
    old=A/'service_owned_workflows_20261006/lowalpha_huber_residual_bank20_evidence_publication'
    assert not owned(read(old/'native_launch.json'))
    assert read(old/'service_execution.json')['status']=='failed'
    text=SOURCE.read_text(encoding='utf-8')
    before='service_owned_workflows_20261006/simplex_residual47_round106_full_registration'
    assert text.count(before)==1
    text=text.replace(before,'service_owned_workflows_20261006/simplex_residual47_round106_full_registration_v5')
    before='lowalpha_huber_residual_{phase}_github_20261006';assert text.count(before)==1
    text=text.replace(before,'lowalpha_huber_residual_{phase}_github_v2_20261006')
    before="    before=\"    sources += [p for p in bank.rglob('*.json') if not p.name.startswith('model_dump_')]\""
    assert text.count(before)==1
    # Extend the actual source list in the inner template, retaining every raw
    # failed publication record. Current logs are never immutable inputs.
    injection="""    failure_sources = [ORIGINAL_PUBLICATION_SOURCE,
        A/'lowalpha_huber_residual_bank_github_20261006/failure.json',
        *list((A/'service_owned_workflows_20261006/lowalpha_huber_residual_bank20_evidence_publication').glob('*.json')),
        *list((A/'service_owned_workflows_20261006/lowalpha_huber_residual_bank20_evidence_publication').glob('*.log'))]
    anchor = "    sources += [p for p in bank.rglob('*.json') if not p.name.startswith('model_dump_')]"
    assert text.count(anchor)==1
    text=text.replace(anchor,'    sources += FAILED_PUBLICATION_SOURCES\\n'+anchor)
"""
    # The original replacement still finds the same anchor in the extended body.
    text=text.replace(before,injection+before)
    before="'PUBLICATION_TEMPLATE':SOURCE}"
    assert text.count(before)==1
    text=text.replace(before,"'PUBLICATION_TEMPLATE':SOURCE,'FAILED_PUBLICATION_SOURCES':failure_sources}")
    ns={'__file__':__file__,'__name__':'actual_lowalpha20_failed_transport_recovery_v2',
        'ORIGINAL_PUBLICATION_SOURCE':SOURCE}
    exec(compile(text,str(SOURCE),'exec'),ns)
    import publish_classifier_consensus_workflows_20261006 as helpers
    prior=helpers.sync.git;retries=[]
    def retry_git(*args,**kwargs):
        for attempt in range(3):
            try:return prior(*args,**kwargs)
            except RuntimeError as error:
                if args[0] not in ('ls-remote','push','fetch') or not any(w in str(error).lower() for w in ('tls','ssl','unable to access','connection','timed out')):raise
                retries.append({'command':args[0],'attempt':attempt+1,'error':str(error)[:1200]})
                if attempt==2:raise
                time.sleep(2)
    helpers.sync.git=retry_git
    try:ns['main']()
    finally:
        helpers.sync.git=prior
        folder=A/'lowalpha_huber_residual_bank_github_v2_20261006'
        if folder.exists():create(folder/'actual_transport_retries.json',{'attempts':retries,'TLS_verification_unchanged':True})


if __name__=='__main__':main()
