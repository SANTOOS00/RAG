Here is the step-by-step breakdown of how to implement the **Indexing** stage for the **RAG against the machine** project:

---

### 1. File Ingestion

* Traverse and read all relevant source files inside the `data/raw/vllm-0.10.1/` directory.


* **Strict Constraint:** The `file_path` for each source chunk must match the relative path in the repository **verbatim** (e.g., `data/raw/vllm-0.10.1/docs/features/lora.md`). Any path alterations or absolute paths will result in a 0 score on Recall@k during Moulinette evaluation.



---

### 2. Chunking Strategies

The subject requires implementing two distinct chunking strategies:

1. **Python Code Chunking:**
* Parse Python files according to code structure (using AST, classes, or functions) to ensure logical context remains intact.


2. **Markdown / Text Chunking:**
* Split documentation and text files based on section headings (`#`, `##`, `###`) or paragraphs.



#### **Chunking Constraints:**

* **Max Size:** Configurable via `--max_chunk_size` CLI flag (defaults to `2000` characters).


* **Strict Limit:** No individual chunk may exceed 2000 characters; retrieving an oversized chunk invalidates the entire output during grading.


* **Metadata Tracking:** Each chunk must maintain precise metadata:
* `file_path` (string)


* `first_character_index` (integer)


* `last_character_index` (integer)





---

### 3. Text Preprocessing & Tokenization

Process the raw text of each chunk to prepare it for indexing:

* Case normalization (lowercase).
* Tokenization (splitting into words/tokens).
* Optional stopword removal or stemming to improve lexical retrieval quality.

---

### 4. Search Indexing (BM25 or TF-IDF)

Implement at least one of the two mandatory lexical search algorithms:

* **BM25 (Recommended):**
* Computes relevance using Term Frequency (TF) and Inverse Document Frequency (IDF) with document length normalization.


* **TF-IDF:**
* Vectorizes text chunks into a sparse matrix representation using `scikit-learn` or a custom implementation.



---

### 5. Persistence & Storage

* Save all precomputed index structures under `data/processed/`.


* Persist both the lexical index parameters (e.g., matrices, vocabulary, IDF arrays) and the chunk metadata list (`file_path`, `first_character_index`, `last_character_index`).


* Serialization can be handled using tools like `pickle` or `joblib`.

---

### Required CLI Command

Execution must run through `uv`, using `Python Fire` and `tqdm` progress bars:

```bash
uv run python -m src index --max_chunk_size 2000
```[cite: 1]

* **Performance Target:** Complete indexing of the entire codebase must take **under 5 minutes**[cite: 1].

```

إليك الشرح التفصيلي لـ **Indexing** (الفهرسة) باللغة العربية، وفقاً لمتطلبات مشروع **RAG against the machine**:

---

### 1. Ingestion / قراءة الملفات

* تقوم بمسح وقراءة جميع الملفات البرمجية والوثائق الموجودة داخل المسار `data/raw/vllm-0.10.1/`.


* **شرط صارم:** يجب أن يكون المسار (`file_path`) مطابقتً تماماً للمسار النسبي للملف داخل المجلد (مثال: `data/raw/vllm-0.10.1/docs/features/lora.md`). أي تغيير في هذا المسار أو استخدام مسار مطلق (Absolute Path) سيتسبب في حصولك على نقطة 0 في التقييم من طرف الـ Moulinette.



---

### 2. Chunking Strategies (تقطيع النصوص)

يتطلب المشروع تطبيق طريقتين للملفات:

1. **Python Code Chunking:**
* تقطيع كود بايثون بناءً على بنيته البرمجية (باستخدام مكتبة `ast` لتحديد الدوال `Functions` والفئات `Classes`) لضمان عدم قطع السياق البرمجي.


2. **Markdown / Text Chunking:**
* تقطيع وثائق Markdown بناءً على العناوين الرئيسيّة والفرعيّة (`#`, `##`, `###`) أو الفقرات.



#### **قيود عملية التقطيع (Chunking):**

* **الحجم الأقصى:** الخيار `--max_chunk_size` يحدد الحد الأقصى للحجم (القيمة الافتراضية هي 2000 حرف).


* **قاعدة صارمة:** أي قطعة (Chunk) يتجاوز حجمها 2000 حرف تجعل مخرجات المشروع بالكامل غير صالحة للتقييم لدى الـ Moulinette.


* **البيانات الوصفية (Metadata):** يجب الاحتفاظ مع كل قطعة بـ:
* `file_path` (مسار الملف)


* `first_character_index` (مؤشر بداية القطعة)


* `last_character_index` (مؤشر نهاية القطعة)





---

### 3. Preprocessing & Tokenization (معالجة النصوص)

تجهيز النص الخاص بكل قطعة للبناء:

* تحويل جميع النصوص إلى حروف صغيرة (Lowercase).
* **Tokenization:** تقسيم النصوص إلى كلمات أو رموز (Tokens).
* تنظيف النصوص (إزالة الكلمات الشائعة Stopwords أو تطبيق Stemming لتحسين دقة البحث).

---

### 4. بناء الفهرس (BM25 أو TF-IDF)

يجب تطبيق إحدى الخوارزميتين للبحث اللفظي (Lexical Search):

* **الخيار الأول: BM25 (الموصى به)**
* يحسب درجة التشابه بناءً على تكرار الكلمات (TF) وتكرارها العكسي في المستندات (IDF) مع تعديل طول القطع.


* **الخيار الثاني: TF-IDF**
* يحول القطع النصية إلى مصفوفة نادرة (Sparse Matrix) يسهل البحث فيها باستخدام مكتبات مثل `scikit-learn`.



---

### 5. حفظ الفهرس (Persistence)

* تخزين الفهرس الناتج داخل مجلد `data/processed/`.


* العناصر التي يتم حفظها:
* بيانات الفهرس (مصفوفات TF-IDF أو معاملة BM25).
* قائمة القطع (Chunks) مرفقة بالبيانات الوصفية (`file_path`, `first_character_index`, `last_character_index`).


* يمكن استخدام `pickle` أو `joblib` للتخزين في بايثون.

---

### الأمر البرمجي للتشغيل (CLI Command)

تُنفّذ العملية باستعمال `uv` مع واجهة `Python Fire` ومؤشر التقدم `tqdm`:

```bash
uv run python -m src index --max_chunk_size 2000
```[cite: 1]

* **الأداء:** يجب أن تستغرق عملية الفهرسة الشاملة **أقل من 5 دقائق**[cite: 1].

```