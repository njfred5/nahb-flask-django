from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/health")
def health():
    return jsonify({"status": "ok", "message": "my flask API is running"})

if __name__ == "__main__":
    app.run(debug=True)
