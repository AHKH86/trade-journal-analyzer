from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List
import csv


@dataclass
class Trade:
    date: str
    symbol: str
    side: str
    pnl: float


class TradeJournal:

    def __init__(self):
        self.trades: List[Trade] = []

    def load_csv(self, file: str):
        path = Path(file)
        if not path.exists():
            raise FileNotFoundError(file)

        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                trade = Trade(
                    date=row["date"],
                    symbol=row["symbol"],
                    side=row["side"],
                    pnl=float(row["pnl"])
                )
                self.trades.append(trade)

    @property
    def total_trades(self):
        return len(self.trades)

    @property
    def winners(self):
        return [t for t in self.trades if t.pnl > 0]

    @property
    def losers(self):
        return [t for t in self.trades if t.pnl < 0]

    @property
    def gross_profit(self):
        return sum(t.pnl for t in self.winners)

    @property
    def gross_loss(self):
        return abs(sum(t.pnl for t in self.losers))

    @property
    def net_profit(self):
        return sum(t.pnl for t in self.trades)

    @property
    def win_rate(self):
        if self.total_trades == 0:
            return 0
        return len(self.winners) / self.total_trades * 100

    @property
    def average_win(self):
        if not self.winners:
            return 0
        return self.gross_profit / len(self.winners)

    @property
    def average_loss(self):
        if not self.losers:
            return 0
        return self.gross_loss / len(self.losers)

    @property
    def profit_factor(self):
        if self.gross_loss == 0:
            return float("inf")
        return self.gross_profit / self.gross_loss

    def max_drawdown(self):
        equity = peak = drawdown = 0
        for trade in self.trades:
            equity += trade.pnl
            peak = max(peak, equity)
            drawdown = max(drawdown, peak - equity)
        return drawdown

    def equity_curve(self):
        equity = 0
        curve = []
        for trade in self.trades:
            equity += trade.pnl
            curve.append(round(equity, 2))
        return curve

    def best_trade(self):
        return max(self.trades, key=lambda t: t.pnl) if self.trades else None

    def worst_trade(self):
        return min(self.trades, key=lambda t: t.pnl) if self.trades else None

    def symbol_statistics(self):
        stats = {}
        for trade in self.trades:
            stats.setdefault(trade.symbol, {"profit":0,"trades":0,"wins":0})
            stats[trade.symbol]["profit"] += trade.pnl
            stats[trade.symbol]["trades"] += 1
            if trade.pnl > 0:
                stats[trade.symbol]["wins"] += 1
        return stats

    def print_report(self):
        print("="*55)
        print("TRADE JOURNAL ANALYZER")
        print("="*55)
        print(f"Total Trades: {self.total_trades}")
        print(f"Winners: {len(self.winners)}")
        print(f"Losers: {len(self.losers)}")
        print(f"Net Profit: {self.net_profit:.2f}")
        print(f"Gross Profit: {self.gross_profit:.2f}")
        print(f"Gross Loss: {self.gross_loss:.2f}")
        print(f"Win Rate: {self.win_rate:.2f}%")
        print(f"Average Win: {self.average_win:.2f}")
        print(f"Average Loss: {self.average_loss:.2f}")
        print(f"Profit Factor: {self.profit_factor:.2f}")
        print(f"Max Drawdown: {self.max_drawdown():.2f}")

def create_sample_csv(file_name="sample_trades.csv"):
    path = Path(file_name)
    if path.exists():
        return
    rows = [
        ["date","symbol","side","pnl"],
        ["2026-07-01","XAUUSD","BUY",120],
        ["2026-07-01","EURUSD","SELL",-45],
        ["2026-07-02","NAS100","BUY",180],
        ["2026-07-02","BTCUSD","SELL",-60],
    ]
    with open(path,"w",newline="",encoding="utf-8") as f:
        csv.writer(f).writerows(rows)

def main():
    create_sample_csv()
    j=TradeJournal()
    j.load_csv("sample_trades.csv")
    j.print_report()

if __name__=="__main__":
    main()
