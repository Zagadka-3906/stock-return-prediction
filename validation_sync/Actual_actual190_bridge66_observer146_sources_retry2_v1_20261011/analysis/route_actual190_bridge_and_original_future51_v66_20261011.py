from pathlib import Path
import sys,runpy
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
def execute(driver):
 import prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 as base
 from run_dependency_queue_v3_20261006 import read
 assert base.allowed();mapping=read(A/'actual190_bridge65_and_unchanged_future51_recovery66_admission_v1_20261011.json')['mapping'];original=base.closed
 base.closed=lambda n:original(mapping.get(n,n))
 try:runpy.run_path(str(A/driver),run_name='__main__')
 finally:base.closed=original
