# jomiel

`jomiel` is the meta inquiry middleware for distributed systems. It
returns meta data for content on [video-sharing][40] websites (e.g.
YouTube) and runs as a service, responding to client inquiries.

Two core technologies serve as a basis for `jomiel`:

- [Protocol Buffers][20] for platform-independent data serialization
- [ZeroMQ][21] as the messaging library

The client applications can be written in modern [languages][5] for most
platforms.

![Example (jomiel)](./docs/examples/jomiel-framed.svg)

## Table of Contents

<!-- vim-markdown-toc GFM -->

* [Features](#features)
* [Getting started](#getting-started)
    * [Website coverage](#website-coverage)
* [HOWTO](#howto)
* [Versioning](#versioning)
* [License](#license)
* [Acknowledgements](#acknowledgements)
    * [Subprojects](#subprojects)

<!-- vim-markdown-toc -->

## Features

- Plug-in system enabling customization to add support for media hosts
- Support for authentication and encryption (CURVE and SSH)
- [ZeroMQ][21] supports every modern language and platform
- [Protocol Buffers][20] are language-neutral, platform-neutral
- Highly configurable
- Runs as a service

## Getting started

- **`jomiel` requires [Python 3.5+][22]**

To install `jomiel` from from [PyPI][24]:

```shell
pip install jomiel        # For the latest release
jomiel                    # Starts the service
```

To run `jomiel` from the repository:

- Make sure you have installed protobuf compiler first (debian:
  protobuf-compiler)

```shell
git clone https://github.com/guendto/jomiel.git && cd jomiel
pip install -r ./requirements.txt
python setup.py build_py    # Generate the protobuf message bindings
python jomiel               # Starts the service
```

`jomiel` is still a young project. Once you have `jomiel` running, you
can experiment sending inquries to it:

- [examples][5] - the demo programs written in most modern languages
- [yomiel][1] - the pretty printer for `jomiel` messages

### Website coverage

```shell
jomiel --plugin-list    # List supported websites
```

The website coverage is currently very limited. The plugins can be
found in the jomiel/plugin/ directory.

- `jomiel` is written in [Python][22] which is an easy language to learn
- Additional support can be implemented by adding new plugins

**Notes for those considering contributing new plugins**

- Make sure the site is not dedicated to copyright infringement, be that
  they host the media or the link to it
- Make sure the site is not NSFW

## HOWTO

See [docs/HOWTO](./docs/HOWTO.md).

## Versioning

`jomiel` uses a custom versioning scheme. With each new release, the
release date (and time) will be used for the version number. `jomiel`
uses the format `yy.m.d` for version numbers.

**For example**

`2019-07-25` would become `19.7.25`. An additional number (time) will be
added to the version number, if another release was made on the same day
(e.g. `19.7.25` would become `19.7.25.1041`, "1041" being 10:41 for the
local time).

**The exception**

When run from the repository, the output of the `git-describe` and the
`git-show` command will be used for the version number, instead.

## License

`jomiel` is licensed under the [Apache License version 2.0][23] (APLv2).

## Acknowledgements

- Linted by [pylint][25], [flake8][26] and [yamllint][27]
- Formatted by [yapf][28]

### Subprojects

`jomiel` subtrees (includes) the following subprojects:

- [jomiel-proto.git][3] (jomiel/comm/proto)
- [jomiel-comm.git][2]  (jomiel/comm)
- [jomiel-kore.git][4]  (jomiel/kore)

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
[40]: https://en.wikipedia.org/wiki/Video_hosting_service
