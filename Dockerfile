FROM python:3.12.2
# # --- NETFREE CERT INTSALL ---
# ADD https://netfree.link/dl/unix-ca.sh /home/netfree-unix-ca.sh 
# RUN cat  /home/netfree-unix-ca.sh | sh
# ENV NODE_EXTRA_CA_CERTS=/etc/ca-bundle.crt
# ENV REQUESTS_CA_BUNDLE=/etc/ca-bundle.crt
# ENV SSL_CERT_FILE=/etc/ca-bundle.crt
# # --- END NETFREE CERT INTSALL ---
WORKDIR /app

COPY ./ /app

RUN mkdir /usr/share/filebeat

RUN touch /usr/share/filebeat/app.log

RUN  pip install .

# RUN pytest
