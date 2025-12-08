# Cache-Augmented Generation (CAG)

## Overview
Cache-Augmented Generation (CAG) is an optimization-focused alternative to Retrieval-Augmented Generation (RAG).  
Instead of retrieving external documents for every query, CAG reuses previously generated and validated responses using semantic similarity.

This project demonstrates a complete and reproducible CAG pipeline designed to reduce latency, improve efficiency, and support repeated-query scenarios.

---

## Key Features
- Semantic cache-based response reuse
- Instruction-tuned text generation using FLAN-T5
- Sentence embedding–based similarity matching
- Response validation with self-repair mechanism
- Metrics tracking (cache hits, repairs, response length)
- Lightweight Flask-based demo UI
- Fully offline and reproducible execution

---

## Architecture Summary
1. User query is embedded using sentence embeddings  
2. Semantic similarity search is performed on cached responses  
3. High-confidence cache hits are reused directly  
4. New responses are generated only when needed  
5. Validated responses are stored back into the cache  

CAG reduces computational overhead compared to traditional RAG systems that perform document retrieval at every query.

---

## Project Structure
CAG_Project/
│
├── src/
│ ├── model.py
│ ├── cache.py
│ ├── embeddings.py
│ ├── validator.py
│ ├── metrics.py
│ └── logger.py
│
├── ui/
│ ├── app.py
│ └── templates/
│ └── index.html
│
├── main.py
├── run_experiments.py
├── requirements.txt
└── README.md