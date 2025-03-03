import replicate
import os
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Get API key from environment variables
REPLICATE_API_KEY = os.getenv("REPLICATE_API_KEY")

# Initialize Replicate client
client = replicate.Client(api_token=REPLICATE_API_KEY)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_image():
    data = request.json
    prompt = data.get("prompt", "")

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    try:
        # Use Stable Diffusion model on Replicate
        model = client.models.get("stability-ai/sdxl")


        # Get the latest version
        version = model.versions.list()[0]  # Get the latest version dynamically

        # Generate image using `.run()`
        output = client.run(
            version,
            input={"prompt": prompt}
        )

        # Get the image URL from the output
        if output and isinstance(output, list):
            image_url = output[0]  # First image in response
            return jsonify({"image_url": image_url})
        else:
            return jsonify({"error": "Failed to generate image"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
