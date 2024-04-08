import os

import requests


def draft_gpt(openai_api_key=os.environ["OPENAI_API_KEY"], gpt_model=os.environ["GPT_MODEL"]):

    if openai_api_key is None:
        raise ValueError("OpenAI API key is not set in environment variables.")

    with open("incident_description3.txt", "r") as file:
        incident_desc = file.read().replace("\n", "")

    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}",
    }

    data = {
        "model": gpt_model,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that will help with EC2 instance issues. You will respond in markdown format"},
            {
                "role": "user",
                "content": incident_desc,
            },
        ],
    }

    response = requests.post(url, headers=headers, json=data)
    response_txt = response.json()["choices"][0]["message"]["content"]

    # Check if the request was successful
    if response.status_code == 200:
        print("Response from OpenAI:", response.json())
        print("\n")
        print(response.json()["choices"][0]["message"]["content"])
        print("\n")
        with open("response.md", "w") as file:
            file.write(response_txt)
        print('Response has been written to response.md')
    else:
        print("Error:", response.status_code, response.text)

    return response.status_code


def test_draft_gpt():
    assert draft_gpt() == 200


if __name__ == "__main__":
    draft_gpt()
