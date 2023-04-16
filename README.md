# Relevant Scientific Evidence Retrieval and Verification API for Climate impact related queries

## Main concepts

The API is created to perform scientific verification of claims
extracted from Climate Change related news articles in order to detect
potential inaccuracies of the latter.

### General workflow

```mermaid
flowchart TB
   subgraph client1 [Client]
      A(Media Article text or URL) -->|Split into sentences| S1("Sentence 1")
      A -->|Split into sentences| S2("Sentence 2")
      A -->|Split into sentences| SN("...")
      S1 --> CR{"Climate related?\n (Optional)"}
      S2 --> CR
      SN --> CR
      CR -->|Yes| IC{"Is a claim? \n(Optional)"}
      CR --No --x N[ Ignore ]
      IC --No --x N1[Ignore]
   end
   subgraph API
      IC -- Yes ---> E["Retrieve Top k most similar evidences"]
      E --> R["Re-rank using citation metrics (Optional)"]
      R --> VC[["Validate with Climate-BERT based model"]]
   end
   subgraph client2 [ Client ]
      R ---> VM[["Validate with MultiVerS"]]
      VC --> D["Display predictions"]
      VM --> D
   end
    style R stroke:#808080,stroke-width:2px,stroke-dasharray: 5 5
    style CR stroke:#808080,stroke-width:2px,stroke-dasharray: 5 5
    style IC stroke:#808080,stroke-width:2px,stroke-dasharray: 5 5

```

### Main functionality
**The API performs 2 main tasks**
- Evidence retrieval for given claim(s) under all `evidence` endpoints
- Evidence retrieval + verification for given claim(s) under all `vefify` endpoints
- Supplementary task of splitting text into sentences under `split` endpoint
to enable Chrome extension functioning

#### Model for claim verification against retrieved evidence

### Scientific evidences index and database
Please read [Evidence database creation](doc/db.md) section

### API description
[Formal description of the API](doc/api.md)

## Local development

1. Create a python3.10-based virtual environment
2. Download SQLight dbs with metadata and FAISS indices from Google Drive
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