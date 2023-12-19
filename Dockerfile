FROM python:3.10-slim
WORKDIR /Auto-adding-products-to-VK-cart
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"
COPY requirement.txt .
RUN python3 -m pip install -r requirement.txt
ENTRYPOINT ["python3"]
CMD ["./run.py"]