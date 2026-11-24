#!/usr/bin/env python3
"""
ক্লাস ৮ — ল্যাব

এতদিন আমরা একটা হাতে বানানো টেক্সট ফাইল পড়েছি আর নিজে split করেছি।
সেটা শেখার জন্য ঠিক ছিল। কিন্তু অফিসে data আসে দুইটা ফরম্যাটে —
CSV আর JSON। আজ সেই দুইটা।

চালানোর নিয়ম (repo-র মূল ফোল্ডার থেকে):

    python3 module-04/starter/sales_files.py

TODO লেখা জায়গাগুলো আপনি পূরণ করবেন। উপরের অংশ (parse_record, totals_by)
গত ক্লাসেরই — ওটা দেওয়াই আছে, আজ ছোঁয়ার দরকার নেই।
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


# ---------- গত ক্লাসের দুইটা function — দেওয়াই আছে ----------
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


# ---------- ধাপ ১: dictionary-র list → CSV ফাইল ----------
def write_clean_csv(path, records):
    """csv.DictWriter দিয়ে লিখুন।

    ইঙ্গিত:
        with open(path, "w", encoding="utf-8", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=COLUMNS)
            writer.writeheader()
            for rec in records:
                writer.writerow(rec)

    newline="" কেন? না দিলে Windows-এ প্রতি সারির পরে একটা ফাঁকা সারি পড়ে।
    """
    # TODO
    pass


# ---------- ধাপ ৩: CSV → dictionary-র list ----------
def read_clean_csv(path):
    """csv.DictReader দিয়ে পড়ুন।

    মনে রাখার জিনিস — CSV ফাইলে কোনো type থাকে না। সব ঘর string হয়ে আসে।
    তাই quantity আর amount নিজে বদলে নিতে হবে।

    ইঙ্গিত:
        records = []
        with open(path, encoding="utf-8", newline="") as fh:
            for row in csv.DictReader(fh):
                row["quantity"] = int(row["quantity"])
                row["amount"] = float(row["amount"])
                records.append(row)
        return records
    """
    # TODO
    return []


def main():
    os.makedirs(OUTDIR, exist_ok=True)

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

    # ---------- ধাপ ১: উপরের function-টা ডাকুন ----------
    # TODO: write_clean_csv(CLEAN_CSV, records)
    # TODO: print করে বলুন কোথায় লেখা হলো


    # ---------- ধাপ ২: csv.reader দিয়ে পড়ে দেখুন সব string ----------
    # ইঙ্গিত:
    #   with open(CLEAN_CSV, encoding="utf-8", newline="") as fh:
    #       reader = csv.reader(fh)
    #       header = next(reader)      # প্রথম সারিটা হেডার, সরিয়ে রাখলাম
    #       first = next(reader)
    #   print(repr(first[5]))          # '1240.5' — কোটেশনসহ, মানে string

    # TODO


    # ---------- ধাপ ৩: DictReader দিয়ে ফেরত আনুন ----------
    # TODO: back = read_clean_csv(CLEAN_CSV)
    # TODO: back[0]["amount"] ছাপিয়ে type দেখুন — এবার float


    # ---------- ধাপ ৪: সেই পুরনো হিসাব, নতুন ফাইল থেকে ----------
    # ইঙ্গিত:
    #   totals, counts = totals_by(back, "payment")
    #   for name in sorted(totals):
    #       print(f"   {name:<18} {counts[name]}টা   {sales_tools.taka(totals[name])}")
    #
    # সব মিলিয়ে ৳5097.75 আসতেই হবে। না আসলে উপরে কোথাও ভুল।

    # TODO


    # ---------- ধাপ ৫: সারাংশটা একটা ছোট CSV-তে লিখুন ----------
    # ঘর তিনটা: payment, orders, total_amount
    # ইঙ্গিত: DictWriter, fieldnames=["payment", "orders", "total_amount"]

    # TODO


    # ---------- ধাপ ৬: একই সারাংশ JSON-এ ----------
    # ইঙ্গিত:
    #   summary = {
    #       "company": "ThelaGari",
    #       "counted": len(back),
    #       "grand_total": round(sum(totals.values()), 2),
    #       "by_payment": payment_part,     # dictionary-র ভেতরে dictionary
    #   }
    #   with open(SUMMARY_JSON, "w", encoding="utf-8") as fh:
    #       json.dump(summary, fh, ensure_ascii=False, indent=2)
    #
    # ensure_ascii=False না দিলে বাংলা লেখা এ এরকম হয়ে যায়।
    # indent=2 না দিলে পুরোটা এক লাইনে — মানুষ পড়তে পারে না।

    # TODO


    # ---------- ধাপ ৭: JSON ফেরত পড়ুন ----------
    # ইঙ্গিত:
    #   with open(SUMMARY_JSON, encoding="utf-8") as fh:
    #       loaded = json.load(fh)
    #   print(type(loaded["grand_total"]))   # float — নিজে বদলাতে হলো না
    #
    # CSV আর JSON-এর আসল তফাতটা এই এক লাইনে।

    # TODO


    # ---------- বোনাস: নামের ভেতরে কমা ----------
    # module-04/data/items_messy.csv খুলে দেখুন। ITM-02-র নামে একটা কমা আছে।
    # csv.DictReader দিয়ে পড়ুন, তারপর একই লাইন হাতে .split(",") করে দেখুন।
    # কয়টা ঘর পেলেন?

    # TODO


if __name__ == "__main__":
    main()


# ---------- মিলিয়ে দেখুন ----------
#   মোট লাইন 10টা · বাতিল 1টা · হিসাবে 9টা
#   payment ধরে:  bkash ৳2484.00 · card ৳812.00 · cash on delivery ৳661.50
#                 nagad ৳908.00 · rocket ৳232.25
#   সব মিলিয়ে:    ৳5097.75   ← ক্লাস ৫, ৬, ৭ আর ৮ — চারবারই একই
#
#   তিনটা ফাইল তৈরি হওয়ার কথা module-04/output/ ফোল্ডারে:
#     sales_clean.csv · summary_by_payment.csv · summary.json
