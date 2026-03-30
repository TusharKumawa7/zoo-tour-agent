FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY zoo_agent_app/ ./zoo_agent_app/
EXPOSE 8080
CMD ["adk", "api_server", "--port", "8080", "zoo_agent_app"]
