"""README numbers must match computed outputs (reports/headline_metrics.json)."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
M = json.loads((ROOT / "reports" / "headline_metrics.json").read_text(encoding="utf-8"))
README = (ROOT / "README.md").read_text(encoding="utf-8")


def test_book_numbers():
    assert f"{M['rows']:,} transactions" in README
    assert f"${M['net_premium_musd']}M net premium" in README
    assert f"loss ratio {M['loss_ratio_pct']}%" in README
    assert f"combined ratio {M['combined_ratio_pct']}%" in README
    assert f"({M['states']} states)" in README


def test_q3_numbers():
    assert f"Q3 {M['q3_loss_ratio_pct']}% vs {M['other_quarters_loss_ratio_pct']}%" in README
    assert f"+{M['q3_spike_points']} points" in README
    assert f"**{M['fl_gulf_home_share_of_q3_excess_pct']}%** of Q3 excess" in README
    assert f"{M['fl_gulf_home_share_of_premium_pct']}% of premium" in README


def test_growth_and_churn():
    assert f"Commercial premium **+{M['yoy_growth_pct']['Commercial']}%**" in README
    assert f"Auto **+{M['yoy_growth_pct']['Auto']}%**" in README
    c = M["churn_by_tenure_pct"]
    assert f"churn {c['0-12mo']}% for 0-12 months" in README
    assert f"χ² = {M['churn_chi2']['chi2']}" in README
    assert f"({M['uw_margin_by_line_pct']['Commercial']}% vs Auto {M['uw_margin_by_line_pct']['Auto']}%)" in README


def test_stats_script_output_matches_readme():
    out = subprocess.run([sys.executable, str(ROOT / "analysis" / "06_statistical_tests.py")],
                         capture_output=True, text=True, encoding="utf-8", check=True,
                         env={**__import__("os").environ, "PYTHONIOENCODING": "utf-8", "MPLBACKEND": "Agg"}).stdout
    assert "p = 0.0130" in out and "p = 0.013" in README
    assert "[+0.036, +0.118]" in out and "[+0.036, +0.118]" in README


def test_stress_test_layer_is_consistent():
    out = subprocess.run([sys.executable, str(ROOT / "analysis" / "07_cat_stress_test.py")],
                         capture_output=True, text=True, encoding="utf-8", check=True,
                         env={**__import__("os").environ, "PYTHONIOENCODING": "utf-8", "MPLBACKEND": "Agg"}).stdout
    assert "$26.95M" in out and "Layer to cover 1-in-100      : $16.50M xs $10.46M" in out
    assert "$16.50M xs $10.46M" in README


def test_no_retracted_claims():
    for stale in ("~15 points", "~12%", "~23%", "~40%", "65,000+", "$100–200K"):
        assert stale not in README.split("Limitations and corrections")[0]
