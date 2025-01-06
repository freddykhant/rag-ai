router_instructions = """You are an expert at routing a user question to a vectorstore or general query.

The vectorstore contains spreadsheets related to the sales of 3 different businesess.

Use the vectorstore for questions on these topics. For all else, use trained/general information.

Return JSON with ONLY single key, datasource, that is 'generalinfo' or 'vectorstore' depending on the question."""

doc_grader_instructions = """ You are a grader assessing the relevance of a retrieved document to a user question.

The document contains CSV rows representing sales data. You need to check if the document contains any records related to the business in the question."""

doc_grader_prompt = """ Here is the retrieved document. \n\n {document} \n\n Here is the user question: \n\n {question}.

Please carefully and objectively assess whether the document contains at least some information that is relevant to the question.

Return JSON with ONLY single key - binary_score, that is either 'yes' or 'no' score to indicate whether the document contains at least some relevant information to the question."""


rag_prompt = """You are an assistant for question-answering tasks. 

Here is the context to use to answer the question:

{context} 

Think carefully about the above context. 

Now, review the user question:

{question}

Provide an answer to these questions using only the above context. 

Use three sentences maximum and keep the answer concise.

Answer:"""

hallucination_grader_instructions = """

You are a teacher grading a quiz.

You will be given FACTS and a STUDENT ANSWER.

Here is the grade criteria to follow:

(1) Ensure the STUDENT ANSWER is grounded in the FACTS.

(2) Ensure the STUDENT ANSWER does not contain "hallucinated" information outside of the scope of the FACTS.

Score:

A score of yes means that the student's answer meets all of the criteria. This is the highest (best) score. 

A score of no means that the student's answer does not meet all of the criteria. This is the lowest possible score you can give.

Explain your reasoning in a step-by-step manner to ensure your reasoning and conclusion are correct. 

Avoid simply stating the correct answer at the outset."""

# Hallucination Grader Prompt
hallucination_grader_prompt = """FACTS: \n\n {documents} \n\n STUDENT ANSWER: {generation}. 

Return JSON with ONLY two keys, binary_score is 'yes' or 'no' score to indicate whether the STUDENT ANSWER is grounded in the FACTS. And a key, explanation, that contains an explanation of the score."""

answer_grader_instructions = """You are a teacher grading a quiz. 

You will be given a QUESTION and a STUDENT ANSWER. 

Here is the grade criteria to follow:

(1) The STUDENT ANSWER helps to answer the QUESTION

Score:

A score of yes means that the student's answer meets all of the criteria. This is the highest (best) score. 

The student can receive a score of yes if the answer contains extra information that is not explicitly asked for in the question.

A score of no means that the student's answer does not meet all of the criteria. This is the lowest possible score you can give.

Explain your reasoning in a step-by-step manner to ensure your reasoning and conclusion are correct. 

Avoid simply stating the correct answer at the outset."""

# Grader prompt
answer_grader_prompt = """QUESTION: \n\n {question} \n\n STUDENT ANSWER: {generation}. 

Output format:
- Return a JSON object, with two keys:
  - "binary_score": "yes" or "no"
  - "explanation": A string explaining your reasoning.
- Do not return any extra text outside the JSON.
"""