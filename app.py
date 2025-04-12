from flask import Flask, request, jsonify
from flask_cors import CORS
from src.incogen_exp.main import run
from src.incogen_exp.helpers import image_to_base64
import PIL

app = Flask(__name__)
CORS(app)  # Enable CORS if needed for frontend access

# API Route for testing connection
@app.route('/test-connection', methods=['GET'])
def test_connection():
    return jsonify({"message": "Server is up and running!"}), 200

# API Route to trigger CrewAI
@app.route('/run_crew', methods=['POST'])
def run_crew():
    try:
        data = request.json
        input_text = data.get("input_text", "")

        if not input_text:
            return jsonify({"message": "Missing input_text param"}), 400
        
        crewai_response = run(input_text=input_text)
        
        if crewai_response == "LIMIT_EXCEEDED":
            return jsonify({"message": "Ingredient Limit exceeded"}), 400
        elif isinstance(crewai_response, list) and all(isinstance(item, PIL.Image.Image) for item in crewai_response):
            poster = [image_to_base64(page) for page in crewai_response]
            return jsonify({"message": "API SUCCESS","res":poster}), 200
        
    except Exception as e:
        return jsonify({"message":"Some internal error occured!","error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)