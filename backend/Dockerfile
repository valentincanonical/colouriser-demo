FROM ubuntu:20.04 AS build

RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip python3.8-venv

RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt

FROM ubuntu:20.04
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 libgl1 libglib2.0-0 python3-distutils && \
    apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/* /tmp/library-scripts/

COPY --from=build /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app/
COPY . .

ENV GRPC_ADDRESS=127.0.0.1
ENV GRPC_PORT=9001

ENTRYPOINT [ "/opt/venv/bin/python3" ]
CMD [ "backend.py" ]
