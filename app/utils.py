from openai import OpenAI
from app.config import settings


def moderate_string_by_openai(string_to_check: str):
    try:
        client = OpenAI(
            api_key=settings.OPENAI_API_KEY,
            project=settings.OPENAI_PROJECT_NAME,
        )
        response = client.moderations.create(
            model="omni-moderation-latest",
            input=string_to_check,
        )
        return response.results[0].flagged
    except Exception as e:
        print(f"Unknown OpenAI error: {e}")
        return None


def create_answer_by_openai(post: str, comment: str):
    try:
        client = OpenAI(
            api_key=settings.OPENAI_API_KEY_2,
            project=settings.OPENAI_PROJECT_NAME_2,
        )
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": f"You are a helpful assistant to the author of this article - {post}. "
                               f"Answer briefly in one sentence."},
                {
                    "role": "user",
                    "content": comment,
                }
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Unknown OpenAI error: {e}")
        return None
