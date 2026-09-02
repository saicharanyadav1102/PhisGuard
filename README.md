# PhishGuard 🛡️

A privacy-preserving, real-time phishing detection system that uses client-side behavioral analysis and a Random Forest machine learning model to neutralize zero-day threats. 

Unlike traditional security tools that rely on static URL blacklists, PhishGuard monitors **how a website behaves** (e.g., hidden overlays, redirection chains, iframe ratios) to catch malicious sites before they are ever reported.

## 🚀 Key Features
- **Zero-Day Threat Detection:** Identifies phishing sites based on behavior rather than relying on outdated domain blacklists.
- **Privacy-by-Design:** Extracts behavioral features locally in your browser. Your raw browsing history and URLs never leave your machine.
- **Ultra-Low Latency:** Uses a lightweight Random Forest classifier to achieve <150ms inference times, ensuring a seamless browsing experience.
- **Visual Threat Blocking:** Instantly injects a high-contrast red warning overlay into the DOM to physically prevent interaction with dangerous sites.

## 🧠 System Architecture
The system is fully decoupled into two main components:
1. **The "Front Guard" (Browser Extension):** A Manifest V3 JavaScript extension that tracks HTTP redirection hops and inspects the structural DOM for clickjacking anomalies (Region of Interest tracking).
2. **The "Decision Engine" (Flask Backend):** A Python REST API utilizing `scikit-learn`. It receives anonymized feature vectors and returns a probability confidence score.

## 🛠️ Installation & Setup

### 1. Start the Inference Server (Backend)
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Generate the dataset and train the Machine Learning model:
   ```bash
   python generate_dataset.py
   python train_model.py
   ```
4. Start the Flask API:
   ```bash
   python app.py
   ```
   *(The server will start listening on `http://127.0.0.1:5000`)*

### 2. Install the Browser Extension (Frontend)
1. Open Google Chrome or Microsoft Edge.
2. Navigate to `chrome://extensions/` (or `edge://extensions/`).
3. Toggle **Developer mode** ON (usually in the top right corner).
4. Click **Load unpacked** and select the `extension` folder from this repository.
5. **Crucial:** Click "Details" on the PhishGuard extension card and enable **"Allow access to file URLs"** if you intend to test it on local `.html` files.

## 💻 Tech Stack
- **Machine Learning:** Python, Scikit-Learn, Pandas, NumPy, Joblib
- **Backend API:** Flask, Flask-CORS
- **Client-Side Agent:** JavaScript (Manifest V3 WebExtensions API), HTML5, CSS3
