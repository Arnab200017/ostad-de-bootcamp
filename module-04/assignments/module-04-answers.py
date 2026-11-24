#!/usr/bin/env python3
"""
মডিউল ৪-এর অ্যাসাইনমেন্ট — সমাধান

নিজে চেষ্টা করার পরে দেখবেন। আগে দেখলে শেখাটা হবে না — এটা আমি বহুবার
দেখেছি।

চালান:  python3 module-04/assignments/module-04-answers.py
"""

import csv
import json
import os

import sales_tools

PATH = os.path.join("module-04", "data", "raw_sales_week2.txt")
OUTDIR = os.path.join("module-04", "output", "assignment")

COLUMNS = ["order_id", "order_date", "customer_name", "item_name",
           "quantity", "amount", "payment", "status"]


def parse_record(raw):
    parts = raw.split(";")
    return {
        "order_id":      sales_tools.clean_id(parts[0]),
        "order_date":    parts[1].strip(),
        "customer_name": sales_tools.clean_name(parts[2]),
        "item_name":     parts[3].strip(),
        "quantity":      int(parts[4].strip()),
        "amount":        sales_tools.clean_amount(parts[5]),
        "payment":       parts[6].strip().lower(),
        "status":        parts[7].strip().lower(),
    }


def totals_by(records, key):
    totals = {}
    counts = {}
    for rec in records:
        name = rec[key]
        totals[name] = totals.get(name, 0.0) + rec["amount"]
        counts[name] = counts.get(name, 0) + 1
    return totals, counts


# ========== লেভেল ১ ==========
def level_1():
    print("===== লেভেল ১ — পণ্য ধরে হিসাব =====")
    print()

    with open(PATH, encoding="utf-8") as fh:
        lines = fh.read().strip().split("\n")

    records = []
    cancelled = 0

    for raw in lines:
        rec = parse_record(raw)
        if rec["status"] == "cancelled":
            cancelled = cancelled + 1
            continue
        records.append(rec)

    print(f"মোট লাইন: {len(lines)}টা  ·  বাতিল: {cancelled}টা  ·  হিসাবে: {len(records)}টা")
    print()

    totals, counts = totals_by(records, "item_name")

    print("পণ্য ধরে হিসাব")
    for name in sorted(totals):
        print(f"   {name:<20} {counts[name]}টা   {sales_tools.taka(totals[name])}")
    print(f"   {'সব মিলিয়ে':<20} {len(records)}টা   {sales_tools.taka(sum(totals.values()))}")
    print()

    # সবচেয়ে বড়টা — একটা ঘর বাইরে রেখে loop-এ মিলিয়ে দেখা
    top_name = ""
    top_money = 0.0
    for name in totals:
        if totals[name] > top_money:
            top_money = totals[name]
            top_name = name

    print(f"সবচেয়ে বেশি বিক্রি: {top_name} — {sales_tools.taka(top_money)} ({counts[top_name]}টা অর্ডার)")
    print()

    return records, totals, counts, cancelled, len(lines), top_name


# ========== লেভেল ২ ==========
def level_2(records, totals, counts):
    print("===== লেভেল ২ — CSV =====")
    print()

    os.makedirs(OUTDIR, exist_ok=True)
    clean = os.path.join(OUTDIR, "sales_week2_clean.csv")
    summary = os.path.join(OUTDIR, "item_summary.csv")

    # ---- সব record ----
    with open(clean, "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=COLUMNS)
        writer.writeheader()
        for rec in records:
            writer.writerow(rec)
    print(f"লেখা হলো: {clean}  ({len(records)}টা সারি + হেডার)")

    # ---- সারাংশ ----
    with open(summary, "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["item_name", "orders", "total_amount"])
        writer.writeheader()
        for name in sorted(totals):
            writer.writerow({
                "item_name": name,
                "orders": counts[name],
                "total_amount": round(totals[name], 2),
            })
    print(f"লেখা হলো: {summary}       ({len(totals)}টা সারি + হেডার)")
    print()

    # ---- ফেরত পড়া ----
    back = []
    with open(clean, encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            row["quantity"] = int(row["quantity"])
            row["amount"] = float(row["amount"])      # এটা না করলে যোগ হবে না
            back.append(row)

    total = 0.0
    for rec in back:
        total = total + rec["amount"]

    print(f"CSV থেকে ফেরত পড়লাম: {len(back)}টা record")
    print(f"সব মিলিয়ে: {sales_tools.taka(total)}   ← মিলে গেছে")
    print()

    return back


# ========== লেভেল ৩ ==========
def level_3(records, totals, counts, cancelled, top_name):
    print("===== লেভেল ৩ — JSON =====")
    print()

    os.makedirs(OUTDIR, exist_ok=True)
    path = os.path.join(OUTDIR, "report_week2.json")

    by_date, date_counts = totals_by(records, "order_date")

    by_item = {}
    for name in sorted(totals):
        by_item[name] = round(totals[name], 2)

    by_day = {}
    for day in sorted(by_date):
        by_day[day] = round(by_date[day], 2)

    days = sorted(by_date)

    report = {
        "company": "ThelaGari",
        "week": f"{days[0]} → {days[-1]}",
        "counted": len(records),
        "cancelled": cancelled,
        "grand_total": round(sum(totals.values()), 2),
        "top_item": {
            "item_name": top_name,
            "orders": counts[top_name],
            "total_amount": round(totals[top_name], 2),
        },
        "by_item": by_item,
        "by_date": by_day,
    }

    with open(path, "w", encoding="utf-8") as fh:
        json.dump(report, fh, ensure_ascii=False, indent=2)
    print(f"লেখা হলো: {path}")
    print()

    with open(path, encoding="utf-8") as fh:
        loaded = json.load(fh)

    gt = loaded["grand_total"]
    print(f"grand_total        = {gt}   ← type {type(gt).__name__}")
    print(f"top_item.item_name = {loaded['top_item']['item_name']}")
    print(f"by_item-এ ঘর       = {len(loaded['by_item'])}টা")
    print()
    print("CSV-তে float() করতে হয়েছিল, JSON-এ হলো না — কারণ JSON ফাইলেই লেখা")
    print("থাকে কোনটা সংখ্যা আর কোনটা লেখা। CSV-তে সব কমা দিয়ে আলাদা করা লেখা,")
    print("আর কিছুই না।")


def main():
    records, totals, counts, cancelled, nlines, top_name = level_1()
    level_2(records, totals, counts)
    level_3(records, totals, counts, cancelled, top_name)


if __name__ == "__main__":
    main()
