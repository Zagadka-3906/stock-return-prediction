import argparse
from HuberSparse150_all5_annual_receiver_runtime_v1_20261009 import execute
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('phase',choices=('controls','scores'))
    execute('publish_HuberSparse59_evidence_v1_20261009.py',parser.parse_args().phase)
