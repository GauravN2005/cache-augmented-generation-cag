from src.model import CAGModel

# Choose a small model for demo
model = CAGModel(model_name="gpt2")

print("=== CAG DEMO STARTED ===")
while True:
    prompt = input("\nEnter your prompt: ")

    if prompt.lower() == "exit":
        break

    output = model.generate(prompt)
    print("\n🟦 Response:\n", output)
