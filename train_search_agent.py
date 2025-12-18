def train_search_agent(df, query):
    return df[
        (df["source"] == query["source"]) &
        (df["destination"] == query["destination"]) &
        (df["class"] == query["class"])
    ].copy()
