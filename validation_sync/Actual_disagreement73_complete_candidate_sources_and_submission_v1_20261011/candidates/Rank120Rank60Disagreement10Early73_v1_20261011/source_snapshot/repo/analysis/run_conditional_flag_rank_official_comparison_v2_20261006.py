"""Use the recovered genuine bank; preserve all original comparison mathematics."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path.insert(0, str(A))
SOURCE = A / 'run_conditional_flag_rank_official_comparison_20261006.py'


def main():
    text = SOURCE.read_text(encoding='utf-8')
    text = text.replace("OUT = A / 'conditional_flag_rank_official_comparison_20261006'", "OUT = A / 'conditional_flag_rank_official_comparison_v2_20261006'")
    text = text.replace("BANK = A / 'conditional_flag_rank_bank_20261006'", "BANK = A / 'conditional_flag_rank_bank_v2_20261006'")
    text = text.replace("service_owned_workflows_20261006/conditional_flag_rank_native_bank'", "service_owned_workflows_20261006/conditional_flag_rank_native_bank_v2'")
    text = text.replace('sources = [Path(__file__),', 'sources = [Path(__file__), SOURCE,')
    namespace = {'__file__': __file__, '__name__': 'conditional_flag_recovered_bank_comparison', 'SOURCE': SOURCE}
    exec(compile(text, str(SOURCE), 'exec'), namespace)
    namespace['main']()


if __name__ == '__main__':
    main()
