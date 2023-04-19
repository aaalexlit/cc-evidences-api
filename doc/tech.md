## Local development

1. Create a python3.10-based virtual environment
2. Download SQLight dbs with metadata and FAISS indices from Google Drive
to the corresponding folders
   ```shell
   
   ```
1. Switch to the created virtual env and install the dependencies
    ```bash
    pip install -r requirements.txt
    pip install $(spacy info en_core_web_sm --url)
    ```
1. Run the app by executing [evidence_api.py](evidence_api.py)
1. Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to see API specification

## Generate Markdown from OpenAPI schema

[api.md](doc/api.md) is generated from [openapi.json](doc/openapi.json) using
[widdershins](https://mermade.github.io/widdershins/ConvertingFilesBasicCLI.html)
the following way
```shell
widdershins --language_tabs 'python:Python' 'shell:Shell' 'javascript:Javascript' --summary -o doc/api.md doc/openapi.json
```