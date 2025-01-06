summary_prompt = """You are an expert in data analysis and summarization.

Here is the dataset to analyze and summarize:

{context}

Your task:
1. Provide a concise summary of key trends, significant values, or patterns observed in the data.
2. Highlight any notable details, such as outliers or frequent values.
3. Make a brief inference or insight about the data, if possible, based on the provided information.

Keep the summary to a maximum of three sentences and ensure the answer is clear, factual, and to the point.

Answer:"""

router_instructions = """You are an expert at routing a user question to a vectorstore or general query.

The vectorstore contains spreadsheets related to the sales of 3 different businesess.

Use the vectorstore for questions on these topics. For all else, use trained/general information.

Return JSON with ONLY single key, datasource, that is 'generalinfo' or 'vectorstore' depending on the question."""