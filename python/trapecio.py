"""
Análisis Numérico · Unidad 3 · Sesión 12
Integración numérica: regla del trapecio compuesto. Tráfico de red de un microservicio.

La tasa de transferencia (Mbps) durante un pico de 12 segundos es
    R(t) = 10 + 5·sen(pi·t/4) + e^(0.15·t)
y el total de datos transferidos (Megabits) es
    D = integral de 0 a 12 de R(t) dt

Fernando Istaña Flores · Universidad Peruana Unión
"""

import math


# --------------------------------------------------------------------------
# Modelo
# --------------------------------------------------------------------------
def R(t):
    """Tasa de transferencia en Mbps (el seno trabaja en radianes)."""
    return 10 + 5 * math.sin(math.pi * t / 4) + math.exp(0.15 * t)


def integral_exacta(a=0.0, b=12.0):
    """Primitiva: 10t − (20/pi)·cos(pi·t/4) + e^(0.15t)/0.15."""
    F = lambda t: 10 * t - (20 / math.pi) * math.cos(math.pi * t / 4) + math.exp(0.15 * t) / 0.15
    return F(b) - F(a)


# --------------------------------------------------------------------------
# Módulo de cálculo
# --------------------------------------------------------------------------
def trapecio_compuesto(f, a, b, n):
    """
    Regla del trapecio compuesto con n subintervalos de igual ancho.

        h = (b − a) / n
        I ≈ (h/2)·[ f(x0) + 2·(f(x1) + … + f(x_{n−1})) + f(xn) ]

    Los extremos pesan 1 y los nodos interiores pesan 2.
    """
    if n < 1:
        raise ValueError("n debe ser un entero positivo.")
    h = (b - a) / n
    interior = sum(f(a + i * h) for i in range(1, n))
    return h / 2 * (f(a) + 2 * interior + f(b))


def malla(f, a, b, n):
    """Lista de (i, t_i, f(t_i), peso) para mostrar el cálculo a mano."""
    h = (b - a) / n
    return [(i, a + i * h, f(a + i * h), 1 if i in (0, n) else 2) for i in range(n + 1)]


if __name__ == "__main__":
    a, b = 0.0, 12.0
    exacta = integral_exacta(a, b)

    print("=" * 74)
    print("PARTE 1 · TRAPECIO COMPUESTO CON n = 4")
    print("=" * 74)
    n = 4
    h = (b - a) / n
    print("  h = (b − a)/n = (%g − %g)/%d = %g s" % (b, a, n, h))
    print()
    print("   i     t_i     5·sen(pi·t/4)    e^(0.15t)        R(t_i)   peso   peso·R")
    suma = 0.0
    for i, t, y, w in malla(R, a, b, n):
        s = 5 * math.sin(math.pi * t / 4)
        e = math.exp(0.15 * t)
        suma += w * y
        print("  %2d  %6.2f   %13.6f   %10.6f   %12.6f   %4d   %10.6f" % (i, t, s + 0.0, e, y, w, w * y))
    I4 = trapecio_compuesto(R, a, b, n)
    print()
    print("  Suma ponderada = %.6f" % suma)
    print("  I_trapecio = (h/2)·suma = (%g/2)·%.6f = %.6f Mb" % (h, suma, I4))

    print()
    print("=" * 74)
    print("VALOR EXACTO (integración analítica)")
    print("=" * 74)
    print("  D = [10t − (20/pi)·cos(pi·t/4) + e^(0.15t)/0.15] de 0 a 12")
    print("    = 120 + 40/pi + (e^1.8 − 1)/0.15")
    print("    = 120 + %.6f + %.6f = %.6f Mb" % (40 / math.pi, (math.exp(1.8) - 1) / 0.15, exacta))

    print()
    print("=" * 74)
    print("PARTE 2 · ANÁLISIS DE CONVERGENCIA")
    print("=" * 74)
    print("  %6s %10s %16s %16s %12s %10s" % ("n", "h", "I_trapecio", "error absoluto", "error %", "razón"))
    previo = None
    filas = []
    for n in (4, 10, 50, 100, 1000):
        I = trapecio_compuesto(R, a, b, n)
        ea = abs(exacta - I)
        er = ea / abs(exacta) * 100
        razon = "" if previo is None else "%.2f" % (previo[1] / ea)
        print("  %6d %10.4f %16.6f %16.6e %12.6f %10s" % (n, (b - a) / n, I, ea, er, razon))
        filas.append((n, I, ea, er))
        previo = (n, ea)
    print()
    print("  'razón' = error anterior / error actual. El trapecio es de orden h²:")
    print("  si n se multiplica por k, el error se divide aproximadamente entre k².")
    print("  De 100 a 1000 (k = 10) el error baja unas %.0f veces." % (filas[3][2] / filas[4][2]))

    # ----------------------------------------------------------------------
    # Gráficas: la función con los 4 trapecios, y el error contra n
    # ----------------------------------------------------------------------
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        t = [a + (b - a) * k / 600 for k in range(601)]
        fig, ax = plt.subplots(figsize=(7.4, 4.2), dpi=200)
        pts = malla(R, a, b, 4)
        for i in range(4):
            x0, y0 = pts[i][1], pts[i][2]
            x1, y1 = pts[i + 1][1], pts[i + 1][2]
            ax.fill([x0, x0, x1, x1], [0, y0, y1, 0], color="#c8890a", alpha=0.18,
                    edgecolor="#c8890a", linewidth=1.2, label="trapecios (n = 4)" if i == 0 else None)
        ax.fill_between(t, [R(v) for v in t], color="#14366b", alpha=0.06)
        ax.plot(t, [R(v) for v in t], color="#14366b", linewidth=2, label="R(t) = 10 + 5·sen(πt/4) + e^(0.15t)")
        ax.scatter([p[1] for p in pts], [p[2] for p in pts], color="#101c33", zorder=3, s=36, label="nodos tᵢ")
        for p in pts:
            ax.annotate("%.3f" % p[2], (p[1], p[2]), textcoords="offset points", xytext=(4, 7), fontsize=8, color="#3c4a63")
        ax.set_xlabel("Tiempo t (s)")
        ax.set_ylabel("Tasa R(t) (Mbps)")
        ax.set_title("Trapecio compuesto, n = 4: %.4f Mb  ·  exacto: %.4f Mb" % (I4, exacta))
        ax.set_ylim(0, 21)
        ax.grid(color="#dfe5ef", linewidth=0.8)
        ax.set_axisbelow(True)
        for lado in ("top", "right"):
            ax.spines[lado].set_visible(False)
        ax.legend(frameon=False, fontsize=8, loc="lower right")
        fig.tight_layout()
        fig.savefig("trapecio_s12.png")

        fig, ax = plt.subplots(figsize=(7.4, 3.8), dpi=200)
        ns = [4, 10, 20, 50, 100, 200, 500, 1000]
        errs = [abs(exacta - trapecio_compuesto(R, a, b, k)) for k in ns]
        ax.loglog(ns, errs, "o-", color="#14366b", linewidth=2, label="error absoluto")
        ax.loglog(ns, [errs[0] * (4 / k) ** 2 for k in ns], "--", color="#c8890a", label="pendiente −2 (orden h²)")
        for k, e in zip(ns, errs):
            if k in (4, 10, 50, 100, 1000):
                ax.annotate("%.2e" % e, (k, e), textcoords="offset points", xytext=(6, 4), fontsize=8, color="#3c4a63")
        ax.set_xlabel("Número de subintervalos n")
        ax.set_ylabel("|D − I_trapecio| (Mb)")
        ax.set_title("Convergencia del trapecio compuesto")
        ax.grid(color="#dfe5ef", linewidth=0.8, which="both")
        for lado in ("top", "right"):
            ax.spines[lado].set_visible(False)
        ax.legend(frameon=False, fontsize=9)
        fig.tight_layout()
        fig.savefig("convergencia_s12.png")
        print()
        print("  Gráficas guardadas en trapecio_s12.png y convergencia_s12.png")
    except ImportError:
        print()
        print("  (matplotlib no está instalado: se omitieron las gráficas)")
