"""
AI UPI Cashflow Reconciler for Indian MSMEs
Starter demo: matches UPI credits to invoices and estimates short-term cash flow.

This is a practical, commented script you can extend with real data or AI matching.
"""

import pandas as pd
from datetime import datetime, timedelta
from difflib import SequenceMatcher

# ---------------------------------------------------------------------------
# Sample data (replace with real CSV loads in production)
# ---------------------------------------------------------------------------

# Typical UPI export columns: date, amount, description / payee, utr
upi_transactions = [
    {"date": "2026-11-15", "amount": 25000.00, "description": "Rahul Sharma UPI", "utr": "UPI123456789"},
    {"date": "2026-11-16", "amount": 18500.50, "description": "Payment for INV-1042", "utr": "UPI987654321"},
    {"date": "2026-11-17", "amount": 12000.00, "description": "Priya Patel", "utr": "UPI112233445"},
    {"date": "2026-11-18", "amount": 5000.00, "description": "Partial payment INV-1050", "utr": "UPI556677889"},
    {"date": "2026-11-19", "amount": 32000.00, "description": "Unknown sender", "utr": "UPI998877665"},
]

# Typical invoice list: invoice_no, customer, amount, due_date, status
invoices = [
    {"invoice_no": "INV-1041", "customer": "Rahul Sharma", "amount": 25000.00, "due_date": "2026-11-14", "status": "open"},
    {"invoice_no": "INV-1042", "customer": "ABC Traders", "amount": 18500.50, "due_date": "2026-11-15", "status": "open"},
    {"invoice_no": "INV-1048", "customer": "Priya Patel", "amount": 12000.00, "due_date": "2026-11-16", "status": "open"},
    {"invoice_no": "INV-1050", "customer": "XYZ Services", "amount": 15000.00, "due_date": "2026-11-10", "status": "open"},
    {"invoice_no": "INV-1055", "customer": "New Client", "amount": 32000.00, "due_date": "2026-11-20", "status": "open"},
]

upi_df = pd.DataFrame(upi_transactions)
invoice_df = pd.DataFrame(invoices)

# Convert dates
upi_df["date"] = pd.to_datetime(upi_df["date"])
invoice_df["due_date"] = pd.to_datetime(invoice_df["due_date"])


def name_similarity(a: str, b: str) -> float:
    """Simple string similarity (0-1). Replace with embeddings or LLM scoring later."""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def match_transactions(upi_df: pd.DataFrame, invoice_df: pd.DataFrame, date_window_days: int = 7):
    """
    Rule-based matching:
    - Amount within 1 INR tolerance
    - Date of UPI within ± date_window_days of invoice due date
    - Highest name similarity above threshold
    Returns list of match dicts and unmatched lists.
    """
    matches = []
    unmatched_upi = []
    used_invoices = set()

    for _, upi in upi_df.iterrows():
        best_score = 0.0
        best_invoice = None

        for idx, inv in invoice_df.iterrows():
            if idx in used_invoices:
                continue

            # Amount check (allow small rounding differences)
            if abs(upi["amount"] - inv["amount"]) > 1.0:
                continue

            # Date window
            date_diff = abs((upi["date"] - inv["due_date"]).days)
            if date_diff > date_window_days:
                continue

            # Name / description similarity
            score = name_similarity(upi["description"], inv["customer"])
            # Bonus if invoice number appears in description
            if inv["invoice_no"].lower() in upi["description"].lower():
                score += 0.3

            if score > best_score:
                best_score = score
                best_invoice = (idx, inv)

        if best_invoice and best_score >= 0.55:
            idx, inv = best_invoice
            used_invoices.add(idx)
            matches.append({
                "upi_utr": upi["utr"],
                "upi_amount": upi["amount"],
                "upi_date": upi["date"].strftime("%Y-%m-%d"),
                "invoice_no": inv["invoice_no"],
                "customer": inv["customer"],
                "match_score": round(best_score, 2),
                "type": "full" if abs(upi["amount"] - inv["amount"]) < 1 else "partial"
            })
        else:
            unmatched_upi.append(upi.to_dict())

    unmatched_invoices = [
        inv.to_dict() for idx, inv in invoice_df.iterrows() if idx not in used_invoices
    ]

    return matches, unmatched_upi, unmatched_invoices


def cashflow_summary(matches, unmatched_upi, unmatched_invoices):
    """Generate a simple short-term cash-flow view."""
    confirmed = sum(m["upi_amount"] for m in matches)
    pending = sum(inv["amount"] for inv in unmatched_invoices)
    unallocated = sum(u["amount"] for u in unmatched_upi)

    today = datetime(2026, 11, 20)
    next_7 = today + timedelta(days=7)
    next_30 = today + timedelta(days=30)

    return {
        "confirmed_inflows": round(confirmed, 2),
        "unallocated_upi_credits": round(unallocated, 2),
        "pending_receivables": round(pending, 2),
        "as_of": today.strftime("%Y-%m-%d"),
        "note": "Pending receivables assume open invoices. Extend with ageing and probability weights."
    }


def main():
    print("=== AI UPI Cashflow Reconciler – MSME Demo ===\n")

    matches, unmatched_upi, unmatched_invoices = match_transactions(upi_df, invoice_df)

    print("MATCHED TRANSACTIONS")
    print("-" * 60)
    if matches:
        for m in matches:
            print(f"{m['upi_date']} | ₹{m['upi_amount']:,.2f} | {m['invoice_no']} | {m['customer']} | score={m['match_score']}")
    else:
        print("No matches found.")

    print("\nUNMATCHED UPI CREDITS (need manual review)")
    print("-" * 60)
    for u in unmatched_upi:
        print(f"{u['date'].strftime('%Y-%m-%d')} | ₹{u['amount']:,.2f} | {u['description']} | {u['utr']}")

    print("\nOPEN INVOICES STILL UNPAID")
    print("-" * 60)
    for inv in unmatched_invoices:
        print(f"{inv['invoice_no']} | {inv['customer']} | ₹{inv['amount']:,.2f} | due {inv['due_date'].strftime('%Y-%m-%d')}")

    summary = cashflow_summary(matches, unmatched_upi, unmatched_invoices)
    print("\nCASH-FLOW SNAPSHOT")
    print("-" * 60)
    print(f"Confirmed inflows matched to invoices : ₹{summary['confirmed_inflows']:,.2f}")
    print(f"Unallocated UPI credits               : ₹{summary['unallocated_upi_credits']:,.2f}")
    print(f"Pending receivables (open invoices)   : ₹{summary['pending_receivables']:,.2f}")
    print(f"\n{summary['note']}")

    print("\n--- Next steps for production ---")
    print("1. Replace sample data with real UPI export + invoice CSV.")
    print("2. Add fuzzy matching library or LLM-based description scoring.")
    print("3. Handle partial payments and multi-invoice allocations.")
    print("4. Export to Excel and add GST-friendly reports.")


if __name__ == "__main__":
    main()
