# Relevant Scientific Evidence Retrieval and Verification API for Climate impact related queries

## Overview

The API is created to perform scientific verification of claims
extracted from Climate Change related news articles in order to detect
potential inaccuracies of the latter.

### General workflow

```mermaid
flowchart TB
   subgraph client1 [Streamlit Client]
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
      E:::curAppNode --> R["Re-rank using citation metrics (Optional)"]
      R:::curAppNode --> VC[["Validate with Climate-BERT based model"]]
   end
   subgraph client2 [ Streamlit Client ]
      R ---> VM[["Validate with MultiVerS"]]
      VC:::curAppNode --> D["Display predictions"]
      VM --> D
   end
    style R stroke:#808080,stroke-width:2px,stroke-dasharray: 5 5
    style CR stroke:#808080,stroke-width:2px,stroke-dasharray: 5 5
    style IC stroke:#808080,stroke-width:2px,stroke-dasharray: 5 5
    style API fill:#E9EAE0,color:#E7625F
    classDef curAppNode fill:#F7BEC0,color:#C85250,stroke:#E7625F
    linkStyle 10,11 stroke:#F7BEC0,stroke-width:4px,color:#C85250,background-color:#F7BEC0
;

```

## Main functionality
**The API performs 2 main tasks**
- Evidence retrieval for given claim(s) under all `evidence` endpoints
- Evidence retrieval + verification for given claim(s) under all `vefify` endpoints
- Supplementary task of splitting text into sentences under `split` endpoint
to enable Chrome extension functioning

### Model for claim verification against retrieved evidence

[Climatebert-fact-checking model](https://huggingface.co/amandakonet/climatebert-fact-checking) 
available from huggingface

### Scientific evidences index and database
Please read [Evidence database creation](doc/db.md) section

### Split into sentences
[Spacy "en_core_web_sm" pipeline](https://spacy.io/models/en#en_core_web_sm)
is used for text segmentation task  
This model is the smallest and the fastest and according to spacy's 
[Accuracy Evaluation](https://spacy.io/models/en#en_core_web_sm-accuracy) has
the same metric values as the bigger CPU-optimized models

### API description
[Formal description of the API](doc/api.md)

## Local development and deployment
Please refer to the [Technical documentation](doc/tech.md)