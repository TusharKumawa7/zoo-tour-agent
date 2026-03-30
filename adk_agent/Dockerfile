FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY zoo_agent_app/ ./zoo_agent_app/
WORKDIR /app/zoo_agent_app
CMD ["adk", "api_server", "--host", "0.0.0.0", "--port", "8080", "/app"]
