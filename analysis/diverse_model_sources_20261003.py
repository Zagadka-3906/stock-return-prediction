"""Dispatch frozen old/new model banks without mutating either training module."""
from pathlib import Path
import train_diverse_backbones_20261003 as base
import train_neural_bank_20261003 as bank
OUT=bank.OUT
CONFIGS={**base.CONFIGS,**bank.CONFIGS}
NEW_CONFIGS=bank.CONFIGS
YEARS=base.YEARS
read,dump,sha,log=base.read,base.dump,base.sha,base.log
load_bundle,predict_arrays=base.load_bundle,base.predict_arrays


def source_dir(name):
    assert name in CONFIGS
    return (bank.OUT if name in bank.CONFIGS else base.OUT)/name


def model_path(name,year):return source_dir(name)/f'model_{year}.joblib'


def train_one(name,year):
    return bank.train_one(name,year) if name in bank.CONFIGS else base.train_one(name,year)


def verify():
    base.verify();bank.verify()
    assert read(base.OUT/'oof_audit.json')['status']==read(bank.OUT/'oof_audit.json')['status']=='passed'
