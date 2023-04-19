# Evidence database creation

There are 2 evidence databases created for relevant evidence similarity searches:

1. Indexes scientific papers’ abstracts full text
1. Indexes scientific papers’ abstracts broken into individual sentences

The reason for creation of 2 different indexes is that one of the
models that we used for verification takes 2 sentences as input and the other takes a sentence and an abstract.

## Scientific articles sources
Two sources
- [OpenAlex](https://openalex.org/)
- [Semantic Scholar](https://www.semanticscholar.org/)  
were used in combination to retrieve scientific papers’ abstracts and additional information. 
Please see the reasons why to combine the two [here](#Why not use semanticscholar keyword search?)
and [here](#Downsides of OpenAlex)

## Stages

1. **Keyword search**. Perform **keyword search** in [OpenAlex](https://openalex.org/) reproducing the approach from [[1]](#references) to get a 
   comprehensive set of scientific articles abstracts covering the topic of climate impacts in
   csv format.  
   The code for cvs generation is available [here](https://github.com/aaalexlit/cc-claim-verification/blob/main/download/query_openalex.py).
   It's a slightly modified version of the code provided by the paper's authors available 
   [here](https://github.com/mcallaghan/NLP-climate-science-tutorial-CCAI/blob/main/A_obtaining_data.ipynb)  
    According to the authors of the paper at least using Web of Science (WOS) as a source the result
   is expected to be pretty complete
    >    We assessed comprehensiveness by ensuring that our search string returned all references 
   >    from tables 18.5–18.9 in the Fifth Assessment Report (AR5) Working Group II (WGII), 
   >    which deal with the detection and attribution of climate impacts

2. **Citation metrics**. Use [Semantic Scholar](https://www.semanticscholar.org/) API
   to enrich the readily available abstracts with **citation metrics**.  
   [Link to the code](https://github.com/aaalexlit/cc-claim-verification/blob/main/download/semanticscholar/add_info.py)
    1. Gather information on citations count, influential citations count to use it for re-ranking the results of 
   semantic similarity search.
    2. Potentially improve abstract text quality (if there’s a version of the abstract available 
   from Semantic Scholar it replaces the abstract downloaded from OpenAlex). 
   See [this note](#Downsides of OpenAlex) for the details
3. **Index**. Create a vector index of sentence encodings for similarity searches. 
   Semantic similarity is used to retrieve most relevant scientific
  evidences to verify a provided claim. [Sentence transformers](https://www.sbert.net/)
  framework was chosen for this task
  as it is shown to be the most efficient and accurate method to 
  perform semantic searches [[2]](#references)  
  [Haystack framework](https://haystack.deepset.ai/) 
  takes care of vector and metadata indexing and subsequent retrieval

## Workflow
```mermaid
flowchart TB
    A(Keyword boolean query) --> |Fetch from OpenAlex.org| Q("csv with scientific papers' abstracts")
    Q --> |Fetch from semanticscholar.org| B("csv with scientific papers' abstracts\nwith citation metrics")
    B --> |Split abstract into sentences| D["Collection of Haystack\ndocuments"]
    B --> |Check if full abstract text is about climate| G["Collection of Haystack\ndocuments"]
    subgraph Index abstracts for searches with Haystack and sentence transformers
        D --> |sentence transformers| E[(Sentence based \nFAISS index)]
        D --> I[("SQLite DB with \n metainformation")]
        G -->|sentence transformers| F[("Full abstract based \nFAISS index")]
        G --> H[("SQLite DB with \n metainformation")]       
    end
   ```

## Model for sentence embeddings
### Sentence based index
This index is needed to perform 
[symmetric semantic search](https://www.sbert.net/examples/applications/semantic-search/README.html#symmetric-vs-asymmetric-semantic-search)
(ie query and corpus entries are of the same length and can be potentially flipped)  
For sentence based index [all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
model was chosen  
*Why this model?*
- It seems to provide an optimal speed-quality tradeoff
- It is recommended by the sentence-transformers authors
### Abstracts based index
This index is needed to perform 
[asymmetric semantic search](https://www.sbert.net/examples/applications/semantic-search/README.html#symmetric-vs-asymmetric-semantic-search)
(ie query is shorter than corpus entries and flipping them with each other doesn't make sense)  
[msmarco-distilbert-base-tas-b](https://huggingface.co/sebastian-hofstaetter/distilbert-dot-tas_b-b256-msmarco)
model [[3]](#references) tuned for dot-product was chosen for semantic embeddings calculation for abstract based index  
*Why this model?*
- Models tuned for dot-product prefer the retrieval of longer passages than the cosine-similarity ones.
- The model shows good speed and quality on the benchmarks  

**Note:** later I noticed a [note](https://huggingface.co/sebastian-hofstaetter/distilbert-dot-tas_b-b256-msmarco#limitations--bias)
on the huggingface model card that says that
>The model is only trained on relatively short passages of MSMARCO (avg. 60 words length), so it might struggle with longer text.

Therefore, potentially it makes sense to change the model on the next iterations because scientific 
abstracts tend to be [250-300 words long](https://blog.wordvice.com/how-to-decrease-the-length-of-a-research-abstract/#:~:text=Most%20word%20limits%20specify%20a,is%2C%20well%2C%20a%20science.)

## Model to classify abstracts as climage related or not

[Climateattention model from huggingface](https://huggingface.co/kruthof/climateattention-ctw) 
is used to perform this classification.
It is a ClimateBERT [[5]](#references) based classifier fine-tuned on the
ClimaText dataset [[6]](#references) 

### Split into sentences
[Spacy "en_core_web_sm" pipeline](https://spacy.io/models/en#en_core_web_sm)
is used for text segmentation task  
This model is the smallest and the fastest and according to spacy's 
[Accuracy Evaluation](https://spacy.io/models/en#en_core_web_sm-accuracy) has
the same metric values as the bigger CPU-optimized models

## Appendix 

### Why index only abstracts not the full papers?

Abstracts are more manageable in terms of storage.  
According to [[4]](#references) evidence is found in abstract in 
more than 60% cases

### Why not use semanticscholar keyword search?

- No way to perform boolean queries and to reproduce keyword search 
   from the article [[1]](#references) mentioned above
- Not all the articles that has abstracts in OpenAlex do have those 
  in semanticscholar (potentially the reverse is also true)
- Has its own ranking system already included whereas at the first stage 
  we’d like to get all the articles by keywords without any 
  filtering which will happen on the later stages.


### Downsides of OpenAlex

- For copyright reasons, the abstract is stored in an inverted index. 
Sometimes some common words are dropped which results in a weirdly looking text.
Eg the following text "restored" from a response from OpenAlex API

> The climate of the 21 st century is likely to be significantly different from that 20th because human-induced change. An extreme weather event defined as a phenomenon has not been observed for past 30 years and may have occurred by change variability. abnormal can induce natural disasters such floods, droughts, typhoons, heavy snow, etc. How will frequency intensity events affected global warming in century? This could quite interesting matter concern hydrologists who forecast preventing future disasters. In this study, we establish indices analyze trend using estimated data 66 stations controlled Korea Meteorological Administration (KMA) Korea. These analyses showed spatially coherent statistically significant changes tempera ture rainfall occurred. Under change, Korea, unlike past, now being rain temperatures addition phenomena.
> 

Whereas the original text available from
[https://www.eeer.org/journal/view.php?doi=10.4491/eer.2011.16.3.175](https://www.eeer.org/journal/view.php?doi=10.4491/eer.2011.16.3.175)
is the following

> The climate of the 21st century is likely to be significantly different from that of the 20th century because of human-induced climate change. An extreme weather event is defined as a climate phenomenon that has not been observed for the past 30 years and that may have occurred by climate change and climate variability. The abnormal climate change can induce natural disasters such as floods, droughts, typhoons, heavy snow, etc. How will the frequency and intensity of extreme weather events be affected by the global warming change in the 21st
 century? This could be a quite interesting matter of concern to the hydrologists who will forecast the extreme weather events for preventing future natural disasters. In this study, we establish the extreme indices and analyze the trend of extreme weather events using extreme indices estimated from the observed data of 66 stations controlled by the Korea Meteorological Administration (KMA) in Korea. These analyses showed that spatially coherent and statistically significant changes in the extreme events of temperature and rainfall have occurred. Under the global climate change, Korea, unlike in the past, is now being affected by extreme weather events such as heavy rain and abnormal temperatures in addition to changes in climate phenomena.
>


## References

1. Callaghan, M., Schleussner, CF., Nath, S. *et al.*
 Machine-learning-based evidence and attribution mapping of 100,000 climate impact studies. *Nat. Clim. Chang.* **11**, 966–972 (2021). https://doi.org/10.1038/s41558-021-01168-6
2. Reimers, N., & Gurevych, I. (2019). Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks. Conference on Empirical Methods in Natural Language Processing.
3. Hofstätter, S., Lin, S., Yang, J., Lin, J.J., & Hanbury, A. (2021). Efficiently Teaching an Effective Dense Retriever with Balanced Topic Aware Sampling. Proceedings of the 44th International ACM SIGIR Conference on Research and Development in Information Retrieval.
4. Wadden, D., Lo, K., Wang, L.L., Lin, S., van Zuylen, M., Cohan, A., & Hajishirzi, H. (2020). Fact or Fiction: Verifying Scientific Claims. ArXiv, abs/2004.14974.
5. Webersinke, N., Kraus, M., Bingler, J. A., & Leippold, M. (2021). Climatebert: 
A pretrained language model for climate-related text. arXiv preprint arXiv:2110.12010.
6. Varini, F. S., Boyd-Graber, J., Ciaramita, M., & Leippold, M. (2020). ClimaText: 
A dataset for climate change topic detection. arXiv preprint arXiv:2012.00483.
