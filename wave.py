import pygame
from dataclasses import dataclass

@dataclass
class Wave:
    frequency: int
    amplitude: float
    phase_shift: float
