#!/usr/bin/env python3
"""
ক্লাস ৮ — ল্যাবের সমাধান

এতদিন আমরা একটা হাতে বানানো টেক্সট ফাইল পড়েছি আর নিজে split করেছি।
আজ আসল দুইটা ফরম্যাট — CSV আর JSON।

চালান:  python3 module-04/solution/sales_files.py
"""

import csv
import json
import os

import sales_tools

RAW = os.path.join("module-02", "data", "raw_sales.txt")
MESSY = os.path.join("module-04", "data", "items_messy.csv")
OUTDIR = os.path.join("module-04", "output")

CLEAN_CSV = os.path.join(OUTDIR, "sales_clean.csv")
SUMMARY_CSV = os.path.join(OUTDIR, "summary_by_payment.csv")
SUMMARY_JSON = os.path.join(OUTDIR, "summary.json")

COLUMNS = ["order_id", "order_date", "customer_name", "item_name",
           "quantity", "amount", "payment", "status"]


# ---------- গত ক্লাসের function, কপি করে আনা ----------
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


# ---------- ধাপ ১: কাঁচা লাইন থেকে পরিষ্কার CSV ----------
def write_clean_csv(path, records):
    """csv.DictWriter — dictionary-র list সোজা CSV-তে।"""
    with open(path, "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=COLUMNS)
        writer.writeheader()
        for rec in records:
            writer.writerow(rec)


# ---------- ধাপ ৩: CSV থেকে আবার dictionary ----------
def read_clean_csv(path):
    """csv.DictReader — প্রতিটা সারি একটা dictionary হয়ে আসে।

    কিন্তু সব মান string হয়ে আসে। তাই quantity আর amount নিজে বদলে নিতে হয়।
    """
    records = []
    with open(path, encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            row["quantity"] = int(row["quantity"])
            row["amount"] = float(row["amount"])
            records.append(row)
    return records


def main():
    os.makedirs(OUTDIR, exist_ok=True)

    # ---------- কাঁচা ফাইল → record ----------
    with open(RAW, encoding="utf-8") as fh:
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

    # ---------- ধাপ ১ ----------
    write_clean_csv(CLEAN_CSV, records)
    print(f"[১] লেখা হলো: {CLEAN_CSV}")

    with open(CLEAN_CSV, encoding="utf-8") as fh:
        head = fh.read().split("\n")
    print("    প্রথম দুই লাইন —")
    print(f"      {head[0]}")
    print(f"      {head[1]}")
    print()

    # ---------- ধাপ ২: csv.reader — সবই string ----------
    print("[২] csv.reader দিয়ে পড়লে সব ঘর string হয়ে আসে")
    with open(CLEAN_CSV, encoding="utf-8", newline="") as fh:
        reader = csv.reader(fh)
        header = next(reader)          # প্রথম সারিটা হেডার
        first = next(reader)
    print(f"      হেডার   : {header[0]}, {header[1]}, ...")
    print(f"      amount  : {first[5]!r}   ← type {type(first[5]).__name__}")
    print(f"      {first[5]!r} + 1 করলে Python দুইটা লেখা জোড়া দেবে, যোগ করবে না")
    print()

    # ---------- ধাপ ৩: DictReader ----------
    back = read_clean_csv(CLEAN_CSV)
    print(f"[৩] csv.DictReader দিয়ে ফেরত পেলাম {len(back)}টা record")
    print(f"      back[0]['customer_name'] = {back[0]['customer_name']}")
    print(f"      back[0]['amount']        = {back[0]['amount']}   ← type {type(back[0]['amount']).__name__}")
    print()

    # ---------- ধাপ ৪: হিসাব — সেই একই সংখ্যা ----------
    totals, counts = totals_by(back, "payment")
    print("[৪] payment ধরে হিসাব — ফাইল ঘুরে এলেও সংখ্যা এক")
    for name in sorted(totals):
        print(f"      {name:<18} {counts[name]}টা   {sales_tools.taka(totals[name])}")
    print(f"      {'সব মিলিয়ে':<18} {len(back)}টা   {sales_tools.taka(sum(totals.values()))}")
    print()

    # ---------- ধাপ ৫: সারাংশ CSV ----------
    with open(SUMMARY_CSV, "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["payment", "orders", "total_amount"])
        writer.writeheader()
        for name in sorted(totals):
            writer.writerow({
                "payment": name,
                "orders": counts[name],
                "total_amount": round(totals[name], 2),
            })
    print(f"[৫] লেখা হলো: {SUMMARY_CSV}")
    print()

    # ---------- ধাপ ৬: JSON ----------
    by_date, date_counts = totals_by(back, "order_date")

    # dictionary-র ভেতরে dictionary — JSON-এর আসল সুবিধা এটাই
    payment_part = {}
    for name in sorted(totals):
        payment_part[name] = round(totals[name], 2)

    date_part = {}
    for day in sorted(by_date):
        date_part[day] = round(by_date[day], 2)

    summary = {
        "company": "ThelaGari",
        "source_file": RAW,
        "total_lines": len(lines),
        "cancelled": cancelled,
        "counted": len(back),
        "grand_total": round(sum(totals.values()), 2),
        "by_payment": payment_part,
        "by_date": date_part,
    }

    with open(SUMMARY_JSON, "w", encoding="utf-8") as fh:
        json.dump(summary, fh, ensure_ascii=False, indent=2)
    print(f"[৬] লেখা হলো: {SUMMARY_JSON}")
    print("    ভেতরে দেখতে এরকম —")
    print('      "grand_total": 5097.75,')
    print('      "by_payment": { "bkash": 2484.0, ... }')
    print()

    # ---------- ধাপ ৭: JSON ফেরত পড়া — type বেঁচে থাকে ----------
    with open(SUMMARY_JSON, encoding="utf-8") as fh:
        loaded = json.load(fh)

    print("[৭] JSON ফেরত পড়লাম — CSV-র সাথে তফাতটা এখানে")
    gt = loaded["grand_total"]
    print(f"      grand_total = {gt}   ← type {type(gt).__name__}, নিজে বদলাতে হলো না")
    print(f"      by_payment['bkash'] = {loaded['by_payment']['bkash']}")
    print(f"      by_payment-এর ভেতরে {len(loaded['by_payment'])}টা ঘর — CSV-তে এই বাসা বানানো যায় না")
    print()

    # ---------- বোনাস: কমাওয়ালা নাম ----------
    print("[বোনাস] নামের ভেতরে কমা থাকলে কী হয়")
    with open(MESSY, encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    bad = rows[1]
    print(f"      csv module       : {bad['item_name']}")
    with open(MESSY, encoding="utf-8") as fh:
        raw_line = fh.read().split("\n")[2]
    print(f"      হাতে split(',')  : {raw_line.split(',')[1]}")
    print(f"      হাতে split-এ ঘর হয় {len(raw_line.split(','))}টা, অথচ হেডারে ঘর ৪টা")
    print()
    print("এই কারণেই csv module. নিজে split করলে একদিন না একদিন ভাঙবেই।")


if __name__ == "__main__":
    main()
