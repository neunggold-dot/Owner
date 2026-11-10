"""샘플(가짜) 운임 데이터를 만든다. 실제 시장 운임이 아닙니다."""
import random
from datetime import date, timedelta
from pathlib import Path

import pandas as pd

random.seed(42)

ROUTES = {
    # route: (cargo, base rate USD/MT, qty range)
    "Pohang-Shanghai": ("Steel coil", 18, (3000, 8000)),
    "Dangjin-Ho Chi Minh": ("Steel plate", 26, (5000, 12000)),
    "Incheon-Kaohsiung": ("Rebar", 21, (3000, 6000)),
    "Busan-Osaka": ("Section steel", 15, (2000, 5000)),
    "Qingdao-Pohang": ("Scrap", 14, (8000, 20000)),
}
VESSELS = ["MV SAMPLE ONE", "MV SAMPLE TWO", "MV DEMO STAR", "MV TEST GLORY"]

rows = []
start = date(2026, 1, 5)
for i in range(120):
    d = start + timedelta(days=random.randint(0, 300))
    route = random.choice(list(ROUTES))
    cargo, base, (lo, hi) = ROUTES[route]
    season = 1 + 0.15 * ((d.month % 6) - 3) / 3
    rows.append(
        {
            "date": d.isoformat(),
            "route": route,
            "load_port": route.split("-")[0],
            "discharge_port": route.split("-")[1],
            "cargo": cargo,
            "vessel": random.choice(VESSELS),
            "quantity_mt": round(random.randint(lo, hi), -2),
            "rate_usd_mt": round(base * season * random.uniform(0.9, 1.1), 2),
        }
    )

out = Path(__file__).parent / "sample_data" / "freight_fixtures_sample.csv"
out.parent.mkdir(exist_ok=True)
pd.DataFrame(rows).sort_values("date").to_csv(out, index=False)
print(f"saved {out}")
