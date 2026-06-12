def get_retriever(vector_store):

    retriever = vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 5,        # final documents sent to LLM
            "fetch_k": 20  # broader search pool first
        }
    )

    return retriever