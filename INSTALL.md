Teaiso INSTALL
==============

**The ISO generation tool for GNU/Linux**

## Installation

For more information please consult the [doc/Installation.md](doc/Installation.md) document.

#### Local install

`git clone https://gitlab.com/tearch-linux/applications-and-tools/teaiso && make build && make install`

#### Network install

`wget https://gitlab.com/tearch-linux/applications-and-tools/teaiso/-/raw/master/netinstall -O - | bash`

#### Docker image install

`docker build -t teaiso .`

For building profile:

```shell
docker run --rm \
    -v /home/user/teaiso-profile:/profile \
    -v /home/user/teaiso-output:/output \
    --privileged\
    teaiso
```

## See also:

* [doc/Installation.md](doc/Installation.md)
* [doc/starting-use-case.md](doc/starting-use-case.md)
