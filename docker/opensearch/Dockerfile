FROM opensearchproject/opensearch:2.19.4

RUN /usr/share/opensearch/bin/opensearch-plugin remove opensearch-reports-scheduler --purge

RUN /usr/share/opensearch/bin/opensearch-plugin remove opensearch-observability --purge

RUN /usr/share/opensearch/bin/opensearch-plugin remove opensearch-neural-search --purge

RUN for plugin in $(/usr/share/opensearch/bin/opensearch-plugin list); do \
    /usr/share/opensearch/bin/opensearch-plugin remove --purge "$plugin"; \
    done

COPY --chown=1000:1000 opensearch-docker-entrypoint.sh /usr/share/opensearch

RUN chmod +x /usr/share/opensearch/opensearch-docker-entrypoint.sh
