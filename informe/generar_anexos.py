"""Genera los fragmentos LaTeX de los anexos a partir de las tablas exportadas por el notebook.

Uso (desde la raíz del repositorio):  python informe/generar_anexos.py
"""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
SALIDA = ROOT / "informe" / "generado"
SALIDA.mkdir(exist_ok=True)

REEMPLAZOS = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#", "_": r"\_",
              "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}"}


def tex(valor):
    return "".join(REEMPLAZOS.get(ch, ch) for ch in str(valor))


metricas = pd.read_csv(ROOT / "powerbi" / "data" / "dim_metricas.csv", encoding="utf-8")
campos = [c for c in metricas.columns if c not in ("orden", "Nombre")]
bloques = []
for _, fila in metricas.iterrows():
    filas = "\n".join(rf"\textbf{{{tex(c)}}} & {tex(fila[c])} \\" for c in campos)
    bloques.append(rf"""\subsection*{{A.{fila['orden']} {tex(fila['Nombre'])}}}
\begin{{footnotesize}}
\begin{{longtable}}{{@{{}}p{{0.27\textwidth}}p{{0.69\textwidth}}@{{}}}}
\toprule
{filas}
\bottomrule
\end{{longtable}}
\end{{footnotesize}}
""")
(SALIDA / "anexo_diccionario.tex").write_text("\n".join(bloques), encoding="utf-8")
print("Anexo del diccionario:", len(metricas), "métricas →", SALIDA / "anexo_diccionario.tex")
