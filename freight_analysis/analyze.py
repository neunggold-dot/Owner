"""운임(Fixture) 데이터 분석 스크립트.

CSV 필수 컬럼:
  date, route, cargo, quantity_mt, rate_usd_mt
선택 컬럼:
  vessel, load_port, discharge_port

사용 예:
  python -m freight_analysis.analyze                       # 샘플 데이터
  python -m freight_analysis.analyze my_fixtures.csv       # 내 데이터
  python -m freight_analysis.analyze my.csv --route "Pohang-Shanghai"

결과물: output/ 폴더에 report.md, route_summary.csv, monthly_trend.png
"""
import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

HERE = Path(__file__).parent
SAMPLE = HERE / "sample_data" / "freight_fixtures_sample.csv"
REQUIRED = ["date", "route", "cargo", "quantity_mt", "rate_usd_mt"]


def load(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        raise SystemExit(f"❌ 필수 컬럼이 없습니다: {missing}")
    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.to_period("M").astype(str)
    df["freight_usd"] = df["quantity_mt"] * df["rate_usd_mt"]
    return df


def route_summary(df: pd.DataFrame) -> pd.DataFrame:
    g = df.sort_values("date").groupby("route")
    out = pd.DataFrame(
        {
            "건수": g.size(),
            "총물량_MT": g["quantity_mt"].sum(),
            "평균운임_USD_MT": g["rate_usd_mt"].mean().round(2),
            "최저": g["rate_usd_mt"].min(),
            "최고": g["rate_usd_mt"].max(),
            "최근운임": g["rate_usd_mt"].last(),
            "총운임_USD": g["freight_usd"].sum().round(0),
        }
    )
    return out.sort_values("총물량_MT", ascending=False)


def monthly_trend(df: pd.DataFrame) -> pd.DataFrame:
    # 물량 가중 평균 운임
    m = df.groupby(["month", "route"]).apply(
        lambda x: (x["rate_usd_mt"] * x["quantity_mt"]).sum() / x["quantity_mt"].sum(),
        include_groups=False,
    )
    return m.unstack("route").round(2)


def plot(trend: pd.DataFrame, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(10, 5))
    for col in trend.columns:
        ax.plot(trend.index, trend[col], marker="o", label=col)
    ax.set_title("Monthly freight rate by route (volume-weighted, USD/MT)")
    ax.set_xlabel("Month")
    ax.set_ylabel("USD/MT")
    ax.grid(alpha=0.3)
    ax.legend(fontsize=8)
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def main() -> None:
    p = argparse.ArgumentParser(description="운임 데이터 분석")
    p.add_argument("csv", nargs="?", default=str(SAMPLE), help="분석할 CSV (기본: 샘플)")
    p.add_argument("--route", help="특정 항로만 분석")
    p.add_argument("--out", default="output", help="결과 저장 폴더")
    args = p.parse_args()

    df = load(Path(args.csv))
    if args.route:
        df = df[df["route"] == args.route]
        if df.empty:
            raise SystemExit(f"❌ '{args.route}' 항로 데이터가 없습니다.")

    out = Path(args.out)
    out.mkdir(exist_ok=True)

    summary = route_summary(df)
    trend = monthly_trend(df)
    summary.to_csv(out / "route_summary.csv", encoding="utf-8-sig")
    plot(trend, out / "monthly_trend.png")

    report = [
        "# 운임 분석 리포트",
        f"- 데이터: `{args.csv}`",
        f"- 기간: {df['date'].min():%Y-%m-%d} ~ {df['date'].max():%Y-%m-%d}",
        f"- 총 {len(df)}건 / {df['quantity_mt'].sum():,.0f} MT",
        "",
        "## 항로별 요약",
        summary.to_markdown(),
        "",
        "## 월별 물량가중 평균운임 (USD/MT)",
        trend.to_markdown(),
        "",
        "![trend](monthly_trend.png)",
    ]
    (out / "report.md").write_text("\n".join(report), encoding="utf-8")

    print(summary.to_string())
    print(f"\n✅ 결과 저장: {out.resolve()}")


if __name__ == "__main__":
    main()
