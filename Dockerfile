# 使用 AlmaLinux 9 作為基礎映像
FROM almalinux:9

# 安裝必要的依賴
RUN dnf -y update && dnf -y install \
#    curl \
    git \
    sudo \
    bzip2 \
    && dnf clean all

# 安裝 Miniconda
RUN curl -fsSL https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -o /tmp/miniconda.sh \
    && bash /tmp/miniconda.sh -b -p /opt/miniconda \
    && rm /tmp/miniconda.sh

# 更新 conda
RUN /opt/miniconda/bin/conda update -y conda

# 設定 Conda 環境
WORKDIR /app/CI_Test

# 複製 github repo 到容器中
COPY . /app/CI_Test/.

# 使用 env.yml 創建 Conda 環境
RUN /opt/miniconda/bin/conda env create -f environment.yml

# 設定 PATH 讓 Conda 環境在容器內可用
ENV PATH /opt/miniconda/envs/myenv/bin:$PATH
ENV PYTHONPATH /app:$PYTHONPATH

# 執行 pytest 測試
CMD ["/opt/miniconda/envs/myenv/bin/pytest"]
