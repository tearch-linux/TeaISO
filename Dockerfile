FROM alpine
RUN apk update
RUN apk add git make gcc git musl-dev
RUN apk add xorriso mtools squashfs-toolspy3-yaml busybox unzip binutils wgetutil-linux grub bash perl tar
RUN git clone https://gitlab.com/tearch-linux/applications-and-tools/teaiso /tmp/teaiso
RUN cd /tmp/teaiso && make && make install DESTDIR=/
RUN apk del git make gcc git musl-dev
RUN rm -rf /tmp/teaiso
RUN mkdir -p /profile /output
CMD /usr/bin/mkteaiso -p /profile -o /output
