FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /workspace/project
COPY workbench_core /workspace/workbench_core
COPY ["minimaxm2-vs-sonnet4-5-vs-kimik2-vs-gemini3/enhance.py", "/workspace/project/enhance.py"]
COPY ["minimaxm2-vs-sonnet4-5-vs-kimik2-vs-gemini3/enhancement/profile.json", "/workspace/project/enhancement/profile.json"]
USER 65532:65532
ENTRYPOINT ["python", "enhance.py"]
CMD ["check"]
