"""
Ejercicio 2 — Multiprocesos: Integración numérica de funciones físicas
=======================================================================
Conceptos: multiprocessing.Pool, Pool.starmap, división del intervalo,
           regla del trapecio, combinación de resultados.

Contexto físico
---------------
Muchas magnitudes físicas se calculan como integrales definidas.
Ejemplos que resolveremos aquí:

  1. Trabajo de una fuerza variable:
       W = ∫ F(x) dx   donde  F(x) = k·x  (resorte de Hooke)
       Solución analítica: W = ½ k x²

  2. Energía irradiada (distribución de Planck, aprox. numérica):
       u(ν) = (8π h / c³) · ν³ / (e^{hν/kT} − 1)
       Integramos en un rango finito de frecuencias.

  3. Longitud de arco de una trayectoria parabólica (proyectil):
       y(x) = x·tan(θ) − g·x²/(2v₀²cos²θ)
       L = ∫ √(1 + (dy/dx)²) dx

Método numérico: regla del trapecio compuesta.
  ∫_a^b f(x) dx ≈ h/2 · [f(a) + 2·f(x₁) + 2·f(x₂) + ... + f(b)]
  donde h = (b−a)/N es el ancho de cada subintervalo.

Estrategia paralela
-------------------
Dividimos el intervalo [a, b] en 'P' sub-intervalos (uno por proceso).
Cada proceso integra su tramo y devuelve el valor parcial.
El resultado final es la suma de todos los tramos.

Tareas para el estudiante
-------------------------
1. Aumenta N_SUBINTERVALOS a 10_000_000. ¿Mejora la precisión?
2. Agrega una cuarta función (p. ej. campo gravitacional).
3. Compara el speedup para N_SUBINTERVALOS pequeños vs. grandes.
   ¿Cuándo vale la pena usar múltiples procesos?
"""

import math
import multiprocessing
import time
from typing import Callable


# ---------------------------------------------------------------------------
# Parámetros
# ---------------------------------------------------------------------------

N_SUBINTERVALOS = 2_000_000   # subintervalos de la regla del trapecio
N_PROCESOS      = 4


# ---------------------------------------------------------------------------
# Funciones físicas a integrar
# ---------------------------------------------------------------------------

# 1. Fuerza de un resorte (Ley de Hooke): F(x) = k·x
K_RESORTE = 50.0  # N/m

def fuerza_resorte(x: float) -> float:
    return K_RESORTE * x


# 2. Densidad espectral de energía de Planck u(ν) [J·s/m³]
H_PLANCK = 6.626e-34   # J·s
C_LUZ    = 3.0e8       # m/s
K_BOLTZ  = 1.38e-23    # J/K
T_PLANCK = 5778.0      # K (temperatura superficial del Sol)

def planck(nu: float) -> float:
    """Densidad espectral de Planck."""
    exp_arg = H_PLANCK * nu / (K_BOLTZ * T_PLANCK)
    if exp_arg > 709:   # evitar overflow en exp
        return 0.0
    return (8 * math.pi * H_PLANCK / C_LUZ**3) * nu**3 / (math.exp(exp_arg) - 1)


# 3. Integrando de la longitud de arco de un proyectil
G       = 9.8     # m/s²
V0      = 30.0    # m/s
THETA   = math.radians(45)  # ángulo de lanzamiento

def longitud_arco_proyectil(x: float) -> float:
    """√(1 + (dy/dx)²) para la trayectoria parabólica."""
    cos2 = math.cos(THETA)**2
    dydx = math.tan(THETA) - G * x / (V0**2 * cos2)
    return math.sqrt(1 + dydx**2)


# ---------------------------------------------------------------------------
# Worker: integra f en el subintervalo [a_local, b_local]
# ---------------------------------------------------------------------------

def integrar_tramo(args: tuple) -> float:
    """Aplica la regla del trapecio en un subintervalo.

    Parámetros
    ----------
    args : (nombre_funcion, a_local, b_local, n_local)
    """
    nombre, a_local, b_local, n_local = args

    # Recuperar la función por nombre (necesario en procesos hijo)
    funciones = {
        "resorte":     fuerza_resorte,
        "planck":      planck,
        "proyectil":   longitud_arco_proyectil,
    }
    f = funciones[nombre]

    h = (b_local - a_local) / n_local
    total = 0.5 * (f(a_local) + f(b_local))
    for i in range(1, n_local):
        total += f(a_local + i * h)
    return total * h


# ---------------------------------------------------------------------------
# Integración secuencial y paralela
# ---------------------------------------------------------------------------

def integrar(nombre: str, a: float, b: float, n: int, n_proc: int) -> tuple:
    """Integra la función 'nombre' en [a, b] con n subintervalos y n_proc procesos."""
    puntos = [a + i * (b - a) / n_proc for i in range(n_proc + 1)]
    ns = [n // n_proc] * n_proc
    ns[-1] += n % n_proc  # el último proceso absorbe el residuo

    tareas_par = [
        (nombre, puntos[i], puntos[i + 1], ns[i])
        for i in range(n_proc)
    ]
    tarea_seq = [(nombre, a, b, n)]

    # Secuencial
    t0 = time.perf_counter()
    resultado_seq = integrar_tramo(tarea_seq[0])
    t_seq = time.perf_counter() - t0

    # Paralelo
    t0 = time.perf_counter()
    with multiprocessing.Pool(processes=n_proc) as pool:
        parciales = pool.map(integrar_tramo, tareas_par)
    resultado_par = sum(parciales)
    t_par = time.perf_counter() - t0

    return resultado_seq, t_seq, resultado_par, t_par


# ---------------------------------------------------------------------------
# Programa principal
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 65)
    print("INTEGRACIÓN NUMÉRICA — Regla del trapecio + multiprocesos")
    print("=" * 65)
    print(f"  Subintervalos : {N_SUBINTERVALOS:,}")
    print(f"  Procesos      : {N_PROCESOS}")

    # ── 1. Trabajo del resorte ───────────────────────────────────────────
    a1, b1 = 0.0, 2.0   # [m]
    analitico1 = 0.5 * K_RESORTE * b1**2 - 0.5 * K_RESORTE * a1**2
    r_seq1, t_seq1, r_par1, t_par1 = integrar(
        "resorte", a1, b1, N_SUBINTERVALOS, N_PROCESOS)

    print(f"\n1. Trabajo del resorte  W = ∫F(x)dx  en [{a1}, {b1}] m")
    print(f"   Analítico  : {analitico1:.6f} J")
    print(f"   Secuencial : {r_seq1:.6f} J  ({t_seq1:.3f} s)")
    print(f"   Paralelo   : {r_par1:.6f} J  ({t_par1:.3f} s)  "
          f"speedup={t_seq1/t_par1:.1f}x")

    # ── 2. Densidad espectral de Planck ──────────────────────────────────
    a2, b2 = 1e13, 3e15   # rango de frecuencias UV-visible [Hz]
    r_seq2, t_seq2, r_par2, t_par2 = integrar(
        "planck", a2, b2, N_SUBINTERVALOS, N_PROCESOS)

    print(f"\n2. Energía espectral de Planck  en [{a2:.0e}, {b2:.0e}] Hz")
    print(f"   (no tiene solución analítica simple en rango finito)")
    print(f"   Secuencial : {r_seq2:.4e} J·s/m³  ({t_seq2:.3f} s)")
    print(f"   Paralelo   : {r_par2:.4e} J·s/m³  ({t_par2:.3f} s)  "
          f"speedup={t_seq2/t_par2:.1f}x")

    # ── 3. Longitud de arco del proyectil ────────────────────────────────
    x_max = V0**2 * math.sin(2 * THETA) / G   # alcance horizontal
    a3, b3 = 0.0, x_max
    r_seq3, t_seq3, r_par3, t_par3 = integrar(
        "proyectil", a3, b3, N_SUBINTERVALOS, N_PROCESOS)

    print(f"\n3. Longitud de arco del proyectil  en [0, {x_max:.2f}] m")
    print(f"   (v₀={V0} m/s, θ=45°, alcance={x_max:.2f} m)")
    print(f"   Secuencial : {r_seq3:.6f} m  ({t_seq3:.3f} s)")
    print(f"   Paralelo   : {r_par3:.6f} m  ({t_par3:.3f} s)  "
          f"speedup={t_seq3/t_par3:.1f}x")

    print()
