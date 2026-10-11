from pathlib import Path
import sys,runpy
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
def execute(driver):
 import prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 as base
 from run_dependency_queue_v3_20261006 import read,sha
 assert base.allowed()
 data=read(A/'flag17_gain_main_delivery_actual_recovery65_v2_20261011.json');assert sha(data['protocol_alias'])==sha(data['protocol_actual'])==data['sha256']
 original=base.closed
 base.closed=lambda n:original(data['mapping'].get(n,n))
 try:runpy.run_path(str(A/driver),run_name='__main__')
 finally:base.closed=original
