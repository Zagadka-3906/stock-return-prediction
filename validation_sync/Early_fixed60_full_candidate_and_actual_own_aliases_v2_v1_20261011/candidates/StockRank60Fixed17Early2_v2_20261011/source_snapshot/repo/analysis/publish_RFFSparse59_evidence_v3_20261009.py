import argparse
from RFFSparse151_source_closure_receiver_runtime_v1_20261009 import execute
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('phase',choices=('controls','scores'))
    execute('publish_RFFSparse59_evidence_v2_20261009.py',parser.parse_args().phase)
