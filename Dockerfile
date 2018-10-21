FROM docker.io/python:3.6.6

ENV OUTDIR "/build"

RUN pip install \
	grpcio-tools \
	googleapis-common-protos

WORKDIR /build

CMD python -m grpc_tools.protoc -I "${OUTDIR}" \
	--python_out="${OUTDIR}" \
	--grpc_python_out="${OUTDIR}" \
	*.proto
