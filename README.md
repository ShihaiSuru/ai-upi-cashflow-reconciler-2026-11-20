# AI UPI Cashflow Reconciler

**Practical fintech tool for Indian MSMEs**  
Built for founders focused on AI-powered cash-flow systems.

## The Problem

Indian MSMEs (especially those dealing with retail, wholesale, or services) heavily rely on UPI for payments. However:

- Matching UPI credits to specific invoices is manual and time-consuming.
- Partial payments, delayed settlements, and vague UPI descriptions (e.g., "Payment from Rahul") create mismatches.
- This leads to inaccurate cash-flow visibility, delayed follow-ups on receivables, GST reconciliation issues, and poor working capital decisions.
- Founders and accountants waste hours every week instead of focusing on growth.

## The Solution

A lightweight, AI-ready reconciler that:

1. Ingests UPI transaction exports (from bank apps or aggregators) and invoice lists (CSV/Excel).
2. Automatically matches transactions to invoices using amount, date proximity, and description similarity.
3. Flags exact matches, partial payments, and unmatched items.
4. Generates a short-term cash-flow summary: confirmed inflows, pending receivables, and risk flags.
5. Designed to be extended with LLMs or embeddings for smarter description matching (e.g., resolving "Rahul Sharma" vs invoice customer name).

This is a starter implementation focused on practical utility for MSMEs — not a full SaaS product, but a clear demonstration of the approach.

## Features (Current Demo)

- Sample data for UPI transactions and invoices
- Rule-based matching (exact amount + date window + basic name similarity)
- Clear reporting of matched, partial, and unmatched items
- Simple cash-flow projection (7-day and 30-day view)
- Fully commented code ready for AI enhancements

## Usage

### Prerequisites
- Python 3.8+
- `pandas` (install with `pip install pandas`)

### Run the demo
```bash
python upi_reconciler.py
```

The script uses built-in sample data. Replace the sample lists with your real CSV loads for actual use.

### Extending it
- Load real data: `pd.read_csv("upi_export.csv")` and `pd.read_csv("invoices.csv")`
- Add fuzzy matching with `rapidfuzz` or `thefuzz`
- Integrate an LLM call (OpenAI, Groq, or local) to score description similarity
- Export results to Excel for accountants

## Why This Matters for Indian MSMEs

Accurate, near-real-time cash-flow visibility is a superpower. Tools like this reduce the gap between payment received and invoice closed, improve collection rates, and give founders reliable data for decisions on inventory, salaries, or new orders.

## License

MIT — free to use, modify, and build upon for commercial MSME tools.

---

*Created as a practical demo of AI cash-flow systems for Indian MSMEs.*
