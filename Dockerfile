FROM xf1280/gibson:0.3.1
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
RUN echo "export LD_LIBRARY_PATH=/usr/local/nvidia/lib64:/usr/local/nvidia/bin:$LD_LIBRARY_PATH" >> ~/.bashrc

#download the dataset
RUN wget -qO- https://storage.googleapis.com/gibsonassets/dataset.tar.gz \
    | tar xzv -C /root/mount/gibson/gibson/assets


#gibson's default activated conda env is py3.5
#RUN pip install -U https://s3-us-west-2.amazonaws.com/ray-wheels/latest/ray-0.5.3-cp35-cp35m-manylinux1_x86_64.whl
RUN pip install --upgrade tensorflow gym pssh scipy opencv-python bokeh jupyter psutil lz4

RUN git clone https://github.com/jhpenger/ray-gibson.git
WORKDIR ray-gibson
RUN pip install -U .whl/frac_wheels/ray-0.5.3-cp35-cp35m-manylinux1_x86_64.whl

RUN ssh-keygen -f /root/.ssh/id_rsa -P "" \
    && echo "StrictHostKeyChecking no" >> /etc/ssh/ssh_config \
    && touch ~/.ssh/authorized_keys \
    && cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
