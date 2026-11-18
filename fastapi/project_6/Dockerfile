FROM python:3.13-slim
WORKDIR /app
RUN groupadd --system learning && useradd --system --gid learning learning \
    && mkdir /data && chown learning:learning /data
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY project_6/study_api ./study_api
USER learning
ENV TASKS_DB=/data/tasks.db
EXPOSE 8000
CMD ["python", "-m", "uvicorn", "study_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
