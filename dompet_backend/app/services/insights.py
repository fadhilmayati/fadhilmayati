from __future__ import annotations

from collections import defaultdict
from datetime import date

from ..models.transaction import CashflowSummary
from .database import InMemorySession


class InsightService:
    def __init__(self, session: InMemorySession):
        self.session = session

    def cashflow_summary(self, user_id: str, start: date | None = None, end: date | None = None) -> CashflowSummary:
        transactions = list(self.session.iter_transactions(user_id, start=start, end=end))

        income = sum(tx.amount for tx in transactions if tx.amount > 0)
        expense = sum(abs(tx.amount) for tx in transactions if tx.amount < 0)
        net = income - expense
        saving_rate = (net / income) if income else 0.0

        return CashflowSummary(
            total_income=round(income, 2),
            total_expense=round(expense, 2),
            net_cashflow=round(net, 2),
            saving_rate=round(saving_rate, 2),
        )

    def expense_by_category(self, user_id: str, start: date | None = None, end: date | None = None) -> dict[str, float]:
        totals: dict[str, float] = defaultdict(float)
        for tx in self.session.iter_transactions(user_id, start=start, end=end):
            if tx.amount >= 0:
                continue
            totals[tx.category or "uncategorised"] += abs(tx.amount)

        return {category: round(value, 2) for category, value in totals.items()}

    def income_opportunities(self, summary: CashflowSummary) -> list[str]:
        recommendations: list[str] = []
        if summary.saving_rate < 0.2:
            recommendations.append(
                "Increase emergency fund contributions to reach at least a 20% saving rate."
            )
        if summary.net_cashflow <= 0:
            recommendations.append(
                "Review recurring subscriptions and renegotiate utility bills to reduce monthly burn."
            )
        if summary.total_income < 5000:
            recommendations.append(
                "Explore part-time gig economy platforms popular in Malaysia such as Grab, FoodPanda, or Upwork."
            )
        else:
            recommendations.append(
                "Consider optimising EPF/PRS contributions for tax relief while reallocating surplus into higher-yield instruments."
            )
        return recommendations
