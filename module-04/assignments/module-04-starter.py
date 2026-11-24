#!/usr/bin/env python3
"""
মডিউল ৪-এর অ্যাসাইনমেন্ট — starter

এই ফাইলটা প্রথমবারেই চলে। চালিয়ে দেখুন — শূন্য ছাপাবে। তারপর TODO ধরে ধরে
ভরতে থাকুন, প্রতিটা TODO-র পরে একবার করে চালান।

চালানোর নিয়ম (repo-র মূল ফোল্ডার থেকে):

    python3 module-04/assignments/module-04-starter.py

নিজের repo-তে নিয়ে গেলে PATH দুইটা বদলে নেবেন।
"""

import csv
import json
import os

import sales_tools       # module-04/solution/sales_tools.py পাশে কপি করে নিন

PATH = os.path.join("module-04", "data", "raw_sales_week2.txt")
OUTDIR = os.path.join("module-04", "output", "assignment")


def parse_record(raw):
    """ক্লাস ৭-এর function — দেওয়াই আছে, কপি করে এনেছি।"""
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
    """ক্লাস ৭-এর function — এটাও দেওয়া আছে।

    key = "item_name" দিলে পণ্য ধরে, "order_date" দিলে তারিখ ধরে।
    """
    totals = {}
    counts = {}
    for rec in records:
        name = rec[key]
        totals[name] = totals.get(name, 0.0) + rec["amount"]
        counts[name] = counts.get(name, 0) + 1
    return totals, counts


# ========== লেভেল ১ ==========
def level_1():
    with open(PATH, encoding="utf-8") as fh:
        lines = fh.read().strip().split("\n")

    records = []
    cancelled = 0

    for raw in lines:
        rec = parse_record(raw)
        # TODO: status "cancelled" হলে cancelled বাড়ান আর continue
        # TODO: নইলে records.append(rec)
        pass

    print(f"মোট লাইন: {len(lines)}টা  ·  বাতিল: {cancelled}টা  ·  হিসাবে: {len(records)}টা")
    print()

    totals, counts = totals_by(records, "item_name")

    print("পণ্য ধরে হিসাব")
    # TODO: sorted(totals) ঘুরে প্রতিটা পণ্যের নাম, কয়টা আর কত টাকা ছাপান
    #       print(f"   {name:<20} {counts[name]}টা   {sales_tools.taka(totals[name])}")

    print(f"   {'সব মিলিয়ে':<20} {len(records)}টা   {sales_tools.taka(sum(totals.values()))}")
    print()

    # TODO: সবচেয়ে বেশি টাকার পণ্যটা বের করুন (ক্লাস ৭-এর best_day-র নিয়মেই)

    return records, totals, counts


# ========== লেভেল ২ ==========
def level_2(records, totals, counts):
    os.makedirs(OUTDIR, exist_ok=True)
    clean = os.path.join(OUTDIR, "sales_week2_clean.csv")
    summary = os.path.join(OUTDIR, "item_summary.csv")

    columns = ["order_id", "order_date", "customer_name", "item_name",
               "quantity", "amount", "payment", "status"]

    # TODO: csv.DictWriter দিয়ে সব record clean ফাইলে লিখুন (newline="" মনে রাখবেন)

    # TODO: csv.DictWriter দিয়ে item_summary.csv লিখুন
    #       ঘর তিনটা: item_name, orders, total_amount

    # TODO: csv.DictReader দিয়ে clean ফাইলটা আবার পড়ুন
    #       amount কে float() করতে ভুলবেন না — নইলে যোগ হবে না
    back = []

    print(f"CSV থেকে ফেরত পড়লাম: {len(back)}টা record")
    if back:
        total = 0.0
        for rec in back:
            total = total + rec["amount"]
        print(f"সব মিলিয়ে: {sales_tools.taka(total)}")
    print()

    return back


# ========== লেভেল ৩ ==========
def level_3(records, totals, counts):
    os.makedirs(OUTDIR, exist_ok=True)
    path = os.path.join(OUTDIR, "report_week2.json")

    by_date, date_counts = totals_by(records, "order_date")

    # TODO: by_item আর by_date dictionary দুইটা বানান (round(..., 2) করে)

    # TODO: report dictionary বানান — অ্যাসাইনমেন্টের গড়ন অনুযায়ী

    # TODO: json.dump(report, fh, ensure_ascii=False, indent=2)

    # TODO: json.load() দিয়ে ফেরত পড়ে type আর top_item ছাপান

    print(f"(লেভেল ৩ শেষ হলে এখানে লেখা হবে: {path})")


def main():
    records, totals, counts = level_1()
    back = level_2(records, totals, counts)
    level_3(records, totals, counts)


if __name__ == "__main__":
    main()


# ---------- মিলিয়ে দেখুন ----------
#   মোট লাইন 18টা · বাতিল 2টা · হিসাবে 16টা
#   সব মিলিয়ে ৳8785.00
#   সবচেয়ে বেশি: Miniket Chal 5kg — ৳4341.75 (4টা অর্ডার)
#   পণ্য মোট 9 রকম
