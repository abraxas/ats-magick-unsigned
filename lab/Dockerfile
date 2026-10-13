FROM ubuntu:24.04 AS build

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        brotli \
        ca-certificates \
        cmake \
        g++ \
        libbrotli-dev \
        libcap-dev \
        libgomp1 \
        libhwloc-dev \
        libmagick++-dev \
        libpcre2-dev \
        libssl-dev \
        libxml2-dev \
        ninja-build \
        pkg-config \
        python3 \
        zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /src
COPY . /src

RUN cmake -B /build -G Ninja \
        -DCMAKE_BUILD_TYPE=Release \
        -DCMAKE_INSTALL_PREFIX=/opt/ats \
        -DBUILD_TESTING=OFF \
        -DBUILD_REGRESSION_TESTING=OFF \
        -DENABLE_AUTEST=OFF \
        -DENABLE_DOCS=OFF \
        -DENABLE_EXAMPLE=OFF \
        -DENABLE_QUICHE=OFF \
        -DENABLE_CRIPTS=OFF \
        -DENABLE_VERIFY_PLUGINS=OFF \
        -DBUILD_EXPERIMENTAL_PLUGINS=ON \
        -DENABLE_MAGICK=ON \
        -DENABLE_POSIX_CAP=ON \
        -DWITH_USER=nobody \
    && cmake --build /build --parallel 3 \
    && cmake --install /build \
    && test -f /opt/ats/libexec/trafficserver/magick.so \
    && test -x /opt/ats/bin/traffic_server

FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive
LABEL lab=ats-10.2.0-lab

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        libbrotli1 \
        libcap2 \
        libgomp1 \
        libhwloc15 \
        libmagick++-6.q16-9t64 \
        libmagickcore-6.q16-7t64 \
        libmagickwand-6.q16-7t64 \
        libpcre2-8-0 \
        libssl3t64 \
        libxml2 \
        zlib1g \
    && rm -rf /var/lib/apt/lists/*

COPY --from=build /opt/ats /opt/ats
COPY plugins/experimental/magick/keys/rsa256-public.key \
    /opt/ats/etc/trafficserver/rsa256-public.key

RUN mkdir -p /opt/ats/var/trafficserver /opt/ats/var/log/trafficserver /tmp/oracle \
    && chown -R nobody:nogroup /opt/ats/var /tmp/oracle \
    && chmod 1777 /tmp/oracle \
    && test -f /opt/ats/libexec/trafficserver/magick.so \
    && test -x /opt/ats/bin/traffic_server

ENV PATH="/opt/ats/bin:${PATH}"
WORKDIR /opt/ats
EXPOSE 8080
CMD ["traffic_server"]
