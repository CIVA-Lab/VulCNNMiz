FROM ubuntu

RUN mkdir -p /opt/sent2vec/src
ADD setup.py /opt/sent2vec/
ADD src /opt/sent2vec/src/
ADD Makefile /opt/sent2vec/
ADD requirements.txt /opt/sent2vec/

RUN apt-get update
RUN apt-get install -y libpthread-stubs0-dev
RUN apt-get install -y libevent-dev
RUN apt-get install -y python3-pip python3-dev build-essential
RUN apt-get update
RUN apt-get install -y libevent-pthreads-2.1-7
#RUN apt-get install -y libevent-pthreads-2.1.6
WORKDIR /opt/sent2vec

RUN pip3 install --upgrade pip
RUN pip3 install cython
RUN pip3 install numpy
#RUN pip3 install -r requirements.txt

RUN pip3 install .
RUN make
RUN pip3 install networkx
RUN pip3 install pandas

RUN apt-get install -y git
RUN apt-get install -y unzip
RUN apt-get install -y wget

RUN wget "https://drive.google.com/u/0/uc?id=1o_xP_kaZBV5ghZ1WjKzXBnQYilED2PMw&export=download&confirm=t&uuid=7b95fffe-7ac4-47e9-a447-cbe101635481" -O model.bin
RUN apt-get install nano
RUN git clone https://github.com/ekincanufuktepe/VulCNN.git
RUN apt-get update
RUN apt-get install -y graphviz graphviz-dev

RUN pip3 install pygraphviz
RUN pip3 install pydot
RUN pip3 install lap
RUN pip3 install torch
RUN pip3 install -U scikit-learn
RUN pip3 install tqdm
RUN pip3 install pretty table
RUN pip3 install transformers
RUN pip3 install pyrotechnics

RUN unzip ./VulCNN/pdgs/No-Vul.zip -d ./VulCNN/pdgs
RUN unzip ./VulCNN/pdgs/Vul.zip -d ./VulCNN/pdgs