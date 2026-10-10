"""Expand the rank margin to the whole [0,1] range after actual deadzone evidence."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'


def main():
    kernel = (A / 'causal_entry_exit_buffer_20261006.py').read_text(encoding='utf-8')
    assert kernel.count('assert 0. <= margin <= .1') == 1
    wider = kernel.replace('assert 0. <= margin <= .1', 'assert 0. <= margin <= 1.')
    target = A / 'causal_entry_exit_buffer_v2_20261006.py'
    compile(wider, str(target), 'exec')
    assert not target.exists()
    with target.open('x', encoding='utf-8', newline='') as stream: stream.write(wider)
    previous = A / 'verify_causal_entry_exit_buffer_full_controls_v2_20261006.py'
    text = previous.read_text(encoding='utf-8')
    text = text.replace('from causal_entry_exit_buffer_20261006 import transform',
        'from causal_entry_exit_buffer_v2_20261006 import transform')
    text = text.replace("A / 'causal_entry_exit_buffer_20261006.py'", "A / 'causal_entry_exit_buffer_v2_20261006.py'")
    text = text.replace("OUT = A / 'causal_entry_exit_buffer_full_controls_v2_20261006'",
        "OUT = A / 'causal_entry_exit_buffer_full_controls_v3_20261006'")
    text = text.replace('margins = [0., .00025, .0005, .001, .002, .004, .008, .016, .032, .064, .1]',
        'margins = [0., .00025, .0005, .001, .002, .004, .008, .016, .032, .064, .1, .2, .4, .6, .8, 1.]')
    text = text.replace("A / 'recover_causal_entry_exit_buffer_controls_v2_20261006.py',",
        "A / 'recover_causal_entry_exit_buffer_controls_v2_20261006.py',\n"
        "        A / 'expand_causal_entry_exit_buffer_controls_v3_20261006.py',\n"
        "        A / 'causal_entry_exit_buffer_full_controls_v2_20261006/verification.json',\n"
        "        A / 'causal_entry_exit_buffer_full_controls_v2_20261006/actual_parent_transition_diagnostic.json',")
    text = text.replace("'actual_all11_margin_controls'", "'actual_all16_margin_controls'")
    target = A / 'verify_causal_entry_exit_buffer_full_controls_v3_20261006.py'
    compile(text, str(target), 'exec')
    assert not target.exists()
    with target.open('x', encoding='utf-8', newline='') as stream: stream.write(text)
    print('created wider source and 16-case full controls without changing earlier frozen sources')


if __name__ == '__main__': main()
