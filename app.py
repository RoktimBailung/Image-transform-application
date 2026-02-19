import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt

import cv2
import numpy as np
import os
from flask import Flask, render_template, request, send_file, jsonify

app = Flask(__name__, static_folder='static')

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def generate_histogram(image_path, output_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    plt.figure()
    plt.hist(img.ravel(), bins=256, range=[0,256])
    plt.xlabel("Pixel Intensity")
    plt.ylabel("Frequency")
    plt.title("Histogram")
    plt.savefig(output_path)
    plt.close()


# ---------------- HOME ----------------
@app.route('/')
def home():
    return render_template('index.html')

# ---------------- HISTOGRAM ----------------
@app.route('/histogram', methods=['POST'])
def histogram():

    original_path = os.path.join(app.config['UPLOAD_FOLDER'], 'current.jpg')
    processed_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output.jpg')

    original_hist_path = os.path.join(app.config['UPLOAD_FOLDER'], 'original_hist.jpg')
    processed_hist_path = os.path.join(app.config['UPLOAD_FOLDER'], 'processed_hist.jpg')

    generate_histogram(original_path, original_hist_path)
    generate_histogram(processed_path, processed_hist_path)

    return jsonify({
        "original_hist": "/uploads/original_hist.jpg",
        "processed_hist": "/uploads/processed_hist.jpg"
    })


# ------------- SERVE UPLOADED FILES -------------
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))


# ------------- IMAGE UPLOAD -------------
@app.route('/upload', methods=['POST'])
def upload_image():
    file = request.files['image']

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'current.jpg')
    file.save(filepath)

    return jsonify({
        "image_url": "/uploads/current.jpg"
    })


# ------------- NEGATIVE -------------
@app.route('/negative', methods=['POST'])
def negative():
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'current.jpg')

    img = cv2.imread(filepath)
    negative_img = 255 - img

    output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output.jpg')
    cv2.imwrite(output_path, negative_img)

    return jsonify({
        "image_url": "/uploads/output.jpg"
    })


# ------------- LOG TRANSFORMATION -------------
@app.route('/log', methods=['POST'])
def log_transform():
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'current.jpg')

    img = cv2.imread(filepath)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    c = 255 / np.log(1 + np.max(img_gray))
    log_image = c * (np.log(img_gray + 1))
    log_image = np.array(log_image, dtype=np.uint8)

    output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output.jpg')
    cv2.imwrite(output_path, log_image)

    return jsonify({
        "image_url": "/uploads/output.jpg"
    })


# ------------- GAMMA TRANSFORMATION -------------
@app.route('/gamma', methods=['POST'])
def gamma_transform():
    gamma_value = float(request.form.get('gamma', 2.0))

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'current.jpg')

    img = cv2.imread(filepath)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    gamma_corrected = np.array(
        255 * (img_gray / 255) ** gamma_value,
        dtype=np.uint8
    )

    output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output.jpg')
    cv2.imwrite(output_path, gamma_corrected)

    return jsonify({
        "image_url": "/uploads/output.jpg"
    })


# ------------- THRESHOLD -------------
@app.route('/threshold', methods=['POST'])
def threshold_transform():
    threshold_value = int(request.form.get('threshold', 127))

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'current.jpg')

    img = cv2.imread(filepath)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    _, threshold_img = cv2.threshold(
        img_gray,
        threshold_value,
        255,
        cv2.THRESH_BINARY
    )

    output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output.jpg')
    cv2.imwrite(output_path, threshold_img)

    return jsonify({
        "image_url": "/uploads/output.jpg"
    })


# ------------- CONTRAST STRETCHING -------------
@app.route('/contrast', methods=['POST'])
def contrast_transform():
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'current.jpg')

    img = cv2.imread(filepath)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    r_min = np.min(img_gray)
    r_max = np.max(img_gray)

    contrast_img = (img_gray - r_min) * (255 / (r_max - r_min))
    contrast_img = np.array(contrast_img, dtype=np.uint8)

    output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output.jpg')
    cv2.imwrite(output_path, contrast_img)

    return jsonify({
        "image_url": "/uploads/output.jpg"
    })


# ------------- RUN SERVER -------------
if __name__ == "__main__":
    app.run()
