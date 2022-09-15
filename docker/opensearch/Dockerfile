FROM opensearchproject/opensearch:2.2.1

RUN /usr/share/opensearch/bin/opensearch-plugin remove opensearch-reports-scheduler --purge

RUN /usr/share/opensearch/bin/opensearch-plugin list | xargs -l /usr/share/opensearch/bin/opensearch-plugin remove --purge

COPY --chown=1000:1000 --chmod=0755 opensearch-docker-entrypoint.sh /usr/share/opensearch
