summary_prompt = """You are an expert in data analysis and summarization.

Here is the dataset to analyze and summarize:

{context}

Here is the topic you need to summarize and make analysis on:
{topic}

Your task:
1. Provide a concise summary of key trends, significant values, or patterns observed in the data.
2. Highlight any notable details, such as outliers or frequent values.
3. Make a brief inference or insight about the data, if possible, based on the provided information.

Keep the summary to a maximum of three sentences and ensure the answer is clear, factual, and to the point.

Answer:"""

answer_prompt = """You are an expert in data analysis and question answering.

Here is the dataset to analyze and reference:

{context}

Here is the question you need to answer:
{topic}

Your task:
1. Provide a clear and concise answer to the users question based on the information provided in the dataset.
2. If relevant, include any key data points that support your answer.
3. If the question cannot be answered directly from the data, provide an explanation or suggest an alternative insight based on the available information.

Keep your response to a maximum of three sentences and ensure the answer is precise, factual, and directly addresses the question.

Answer:"""
