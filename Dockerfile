FROM alpine
RUN apk update
RUN apk add git make gcc git musl-dev
RUN apk add xorriso mtools squashfs-tools py3-yaml busybox unzip binutils wget
RUN apk add grub bash perl tar zstd coreutils dosfstools e2fsprogs util-linux 
RUN git clone https://gitlab.com/tearch-linux/applications-and-tools/teaiso /tmp/teaiso
RUN cd /tmp/teaiso && make && make install DESTDIR=/
RUN apk del git gcc git musl-dev
RUN rm -rf /tmp/teaiso
RUN mkdir -p /profile /output
CMD /usr/bin/mkteaiso -p /profile -o /output
