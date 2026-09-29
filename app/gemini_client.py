import json
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from app.config import get_settings

settings = get_settings()


def generate_text(prompt, model):
    if not settings.gemini_api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. Add your Gemini API key to the Render Environment Variables."
        )

    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        + model
        + ":generateContent"
    )

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }

    data = json.dumps(payload).encode("utf-8")

    max_retries = 5

    for attempt in range(max_retries):
        request = Request(
            url,
            data=data,
            headers={
                "Content-Type": "application/json",
                "x-goog-api-key": settings.gemini_api_key,
            },
            method="POST",
        )

        try:
            with urlopen(request, timeout=120) as response:
                body = response.read().decode("utf-8")

            result = json.loads(body)

            candidates = result.get("candidates", [])

            if not candidates:
                raise RuntimeError(
                    "Gemini returned no candidates: " + body
                )

            parts = candidates[0].get("content", {}).get("parts", [])

            text_parts = [
                part.get("text", "")
                for part in parts
                if part.get("text")
            ]

            text = "\n".join(text_parts).strip()

            if not text:
                raise RuntimeError("Gemini returned an empty response.")

            return text

        except HTTPError as exc:
            details = exc.read().decode("utf-8", errors="replace")

            # Retry temporary errors
            if exc.code in (408, 429) or 500 <= exc.code < 600:
                if attempt < max_retries - 1:
                    delay = 2 ** attempt

                    print(
                        "Gemini temporary error HTTP {0}. "
                        "Retrying in {1} seconds...".format(
                            exc.code, delay
                        )
                    )

                    time.sleep(delay)
                    continue

            # Do not retry permanent errors
            raise RuntimeError(
                "Gemini API error (HTTP {0}): {1}".format(
                    exc.code, details
                )
            )

        except URLError as exc:
            if attempt < max_retries - 1:
                delay = 2 ** attempt

                print(
                    "Gemini connection error. "
                    "Retrying in {0} seconds...".format(delay)
                )

                time.sleep(delay)
                continue

            raise RuntimeError(
                "Could not connect to Gemini API: {0}".format(
                    exc.reason
                )
            )

    raise RuntimeError(
        "Gemini API is temporarily unavailable after multiple retries. "
        "Please try again later."
    )
