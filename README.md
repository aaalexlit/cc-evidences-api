# cc-evidences-api

# Local development

1. Create a python3.10-based virtual environment
2. Switch to the created virtual env and install the dependencies
    ```bash
    pip install -r requirements.txt
    pip install $(spacy info en_core_web_sm --url)
    ```
3. Run the app by executing [evidence_api.py](evidence_api.py)
4. Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to see API specification