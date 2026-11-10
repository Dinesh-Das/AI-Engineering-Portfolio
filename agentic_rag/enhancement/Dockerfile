FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /workspace/project
COPY workbench_core /workspace/workbench_core
COPY ["agentic_rag/enhance.py", "/workspace/project/enhance.py"]
COPY ["agentic_rag/enhancement/profile.json", "/workspace/project/enhancement/profile.json"]
USER 65532:65532
ENTRYPOINT ["python", "enhance.py"]
CMD ["check"]
