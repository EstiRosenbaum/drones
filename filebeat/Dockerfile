FROM docker.elastic.co/beats/filebeat:7.15.0
# --- NETFREE CERT INTSALL ---
ADD https://netfree.link/dl/unix-ca.sh /home/netfree-unix-ca.sh 
RUN cat  /home/netfree-unix-ca.sh | sh
ENV NODE_EXTRA_CA_CERTS=/etc/ca-bundle.crt
ENV REQUESTS_CA_BUNDLE=/etc/ca-bundle.crt
ENV SSL_CERT_FILE=/etc/ca-bundle.crt
# --- END NETFREE CERT INTSALL ---
USER root

COPY filebeat.yml /usr/share/filebeat/filebeat.yml
COPY --chown=root:filebeat filebeat.yml /usr/share/filebeat/filebeat.yml
RUN chown root /usr/share/filebeat/filebeat.yml
