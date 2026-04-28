"""
Particle dataclass mirroring the C `particle` struct.
"""

from __future__ import annotations

from dataclasses import dataclass

from constants import KG_TO_MEV
from formulae import calc_charge, calc_mass
from lifetime import calc_lifetime_seconds


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
    t_exp_sec: float = 0.0   # experimental mean lifetime in seconds (0 = stable / unknown)

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
        """Relative mass error vs experiment, in percent (None if no exp value)."""
        if self.m_exp_mev <= 0.0:
            return None
        return (self.mass_mev - self.m_exp_mev) / self.m_exp_mev * 100.0

    @property
    def lifetime_seconds(self) -> float:
        """Predicted mean lifetime in seconds (per [B47]). +∞ for stable states."""
        return calc_lifetime_seconds(
            self.eps, self.k, self.P, self.Q, self.kap, self.charge, self.mass_kg
        )

    @property
    def lifetime_log_error(self) -> float | None:
        """log10(T_predicted / T_measured); None if no measurement available."""
        from math import isfinite, log10
        if self.t_exp_sec <= 0.0:
            return None
        T = self.lifetime_seconds
        if not isfinite(T) or T <= 0.0:
            return float("inf")
        return log10(T / self.t_exp_sec)


# Reference particle list — the same set used in the C reference.
# Quantum numbers and experimental masses match heimmass.c verbatim.
# Experimental lifetimes from Particle Data Group (rounded mean-life values).
# 0.0 = stable or unknown.
#
# Notes:
#  - K_0 in Heim's framework is a single state; experimentally it manifests
#    as K_S / K_L mixture. We use K_S = 8.954e-11 s for comparison.
#  - π_+- is an average of π+ and π−; both have lifetime 2.6033e-8 s.
#  - All four Δ states are degenerate in Heim, but PDG lists them with
#    full width Γ ≈ 117 MeV → τ = ℏ/Γ ≈ 5.63e-24 s.
#  - Σ_0 decays electromagnetically (Σ_0 → Λγ), τ ≈ 7.4e-20 s.
#  - Heim's neutral electron e_0 is a prediction with no observed counterpart.
REFERENCE_PARTICLES: list[Particle] = [
    Particle("neutral electron", "e_0",       1, 1, 1, 1, 0, 0,    0.00000000, 0.0),
    Particle("electron",         "e_-",       1, 1, 1, 1, 0, 1,    0.51099907, 0.0),  # stable
    Particle("muon",             "miu_-",     1, 1, 1, 1, 1, 0,  105.65838900, 2.197e-6),
    Particle("eta",              "eta",       1, 1, 0, 0, 0, 0,  547.30000000, 5.0e-19),
    Particle("charged kaon",     "KAPPA_+",   1, 1, 1, 0, 1, 0,  493.67700000, 1.238e-8),
    Particle("neutral kaon",     "KAPPA_0",   1, 1, 1, 0, 1, 1,  497.67200000, 8.954e-11),  # K_S
    Particle("charged pion",     "pi_+-",     1, 1, 2, 0, 0, 0,  139.57018000, 2.6033e-8),
    Particle("neutral pion",     "pi_0",      1, 1, 2, 0, 0, 1,  134.97660000, 8.43e-17),
    Particle("lambda",           "LAMBDA",    1, 2, 0, 1, 0, 0, 1115.68300000, 2.632e-10),
    Particle("omega",            "OMEGA_-",   1, 2, 0, 3, 0, 0, 1672.45000000, 8.21e-11),
    Particle("proton",           "p",         1, 2, 1, 1, 0, 0,  938.27231000, 0.0),  # stable
    Particle("neutron",          "n",         1, 2, 1, 1, 0, 1,  939.56563000, 879.4),
    Particle("neutral xi",       "XI_0",      1, 2, 1, 1, 1, 0, 1314.90000000, 2.90e-10),
    Particle("charged xi",       "XI_-",      1, 2, 1, 1, 1, 1, 1321.32000000, 1.639e-10),
    Particle("positive sigma",   "SIGMA_+",   1, 2, 2, 1, 0, 0, 1189.37000000, 8.018e-11),
    Particle("neutral sigma",    "SIGMA_0",   1, 2, 2, 1, 0, 1, 1192.64200000, 7.4e-20),
    Particle("negative sigma",   "SIGMA_-",   1, 2, 2, 1, 0, 2, 1197.44900000, 1.479e-10),
    Particle("2 charged delta",  "DELTA_++",  1, 2, 3, 3, 0, 0, 1232.00000000, 5.63e-24),
    Particle("positive delta",   "DELTA_+",   1, 2, 3, 3, 0, 1, 1232.00000000, 5.63e-24),
    Particle("neutral delta",    "DELTA_0",   1, 2, 3, 3, 0, 2, 1232.00000000, 5.63e-24),
    Particle("negative delta",   "DELTA_-",   1, 2, 3, 3, 0, 3, 1232.00000000, 5.63e-24),
]


__all__ = ["Particle", "REFERENCE_PARTICLES"]
