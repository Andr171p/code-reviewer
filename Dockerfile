FROM python:3.13

WORKDIR /dio_employee_assistant

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python -c "from transformers import AutoModel; AutoModel.from_pretrained('deepvk/USER-bge-m3')"

CMD ["/bin/bash", "-c", "python main.py"]