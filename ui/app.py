from flask import Flask, render_template, request
import sys
import os

# Allow importing src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.model import CAGModel

app = Flask(__name__)

# ✅ No model_name argument
model = CAGModel()

@app.route("/", methods=["GET", "POST"])
def home():
    response = ""
    if request.method == "POST":
        prompt = request.form.get("prompt")
        response = model.generate(prompt)
    return render_template("index.html", response=response)

if __name__ == "__main__":
    app.run(debug=True)
