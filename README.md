# 👁️LenSight: Multimodal Deepfake & Misinformation Scanner

LenSight is an advanced 3-Tier web application designed to detect AI-manipulated media and textual misinformation. By combining visual artifact detection (CNN/Vision models) with textual sentiment analysis (BERT) and live web cross-referencing, it provides digital security professionals and journalists with a comprehensive truth-probability report.

#Core Features
Multimodal Fusion Analysis:** Evaluates both image anomalies and textual claims simultaneously or independently.
Live Web Fact-Checking:** Automatically queries the DuckDuckGo API to cross-reference suspicious claims with live internet headlines.
Visual Analysis Map:** Generates a simulated activation map overlay to visually guide users toward irregular pixel clusters.
Persistent Data Layer:** Utilises an integrated SQLite database to securely log and timestamp all analysis reports.
Researcher Mode Telemetry:** Provides advanced users with raw model JSON outputs and strict file-size security checks.

#Setup and Run Instructions

#1. Install Dependencies
Ensure you have Python 3.8+ installed. Open your terminal and run:
```bash
pip install fastapi uvicorn streamlit python-multipart transformers torch torchvision pillow duckduckgo-search
