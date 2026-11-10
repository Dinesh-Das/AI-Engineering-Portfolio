FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /workspace/project
COPY workbench_core /workspace/workbench_core
COPY ["sonnet4-vs-qwen3-coder/enhance.py", "/workspace/project/enhance.py"]
COPY ["sonnet4-vs-qwen3-coder/enhancement/profile.json", "/workspace/project/enhancement/profile.json"]
USER 65532:65532
ENTRYPOINT ["python", "enhance.py"]
CMD ["check"]
