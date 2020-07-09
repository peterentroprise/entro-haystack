FROM tiangolo/uvicorn-gunicorn-machine-learning:python3.7

ENV TIMEOUT 1000

ENV GRACEFUL_TIMEOUT 1000

# fastAPI

RUN conda install -c conda-forge fastapi

# haystack

RUN pip install git+https://github.com/deepset-ai/haystack.git

RUN pip install farm-haystack

# wandb

RUN pip install --upgrade wandb

RUN wandb login 47d3a85229ed086517bbc6a1adb7995f989b089e

#gcloud storage

RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg  add - && apt-get update -y && apt-get install google-cloud-sdk -y

COPY ./service-account.json /app

ENV GOOGLE_APPLICATION_CREDENTIALS="service-account.json"

RUN gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}

# Copy blank outputs/ folder for a target.

COPY ./app/trained-model /app/trained-model

RUN gsutil cp -R gs://entro-haystack-models/trained-model /app

COPY ./app /app