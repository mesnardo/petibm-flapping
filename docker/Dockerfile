# Dockerfile for 2D flapping wing with PetIBM.

FROM barbagroup/petibm:0.4-GPU-OpenMPI-ubuntu
MAINTAINER Olivier Mesnard <mesnardo@gwu.edu>

# Install basic requirements.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        git \
        wget && \
    rm -rf /var/lib/apt/lists/*

# petibm-flapping.
RUN cd /opt && \
    git clone https://github.com/mesnardo/petibm-flapping.git && \
    cd petibm-flapping && \
    make all

EXPOSE 23
CMD ["/usr/sbin/sshd", "-D", "-p", "23"]