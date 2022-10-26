# Base OS layer: Latest Ubuntu LTS
FROM jupyter/tensorflow-notebook

# install additional packages
COPY requirements.txt /home/jovyan/work/requirements.txt
WORKDIR /home/jovyan/work
RUN pip install -r requirements.txt
COPY . /home/jovyan/work
# continue as before...

# Download the nlp essentials
RUN python -m spacy download nl_core_news_lg

EXPOSE 8888