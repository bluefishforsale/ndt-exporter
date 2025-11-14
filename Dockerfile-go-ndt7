FROM --platform=${TARGETPLATFORM} golang:1.21-bullseye

ARG TARGETPLATFORM
ARG BUILDPLATFORM

RUN apt-get update && apt-get install -y \
    python3-pip \
    python3 \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install prometheus-client

# Install ndt7-client to a known location
RUN go install github.com/m-lab/ndt7-client-go/cmd/ndt7-client@latest \
    && cp /go/bin/ndt7-client /usr/local/bin/ndt7-client \
    && chmod +x /usr/local/bin/ndt7-client

RUN mkdir /app
COPY run-speedtest.py /app/
RUN chmod +x /app/run-speedtest.py

EXPOSE 9140

ENTRYPOINT [ "/app/run-speedtest.py" ]
