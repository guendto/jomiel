# jomiel

`jomiel` is the meta inquiry middleware for distributed systems. It
returns meta data for content on [video-sharing] websites (e.g.
YouTube) and runs as a service responding to client inquiries.

Two core technologies serve as a basis for `jomiel`:

- [Protocol Buffers] for platform-independent data serialization
- [ZeroMQ] as the messaging library

The client applications can be written in modern [languages][examples]
for most platforms.

`jomiel` is a spiritual successor to (now defunct) [libquvi].

![Example (jomiel)](./docs/demo.svg)

## Table of Contents

<!-- vim-markdown-toc GFM -->

- [Features](#features)
- [Getting started](#getting-started)
  - [Website coverage](#website-coverage)
  - [If you are contributing new plugins](#if-you-are-contributing-new-plugins)
- [HOWTO](#howto)
- [License](#license)
- [Acknowledgements](#acknowledgements)
  - [Subprojects](#subprojects)

<!-- vim-markdown-toc -->

## Features

- Customizable plugin system for adding support for video-sharing
  websites

- Messaging ([Protocol Buffers]) is language-neutral and
  platform-neutral

- Support for authentication and encryption (CURVE and SSH)

- [ZeroMQ] supports every modern language and platform

- Runs fully as a service

- Highly configurable

## Getting started

- `jomiel` requires [Python] 3.6+

To install `jomiel` from from [PyPI]:

```shell
pip install jomiel        # For the latest release
jomiel                    # Starts the service
```

To run `jomiel` from the repository:

```shell
git clone https://github.com/guendto/jomiel.git
cd jomiel
pip install -e .
jomiel                    # Starts the service
```

`jomiel` is still a young project. Once you have `jomiel` running, you
can try sending inquiries with:

- [examples] - the demo programs written in most modern languages
- [yomiel] - the pretty printer for `jomiel` messages

### Website coverage

```shell
jomiel --plugin-list    # List supported websites
```

The video-sharing website coverage is still very limited.

- `jomiel` is written in [Python] which is an easy language to learn
- Additional support can be implemented by adding new plugins

See the jomiel/plugin/ directory for the existing plugins.

### If you are contributing new plugins

- Make sure the site is not dedicated to copyright infringement (be that
  they host the media or the link to it)

- Make sure the site is not NSFW

## HOWTO

See [docs/HOWTO](./docs/HOWTO.md).

## License

`jomiel` is licensed under the [Apache License version 2.0][aplv2].

## Acknowledgements

`jomiel` uses [pre-commit] and its many hooks to lint and format the
project files. See the .pre-commit-config.yaml file for details.

### Subprojects

`jomiel` has the following subtrees (see git-subtree):

- [src/jomiel/comm/](src/jomiel/comm/) of [jomiel-comm]
- [src/jomiel/kore/](src/jomiel/kore/) of [jomiel-kore]

[video-sharing]: https://en.wikipedia.org/wiki/Video_hosting_service
[protocol buffers]: https://developers.google.com/protocol-buffers/
[examples]: https://github.com/guendto/jomiel-examples/
[python]: https://www.python.org/about/gettingstarted/
[jomiel-comm]: https://github.com/guendto/jomiel-comm/
[jomiel-kore]: https://github.com/guendto/jomiel-kore/
[yomiel]: https://github.com/guendto/jomiel-yomiel/
[aplv2]: https://www.tldrlegal.com/l/apache2
[pre-commit]: https://pre-commit.com/
[libquvi]: http://quvi.sf.net/
[zeromq]: https://zeromq.org/
[pypi]: https://pypi.org/
