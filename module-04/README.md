# মডিউল ৪ — dictionary আর ডেটা নিয়ে কাজ

মডিউল ৩-এর অ্যাসাইনমেন্টে payment ধরে হিসাব করতে দশটা variable আর পাঁচটা
`elif` লাগছিল। এই মডিউলে সেটা তিন লাইনে নামবে।

---

## 🚀 ইন্টার‍্যাক্টিভ নোটবুক — ব্রাউজারেই চালান

ক্লাসের সব বিষয় এক জায়গায়, নিজের হাতে চালিয়ে শেখার জন্য।
**কিছু ইনস্টল করা লাগবে না** — শুধু একটা Google অ্যাকাউন্ট।

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sadathasan4/ostad-de-bootcamp/blob/main/module-04/ThelaGari_Python_Lab_Module4.ipynb)

```
https://colab.research.google.com/github/sadathasan4/ostad-de-bootcamp/blob/main/module-04/ThelaGari_Python_Lab_Module4.ipynb
```

ভেতরে — ব্যাখ্যা, চালানোর মতো কোড, **নিজে চেষ্টা করুন** অনুশীলন, লুকানো
উত্তর, একটা মিনি-ল্যাব আর দুইটা চ্যালেঞ্জ। সবগুলোই নিজে মিলিয়ে দেখে বলে
দেবে ঠিক হয়েছে কি না।

> **আপডেট ২৩ নভেম্বর** — ক্লাস ৮-এর অংশটা (পর্ব ৪: CSV আর JSON) যোগ করা
> হয়েছে। আগে খুলে থাকলে ট্যাবটা বন্ধ করে আবার খুলুন।
> মডিউল ৩-এর নোটবুক: `module-03/ThelaGari_Python_Lab_Module3.ipynb`

---

## ক্লাস ৭ — dictionary

### যা শিখবো

- `dictionary` — নাম ধরে জিনিস রাখা আর খোঁজা
- পড়া — `[]` বনাম `.get()`, আর `KeyError`
- যোগ, বদল, মোছা — `del`, `.pop()`
- loop — `for k in d`, `.values()`, `.items()`, `sorted()`
- **গোনা আর জমা করার প্যাটার্ন** — `d[k] = d.get(k, 0) + x`
- record = dictionary — `parts[5]` আর মনে রাখতে হবে না
- list-এর ভেতরে dictionary — API আর JSON-এর আসল গড়ন

### ল্যাব

গত মডিউলের সেই একই হিসাব, এবার dictionary দিয়ে।

| ফাইল | কী |
|---|---|
| `starter/sales_dict.py` | সাতটা TODO — ক্লাসে এটাই পূরণ করবেন |
| `starter/sales_tools.py` | গত মডিউলের সেই ফাইলটাই, পাশে কপি করা |
| `solution/sales_dict.py` | সমাধান — নিজে চেষ্টা করার পরে দেখবেন |
| `solution/EXPECTED_OUTPUT_class7.txt` | ঠিক কী ছাপা হওয়ার কথা |

data আসছে মডিউল ২ থেকে — `module-02/data/raw_sales.txt`.

চালানোর নিয়ম (repo-র **মূল ফোল্ডার** থেকে):

```bash
python3 module-04/starter/sales_dict.py
```

### যে সংখ্যাগুলো মিলতে হবে

```
bkash              3টা   ৳2484.00
nagad              2টা   ৳908.00
card               1টা   ৳812.00
cash on delivery   2টা   ৳661.50
rocket             1টা   ৳232.25
সব মিলিয়ে                ৳5097.75

সবচেয়ে বেশি টাকার দিন: 2026-10-07 — ৳1590.50
সবচেয়ে বড় অর্ডার: ORD100045 — ৳1240.50
```

> **৳5097.75** — এই সংখ্যাটা ক্লাস ৫, ৬ আর ৭-এ একই। কোড তিনবার বদলেছে,
> উত্তর বদলায়নি। এটাই ঠিক পথে আছেন তার প্রমাণ।

---

## ক্লাস ৮ — CSV আর JSON

### যা শিখবো

- CSV আসলে কী, আর আমাদের হাতে বানানো ফাইলটার সমস্যা কোথায়
- লেখা — `csv.writer`, `csv.DictWriter`, আর `newline=""` কেন লাগে
- পড়া — `csv.DictReader`, আর **সব ঘর string হয়ে ফেরে**
- `repr()` দিয়ে ধরা — `'1240.5'` সংখ্যা না, লেখা
- JSON — `json.dump`, `json.load`, `ensure_ascii=False`, `indent=2`
- নামের ভেতরে কমা থাকলে কী হয় — কেন নিজে `split(",")` করতে নেই
- কোনটা কখন — টেবিলের মতো data CSV-তে, বাসার মতো data JSON-এ

### ল্যাব

সাত ধাপ। একই data, এবার আসল ফরম্যাটে ঘুরে আসবে।

| ফাইল | কী |
|---|---|
| `starter/sales_files.py` | সাত ধাপের TODO — ক্লাসে এটাই পূরণ করবেন |
| `solution/sales_files.py` | সমাধান — নিজে চেষ্টা করার পরে |
| `solution/EXPECTED_OUTPUT_class8.txt` | ঠিক কী ছাপা হওয়ার কথা |
| `data/items_messy.csv` | নামের ভেতরে কমাওয়ালা ফাইল |

চালানোর নিয়ম (repo-র **মূল ফোল্ডার** থেকে):

```bash
python3 module-04/starter/sales_files.py
```

তিনটা ফাইল তৈরি হবে `module-04/output/` ফোল্ডারে —
`sales_clean.csv`, `summary_by_payment.csv`, `summary.json`.

> **৳5097.75** — ক্লাস ৫, ৬, ৭ আর ৮, চারবারই একই। ফাইল বদলেছে, উত্তর
> বদলায়নি।

### আজকের তিনটা কথা

1. **CSV-তে কোনো type নেই** — পড়ার সাথে সাথেই `float()`। না করলে error
   আসবে না, শুধু উত্তর ভুল হবে।
2. **নিজে `split(",")` করবেন না** — একটা কমা একদিন সব ভেঙে দেবে।
3. **JSON-এ গড়ন আর type দুইটাই বাঁচে** — তাই সারাংশ, config আর API-র data
   JSON-এ রাখি।

---

## অ্যাসাইনমেন্ট

প্রতি মডিউলে একটা, মডিউলের শেষে। **মডিউল ৪-এরটা এখন পাওয়া যাচ্ছে** —
ক্লাস ৭ আর ৮ মিলিয়ে, তিনটা লেভেলে।

👉 `module-04/assignments/module-04.md`

এবার নতুন data — `data/raw_sales_week2.txt`, ১৮টা লাইন, আর একই পণ্য
বারবার এসেছে।

| ফাইল | কী |
|---|---|
| `assignments/module-04.md` | কাজটা কী |
| `assignments/module-04-starter.py` | প্রথমবারেই চলে, শূন্য ছাপায় |
| `assignments/module-04-answers.py` | সমাধান — নিজে চেষ্টার পরে |
| `assignments/EXPECTED_OUTPUT_module-04.txt` | ঠিক কী ছাপা হওয়ার কথা |

মিলিয়ে নেওয়ার তিনটা সংখ্যা: মোট **৳8785.00** · হিসাবে **16**টা অর্ডার ·
সবচেয়ে বেশি **Miniket Chal 5kg** (৳4341.75)

জমা দেবেন মডিউল ৫ শুরুর আগে। যাঁদের মডিউল ৩-এরটা এখনো বাকি:
`module-03/assignments/module-03.md`

---

## ফোল্ডার

```
module-04/
  data/           ল্যাব আর অ্যাসাইনমেন্টের data ফাইল
  starter/        TODO ভরা ফাইল — আপনি পূরণ করবেন
  solution/       সমাধান — পরে দেখবেন
  assignments/    মডিউলের শেষের কাজ
  output/         কোড চালালে এখানে ফাইল তৈরি হবে (git-এ যায় না)
```

> `output/` ফোল্ডারটা `.gitignore`-এ আছে। **কোড repo-তে রাখি, কোডের
> ফলাফল না** — এটা একটা ভালো অভ্যাস, এখন থেকেই করুন।
