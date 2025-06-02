from openai import OpenAI, RateLimitError, APIError

def get_client():
    return OpenAI()

def ask(prompt, temperature=0.3, model="gpt-3.5-turbo"):
    """Return LLM answer or a stub if quota/billing is missing."""
    try:
        rsp = get_client().chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are Symphony, an elite strategy-consulting analyst. "
                        "Write crisp, C-suite-ready insights; numbers first, no fluff."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=temperature,
        )
        return rsp.choices[0].message.content.strip()
    except RateLimitError:
        return "⚠️  LLM quota exhausted – add billing or use a different key."
    except APIError as e:
        return f"⚠️  API error: {e.__class__.__name__}"

