from src.model import CAGModel

model = CAGModel(model_name="gpt2")

# Test prompts
test_prompts = [
    "What is artificial intelligence?",
    "Explain AI.",
    "Where is AI used?",
    "What do you mean by machine learning?",
    "Explain deep learning.",
    "Tell me uses of AI.",
    "What is ML?",
    "Describe neural networks."
]

print("=== Running Experiments ===")

for p in test_prompts:
    print("\nPrompt:", p)
    output = model.generate(p)
    print("Output:", output)

print("\n=== Final Metrics ===")
print(model.metrics.report())
