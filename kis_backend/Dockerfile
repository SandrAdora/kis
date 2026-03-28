# ── Stage: base image ────────────────────────────────────────────────────────
# We use the official slim Python image. "slim" strips out compilers and docs
# that are not needed at runtime, keeping the final image small.
FROM python:3.12-slim

# ── System-level setup ───────────────────────────────────────────────────────
# PYTHONDONTWRITEBYTECODE: stops Python from writing .pyc files into the image.
# PYTHONUNBUFFERED: forces stdout/stderr to flush immediately so logs appear
#                  in real time inside Docker (important for debugging).
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# ── Working directory ─────────────────────────────────────────────────────────
# All subsequent commands run relative to this path inside the container.
WORKDIR /app

# ── Install dependencies first (layer-caching trick) ─────────────────────────
# We copy only requirements.txt before the rest of the source code.
# Docker re-uses the cached layer as long as requirements.txt hasn't changed,
# so a code-only change doesn't trigger a full pip install again.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── Copy application source ───────────────────────────────────────────────────
# Copied after dependencies so the expensive pip layer stays cached.
COPY . .

# ── Expose the port Django will listen on ────────────────────────────────────
# This is documentation only — it doesn't actually publish the port.
# You still need -p 8000:8000 (or docker-compose ports:) at runtime.
EXPOSE 8000

# ── Start the development server ─────────────────────────────────────────────
# 0.0.0.0 makes Django listen on all interfaces inside the container so that
# traffic forwarded from the host can actually reach it.
# For production you would swap this for gunicorn or uvicorn.
CMD ["gunicorn", "kis_backend.wsgi:application", "--bind", "0.0.0.0:8000"]
