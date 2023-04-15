---
title: Evidence retrieval v0.1.0
language_tabs:
  - python: Python
  - shell: Shell
  - javascript: Javascript
language_clients:
  - python: ""
  - shell: ""
  - javascript: ""
toc_footers: []
includes: []
search: true
highlight_theme: darkula
headingLevel: 2

---

<!-- Generator: Widdershins v4.0.1 -->

<h1 id="evidence-retrieval">Evidence retrieval v0.1.0</h1>

> Scroll down for code samples, example requests and responses. Select a language for code samples from the tabs above or the mobile navigation menu.

<h1 id="evidence-retrieval-default">Default</h1>

## Get Evidences

<a id="opIdget_evidences_api_phrase_evidence_batch_post"></a>

> Code samples

```python
import requests
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json'
}

r = requests.post('/api/phrase/evidence/batch', headers = headers)

print(r.json())

```

```shell
# You can also use wget
curl -X POST /api/phrase/evidence/batch \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json'

```

```javascript
const inputBody = '{
  "claims": [
    "CO2 is not the cause of our current warming trend.",
    "Natural variation explains a substantial part of global warming observed since 1850"
  ],
  "threshold": 0.6,
  "top_k": 10
}';
const headers = {
  'Content-Type':'application/json',
  'Accept':'application/json'
};

fetch('/api/phrase/evidence/batch',
{
  method: 'POST',
  body: inputBody,
  headers: headers
})
.then(function(res) {
    return res.json();
}).then(function(body) {
    console.log(body);
});

```

`POST /api/phrase/evidence/batch`

Get top_k relevant evidence phrases from scientific articles

> Body parameter

```json
{
  "claims": [
    "CO2 is not the cause of our current warming trend.",
    "Natural variation explains a substantial part of global warming observed since 1850"
  ],
  "threshold": 0.6,
  "top_k": 10
}
```

<h3 id="get-evidences-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|re_rank|query|boolean|false|none|
|body|body|[Claims](#schemaclaims)|true|none|

> Example responses

> 200 Response

```json
[
  [
    {
      "num": 0,
      "title": "string",
      "text": "string",
      "similarity": 0,
      "doi": "string",
      "openalex_id": "string",
      "year": 0,
      "citation_count": 0,
      "influential_citation_count": 0
    }
  ]
]
```

<h3 id="get-evidences-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<h3 id="get-evidences-responseschema">Response Schema</h3>

Status Code **200**

*Response Get Evidences Api Phrase Evidence Batch Post*

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|Response Get Evidences Api Phrase Evidence Batch Post|[array]|false|none|none|
|» EvidenceOutput|[EvidenceOutput](#schemaevidenceoutput)|false|none|none|
|»» num|integer|true|none|none|
|»» title|string|true|none|none|
|»» text|string|true|none|none|
|»» similarity|number|false|none|none|
|»» doi|string|false|none|none|
|»» openalex_id|string|false|none|none|
|»» year|integer|false|none|none|
|»» citation_count|integer|false|none|none|
|»» influential_citation_count|integer|false|none|none|

<aside class="success">
This operation does not require authentication
</aside>

## Verify

<a id="opIdverify_api_abstract_verify_batch_post"></a>

> Code samples

```python
import requests
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json'
}

r = requests.post('/api/abstract/verify/batch', headers = headers)

print(r.json())

```

```shell
# You can also use wget
curl -X POST /api/abstract/verify/batch \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json'

```

```javascript
const inputBody = '{
  "claims": [
    "CO2 is not the cause of our current warming trend.",
    "Natural variation explains a substantial part of global warming observed since 1850"
  ],
  "threshold": 0.6,
  "top_k": 10
}';
const headers = {
  'Content-Type':'application/json',
  'Accept':'application/json'
};

fetch('/api/abstract/verify/batch',
{
  method: 'POST',
  body: inputBody,
  headers: headers
})
.then(function(res) {
    return res.json();
}).then(function(body) {
    console.log(body);
});

```

`POST /api/abstract/verify/batch`

Verify claim against phrases extracted from scientific paper abstracts

> Body parameter

```json
{
  "claims": [
    "CO2 is not the cause of our current warming trend.",
    "Natural variation explains a substantial part of global warming observed since 1850"
  ],
  "threshold": 0.6,
  "top_k": 10
}
```

<h3 id="verify-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|include_title|query|boolean|false|none|
|re_rank|query|boolean|false|none|
|filter_nei|query|boolean|false|none|
|body|body|[Claims](#schemaclaims)|true|none|

> Example responses

> 200 Response

```json
[
  [
    {
      "num": 0,
      "title": "string",
      "text": "string",
      "similarity": 0,
      "doi": "string",
      "openalex_id": "string",
      "year": 0,
      "citation_count": 0,
      "influential_citation_count": 0,
      "label": "SUPPORTS",
      "probability": 0
    }
  ]
]
```

<h3 id="verify-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<h3 id="verify-responseschema">Response Schema</h3>

Status Code **200**

*Response Verify Api Abstract Verify Batch Post*

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|Response Verify Api Abstract Verify Batch Post|[array]|false|none|none|
|» VerifiedEvidenceOutput|[VerifiedEvidenceOutput](#schemaverifiedevidenceoutput)|false|none|none|
|»» num|integer|true|none|none|
|»» title|string|true|none|none|
|»» text|string|true|none|none|
|»» similarity|number|false|none|none|
|»» doi|string|false|none|none|
|»» openalex_id|string|false|none|none|
|»» year|integer|false|none|none|
|»» citation_count|integer|false|none|none|
|»» influential_citation_count|integer|false|none|none|
|»» label|string|true|none|none|
|»» probability|number|true|none|none|

#### Enumerated Values

|Property|Value|
|---|---|
|label|SUPPORTS|
|label|REFUTES|
|label|NOT_ENOUGH_INFO|

<aside class="success">
This operation does not require authentication
</aside>

## Split

<a id="opIdsplit_api_split_post"></a>

> Code samples

```python
import requests
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json'
}

r = requests.post('/api/split', headers = headers)

print(r.json())

```

```shell
# You can also use wget
curl -X POST /api/split \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json'

```

```javascript
const inputBody = '{
  "text": "There is no climate emergency. OPINION: The science and data strongly support that our planet’s ecosystems are thriving and that humanity is benefiting from modestly increasing temperature and an increase in carbon dioxide. These facts refute the claim that Earth is spiraling into one man-made climate catastrophe after another. Carbon dioxide (CO2) is portrayed as a demon molecule fueling run-away greenhouse warming. If you get your news only from mainstream media, you would likely believe that CO2 levels are dangerously high and unprecedented. You would be wrong. Concentrations of this gas are slightly less than 420 parts-per-million (ppm), or one-sixth the average historic levels of 2,600 ppm for the last 600 million years. Increases in carbon dioxide in the last 150 years, largely from the burning of fossil fuels, have reversed a dangerous downward trend in the gas’ concentration. During the last glacial period, concentrations nearly reached the “line of death” at 150 parts per million, below which plants die. Viewed in the long-term geologic context, we are actually CO2 impoverished."
}';
const headers = {
  'Content-Type':'application/json',
  'Accept':'application/json'
};

fetch('/api/split',
{
  method: 'POST',
  body: inputBody,
  headers: headers
})
.then(function(res) {
    return res.json();
}).then(function(body) {
    console.log(body);
});

```

`POST /api/split`

> Body parameter

```json
{
  "text": "There is no climate emergency. OPINION: The science and data strongly support that our planet’s ecosystems are thriving and that humanity is benefiting from modestly increasing temperature and an increase in carbon dioxide. These facts refute the claim that Earth is spiraling into one man-made climate catastrophe after another. Carbon dioxide (CO2) is portrayed as a demon molecule fueling run-away greenhouse warming. If you get your news only from mainstream media, you would likely believe that CO2 levels are dangerously high and unprecedented. You would be wrong. Concentrations of this gas are slightly less than 420 parts-per-million (ppm), or one-sixth the average historic levels of 2,600 ppm for the last 600 million years. Increases in carbon dioxide in the last 150 years, largely from the burning of fossil fuels, have reversed a dangerous downward trend in the gas’ concentration. During the last glacial period, concentrations nearly reached the “line of death” at 150 parts per million, below which plants die. Viewed in the long-term geologic context, we are actually CO2 impoverished."
}
```

<h3 id="split-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[TextToSplit](#schematexttosplit)|true|none|

> Example responses

> 200 Response

```json
[
  "string"
]
```

<h3 id="split-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<h3 id="split-responseschema">Response Schema</h3>

Status Code **200**

*Response Split Api Split Post*

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|Response Split Api Split Post|[string]|false|none|none|

<aside class="success">
This operation does not require authentication
</aside>

## Healthcheck

<a id="opIdhealthcheck_healthcheck_get"></a>

> Code samples

```python
import requests
headers = {
  'Accept': 'application/json'
}

r = requests.get('/healthcheck', headers = headers)

print(r.json())

```

```shell
# You can also use wget
curl -X GET /healthcheck \
  -H 'Accept: application/json'

```

```javascript

const headers = {
  'Accept':'application/json'
};

fetch('/healthcheck',
{
  method: 'GET',

  headers: headers
})
.then(function(res) {
    return res.json();
}).then(function(body) {
    console.log(body);
});

```

`GET /healthcheck`

> Example responses

> 200 Response

```json
"string"
```

<h3 id="healthcheck-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|string|

<aside class="success">
This operation does not require authentication
</aside>

## Readme

<a id="opIdreadme__get"></a>

> Code samples

```python
import requests
headers = {
  'Accept': 'application/json'
}

r = requests.get('/', headers = headers)

print(r.json())

```

```shell
# You can also use wget
curl -X GET / \
  -H 'Accept: application/json'

```

```javascript

const headers = {
  'Accept':'application/json'
};

fetch('/',
{
  method: 'GET',

  headers: headers
})
.then(function(res) {
    return res.json();
}).then(function(body) {
    console.log(body);
});

```

`GET /`

> Example responses

> 200 Response

```json
"string"
```

<h3 id="readme-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|string|

<aside class="success">
This operation does not require authentication
</aside>

# Schemas

<h2 id="tocS_Claim">Claim</h2>
<!-- backwards compatibility -->
<a id="schemaclaim"></a>
<a id="schema_Claim"></a>
<a id="tocSclaim"></a>
<a id="tocsclaim"></a>

```json
{
  "claim": "There is no climate emergency",
  "threshold": 0.7,
  "top_k": 10
}

```

Claim

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|threshold|number|false|none|none|
|top_k|integer|false|none|none|
|claim|string|true|none|none|

<h2 id="tocS_Claims">Claims</h2>
<!-- backwards compatibility -->
<a id="schemaclaims"></a>
<a id="schema_Claims"></a>
<a id="tocSclaims"></a>
<a id="tocsclaims"></a>

```json
{
  "claims": [
    "CO2 is not the cause of our current warming trend.",
    "Natural variation explains a substantial part of global warming observed since 1850"
  ],
  "threshold": 0.6,
  "top_k": 10
}

```

Claims

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|threshold|number|false|none|none|
|top_k|integer|false|none|none|
|claims|[string]|true|none|none|

<h2 id="tocS_EvidenceOutput">EvidenceOutput</h2>
<!-- backwards compatibility -->
<a id="schemaevidenceoutput"></a>
<a id="schema_EvidenceOutput"></a>
<a id="tocSevidenceoutput"></a>
<a id="tocsevidenceoutput"></a>

```json
{
  "num": 0,
  "title": "string",
  "text": "string",
  "similarity": 0,
  "doi": "string",
  "openalex_id": "string",
  "year": 0,
  "citation_count": 0,
  "influential_citation_count": 0
}

```

EvidenceOutput

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|num|integer|true|none|none|
|title|string|true|none|none|
|text|string|true|none|none|
|similarity|number|false|none|none|
|doi|string|false|none|none|
|openalex_id|string|false|none|none|
|year|integer|false|none|none|
|citation_count|integer|false|none|none|
|influential_citation_count|integer|false|none|none|

<h2 id="tocS_HTTPValidationError">HTTPValidationError</h2>
<!-- backwards compatibility -->
<a id="schemahttpvalidationerror"></a>
<a id="schema_HTTPValidationError"></a>
<a id="tocShttpvalidationerror"></a>
<a id="tocshttpvalidationerror"></a>

```json
{
  "detail": [
    {
      "loc": [
        "string"
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}

```

HTTPValidationError

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|detail|[[ValidationError](#schemavalidationerror)]|false|none|none|

<h2 id="tocS_TextToSplit">TextToSplit</h2>
<!-- backwards compatibility -->
<a id="schematexttosplit"></a>
<a id="schema_TextToSplit"></a>
<a id="tocStexttosplit"></a>
<a id="tocstexttosplit"></a>

```json
{
  "text": "There is no climate emergency. OPINION: The science and data strongly support that our planet’s ecosystems are thriving and that humanity is benefiting from modestly increasing temperature and an increase in carbon dioxide. These facts refute the claim that Earth is spiraling into one man-made climate catastrophe after another. Carbon dioxide (CO2) is portrayed as a demon molecule fueling run-away greenhouse warming. If you get your news only from mainstream media, you would likely believe that CO2 levels are dangerously high and unprecedented. You would be wrong. Concentrations of this gas are slightly less than 420 parts-per-million (ppm), or one-sixth the average historic levels of 2,600 ppm for the last 600 million years. Increases in carbon dioxide in the last 150 years, largely from the burning of fossil fuels, have reversed a dangerous downward trend in the gas’ concentration. During the last glacial period, concentrations nearly reached the “line of death” at 150 parts per million, below which plants die. Viewed in the long-term geologic context, we are actually CO2 impoverished."
}

```

TextToSplit

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|text|string|true|none|none|

<h2 id="tocS_ValidationError">ValidationError</h2>
<!-- backwards compatibility -->
<a id="schemavalidationerror"></a>
<a id="schema_ValidationError"></a>
<a id="tocSvalidationerror"></a>
<a id="tocsvalidationerror"></a>

```json
{
  "loc": [
    "string"
  ],
  "msg": "string",
  "type": "string"
}

```

ValidationError

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|loc|[anyOf]|true|none|none|

anyOf

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|string|false|none|none|

or

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|integer|false|none|none|

continued

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|msg|string|true|none|none|
|type|string|true|none|none|

<h2 id="tocS_VerifiedEvidenceOutput">VerifiedEvidenceOutput</h2>
<!-- backwards compatibility -->
<a id="schemaverifiedevidenceoutput"></a>
<a id="schema_VerifiedEvidenceOutput"></a>
<a id="tocSverifiedevidenceoutput"></a>
<a id="tocsverifiedevidenceoutput"></a>

```json
{
  "num": 0,
  "title": "string",
  "text": "string",
  "similarity": 0,
  "doi": "string",
  "openalex_id": "string",
  "year": 0,
  "citation_count": 0,
  "influential_citation_count": 0,
  "label": "SUPPORTS",
  "probability": 0
}

```

VerifiedEvidenceOutput

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|num|integer|true|none|none|
|title|string|true|none|none|
|text|string|true|none|none|
|similarity|number|false|none|none|
|doi|string|false|none|none|
|openalex_id|string|false|none|none|
|year|integer|false|none|none|
|citation_count|integer|false|none|none|
|influential_citation_count|integer|false|none|none|
|label|string|true|none|none|
|probability|number|true|none|none|

#### Enumerated Values

|Property|Value|
|---|---|
|label|SUPPORTS|
|label|REFUTES|
|label|NOT_ENOUGH_INFO|

