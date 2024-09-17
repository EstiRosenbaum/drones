FROM docker.elastic.co/beats/filebeat:7.15.0
USER root

COPY filebeat.yml /usr/share/filebeat/filebeat.yml
COPY --chown=root:filebeat filebeat.yml /usr/share/filebeat/filebeat.yml
RUN chown root /usr/share/filebeat/filebeat.yml
