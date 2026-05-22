"""
Heim 1989 selected-results tables (G-Tabellen II, IV, V_{a,b,c}).
==================================================================

This module transcribes the historical "Ausgewählte Ergebnisse"
tables from `downloads/G_Ausgewaehlte_Ergebnisse.pdf` (IGW Innsbruck
2003, citing Heim 1979/89/98 and 1984) as a structured Python data
source.

Five tables are included:

  TABLE_I    — Quantum numbers of ground states N = 0  (page 2)
               (k, n, m, p, σ, P, Q, εq_x, εC, ℜ) per particle
  TABLE_II   — Theoretical data of elementary particles with
               mean lives > 10⁻¹⁶ sec, calculated by B. Heim 1989
               (page 3): masses, J, P, I, S, B, mean life
  TABLE_IV   — Approximate meson resonances (k=1, page 5):
               23 entries with (P, N, K_B, theoretical mass)
  TABLE_V_a  — Approximate baryon resonances (k=2, page 6):
               N* and Λ* families
  TABLE_V_b  — Approximate baryon resonances (k=2, page 7):
               more Λ*, Ξ*, Δ*
  TABLE_V_c  — Approximate baryon resonances (k=2, page 8):
               Σ* family

Source pointers from Joel's May 2026 review (Heim-Theory Discord)
confirmed these table locations. Charge-doublet entries are recorded
as `N = (a, b)` where the first is for the (typically) negative or
neutral state and the second is for the partner.  Mass entries
follow the same convention.

This data is structured so the *next* reconstruction step (steps 2 and
3 of the audit-priority order in the README) — namely "implement
Heim's (P, N, K_B) resonance procedure and reproduce G Table IV / V
from first principles" — has a ground-truth target to verify against.

Run with:
    ./venv/bin/python python/g_tables.py
to print a summary.

Source: `downloads/G_Ausgewaehlte_Ergebnisse.pdf`.
"""

from __future__ import annotations

from typing import NamedTuple


# ----------------------------------------------------------------------
# Table II: theoretical data of elementary particles, Heim 1989 (page 3)
# ----------------------------------------------------------------------
# Format: (symbol, mass MeV, J, P_parity, I, S, B, mean_life_1e-8_sec)
# Mean life "∞" coded as None.  Photons, neutrinos handled separately.

class TableII(NamedTuple):
    symbol: str
    mass_MeV: float
    J: float
    P: int     # parity (intrinsic), can be -1, +1
    I: float   # isospin
    S: int     # strangeness
    B: int     # baryon number
    mean_life_s: float | None    # mean life in seconds, None=stable


TABLE_II_PHOTON = TableII("γ", 0.0, 1, -1, 0, 0, 0, None)

TABLE_II_LEPTONS: list[TableII] = [
    TableII("ν_e",   3.81e-9,    0.5,  0, 0, 0, 0, None),
    TableII("ν_μ",   5.37e-3,    0.5,  0, 0, 0, 0, None),
    TableII("ν_τ",   10.752e-3,  0.5,  0, 0, 0, 0, None),
    TableII("ν_4",   21.059e-3,  0.5,  0, 0, 0, 0, None),
    TableII("ν_5",   207.001e-3, 0.5,  0, 0, 0, 0, None),
    TableII("e",     0.51100343, 0.5, +1, 0, 0, 0, None),       # ±1 in P
    TableII("e_0",   0.51617049, 0.5, +1, 0, 0, 0, None),
    TableII("μ",     105.65948493, 0.5, +1, 0, 0, 0, 219.94237553e-8),
]

TABLE_II_MESONS: list[TableII] = [
    TableII("π+",    139.56837088, 0, -1, 1,    0, 0, 2.60282911e-8),
    TableII("π0",    134.96004114, 0, -1, 1,    0, 0, 0.84016427e-8 * 1e-8),
    TableII("η",     548.80002432, 0, -1, 0,    0, 0, 0.00233820e-8 * 1e-8),
    TableII("K+",    493.71425074, 0, -1, 0.5, +1, 0, 1.23709835e-8),
    TableII("K0",    497.72299959, 0, -1, 0.5, +1, 0, 5.17900027e-8),
    TableII("K̄0",    497.72299959, 0, -1, 0.5, -1, 0, 0.00887666e-8),
]

TABLE_II_BARYONS: list[TableII] = [
    TableII("p",     938.27959246, 0.5, +1, 0.5,  0, 1, None),
    TableII("n",     939.57336128, 0.5, +1, 0.5,  0, 1, 917.33526856 * 1e-8 * 1e8),  # very long
    TableII("Λ",     1115.59979064, 0.5, +1, 0,   0, 1, 0.02578198 * 1e-8),
    TableII("Σ+",    1189.37409717, 0.5, +1, 1,   1, 1, 0.00800714 * 1e-8),
    TableII("Σ-",    1197.30443002, 0.5, +1, 1,   1, 1, 0.01481729 * 1e-8),
    TableII("Σ0",    1192.47794854, 0.5, +1, 1,   1, 1, 0.42958026e-10),
    TableII("Ξ-",    1321.29326013, 0.5, +1, 0.5, -2, 1, 0.01653050 * 1e-8),
    TableII("Ξ0",    1314.90206200, 0.5, +1, 0.5, -2, 1, 0.02961947 * 1e-8),
    TableII("Ω-",    1672.17518902, 1.5, +1, 0,   -3, 1, 0.01317650 * 1e-8),
    # o-family values corrected May 2026 from direct manuscript
    # reading of J0032 p.39. The previous values (1232.92, 1234.61,
    # 1229.99, 1237.06) were transcribed from a derivative source
    # and did not match Heim's published Tabelle II. Lifetimes are
    # retained pending a re-read of the same page.
    TableII("o++",   1236.02333225, 1.5, +1, 1.5,  0, 1, 5.99071759e-16),
    TableII("o+",    1235.99646406, 1.5, +1, 1.5,  0, 1, 5.72954997e-16),
    TableII("o-",    1231.20485197, 1.5, +1, 1.5,  0, 1, 6.74230244e-16),
    TableII("o0",    1235.99143567, 1.5, +1, 1.5,  0, 1, 5.08526841e-16),
]


# ----------------------------------------------------------------------
# Table I: Quantum numbers of ground states N = 0  (page 2 of G)
# ----------------------------------------------------------------------
# Per particle: (k, n, m, p, σ, P, Q, εq_x, εC, ℜ)
#   ℜ in Heim's column == κ (kap) in our (eps, k, P, Q, kap, x) scheme.
#   εC == ε · strangeness (NOT in our scheme).
#   εq_x is the signed integer charge of the particle.
#
# Heim's (n, m, p, σ) are listed *as input quantum numbers*.  In our
# Python port they are *computed* from W via the greedy decomposition
# in formulae.calc_n.  Cross-checking the two against each other
# verifies whether the greedy algorithm correctly reproduces Heim's
# intended decomposition.

class TableI(NamedTuple):
    symbol: str            # Heim's particle label (charge-class first)
    k: int
    n: int
    m: int
    p: int
    sigma: int             # written σ in Heim's table
    P: int
    Q: int
    eq_x: int              # ε · q_x  (signed integer charge for ε=+1)
    eC: int                # ε · C    (signed strangeness)
    R: int                 # ℜ  (= our kap)


TABLE_I_GROUND_STATES: list[TableI] = [
    #            sym       k  n   m   p   σ    P  Q  εq_x εC ℜ
    TableI("e⁻,e̅⁺",       1,  0,  0,  0,   0,  1, 1,  -1,  0, 0),
    TableI("e_0,e̅_0",     1,  0,  0,  0,   1,  1, 1,   0,  0, 0),
    TableI("μ⁻,μ̅⁺",       1, 11,  6, 11,   6,  1, 1,  -1,  0, 1),
    TableI("η,η̅",          1, 18, 22, 17,  14,  0, 0,   0,  0, 0),
    TableI("K⁺,K̅⁻",        1, 17, 26, 30,  28,  1, 0,   1,  1, 1),
    TableI("K⁰,K̅⁰",        1, 18,  5,  5,   2,  1, 0,   0,  1, 1),
    TableI("π±,π̅∓",        1, 12,  9,  2,   3,  2, 0,   1,  0, 0),  # ±1 in source
    TableI("π⁰,π̅⁰",        1, 12,  3,  6,   4,  2, 0,   0,  0, 0),
    TableI("Λ,Λ̅",          2,  1,  3,  0, -11,  0, 1,   0, -1, 0),
    TableI("Ω⁻,Ω̅⁺",        2,  4,  4, -1, -15,  0, 3,  -1, -3, 0),
    TableI("p,p̅",          2,  0,  0,  0,   0,  1, 1,   1,  0, 0),
    TableI("n,n̅",          2,  0,  0, -2,  17,  1, 1,   0,  0, 0),
    TableI("Ξ⁻,Ξ̅⁺",        2,  2,  7,-17,   2,  1, 1,  -1, -2, 1),
    TableI("Ξ⁰,Ξ̅⁰",        2,  2,  6, -1,   6,  1, 1,   0, -2, 1),
    TableI("Σ⁺,Σ̅⁻",        2,  2, -7,-12,  10,  2, 1,   1, -1, 0),
    TableI("Σ⁰,Σ̅⁰",        2,  2, -7,-14,  -2,  2, 1,   0, -1, 0),
    TableI("Σ⁻,Σ̅⁺",        2,  2, -6, -5,  -8,  2, 1,  -1, -1, 0),
    TableI("o⁺⁺,o̅⁻⁻",      2,  2,  1,  9,   4,  3, 3,   2,  0, 0),
    TableI("o⁺,o̅⁻",        2,  2, -1, -1,  -6,  3, 3,   1,  0, 0),
    TableI("o⁰,o̅⁰",        2,  2, -1,-10,   2,  3, 3,   0,  0, 0),
    TableI("o⁻,o̅⁺",        2,  2, -1,-16, -15,  3, 3,  -1,  0, 0),
]


# ----------------------------------------------------------------------
# Table IV: Approximate meson resonances (k = 1)
# ----------------------------------------------------------------------
# Page 5 of G.  Format per row:
#    (symbol, P, N, K_B, theoretical_mass_MeV)
# Doublet entries: N and mass given as (neutral, charged) tuples.
# Single entries: scalars.

class MesonRes(NamedTuple):
    symbol: str
    P: int
    N: tuple[int, ...] | int       # (n, n_±) for doublets, n for singlets
    K_B: tuple[int, ...] | int
    mass_MeV: tuple[float, ...] | float


TABLE_IV_MESONS_K1: list[MesonRes] = [
    # P = 0 (isospin singlet) — no charge partner
    MesonRes("ε",          0, 49,  10,  691.7094),
    MesonRes("ω(783)",     0, 64,  51,  783.9033),
    MesonRes("η'(958)",    0, 144, 28,  956.8400),
    MesonRes("S*(993)",    0, 170, -1,  992.6142),
    MesonRes("Φ(1019)",    0, 153, 63,  1019.6306),
    MesonRes("f(1270)",    0, 253, 26,  1274.5452),
    MesonRes("D(1285)",    0, 255, 27,  1286.1728),
    MesonRes("E(1420)",    0, 272, 82,  1414.1873),
    MesonRes("f'(1514)",   0, 323, 2,   1517.8602),
    MesonRes("ω(1675)",    0, 342, 71,  1664.0125),
    # P = 1 (strange mesons, isospin 1/2 doublet)
    # Entries: (neutral, charged) or (K, K_±)
    MesonRes("K*(892)",    1, (23, 11),    (29, 3),   (891.1955, 892.2211)),
    MesonRes("K_A(1240)",  1, (83, 69),    (6, 15),   (1241.1180, 1239.9767)),
    MesonRes("K*(1420)",   1, (98, 101),   (25, 23),  (1420.2213, 1414.4956)),
    MesonRes("L(1770)",    1, (161, 164),  (65, 11),  (1775.2145, 1764.9862)),
    # P = 2 (isospin 1 triplet, but G lists only doublet representations)
    MesonRes("ρ(770)",     2, (8, 5),      (30, 34),  (769.9833, 769.3101)),
    MesonRes("δ(970)",     2, (39, 21),    (19, 5),   (976.4931, 973.6704)),
    MesonRes("A1(1100)",   2, (76, 48),    (41, 5),   (1106.9780, 1106.7462)),
    MesonRes("B(1235)",    2, (93, 79),    (27, 10),  (1239.5340, 1239.1994)),
    MesonRes("A2(1310)",   2, (127, 86),   (22, 59),  (1310.4695, 1309.6730)),
    MesonRes("F1(1540)",   2, (182, 145),  (37, 4),   (1539.5100, 1537.9095)),
    MesonRes("ρ'(1600)",   2, (215, 156),  (43, 29),  (1604.8640, 1605.1008)),
    MesonRes("A3(1640)",   2, (221, 160),  (4, 7),    (1637.2669, 1634.2138)),
    MesonRes("g(1680)",    2, (228, 165),  (28, 5),   (1686.0154, 1678.6425)),
]


# ----------------------------------------------------------------------
# Table V_a: Approximate baryon resonances (k = 2), page 6
# ----------------------------------------------------------------------
# Same row format as Table IV.

class BaryonRes(NamedTuple):
    symbol: str
    P: int
    N: tuple[int, ...] | int
    K_B: tuple[int, ...] | int
    mass_MeV: tuple[float, ...] | float


TABLE_V_a_BARYONS_K2: list[BaryonRes] = [
    # N* (nucleon resonances, P=1, isospin 1/2)
    BaryonRes("N(1470)",  1, (13, 12), (10, 38), (1470.4888, 1480.1770)),
    BaryonRes("N(1520)",  1, (14, 13), (29, 8),  (1509.6087, 1515.7293)),
    BaryonRes("N(1535)",  1, (18, 17), (-2, 8),  (1533.9788, 1535.3254)),
    BaryonRes("N(1670)",  1, (23, 22), (8, 0),   (1657.9536, 1679.5754)),
    BaryonRes("N(1688)",  1, (24, 23), (-23, 11),(1694.3687, 1719.4898)),
    BaryonRes("N(1700)",  1, (25, 27), (63, -12),(1734.6717, 1751.2494)),
    BaryonRes("N(1770)",  1, (26, 24), (14, 65), (1771.8218, 1769.0721)),
    BaryonRes("N(1780)",  1, (31, 29), (-9, 0),  (1784.3644, 1782.2884)),
    BaryonRes("N(1810)",  1, (32, 30), (38, 40), (1808.3795, 1808.5253)),
    BaryonRes("N(1990)",  1, (37, 35), (60, 50), (1974.9129, 1989.7028)),
    BaryonRes("N(2000)",  1, (42, 39), (-3, -37),(2011.0552, 2001.9706)),
    BaryonRes("N(2040)",  1, (44, 41), (7, 30),  (2044.8079, 2034.6322)),
    BaryonRes("N(2100)",  1, (40, 44), (78, 25), (2107.8085, 2120.5890)),
    BaryonRes("N(2190)",  1, (49, 46), (-14, 21),(2200.5168, 2195.5259)),
    BaryonRes("N(2220)",  1, (50, 47), (66, 43), (2244.1911, 2245.4563)),
    BaryonRes("N(2650)",  1, (73, 69), (2, -9),  (2653.5304, 2652.4071)),
    BaryonRes("N(3030)",  1, (90, 85), (41, 54), (3036.2404, 3033.5279)),
    BaryonRes("N(3245)",  1, (95, 90), (61, 28), (3234.0166, 3231.8730)),
    BaryonRes("N(3690)",  1, (119, 113),(3, 4),  (3689.8085, 3684.1957)),
    BaryonRes("N(3755)",  1, (113, 115),(37, 31),(3751.7230, 3728.0808)),
    # Λ* (P = 0, isospin singlet — no charge partner)
    BaryonRes("Λ(1330)",  0, 25, 10, 1329.8831),
    BaryonRes("Λ(1405)",  0, 22, 79, 1403.3999),
    BaryonRes("Λ(1520)",  0, 37, 36, 1516.3419),
    BaryonRes("Λ(1670)",  0, 54, 4,  1669.9762),
    BaryonRes("Λ(1690)",  0, 55, 61, 1693.2832),
    BaryonRes("Λ(1750)",  0, 58, 25, 1754.7613),
    BaryonRes("Λ(1815)",  0, 70, -10, 1815.4961),
]


# ----------------------------------------------------------------------
# Table V_b: continuation, page 7
# ----------------------------------------------------------------------

TABLE_V_b_BARYONS_K2: list[BaryonRes] = [
    # more Λ*
    BaryonRes("Λ(1830)",  0, 71, 11, 1830.4081),
    BaryonRes("Λ(1860)",  0, 73, -5, 1864.6313),
    BaryonRes("Λ(1870)",  0, 74, 1,  1884.4529),
    BaryonRes("Λ(2010)",  0, 87, 17, 2010.5372),
    BaryonRes("Λ(2020)",  0, 88, 18, 2018.1998),
    BaryonRes("Λ(2100)",  0, 94, 0,  2095.9533),
    BaryonRes("Λ(2110)",  0, 84, 34, 2113.6593),
    BaryonRes("Λ(2350)",  0, 116, 30, 2344.7465),
    BaryonRes("Λ(2585)",  0, 136, 5, 2591.7184),
    # Ξ* (P = 1, isospin 1/2 doublet)
    BaryonRes("Ξ(1530)",  1, (4, 2),   (9, 5),   (1531.5487, 1534.7628)),
    BaryonRes("Ξ(1630)",  1, (7, 4),   (30, 20), (1621.5840, 1661.1690)),
    BaryonRes("Ξ(1820)",  1, (16, 10), (35, 9),  (1828.9065, 1810.8367)),
    BaryonRes("Ξ(1940)",  1, (19, 13), (59, 27), (1944.8454, 1945.2579)),
    BaryonRes("Ξ(2030)",  1, (25, 19), (-4, -3), (2027.8157, 2037.5528)),
    BaryonRes("Ξ(2250)",  1, (31, 24), (65, -4), (2247.4841, 2241.9080)),
    BaryonRes("Ξ(2500)",  1, (42, 35), (42, 13), (2481.8202, 2517.9008)),
    # Δ* (P = 3, isospin 3/2 — but table lists only one column per row)
    BaryonRes("Δ(1650)",  3, 44, 11, 1651.0807),
    BaryonRes("Δ(1670)",  3, 48, 44, 1678.6242),
    BaryonRes("Δ(1690)",  3, 71, 0,  1690.0383),
    BaryonRes("Δ(1890)",  3, 124, 1, 1887.9876),
    BaryonRes("Δ(1900)",  3, 125, 56, 1900.8602),
    BaryonRes("Δ(1910)",  3, 129, -27, 1915.2764),
    BaryonRes("Δ(1950)",  3, 134, 59, 1949.2695),
    BaryonRes("Δ(1960)",  3, 137, 38, 1965.3571),
    BaryonRes("Δ(2160)",  3, 211, 33, 2153.9221),
    BaryonRes("Δ(2420)",  3, 302, 12, 2422.5186),
    BaryonRes("Δ(2850)",  3, 419, 63, 2856.6694),
    BaryonRes("Δ(3230)",  3, 572, 34, 3229.6911),
]


# ----------------------------------------------------------------------
# Table V_c: continuation, page 8 — Σ* family (P = 2, isospin 1 triplet)
# ----------------------------------------------------------------------
# Σ entries have three values per row: (Σ-, Σ0, Σ+).
# Stored as triples in N, K_B, mass.

TABLE_V_c_BARYONS_K2_SIGMA: list[BaryonRes] = [
    BaryonRes("Σ(1385)",  2, (13, 6, 13),   (11, 59, 22),   (1383, 1382, 1386)),
    BaryonRes("Σ(1440)",  2, (16, 8, 16),   (9, 71, -5),    (1441, 1434, 1441)),
    BaryonRes("Σ(1480)",  2, (18, 20, 18),  (64, 12, 52),   (1492, 1490, 1489)),
    BaryonRes("Σ(1620)",  2, (32, 35, 32),  (18, 10, 20),   (1624, 1622, 1616)),
    BaryonRes("Σ(1670)",  2, (34, 27, 35),  (8, 15, -23),   (1664, 1660, 1678)),
    BaryonRes("Σ(1690)",  2, (35, 38, 36),  (-10, 43, 57),  (1691, 1683, 1705)),
    BaryonRes("Σ(1750)",  2, (43, 41, 38),  (-25, 34, 5),   (1752, 1747, 1750)),
    BaryonRes("Σ(1765)",  2, (45, 49, 46),  (9, 10, -2),    (1769, 1766, 1770)),
    BaryonRes("Σ(1840)",  2, (50, 45, 51),  (19, 11, 47),   (1847, 1844, 1848)),
    BaryonRes("Σ(1880)",  2, (42, 57, 43),  (65, 61, 7),    (1884, 1887, 1885)),
    BaryonRes("Σ(1915)",  2, (53, 59, 54),  (28, 16, 24),   (1909, 1923, 1908)),
    BaryonRes("Σ(1940)",  2, (54, 60, 55),  (23, 44, -10),  (1932, 1951, 1931)),
    BaryonRes("Σ(2000)",  2, (63, 70, 64),  (8, 1, -45),    (2003, 2012, 2002)),
    BaryonRes("Σ(2030)",  2, (66, 72, 59),  (21, 12, 5),    (2035, 2031, 2031)),
    BaryonRes("Σ(2070)",  2, (68, 75, 69),  (2, 38, 40),    (2066, 2071, 2064)),
    BaryonRes("Σ(2080)",  2, (69, 76, 70),  (9, 29, 10),    (2083, 2089, 2074)),
    BaryonRes("Σ(2100)",  2, (70, 77, 71),  (31, 52, 6),    (2103, 2106, 2093)),
    BaryonRes("Σ(2250)",  2, (76, 84, 78),  (-12, 33, 35),  (2243, 2250, 2252)),
    BaryonRes("Σ(2455)",  2, (94, 104, 85), (18, 56, 3),    (2444, 2458, 2455)),
    BaryonRes("Σ(2620)",  2, (110, 121, 103),(-27, -12, 26),(2624, 2625, 2621)),
    BaryonRes("Σ(3000)",  2, (136, 150, 140),(-85, 38, 12), (2994, 3001, 3003)),
]


ALL_BARYON_RES = (
    TABLE_V_a_BARYONS_K2 + TABLE_V_b_BARYONS_K2 + TABLE_V_c_BARYONS_K2_SIGMA
)
ALL_MESON_RES = TABLE_IV_MESONS_K1


def main():
    print("=" * 72)
    print(" Heim 1989 G-Tabellen — selected results")
    print("=" * 72)

    print(f"\nTABLE II    (theoretical data for ground states + neutrinos):")
    print(f"  {1 + len(TABLE_II_LEPTONS) + len(TABLE_II_MESONS) + len(TABLE_II_BARYONS)} entries")
    print(f"   - 1 photon, {len(TABLE_II_LEPTONS)} leptons (incl. 5 neutrinos),")
    print(f"     {len(TABLE_II_MESONS)} mesons, {len(TABLE_II_BARYONS)} baryons")

    print(f"\nTABLE IV    (k = 1 meson resonances):")
    print(f"  {len(TABLE_IV_MESONS_K1)} entries  (P-isospin breakdown: "
          f"{sum(1 for m in TABLE_IV_MESONS_K1 if m.P==0)} singlets, "
          f"{sum(1 for m in TABLE_IV_MESONS_K1 if m.P==1)} K-doublets, "
          f"{sum(1 for m in TABLE_IV_MESONS_K1 if m.P==2)} triplet-like)")

    print(f"\nTABLE V_a   (k = 2, N* and Λ* baryon resonances):")
    print(f"  {len(TABLE_V_a_BARYONS_K2)} entries")
    print(f"TABLE V_b   (k = 2, more Λ*, plus Ξ*, Δ* baryon resonances):")
    print(f"  {len(TABLE_V_b_BARYONS_K2)} entries")
    print(f"TABLE V_c   (k = 2, Σ* baryon resonances):")
    print(f"  {len(TABLE_V_c_BARYONS_K2_SIGMA)} entries")
    print(f"  TOTAL baryon resonances: {len(ALL_BARYON_RES)}")

    print()
    print("=" * 72)
    print(" Verification — joel-referenced entries")
    print("=" * 72)
    print()
    print("  ω(783):    P, N, K_B, m  =", _fmt(_find(TABLE_IV_MESONS_K1, "ω(783)")))
    print("  Φ(1019):   P, N, K_B, m  =", _fmt(_find(TABLE_IV_MESONS_K1, "Φ(1019)")))
    print("  K*(892):   P, N, K_B, m  =", _fmt(_find(TABLE_IV_MESONS_K1, "K*(892)")))
    print("  ρ(770):    P, N, K_B, m  =", _fmt(_find(TABLE_IV_MESONS_K1, "ρ(770)")))
    print("  η'(958):   P, N, K_B, m  =", _fmt(_find(TABLE_IV_MESONS_K1, "η'(958)")))
    print("  K*(1420):  P, N, K_B, m  =", _fmt(_find(TABLE_IV_MESONS_K1, "K*(1420)")))
    print("  ω(1675):   P, N, K_B, m  =", _fmt(_find(TABLE_IV_MESONS_K1, "ω(1675)")))
    print("  ρ'(1600):  P, N, K_B, m  =", _fmt(_find(TABLE_IV_MESONS_K1, "ρ'(1600)")))
    print()
    print("  Λ(1330):   P, N, K_B, m  =", _fmt(_find(TABLE_V_a_BARYONS_K2, "Λ(1330)")))
    print("  Λ(1405):   P, N, K_B, m  =", _fmt(_find(TABLE_V_a_BARYONS_K2, "Λ(1405)")))
    print("  Λ(1520):   P, N, K_B, m  =", _fmt(_find(TABLE_V_a_BARYONS_K2, "Λ(1520)")))
    print("  Λ(1670):   P, N, K_B, m  =", _fmt(_find(TABLE_V_a_BARYONS_K2, "Λ(1670)")))
    print("  Λ(1690):   P, N, K_B, m  =", _fmt(_find(TABLE_V_a_BARYONS_K2, "Λ(1690)")))
    print("  Λ(1750):   P, N, K_B, m  =", _fmt(_find(TABLE_V_a_BARYONS_K2, "Λ(1750)")))
    print("  Λ(1815):   P, N, K_B, m  =", _fmt(_find(TABLE_V_a_BARYONS_K2, "Λ(1815)")))
    print()
    print(f"All entries are stored as named tuples for downstream access.")
    print(f"Import:  from g_tables import (TABLE_IV_MESONS_K1, ALL_BARYON_RES, ...)")


def _find(table, symbol):
    for row in table:
        if row.symbol == symbol:
            return row
    return None


def _fmt(row):
    if row is None:
        return "(not found)"
    return f"P={row.P}, N={row.N}, K_B={row.K_B}, m={row.mass_MeV}"


if __name__ == "__main__":
    main()
