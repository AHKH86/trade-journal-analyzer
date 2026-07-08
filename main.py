"""
Trade Journal Analyzer (single-file example)
Reads a CSV with columns:
date,symbol,side,pnl
"""

from __future__ import annotations
import csv
from pathlib import Path

def load_trades(path):
    trades=[]
    with open(path,newline="",encoding="utf-8") as f:
        r=csv.DictReader(f)
        for row in r:
            row["pnl"]=float(row["pnl"])
            trades.append(row)
    return trades

def stats(trades):
    wins=[t for t in trades if t["pnl"]>0]
    losses=[t for t in trades if t["pnl"]<0]
    gross_profit=sum(t["pnl"] for t in wins)
    gross_loss=-sum(t["pnl"] for t in losses)
    total=sum(t["pnl"] for t in trades)
    win_rate=(len(wins)/len(trades)*100) if trades else 0
    pf=(gross_profit/gross_loss) if gross_loss else float("inf")
    equity=0
    peak=0
    max_dd=0
    for t in trades:
        equity+=t["pnl"]
        peak=max(peak,equity)
        max_dd=max(max_dd,peak-equity)
    return {
        "trades":len(trades),
        "wins":len(wins),
        "losses":len(losses),
        "net_profit":round(total,2),
        "gross_profit":round(gross_profit,2),
        "gross_loss":round(gross_loss,2),
        "win_rate":round(win_rate,2),
        "profit_factor":round(pf,2) if pf!=float("inf") else "Infinity",
        "max_drawdown":round(max_dd,2),
    }

def print_report(s):
    print("="*40)
    print("TRADE JOURNAL ANALYZER")
    print("="*40)
    for k,v in s.items():
        print(f"{k:15}: {v}")

if __name__=="__main__":
    sample=Path("sample_trades.csv")
    if not sample.exists():
        sample.write_text(
"""date,symbol,side,pnl
2026-07-01,XAUUSD,BUY,120
2026-07-01,EURUSD,SELL,-50
2026-07-02,NAS100,BUY,80
2026-07-03,BTCUSD,SELL,-30
2026-07-04,XAUUSD,BUY,150
""",encoding="utf-8")
        print("Created sample_trades.csv")
    trades=load_trades(sample)
    report=stats(trades)
    print_report(report)
