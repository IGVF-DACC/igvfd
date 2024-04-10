FROM localstack/localstack:3.3

COPY --chown=localstack create_localstack.sh /etc/localstack/init/ready.d/init-aws.sh

RUN chmod u+x /etc/localstack/init/ready.d/init-aws.sh
