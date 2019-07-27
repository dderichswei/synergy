FROM fedora:29

# Install Ansible Jupyter Kernel
RUN dnf install -y git-all python2-ipykernel python2-jupyter-core gcc python2-devel \
    bzip2 openssh openssh-clients python2-crypto python2-psutil glibc-locale-source && \
    localedef -c -i en_US -f UTF-8 en_US.UTF-8 && \
    pip install --no-cache-dir wheel psutil && \
    rm -rf /var/cache/yum

ENV LANG=en_US.UTF-8 \
    LANGUAGE=en_US:en \
    LC_ALL=en_US.UTF-8

ENV NB_USER notebook
ENV NB_UID 1000
ENV HOME /home/${NB_USER}
ENV ANSIBLE_LIBRARY=${HOME}/hponeview/oneview-ansible/library
ENV ANSIBLE_MODULE_UTILS=${HOME}/hponeview/oneview-ansible/library/module_utils


RUN useradd \
    -c "Default user" \
	-d /home/notebook \
    -u ${NB_UID} \
    ${NB_USER}

#COPY . ${HOME}
USER root
RUN chown -R ${NB_USER} ${HOME}


RUN pip install --no-cache-dir ansible-jupyter-widgets
RUN pip install --no-cache-dir ansible_kernel==0.9.0 && \
    python -m ansible_kernel.install


RUN pip install --no-cache-dir bash_kernel
RUN python -m bash_kernel.install
RUN pip install --no-cache-dir hponeview
RUN mkdir ${HOME}/hponeview
RUN mkdir ${HOME}/notebooks
RUN git -C ${HOME}/hponeview clone https://github.com/HewlettPackard/oneview-ansible.git
RUN chown -R ${NB_USER} ${HOME}/notebooks

USER ${NB_USER}
WORKDIR /home/notebook/notebooks
CMD ["jupyter-notebook", "--ip", "0.0.0.0"]
EXPOSE 8888
