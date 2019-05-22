FROM registry.centos.org/centos/centos:7

ENV F8A_WORKER_VERSION=d403113 \
    AUTH_VERSION=fff8f49
LABEL name="f8analytics ingestion services" \
      description="APIs to invoke worker flow." \
      git-url="https://github.com/fabric8-analytics/f8a-data-ingestion-service" \
      git-path="/" \
      target-file="Dockerfile" \
      app-license="GPL-3.0"

RUN yum install -y epel-release &&\
    yum install -y gcc git python36-pip python36-requests httpd httpd-devel python36-devel openssl-devel &&\
    yum clean all

COPY ./requirements.txt /

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt && rm requirements.txt
RUN pip3 install git+https://github.com/fabric8-analytics/fabric8-analytics-worker.git@${F8A_WORKER_VERSION}
RUN pip3 install git+https://github.com/fabric8-analytics/fabric8-analytics-auth.git@${AUTH_VERSION}

COPY ./src /src

ADD scripts/entrypoint.sh /bin/entrypoint.sh

RUN chmod +x /bin/entrypoint.sh

ENTRYPOINT ["/bin/entrypoint.sh"]
