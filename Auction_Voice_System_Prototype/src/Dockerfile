# ------------------------------------------------------------
#  Hugging Face “Docker Space” for the Auction Voice Agent
# ------------------------------------------------------------
#  • Uses Python 3.11 (works well on the HF build farm)       │
#  • Installs your FastAPI backend plus any extra libs        │
#  • Serves both the API and the static dashboard from /app   │
#  • Exposes **port 7860**, the default expected by HF Spaces │
# ------------------------------------------------------------

FROM python:3.11-slim

#––– system ‑ level deps (optional mic, ffmpeg, etc.)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential ffmpeg && \
    rm -rf /var/lib/apt/lists/*

#––– create unprivileged user (HF best-practice)
ENV UID=1000
RUN useradd -m -u $UID user
USER user

#––– working dir
WORKDIR /app

#––– copy dependency list first (leverages Docker cache)
COPY --chown=user requirements.txt .

#    install Python deps
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

#––– copy application code (API + static html / js / css)
COPY --chown=user . .

#––– FastAPI entry-point
#     Assumes you expose a FastAPI app object called `app`
#     in backend/main.py  →  backend/main.py:app
#
#     If your entry point differs, just change `backend.main:app`
#
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "7860", "--proxy-headers"]

# Hugging Face scans this line; don’t remove
EXPOSE 7860
