import os
import openai

def gpt3(stext):
    openai.api_key = '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'
    response = openai.Completion.create(
      model="text-davinci-002",
      prompt=stext,
      temperature=0,
      max_tokens=200,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0,
      stop=["?"]
    )
    return response

def run(question, answers):
    query = setup(question, answers)
    response = gpt3(query)
    print(response["choices"][0]["text"])

def setup(question, answers):
    base_text = "I am a highly intelligent question answering bot. If you ask me a question that is rooted in truth, I will give you the answer. If you ask me a question that is nonsense, trickery, or has no clear answer, I will respond with \"Unknown\".\n\nQ: What is human life expectancy in the United States?\nA: Human life expectancy in the United States is 78 years.\n\nQ: Who was president of the United States in 1955?\nA: Dwight D. Eisenhower was president of the United States in 1955.\n\nQ: Which party did he belong to?\nA: He belonged to the Republican Party.\n\nQ: What is the square root of banana?\nA: Unknown\n\nQ: How does a telescope work?\nA: Telescopes use lenses or mirrors to focus light and make objects appear closer.\n\nQ: Where were the 1992 Olympics held?\nA: The 1992 Olympics were held in Barcelona, Spain.\n\nQ: How many squigs are in a bonk?\nA: Unknown\n\nQ:"
    formatted_question = question.replace('?', ':')

    for i in range(0,len(answers)):
        answers[i] = answers[i].strip()
    formatted_question = " " + formatted_question + "" + answers[0] + ", " + answers[1] + ", or " + answers[2] + "?\nA: "
    query = base_text + formatted_question
    print(query)
    return query

