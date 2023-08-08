import openai
API_KEY = "INSERT_API_KEY"


openai.api_key = API_KEY


def generate(PROMPT, MaxToken=50, outputs=3):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=PROMPT,
        max_tokens=MaxToken,
        n=outputs
    )
    outputs = []
    for k in response['choices']:
        text = k['text'].strip()
        outputs.append(text)

    return outputs


prompt = "Write a description about ai"

result = generate(prompt, MaxToken=3000,
                  outputs=1)
print(result)
