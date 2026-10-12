"""Compatibilité : la lecture des exports HRC vit dans spinsacademy.hrc."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from spinsacademy.hrc import *  # noqa: E402,F401,F403
from spinsacademy.hrc import ROOT, RAW, NC  # noqa: E402,F401
