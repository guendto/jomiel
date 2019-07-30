# jomiel

`jomiel` is the meta inquiry middleware for distributed systems. Two
core technologies serve as a basis for `jomiel`:

- [Protocol Buffers][20] for platform-independent data serialization
- [ZeroMQ][21] as the messaging library

## About

`jomiel` returns meta data for content on [video-sharing][30] websites
(e.g. YouTube). It runs as a service, responding to client inquiries.

The client applications can be written in modern [languages][5] for most
platforms.

## Features

- Plug-in system enabling customization to add support for media hosts
- Support for authentication and encryption (CURVE and SSH)
- [ZeroMQ][21] supports every modern language and platform
- [Protocol Buffers][20] are language-neutral, platform-neutral
- Highly configurable
- Runs as a service

## License

`jomiel` is licensed under the [Apache License version 2.0][23] (APLv2).

## Requirements

`jomiel` is written for [Python][22] 3.5 and later.

## Installation

You can install the latest version from either [PyPI][24] or from the
git repository.

### PyPI

```shell
$ pip install jomiel        # for the latest release
$ jomiel                    # starts the service
```

### git repository

Make sure you have installed the *protobuffer library* and the
*compiler*. For example, on Debian based systems these are the
`libprotobuf*` and the `protobuf-compiler` packages.

```shell
$ git clone https://github.com/guendto/jomiel.git
$ cd jomiel
$ pip install -r ./requirements.txt
$ python setup.py build_py  # generate the protobuf message bindings
$ python jomiel             # starts the service
```

## Experiment with it

`jomiel` is still a young project. Once you have `jomiel` running, you
can try one of the following to interact with it:

- [examples][5] - the demo programs written in most modern languages
- [yomiel][1] - the pretty printer for `jomiel` messages

They take an input URI to be inquired from `jomiel` and display the
returned meta data.

## Supported websites

The website coverage is currently very limited:

```shell
$ jomiel --plugin-list
```

The plugins can be found in the jomiel/plugin/ directory.

- `jomiel` is written in [Python][22] which is an easy language to learn
- Additional support can be implemented by adding new plugins

**Note**

- Make sure the site is not dedicated to copyright infringement, be that
  they host the media or the link to it

## Development notes

### Versioning

`jomiel` uses a custom versioning scheme. With each new release, the
release date (and time) will be used for the version number. `jomiel`
uses the format `yy.m.d` for version numbers.

**For example**

`2019-07-25` would become `19.7.25`. An additional number (time) will be
added to the version number, if another release was made on the same day
(e.g. `19.7.25` would become `19.7.25.1041`, 1041 would be 10:41 local
time).

**The exception**

When the program runs from the repository code, the output of the
`git-describe` and the `git-show` command will be used for the version
number.

### Subprojects

`jomiel` includes (as `git-subtree`) the following subprojects within
the subdirectories:

- [jomiel-proto.git][3] (jomiel/comm/proto)
- [jomiel-comm.git][2]  (jomiel/comm)
- [jomiel-kore.git][4]  (jomiel/kore)

### Acknowledgements

- Linted by [pylint][25], [flake8][26] and [yamllint][27]
- Formatted by [yapf][28]

[1]: https://github.com/guendto/jomiel-yomiel/
[2]: https://github.com/guendto/jomiel-comm/
[3]: https://github.com/guendto/jomiel-proto/
[4]: https://github.com/guendto/jomiel-kore/
[5]: https://github.com/guendto/jomiel-examples/
[20]: https://developers.google.com/protocol-buffers/
[21]: https://zeromq.org/
[22]: https://www.python.org/about/gettingstarted/
[23]: https://tldrlegal.com/license/apache-license-2.0-(apache-2.0)
[24]: https://pypi.org/
[25]: https://pypi.org/project/pylint/
[26]: https://pypi.org/project/flake8/
[27]: https://pypi.org/project/yamllint/
[28]: https://pypi.org/project/yapf/
[30]: https://en.wikipedia.org/wiki/Video_hosting_service
