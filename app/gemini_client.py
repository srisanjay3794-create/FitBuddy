import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from app.config import get_settings

settings = get_settings()


def generate_text(prompt, model):
    if not settings.gemini_api_key:
        raise RuntimeError(
            'GEMINI_API_KEY is missing. Add your own Gemini API key to the .env file.'
        )

    url = (
        'https://generativelanguage.googleapis.com/v1beta/models/'
        + model
        + ':generateContent'
    )

    payload = {
        'contents': [
            {
                'parts': [
                    {'text': prompt}
                ]
            }
        ]
    }

    data = json.dumps(payload).encode('utf-8')
    request = Request(
        url,
        data=data,
        headers={
            'Content-Type': 'application/json',
            'x-goog-api-key': settings.gemini_api_key,
        },
        method='POST',
    )

    try:
        with urlopen(request, timeout=120) as response:
            body = response.read().decode('utf-8')
    except HTTPError as exc:
        details = exc.read().decode('utf-8', errors='replace')
        raise RuntimeError(
            'Gemini API error (HTTP {0}): {1}'.format(exc.code, details)
        )
    except URLError as exc:
        raise RuntimeError('Could not connect to Gemini API: {0}'.format(exc.reason))

    result = json.loads(body)
    candidates = result.get('candidates', [])
    if not candidates:
        raise RuntimeError('Gemini returned no candidates: {0}'.format(body))

    parts = candidates[0].get('content', {}).get('parts', [])
    text_parts = [part.get('text', '') for part in parts if part.get('text')]
    text = '\n'.join(text_parts).strip()

    if not text:
        raise RuntimeError('Gemini returned an empty response.')

    return text
