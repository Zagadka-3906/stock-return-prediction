"""Actual172 source inventory with validated single-leaf module imports; preserve unlaunched prototypes."""
from pathlib import Path
A=Path(__file__).resolve().parent
import prepare_frontier133172_full_registry_sources_v1_20261010 as prototype
NAMES=list(prototype.NAMES)
NAMES[0]='register_Frontier133172_round172_artifacts_v2_20261010.py'
NAMES[1]='publish_Frontier133172_round172_full_validation_v2_20261010.py'
def source_paths():
    excluded={A/prototype.NAMES[0],A/prototype.NAMES[1]}
    return list(dict.fromkeys([*[p for p in prototype.source_paths() if p not in excluded],A/NAMES[0],A/NAMES[1],Path(__file__)]))
