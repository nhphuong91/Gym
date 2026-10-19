"""Reusable SVG generator for fitness routines."""
from .model import (
    Routine, Section, Exercise, Pair, InfoBox, RulesBox,
    SetCountBox, SetCountEntry, AlternativesTable, AltRow,
)
from .svg_render import render
from .theme import MUSCLE_COLORS, color

__all__ = [
    "Routine", "Section", "Exercise", "Pair", "InfoBox", "RulesBox",
    "SetCountBox", "SetCountEntry", "AlternativesTable", "AltRow",
    "render", "MUSCLE_COLORS", "color",
]
