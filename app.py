from flask import Flask, request, jsonify
from flask_cors import CORS
from src.incogen_exp.main import run

app = Flask(__name__)
CORS(app)  # Enable CORS if needed for frontend access

# API Route to trigger CrewAI
@app.route('/run_crew', methods=['POST'])
def run_crew():
    try:
        data = request.json
        input_text = data.get("input_text", "")

        if not input_text:
            return jsonify({"error": "Missing input_text param"}), 400
        
        crewai_response = run(input_text=input_text)

        return jsonify({"result": "API SUCCESS","crewai_response":crewai_response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)