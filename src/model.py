from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

from .cache import SimpleCache
from .embeddings import EmbeddingModel
from .validator import is_valid_output
from .logger import Logger
from .metrics import Metrics


class CAGModel:
    def __init__(self):
        # Core CAG components
        self.cache = SimpleCache()
        self.embed = EmbeddingModel()
        self.log = Logger()
        self.metrics = Metrics()

        # ✅ Instruction-tuned, local model
        self.tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
        self.model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")

        self.log.log("✅ CAG Model initialized with FLAN-T5 generator")

    # --------------------------------------------------
    # Semantic Cache Search
    # --------------------------------------------------
    def _semantic_search(self, prompt):
        prompt_emb = self.embed.encode(prompt)

        best_score = 0
        best_entry = None

        for entry in self.cache.get_all():
            score = self.embed.cosine_similarity(prompt_emb, entry["embedding"])
            if score > best_score:
                best_score = score
                best_entry = entry

        if best_score > 0.75:
            self.log.log(f"Semantic cache hit (score={best_score:.2f})")
            self.metrics.cache_hits += 1
            self.metrics.semantic_hits += 1
            return best_entry["value"]["response"]

        return None

    # --------------------------------------------------
    # FLAN-T5 Generation
    # --------------------------------------------------
    def _generate(self, prompt):
        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True
        )

        outputs = self.model.generate(
            **inputs,
            max_new_tokens=120,
            temperature=0.5,
            do_sample=True,
            repetition_penalty=1.4,
            no_repeat_ngram_size=4
        )

        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

    # --------------------------------------------------
    # Main CAG Pipeline
    # --------------------------------------------------
    def generate(self, prompt):
        self.metrics.total_requests += 1
        self.log.log(f"User prompt: {prompt}")

        # 1️⃣ Semantic cache lookup
        #cached = self._semantic_search(prompt)
        #if cached:
            #return cached

        # 2️⃣ Context injection (RAP-style)
        context = ""
        previous = self.cache.get_all()
        if previous:
            context = "Previously validated explanations:\n"
            for p in previous[:5]:
                context += f"- {p['value']['response']}\n"
            context += "\n"

        # ✅ STRONG PROMPT TO AVOID CIRCULAR DEFINITIONS
        final_prompt = (
            "You are an AI system that explains concepts to beginners.\n"
            "Give a clear, non-circular definition.\n"
            "Do NOT repeat the same word in the definition.\n\n"
            + context +
            "Question: " + prompt + "\n"
            "Answer:"
        )

        # 3️⃣ Generate response
        response = self._generate(final_prompt)

        # 4️⃣ Validation + Self-repair
        if not is_valid_output(response):
            self.metrics.repairs += 1
            self.log.log("Validation failed → self-repair invoked")
            response = self._generate(
                final_prompt + "\nRewrite the answer clearly."
            )
        else:
            self.metrics.valid_first_try += 1

        # 5️⃣ Save to cache
        embedding = self.embed.encode(prompt)
        self.cache.save(prompt, embedding, {"response": response})

        self.metrics.total_response_length += len(response)

        return response
