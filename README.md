# Integración numérica · Sesión 12

Regla del trapecio compuesto para estimar el tráfico de red de un servidor web, en web y en Python.

Universidad Peruana Unión · Ingeniería de Sistemas · Fernando Istaña Flores
Curso: Análisis Numérico / Métodos Numéricos

---

## Qué hay aquí

| Archivo | Contenido |
|---|---|
| `index.html` | La app web. Un solo archivo, sin dependencias: se abre con doble clic o desde GitHub Pages |
| `python/trapecio.py` | `trapecio_compuesto(f, a, b, n)`, el caso n = 4 paso a paso, la tabla de convergencia y las gráficas |
| `python/salida_trapecio.txt` | La salida del programa, para pegarla en el informe |
| `python/trapecio_s12.png` | R(t) con los cuatro trapecios de n = 4 |
| `python/convergencia_s12.png` | Error contra n en escala log-log (pendiente −2) |
| `informes/` | El informe de la GAA de la Sesión 12 en Word y en PDF |

## La app web

- **Cualquier integral**: f(t) en t o en x (seno y coseno en radianes), intervalo [a, b] y n; todo se recalcula al tipear.
- **Ancho de paso y malla** con los pesos 1, 2, …, 2, 1 y la suma ponderada.
- **La fórmula con los números reemplazados**, el resultado y el error frente al valor exacto, o frente a una referencia numérica si no se conoce.
- **Gráfica** de la función con los trapecios sombreados y lectura con el cursor.
- **Convergencia** para la lista de n que se quiera: valor, error absoluto, error %, razón de errores y orden observado, más la gráfica log-log.
- **Cota del error** |E| ≤ (b − a)·h²/12·máx|f''| y el **n mínimo** para una tolerancia dada.
- La GAA resuelta y una hoja de fórmulas.

## Ejecutar la versión en Python

```bash
cd python
python trapecio.py
```

Solo necesita `matplotlib` para las gráficas; el cálculo usa la biblioteca estándar (`math`).

## Caso resuelto — tráfico de red en un datacenter

R(t) = 10 + 5·sen(πt/4) + e^(0.15t) Mbps durante 12 s; D = ∫₀¹² R(t) dt.

| i | tᵢ | R(tᵢ) | peso |
|---|---|---|---|
| 0 | 0 | 11.000000 | 1 |
| 1 | 3 | 15.103846 | 2 |
| 2 | 6 | 7.459603 | 2 |
| 3 | 9 | 17.392959 | 2 |
| 4 | 12 | 16.049647 | 1 |

```
h = 3      I ≈ (3/2)·[11 + 2·(15.103846 + 7.459603 + 17.392959) + 16.049647] = 160.4437 Mb
exacto     D = 120 + 40/π + (e^1.8 − 1)/0.15 = 166.3967 Mb      error 5.9530 Mb (3.58 %)
```

| n | I_trapecio (Mb) | error absoluto | error % |
|---|---|---|---|
| 4 | 160.443697 | 5.953015 | 3.577604 |
| 10 | 165.530824 | 0.865888 | 0.520376 |
| 50 | 166.362626 | 0.034086 | 0.020485 |
| 100 | 166.388195 | 0.008517 | 0.005119 |
| 1000 | 166.396627 | 0.000085 | 0.000051 |

El error baja como h²: de n = 100 a n = 1000 se divide entre 100.
