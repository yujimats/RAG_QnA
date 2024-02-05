FROM ubuntu:22.04

# tzdataパッケージのインストールと設定
RUN apt-get update && apt-get install -y tzdata && \
    ln -fs /usr/share/zoneinfo/Asia/Tokyo /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata

# パッケージの更新とPythonの依存関係のインストール
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    wget \
    curl \
    llvm \
    libncurses5-dev \
    libncursesw5-dev \
    xz-utils \
    tk-dev \
    libffi-dev \
    liblzma-dev \
    python3-dev \
    python3-numpy \
    python3-pip \
    python3-openssl \
    git

# pythonライブラリインストール
RUN pip install --upgrade pip
RUN pip install pandas==2.0.0
RUN pip install matplotlib==3.8.2
RUN pip install python_dotenv==1.0.1
RUN pip install openai==0.28.0
RUN pip install chromadb==0.3.29
RUN pip install mwclient==0.10.1
RUN pip install mwparserfromhell==0.6.6
RUN pip install tiktoken==0.5.2

# ワーキングディレクトリの設定
WORKDIR /home
