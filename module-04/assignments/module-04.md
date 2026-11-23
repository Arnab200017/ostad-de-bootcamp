# মডিউল ৪-এর অ্যাসাইনমেন্ট

**মডিউল ৪ · ক্লাস ৭ + ক্লাস ৮** · জমা দেবেন মডিউল ৫ শুরুর আগে

---

## এবার নতুন data

মডিউল ৩-এ আমরা `raw_sales.txt`-এর দশটা লাইন নিয়ে কাজ করেছি। সেখানে প্রতিটা
পণ্য একবার করে এসেছিল, তাই "কোন পণ্যে সবচেয়ে বেশি বিক্রি" প্রশ্নটার কোনো মানে
ছিল না।

এই অ্যাসাইনমেন্টে নতুন একটা ফাইল — **`module-04/data/raw_sales_week2.txt`**।
১৮টা লাইন, আর এবার একই পণ্য আর একই গ্রাহক বারবার এসেছে। dictionary-র আসল কাজ
এখানেই।

| লেভেল | কী | কোন ক্লাস | সময় | কার জন্য |
|---|---|---|---|---|
| ১ | পণ্য ধরে হিসাব, dictionary দিয়ে | ক্লাস ৭ | ২৫ মিনিট | সবার জন্য |
| ২ | পরিষ্কার CSV লেখা আর পড়া | ক্লাস ৮ | ২৫ মিনিট | সবার জন্য |
| ৩ | JSON রিপোর্ট | ক্লাস ৮ | ২০ মিনিট | যাঁরা এগিয়ে |

**লেভেল ২ পর্যন্ত করলেই অ্যাসাইনমেন্ট হয়ে গেছে ধরবো।**

---

## ধাপ ০ — ফাইলগুলো নামিয়ে নিন

```bash
cd ~/de-bootcamp/ostad-de-bootcamp
git pull
```

নিজের repo-তে জায়গা বানান:

```bash
cd ~/de-bootcamp/data-engineering-journey
mkdir -p week-04
```

ক্লাসের `sales_tools.py` ফাইলটা পাশে কপি করে নিন — ওটা আবার লিখবেন না:

```bash
cp ~/de-bootcamp/ostad-de-bootcamp/module-04/solution/sales_tools.py week-04/
```

একটা starter ফাইলও দেওয়া আছে, চাইলে ওটা দিয়ে শুরু করুন:
`module-04/assignments/module-04-starter.py`

---

# লেভেল ১ — পণ্য ধরে হিসাব

**ফাইল:** `week-04/item_report.py`

`module-04/data/raw_sales_week2.txt` পড়ুন। প্রতিটা লাইনকে dictionary বানান
(ক্লাস ৭-এর `parse_record`)। **বাতিল (cancelled) অর্ডার বাদ দেবেন** —
`returned` বাদ দেবেন না, ওটা বিক্রি হয়েছিল।

তারপর বের করুন কোন পণ্যে কত টাকা আর কয়টা অর্ডার।

### যা ছাপাতে হবে

```
মোট লাইন: 18টা  ·  বাতিল: 2টা  ·  হিসাবে: 16টা

পণ্য ধরে হিসাব
   Alu 2kg              1টা   ৳207.75
   Apel 1kg             1টা   ৳1105.00
   ...
   সব মিলিয়ে           16টা   ৳8785.00

সবচেয়ে বেশি বিক্রি: Miniket Chal 5kg — ৳4341.75 (4টা অর্ডার)
```

### ইঙ্গিত

গোনার পুরো কাজটা এই দুই লাইনে:

```python
totals[name] = totals.get(name, 0.0) + rec["amount"]
counts[name] = counts.get(name, 0) + 1
```

ক্লাস ৭-এর `totals_by(records, key)` function-টা কপি করে নিন। `key` হিসেবে
`"item_name"` দিলেই কাজ শেষ — নতুন করে কিছু লিখতে হবে না। **এটাই ওই
function-টা লেখার আসল কারণ ছিল।**

### নিজে মিলিয়ে নেওয়ার তিনটা সংখ্যা

- মোট ৳**8785.00**
- হিসাবে ধরা অর্ডার **16**টা
- সবচেয়ে বেশি **Miniket Chal 5kg**, ৳**4341.75**

---

# লেভেল ২ — পরিষ্কার CSV

**ফাইল:** `week-04/to_csv.py`

লেভেল ১-এর record-গুলো নিয়ে দুইটা CSV ফাইল বানান — `week-04/output/`
ফোল্ডারে।

### ফাইল ১ — `sales_week2_clean.csv`

সব record, হেডার সহ। ঘরগুলো এই ক্রমে:

```
order_id,order_date,customer_name,item_name,quantity,amount,payment,status
```

`csv.DictWriter` ব্যবহার করুন। `newline=""` দিতে ভুলবেন না।

### ফাইল ২ — `item_summary.csv`

তিনটা ঘর: `item_name`, `orders`, `total_amount`। পণ্যের নাম অনুযায়ী sort করা।

### তারপর ফেরত পড়ুন

`csv.DictReader` দিয়ে `sales_week2_clean.csv` আবার পড়ুন, আর আবার হিসাব করে
দেখান যে ৳**8785.00**-ই আসছে।

> **যে ভুলটা সবাই করে:** CSV থেকে পড়লে `amount` একটা string হয়ে আসে —
> `"1240.5"`, সংখ্যা না। যোগ করার আগে `float()` করে নিতে হবে। না করলে
> Python লেখাগুলো জোড়া দিতে শুরু করবে, আর আপনি ঘণ্টাখানেক বসে থাকবেন।

### যা ছাপাতে হবে

```
লেখা হলো: week-04/output/sales_week2_clean.csv  (16টা সারি + হেডার)
লেখা হলো: week-04/output/item_summary.csv       (9টা সারি + হেডার)

CSV থেকে ফেরত পড়লাম: 16টা record
সব মিলিয়ে: ৳8785.00   ← মিলে গেছে
```

---

# লেভেল ৩ — JSON রিপোর্ট

**ফাইল:** `week-04/to_json.py`

একটা রিপোর্ট বানান `week-04/output/report_week2.json`-এ। গড়নটা ঠিক এরকম:

```json
{
  "company": "ThelaGari",
  "week": "2026-10-12 → 2026-10-18",
  "counted": 16,
  "cancelled": 2,
  "grand_total": 8785.0,
  "top_item": {
    "item_name": "Miniket Chal 5kg",
    "orders": 4,
    "total_amount": 4341.75
  },
  "by_item": { "Alu 2kg": 207.75, "...": 0 },
  "by_date": { "2026-10-12": 1614.75, "...": 0 }
}
```

লেখার সময় দুইটা জিনিস দিতেই হবে:

```python
json.dump(report, fh, ensure_ascii=False, indent=2)
```

`ensure_ascii=False` না দিলে বাংলা লেখা `এ` এরকম হয়ে যাবে।
`indent=2` না দিলে পুরোটা এক লাইনে, মানুষ পড়তে পারবে না।

### তারপর ফেরত পড়ুন

`json.load()` দিয়ে পড়ে ছাপান:

```python
print(type(report["grand_total"]))      # <class 'float'>
print(report["top_item"]["item_name"])  # Miniket Chal 5kg
```

**প্রশ্নটা মাথায় রাখুন:** CSV-তে `float()` করতে হয়েছিল, JSON-এ হলো না। কেন?
এই পার্থক্যটা `README.md`-তে দুই লাইনে লিখুন।

---

## জমা দেওয়া

নিজের repo-তে push করুন:

```bash
cd ~/de-bootcamp/data-engineering-journey
git add week-04
git commit -m "Module 4 assignment: dictionary, CSV, JSON"
git push
```

`week-04/README.md`-তে তিনটা জিনিস লিখবেন:

1. কোন লেভেল পর্যন্ত করেছেন
2. কোথায় আটকেছিলেন, আর কীভাবে বের হলেন
3. CSV আর JSON-এর পার্থক্যটা নিজের ভাষায় দুই লাইনে

তারপর repo-র লিংকটা ক্লাসের গ্রুপে পাঠান।

---

## আটকে গেলে

- সংখ্যা মিলছে না? আগে `len(records)` ছাপান — **16** আসছে কি না দেখুন। না
  আসলে cancelled বাদ দেওয়ার জায়গায় ভুল।
- `TypeError: unsupported operand` — `float()` করতে ভুলে গেছেন।
- CSV-তে প্রতি সারির পরে ফাঁকা সারি? `newline=""` দেননি।
- JSON-এ `অ` দেখাচ্ছে? `ensure_ascii=False` দেননি।
- এর পরেও না হলে সাপোর্ট ক্লাসে নিয়ে আসুন — রবি, মঙ্গল, বৃহস্পতি রাত ৯টা।
