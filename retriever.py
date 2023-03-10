import os
from haystack.document_stores import FAISSDocumentStore
from haystack.nodes import EmbeddingRetriever


class FAISSIndexer:
    def __init__(self, path_to_index_dir,
                 model_name, embedding_dim,
                 similarity_measure,
                 path_to_postgres=None) -> None:
        self.path_to_index_dir = path_to_index_dir
        # our db is postgres, only need to set path to faiss index
        if path_to_postgres:
            self.path_to_db = path_to_postgres
            self._set_path_to_index()
        # our db is SQLLite
        else:
            self._set_path_to_index_and_db()
        self.embedding_dim = embedding_dim
        self.model_name = model_name
        self.similarity_measure = similarity_measure
        self.document_store = self._init_document_store()
        self.retriever = self._init_retriever()

    def _set_path_to_index(self):
        if not os.path.exists(self.path_to_index_dir):
            raise Exception("Path to index don't exist")
        self.path_to_index = os.path.join(self.path_to_index_dir, "faiss_index")

    def _set_path_to_index_and_db(self):
        self._set_path_to_index()
        self.path_to_db = f"sqlite:///{os.path.join(self.path_to_index_dir, 'faiss_document_store.db')}"

    def _init_document_store(self):
        if os.path.exists(self.path_to_index):
            return FAISSDocumentStore.load(index_path=self.path_to_index)

    def _init_retriever(self, progress_bar=True):
        return EmbeddingRetriever(
            document_store=self.document_store,
            embedding_model=self.model_name,
            model_format='sentence_transformers',
            # include article title into the embedding
            embed_meta_fields=["title"],
            progress_bar=progress_bar
        )

    def retrieve_matches_for_a_phrase(self, phrase, top_k=10):
        return self.retriever.retrieve(phrase, top_k=top_k)

    def retrieve_matches_for_phrases(self, phrases, top_k=10):
        return self.retriever.retrieve_batch(phrases, top_k=top_k)
