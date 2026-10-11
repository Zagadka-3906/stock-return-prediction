from bind_BF16Medium153_actual_receiver_dispatch_v42_20261009 import execute
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('phase',choices=('controls','scores'));execute('publish_BF16Medium78_evidence_v2_20261009.py',p.parse_args().phase)
