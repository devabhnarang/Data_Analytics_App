from flask import Flask, render_template, request
import pandas as pd
from analysis import analyze_any_data

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            file = request.files["file"]

            if not file:
                return render_template("upload.html", error="No file uploaded")

            if file.filename.endswith(".csv"):
                df = pd.read_csv(file)
            else:
                df = pd.read_excel(file)

            results = analyze_any_data(df)
            return render_template("dashboard.html", results=results)

        except Exception as e:
            return render_template("upload.html", error=f"Error analyzing file: {e}")

    return render_template("upload.html")




if __name__ == "__main__":
    app.run(debug=True)
