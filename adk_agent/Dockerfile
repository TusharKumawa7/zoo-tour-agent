FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY zoo_agent_app/ ./zoo_agent_app/
COPY start.sh .
RUN chmod +x start.sh
CMD ["/app/start.sh"]
