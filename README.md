#LenSight: Multimodal Misinformation Detection MVP

#What the software does
LenSight is a localised, multimodal AI prototype designed to detect and flag digital misinformation. It analyses uploaded text for sensationalism and evaluates images for deepfake/manipulation artifacts, providing a unified confidence score and live internet telemetry to verify journalistic claims.

#Core Features Implemented
1. **Dual-Stream Analysis:** Processes text (NLP) and imagery (CNN) simultaneously.
2. **Custom Vision Model:** Utilizes a localised Vision Transformer (ViT) fine-tuned on a subset of the FaceForensics++ dataset to detect structural facial manipulations.
3. **Textual NLP Pipeline:** Uses a fine-tuned BERT model to detect linguistic patterns associated with fake news and clickbait.
4. **Live Web Telemetry:** Integrates DuckDuckGo API to cross-reference textual claims with live news headlines.
5. **Database Logging:** Automatically logs all scan results, user inputs, and confidence scores to a local SQLite database (`lensight.db`) for auditability.
6. **Interactive UI:** A decoupled frontend built with Streamlit, communicating via REST API with a FastAPI backend.

#Setup and Run Instructions
1. Ensure Python 3.9+ is installed on your machine.
2. Clone or extract the project folder to your local directory.
3. Open a terminal in the root directory and install dependencies:
   `pip install -r requirements.txt`
4. **Start the Backend:** Open a terminal and run:
   `python -m uvicorn main:app --reload`
5. **Start the Frontend:** Open a second terminal in the same directory and run:
   `python -m streamlit run app.py`
6. The UI will automatically open in your default web browser at `http://localhost:8501`.

#Sample Inputs for Testing
**Text Test (REAL):** > "WASHINGTON (Reuters) - The United States Senate passed a bipartisan infrastructure bill on Thursday, allocating funds for highway repair and broadband expansion across several states."

**Text Test (FAKE):**
> "Secret government whistleblowers have just revealed a shocking hidden plot to ban all private vehicles by next year!"

**Image Test (FAKE):** Upload any standard FaceSwap image (e.g., a face digitally superimposed onto another body). 

#Known Limitations
1. **Out-of-Distribution (OOD) Generative Images:** The local ViT was trained strictly on FaceForensics++ (manipulation/FaceSwap artifacts). It is highly accurate at detecting localised pixel warping but may misclassify entirely synthetic, from-scratch generations (like StyleGAN2 / thispersondoesnotexist.com) as "REAL" due to the lack of blending artifacts.
2. **NLP Overfitting:** The lightweight BERT model is highly sensitive to punctuation and lack of professional formatting. Unformatted text without traditional news datelines may occasionally trigger false-positive "FAKE" flags.
