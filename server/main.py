# import os
# from flask import Flask
# from flask_cors import CORS
# from config import UPLOAD_FOLDER, PROCESSED_FOLDER, MAX_CONTENT_LENGTH
# from routes.api import api_bp
# from routes.image import image_bp
# from routes.test import test_bp
#
# app = Flask(__name__)
# CORS(app)
#
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER
# app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
#
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# os.makedirs(PROCESSED_FOLDER, exist_ok=True)
#
# # 注册蓝图
# app.register_blueprint(api_bp)
# app.register_blueprint(image_bp)
# app.register_blueprint(test_bp)
#
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)



import os
import uuid
import subprocess
import json  # ✨ 1. Import the json library to handle JSON data
from flask import Flask, request, jsonify, send_file, url_for
from werkzeug.utils import secure_filename
from flask_cors import CORS
import time
from PIL import Image

app = Flask(__name__)
CORS(app)

# ===== Configuration Settings (Your paths are preserved) =====
UPLOAD_FOLDER = './uploads'
PROCESSED_FOLDER = './processed'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
BASE_URL = "http://localhost:5000"

# --- IMPORTANT: Update these paths to match YOUR system ---
# ✨ Using a separate variable for the model directory for clarity
MODEL_DIR = "D:\\a666\\rgzn_gcsj\\SR_UNET2\\output"
SCRIPT_PATH = "D:\\a666\\rgzn_gcsj\\SR_UNET2\\main.py"
PYTHON_PATH = "D:\\a666\\rgzn_gcsj\\SR_UNET2\\.venv\\Scripts\\python.exe"

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

# ===== Directory Creation (Preserved) =====
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)


def allowed_file(filename):
    """Checks if the file extension is allowed."""
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_image_url(filename, folder):
    """Gets the public URL for an image."""
    return url_for('get_image', folder=folder, filename=filename, _external=True)


# ✨ 2. The processing function is rewritten to accept and use the new metadata.
def process_image_with_params(input_path, metadata):
    """
    Calls the main.py inference script using parameters from the frontend metadata.
    """
    try:
        output_dir = app.config['PROCESSED_FOLDER']

        # --- Extract parameters from metadata with safe defaults ---
        # This prevents errors if a parameter is missing from the JSON
        params = metadata.get('advancedParams', {})
        scale = params.get('scale', 4)
        base_channels = params.get('baseChannels', 64)
        bilinear = params.get('bilinear', False)

        # Get the selected model from the metadata
        model_filename = metadata.get('model', 'unet_best.pth')  # Default model
        model_path = os.path.join(MODEL_DIR, model_filename)

        if not os.path.exists(model_path):
            print(f"Error: Model file not found at {model_path}")
            return None, 0

        # Dynamically build the command based on the received parameters
        cmd = [
            PYTHON_PATH, SCRIPT_PATH,
            "infer",
            "--checkpoint", model_path,
            "--lr", input_path,
            "--output_dir", output_dir,
            "--lr_scale", str(scale),
            "--base_channels", str(base_channels),
        ]

        # Add boolean flags like '--bilinear' only if they are true in the metadata
        if bilinear:
            cmd.append("--bilinear")

        # You can add more logic here to handle the 'steps' or 'prompt' if your main.py supports them
        print(f"Frontend prompt received: {metadata.get('prompt', 'N/A')}")
        print(f"Enabled steps: {metadata.get('steps', {})}")

        print(f"Executing command: {' '.join(cmd)}")
        start_time = time.time()

        # Run the subprocess and check for errors
        result = subprocess.run(
            cmd,
            capture_output=True,  # Capture stdout and stderr
            text=True,
            check=True  # This will raise a CalledProcessError if the script returns a non-zero exit code
        )
        duration = time.time() - start_time

        print(f"Inference successful (Duration: {duration:.2f}s)")
        print(f"Script stdout: {result.stdout}")

        # Find the generated output file
        # The output filename format depends on your main.py script
        input_filename_base = os.path.splitext(os.path.basename(input_path))[0]
        expected_output_filename = f"{input_filename_base}_SR.png"
        processed_path = os.path.join(output_dir, expected_output_filename)

        if not os.path.exists(processed_path):
            print(f"Error: Expected output file was not found at {processed_path}")
            # You could add logic here to find any other generated file if needed
            return None, 0

        return expected_output_filename, duration

    except subprocess.CalledProcessError as e:
        # This catches errors from the script itself (non-zero exit code)
        print(f"Error during script execution. Return code: {e.returncode}")
        print(f"Stderr: {e.stderr}")
        print(f"Stdout: {e.stdout}")
        return None, 0
    except Exception as e:
        # This catches other errors (e.g., file not found)
        print(f"An unexpected error occurred in process_image_with_params: {str(e)}")
        return None, 0


# This function is preserved from your original code.
def resize_image(image_path, max_size=1024):
    """Resizes an image if it's too large."""
    try:
        with Image.open(image_path) as img:
            w, h = img.size
            if w > max_size or h > max_size:
                ratio = min(max_size / w, max_size / h)
                new_size = (int(w * ratio), int(h * ratio))
                resample_method = Image.Resampling.LANCZOS if hasattr(Image, 'Resampling') else Image.ANTIALIAS
                img = img.resize(new_size, resample_method)
                img.save(image_path)
                print(f"Resized image: {image_path} to {img.size}")
    except Exception as e:
        print(f"Failed to resize image: {str(e)}")


@app.route('/process-image', methods=['POST'])
def process_image_api():
    """
    API endpoint that now handles both the file and the JSON metadata.
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    if 'metadata' not in request.form:
        return jsonify({'error': 'No metadata part in the request'}), 400

    file = request.files['file']
    metadata_str = request.form['metadata']

    try:
        metadata = json.loads(metadata_str)
        # ==================== START: MODIFIED/ADDED CODE ====================

        # ✨ 1. Log received data to console and file
        print("--- Logging Frontend Data ---")
        print(f"Received Image Filename: {file.filename}")
        # Use json.dumps for pretty-printing the dictionary to the console
        print(f"Received Metadata JSON: {json.dumps(metadata, indent=2, ensure_ascii=False)}")

        # Save the metadata to log.json in the project's root directory
        log_file_path = 'log.json'
        try:
            # Use 'w' mode to overwrite the file on each request, and utf-8 for proper encoding
            with open(log_file_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, ensure_ascii=False, indent=4)
            print(f"Successfully saved metadata to {log_file_path}")
        except Exception as e:
            print(f"Error saving metadata to log file: {e}")

        print("-----------------------------")

        # ===================== END: MODIFIED/ADDED CODE =====================

    except json.JSONDecodeError:
        return jsonify({'error': 'Invalid JSON format in metadata field'}), 400

    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'error': 'No selected file or file type not allowed'}), 400

    try:
        unique_id = uuid.uuid4().hex
        file_ext = os.path.splitext(secure_filename(file.filename))[1]
        unique_filename = f"{unique_id}{file_ext}"

        input_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(input_path)
        print(f"Saved uploaded file to: {input_path}")

        resize_image(input_path, max_size=2048)

        output_filename, duration = process_image_with_params(input_path, metadata)

        if not output_filename:
            return jsonify({'error': 'Image processing failed on the server. Check logs for details.'}), 500

        return jsonify({
            'status': 'success',
            'processing_time': f"{duration:.2f}秒",
            'original_image_url': get_image_url(unique_filename, "uploads"),
            'processed_image_url': get_image_url(output_filename, "processed")
        })

    except Exception as e:
        import traceback
        print(f"An error occurred in the /process-image endpoint: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': f'An internal server error occurred: {str(e)}'}), 500
# def process_image_api():
#     """
#     API endpoint that now handles both the file and the JSON metadata.
#     """
#     # ✨ 3. Check for both 'file' and the new 'metadata' field in the form data
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file part in the request'}), 400
#     if 'metadata' not in request.form:
#         return jsonify({'error': 'No metadata part in the request'}), 400
#
#     file = request.files['file']
#     metadata_str = request.form['metadata']
#
#     # Safely parse the JSON string from the form data
#     try:
#         metadata = json.loads(metadata_str)
#         print(f"Received metadata from frontend: {metadata}")
#     except json.JSONDecodeError:
#         return jsonify({'error': 'Invalid JSON format in metadata field'}), 400
#
#     if file.filename == '' or not allowed_file(file.filename):
#         return jsonify({'error': 'No selected file or file type not allowed'}), 400
#
#     try:
#         # Use a more robust unique filename to avoid collisions
#         unique_id = uuid.uuid4().hex
#         file_ext = os.path.splitext(secure_filename(file.filename))[1]
#         unique_filename = f"{unique_id}{file_ext}"
#
#         input_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
#         file.save(input_path)
#         print(f"Saved uploaded file to: {input_path}")
#
#         resize_image(input_path, max_size=2048)  # Your resize function is preserved
#
#         # ✨ 4. Call the new processing function with the file path AND the parsed metadata
#         output_filename, duration = process_image_with_params(input_path, metadata)
#
#         if not output_filename:
#             return jsonify({'error': 'Image processing failed on the server. Check logs for details.'}), 500
#
#         # Return a success response with the image URLs
#         return jsonify({
#             'status': 'success',
#             'processing_time': f"{duration:.2f}秒",
#             'original_image_url': get_image_url(unique_filename, "uploads"),
#             'processed_image_url': get_image_url(output_filename, "processed")
#         })
#
#     except Exception as e:
#         import traceback
#         print(f"An error occurred in the /process-image endpoint: {str(e)}")
#         print(traceback.format_exc())
#         return jsonify({'error': f'An internal server error occurred: {str(e)}'}), 500


@app.route('/image/<folder>/<filename>')
def get_image(folder, filename):
    """Serves an image from the 'uploads' or 'processed' directory."""
    if folder not in ['uploads', 'processed']:
        return "Invalid folder specified", 404

    directory = app.config['UPLOAD_FOLDER'] if folder == 'uploads' else app.config['PROCESSED_FOLDER']

    try:
        return send_file(os.path.join(directory, filename))
    except FileNotFoundError:
        return "File not found", 404


@app.route('/hello', methods=['GET'])
def testapi():
    """A simple test endpoint to confirm the API is running."""
    app.logger.info('Received /hello request')
    return jsonify({"message": "API service is running"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)