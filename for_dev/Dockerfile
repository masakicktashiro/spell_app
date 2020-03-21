FROM ubuntu:latest

RUN apt-get update
RUN apt-get install -y python3 \
                       python3-pip

RUN apt-get install -y mecab \
    libmecab-dev \
    mecab-ipadic \
    mecab-ipadic-utf8 \
    wget \
    curl \
    vim

RUN pip3 install jupyter click numpy \
                 matplotlib seaborn \
                 pandas tqdm mecab-python3 \
                 mysql-connector-python

RUN pip3 install    flask \
                    flask_restful \
                    transformers \
		    uwsgi
RUN pip3 install  torch==1.4.0+cpu torchvision==0.5.0+cpu -f https://download.pytorch.org/whl/torch_stable.html

ADD ./ /home/
RUN apt-get update \
    && apt-get install -y locales \
    && locale-gen ja_JP.UTF-8 \
    && echo "export LANG=ja_JP.UTF-8" >> ~/.bashrc
WORKDIR /home
CMD ["uwsgi","--ini","/home/uwsgi.ini"]
