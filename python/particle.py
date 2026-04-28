"""
Particle dataclass mirroring the C `particle` struct.
"""

from __future__ import annotations

from dataclasses import dataclass

from constants import KG_TO_MEV
from formulae import calc_charge, calc_mass


@dataclass(frozen=True)
class Particle:
    """
    Heim-theory description of an elementary particle.

    Six integer quantum numbers fully determine the predicted mass and
    electric charge:

        eps   — time-helicity, ±1
        k     — metrical/configuration index
        P     — double iso-spin (P = 2·s)
        Q     — double angular momentum (Q = 2·J)
        kap   — doublet indicator (0 or 1)
        x     — iso-spin multiplet identifier

    All other quantities (charge, mass) are derived from these via the
    1989 mass formula.

    `name`, `symbol`, `m_exp_mev` are bookkeeping for output / comparison.
    """
    name: str
    symbol: str
    eps: int
    k: int
    P: int
    Q: int
    kap: int
    x: int
    m_exp_mev: float = 0.0

    @property
    def charge(self) -> float:
        """Predicted electric charge quantum number, q_x ∈ {…, -1, 0, +1, …}."""
        return calc_charge(self.eps, self.k, self.P, self.Q, self.kap, self.x)

    @property
    def mass_kg(self) -> float:
        """Predicted rest mass in kilograms."""
        return calc_mass(self.eps, self.k, self.P, self.Q, self.kap, self.charge)

    @property
    def mass_mev(self) -> float:
        """Predicted rest mass in MeV/c²."""
        return self.mass_kg * KG_TO_MEV

    @property
    def error_percent(self) -> float | None:
        """Relative error vs experimental mass, in percent (None if no exp value)."""
        if self.m_exp_mev <= 0.0:
            return None
        return (self.mass_mev - self.m_exp_mev) / self.m_exp_mev * 100.0


# Reference particle list — the same set used in the C reference.
# Quantum numbers and experimental masses match heimmass.c verbatim.
REFERENCE_PARTICLES: list[Particle] = [
    Particle("neutral electron", "e_0",       1, 1, 1, 1, 0, 0,    0.00000000),
    Particle("electron",         "e_-",       1, 1, 1, 1, 0, 1,    0.51099907),
    Particle("muon",             "miu_-",     1, 1, 1, 1, 1, 0,  105.65838900),
    Particle("eta",              "eta",       1, 1, 0, 0, 0, 0,  547.30000000),
    Particle("charged kaon",     "KAPPA_+",   1, 1, 1, 0, 1, 0,  493.67700000),
    Particle("neutral kaon",     "KAPPA_0",   1, 1, 1, 0, 1, 1,  497.67200000),
    Particle("charged pion",     "pi_+-",     1, 1, 2, 0, 0, 0,  139.57018000),
    Particle("neutral pion",     "pi_0",      1, 1, 2, 0, 0, 1,  134.97660000),
    Particle("lambda",           "LAMBDA",    1, 2, 0, 1, 0, 0, 1115.68300000),
    Particle("omega",            "OMEGA_-",   1, 2, 0, 3, 0, 0, 1672.45000000),
    Particle("proton",           "p",         1, 2, 1, 1, 0, 0,  938.27231000),
    Particle("neutron",          "n",         1, 2, 1, 1, 0, 1,  939.56563000),
    Particle("neutral xi",       "XI_0",      1, 2, 1, 1, 1, 0, 1314.90000000),
    Particle("charged xi",       "XI_-",      1, 2, 1, 1, 1, 1, 1321.32000000),
    Particle("positive sigma",   "SIGMA_+",   1, 2, 2, 1, 0, 0, 1189.37000000),
    Particle("neutral sigma",    "SIGMA_0",   1, 2, 2, 1, 0, 1, 1192.64200000),
    Particle("negative sigma",   "SIGMA_-",   1, 2, 2, 1, 0, 2, 1197.44900000),
    Particle("2 charged delta",  "DELTA_++",  1, 2, 3, 3, 0, 0, 1232.00000000),
    Particle("positive delta",   "DELTA_+",   1, 2, 3, 3, 0, 1, 1232.00000000),
    Particle("neutral delta",    "DELTA_0",   1, 2, 3, 3, 0, 2, 1232.00000000),
    Particle("negative delta",   "DELTA_-",   1, 2, 3, 3, 0, 3, 1232.00000000),
]


__all__ = ["Particle", "REFERENCE_PARTICLES"]
