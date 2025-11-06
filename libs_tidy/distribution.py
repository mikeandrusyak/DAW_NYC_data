import pandas as pd 
import numpy as np
from scipy.stats import chisquare


def gini_from_counts(counts: pd.Series) -> float:
    """Gini-Koeffizient der Ungleichverteilung, 0 = perfekt gleich."""
    x = counts.to_numpy(dtype=float)
    if x.size == 0 or x.sum() == 0:
        return 0.0
    x_sorted = np.sort(x)
    n = x_sorted.size
    return (2 * np.sum((np.arange(1, n + 1) * x_sorted)) / (n * x_sorted.sum())) - (n + 1) / n

def cv_from_counts(counts: pd.Series) -> float:
    """Variationskoeffizient = std/mean. Robuster als p-Wert bei großen n."""
    x = counts.to_numpy(dtype=float)
    m = x.mean()
    if m == 0:
        return 0.0
    return float(x.std(ddof=0) / m)

def test_imported_data_distribution_light(
    df: pd.DataFrame,
    date_col: str = "created_date",
    # Schwellwerte (tune bei Bedarf):
    max_gini: float = 0.30,       # ~gleichmäßige Abdeckung über die Tage
    max_cv: float = 0.40,         # relative Schwankung ok bis 40%
    min_days_covered: int = 20,   # mind. 20 Tage im Monat sollten vorkommen
    also_check_weekly: bool = True,  # zusätzliche Wochen-Plausibilität
):

    assert date_col in df.columns, f"Column '{date_col}' not in df"

    problems = []

    for month, g in df.groupby("create_month"):
        # Counts pro Tag
        daily = g["create_day"].value_counts().sort_index()

        # Abdeckung: wie viele unterschiedliche Tage mit Daten?
        days_covered = int((daily > 0).sum())

        # Metriken
        gini = gini_from_counts(daily)
        cv = cv_from_counts(daily)

        # Regeln prüfen
        msgs = []
        if days_covered < min_days_covered:
            msgs.append(f"low day coverage ({days_covered} < {min_days_covered})")
        if gini > max_gini:
            msgs.append(f"high Gini ({gini:.3f} > {max_gini:.2f})")
        if cv > max_cv:
            msgs.append(f"high CV ({cv:.3f} > {max_cv:.2f})")

        # Optional: Wochen-Check (aggregierter Blick)
        if also_check_weekly:
            wk = g["created_date"].dt.isocalendar().week
            weekly = wk.value_counts().sort_index()
            cv_w = cv_from_counts(weekly)
            # Wochen dürfen etwas variieren; oft strenger als täglich
            if cv_w > max(max_cv, 0.45):
                msgs.append(f"weekly CV high ({cv_w:.3f} > {max(max_cv, 0.45):.2f})")

        if msgs:
            problems.append(f"{month}: {', '.join(msgs)}")

    assert  len(problems) <= 6, "Non-uniform monthly sampling:\n  - " + "\n  - ".join(problems)
