FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /workspace/project
COPY workbench_core /workspace/workbench_core
COPY ["Multi-Agent-deep-researcher-mcp-windows-linux/enhance.py", "/workspace/project/enhance.py"]
COPY ["Multi-Agent-deep-researcher-mcp-windows-linux/enhancement/profile.json", "/workspace/project/enhancement/profile.json"]
USER 65532:65532
ENTRYPOINT ["python", "enhance.py"]
CMD ["check"]
