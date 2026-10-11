"""Resolve a cleaned historical export to retained bytes or its immutable Git commit."""
from pathlib import Path
import argparse,gzip,json

def main():
    parser=argparse.ArgumentParser(description='查询仓库整理后的历史归档路径')
    parser.add_argument('path',help='原仓库相对路径，例如 validation_sync/round100/...')
    parser.add_argument('--catalog',type=Path,default=Path(__file__).resolve().parents[1]/'validation_sync/archive_index_20261011.jsonl.gz')
    args=parser.parse_args();requested=args.path.replace('\\','/').removeprefix('./')
    with gzip.open(args.catalog,'rt',encoding='utf8') as f:
        for line in f:
            row=json.loads(line)
            if row['removed_path']==requested:
                print(json.dumps(row,ensure_ascii=False,indent=2));return
    parser.exit(1,'未找到该路径的清理记录；文件可能仍保留或不在本次清理范围。\n')

if __name__=='__main__':main()
