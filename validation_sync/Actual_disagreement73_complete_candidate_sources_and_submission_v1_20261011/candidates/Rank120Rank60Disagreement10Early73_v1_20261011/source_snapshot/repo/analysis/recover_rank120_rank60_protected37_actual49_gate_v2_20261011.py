"""Admit the actual completed 49-case prerequisite, preserving all scientific operations."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
def main():
 assert allowed()
 import run_rank120_rank60_after183_protected37_screen_v1_20261011 as m
 actual='actual_rank60_rank20_after183_mixed49_screen_v1_20261011'
 assert read(A/'service_owned_workflows_20261006'/actual/'service_execution.json')['status']=='passed'
 assert not m.OUT.exists(), 'Never restart a populated scientific output'
 old=m.closed
 m.closed=lambda n:closed(actual if n=='actual_rank60_rank20_after183_mixed37_screen_v1_20261011' else n)
 try:m.main()
 finally:m.closed=old
if __name__=='__main__':main()
