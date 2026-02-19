let currentImageUploaded = false;

/* ===================== UTILITIES ===================== */

function cacheBust(url) {
    return url + "?t=" + Date.now();
}

function requireUpload() {
    if (!currentImageUploaded) {
        alert("Upload an image first.");
        return false;
    }
    return true;
}

/* ===================== UPLOAD IMAGE ===================== */

function uploadImage() {
    const input = document.getElementById("imageInput");
    const file = input.files[0];

    if (!file) {
        alert("Please select an image first.");
        return;
    }

    const formData = new FormData();
    formData.append("image", file);

    fetch("/upload", {
        method: "POST",
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("originalImage").src = data.image_url;
        document.getElementById("processedImage").src = data.image_url;
        currentImageUploaded = true;
        updateHistogram();
    })
    .catch(err => console.error("Upload error:", err));
}

/* ===================== GENERIC TRANSFORM ===================== */

function applyTransform(type) {
    if (!requireUpload()) return;

    fetch("/" + type, { method: "POST" })
        .then(res => res.json())
        .then(data => {
            document.getElementById("processedImage").src =
                cacheBust(data.image_url);
            updateHistogram();
        })
        .catch(err => console.error("Transform error:", err));
}

/* ===================== GAMMA ===================== */

function applyGamma() {
    if (!requireUpload()) return;

    const gammaValue = document.getElementById("gammaSlider").value;

    const formData = new FormData();
    formData.append("gamma", gammaValue);

    fetch("/gamma", {
        method: "POST",
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("processedImage").src =
            cacheBust(data.image_url);
        updateHistogram();
    })
    .catch(err => console.error("Gamma error:", err));
}

/* ===================== THRESHOLD ===================== */

function applyThreshold() {
    if (!requireUpload()) return;

    const thresholdValue = document.getElementById("thresholdSlider").value;

    const formData = new FormData();
    formData.append("threshold", thresholdValue);

    fetch("/threshold", {
        method: "POST",
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("processedImage").src =
            cacheBust(data.image_url);
        updateHistogram();
    })
    .catch(err => console.error("Threshold error:", err));
}

/* ===================== HISTOGRAM ===================== */

function updateHistogram() {
    fetch("/histogram", { method: "POST" })
        .then(res => res.json())
        .then(data => {
            document.getElementById("originalHistogram").src =
                cacheBust(data.original_hist);
            document.getElementById("processedHistogram").src =
                cacheBust(data.processed_hist);
        })
        .catch(err => console.error("Histogram error:", err));
}

/* ===================== DOWNLOAD IMAGE ===================== */

function downloadImage() {
    const processedImg = document.getElementById("processedImage").src;

    if (!processedImg) {
        alert("No processed image available.");
        return;
    }

    const link = document.createElement("a");
    link.href = processedImg;
    link.download = "processed_image.jpg";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

/* ===================== RESET IMAGE ===================== */

function resetImage() {
    if (!requireUpload()) return;

    const originalSrc = document.getElementById("originalImage").src;
    document.getElementById("processedImage").src =
        cacheBust(originalSrc);

    updateHistogram();
}

/* ===================== DARK MODE ===================== */

document.addEventListener("DOMContentLoaded", function () {

    const themeButton = document.getElementById("themeButton");

    if (!themeButton) return;

    // Load saved theme
    if (localStorage.getItem("theme") === "dark") {
        document.body.classList.add("dark-mode");
        themeButton.textContent = "☀";
    }

    themeButton.addEventListener("click", function () {

        document.body.classList.toggle("dark-mode");

        if (document.body.classList.contains("dark-mode")) {
            themeButton.textContent = "☀";
            localStorage.setItem("theme", "dark");
        } else {
            themeButton.textContent = "🌙";
            localStorage.setItem("theme", "light");
        }
    });

    /* ===================== SLIDER LIVE VALUES ===================== */

    const gammaSlider = document.getElementById("gammaSlider");
    const thresholdSlider = document.getElementById("thresholdSlider");

    if (gammaSlider) {
        gammaSlider.oninput = function () {
            document.getElementById("gammaValue").innerText = this.value;
        };
    }

    if (thresholdSlider) {
        thresholdSlider.oninput = function () {
            document.getElementById("thresholdValue").innerText = this.value;
        };
    }

});
