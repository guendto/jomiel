# jomiel

`jomiel` is the meta inquiry middleware for distributed systems. It
returns meta data for content on [video-sharing][40] websites (e.g.
YouTube) and runs as a service, responding to client inquiries.

Two core technologies serve as a basis for `jomiel`:

- [Protocol Buffers][20] for platform-independent data serialization
- [ZeroMQ][21] as the messaging library

The client applications can be written in modern [languages][5] for most
platforms.

## Features

- Plug-in system enabling customization to add support for media hosts
- Support for authentication and encryption (CURVE and SSH)
- [ZeroMQ][21] supports every modern language and platform
- [Protocol Buffers][20] are language-neutral, platform-neutral
- Highly configurable
- Runs as a service

## Example

![Example (jomiel)](./docs/examples/jomiel-framed.svg)

## License

`jomiel` is licensed under the [Apache License version 2.0][23] (APLv2).

## Requirements

`jomiel` is written for [Python][22] 3.5 and later.

## Installation

You can install the latest version from either [PyPI][24] or from the
git repository.

### PyPI

```shell
pip install jomiel        # for the latest release
jomiel                    # starts the service
```

### git repository

Make sure you have installed the *protobuffer library* and the
*compiler*. For example, on Debian based systems these are the
`libprotobuf*` and the `protobuf-compiler` packages.

```shell
git clone https://github.com/guendto/jomiel.git
cd jomiel
pip install -r ./requirements.txt
python setup.py build_py  # generate the protobuf message bindings
python jomiel             # starts the service
```

## Status

Keep in mind that `jomiel` is still a young project. Once you have
`jomiel` running, try:

- [examples][5] - the demo programs written in most modern languages
- [yomiel][1] - the pretty printer for `jomiel` messages

To pass input URIs to inquire and display the meta data from `jomiel`.
See also [Development: Supported websites](#supported-websites).

## HOWTO

### Use a proxy

If you need to use a proxy with HTTP connections, you can configure
proxies by setting the environment variables http_proxy and https_proxy.

```shell
export https_proxy="https://localhost:3128"
```

**"In addition to basic HTTP proxies, Requests also supports proxies using
the SOCKS protocol. This is an optional feature that requires that
additional third-party libraries be installed before use."** --
[python-requests.org][41]

```shell
pip install requests[socks]
```

Once you’ve installed those dependencies, using a SOCKS proxy is just as
easy as using a HTTP one:

```shell
export https_proxy="socks5://localhost:5580"
```

The proxy string can be specified with a protocol:// prefix to specify
an alternative proxy protocol (e.g. "socks4://", "socks4a://",
"socks5://" or "socks5h://").

For more information, see the [documentation][42].

### Authenticate and encrypt using CURVE

**"[CURVE is] ... a protocol for secure messaging across the
Internet."** -- [curvezmq.org][43]

Generate a new public and secret CURVE keypair for both server (jomiel)
and client (yomiel):

```shell
jomiel-keygen server client
```

**jomiel (server-side)**

```shell
mkdir -p .curve
mv server.secret_key .curve   # Make server CURVE secret key usable
mv client.key .curve          # Make client CURVE public key usable
jomiel --curve-enable         # Restart jomiel with CURVE enabled
```

`jomiel` will search .curve/ dir for both (allowed) client public keys
and the server secret key. To change the default behaviour, you can use:

    --curve-server-key-file
    --curve-public-key-dir

**yomiel (client-side)**

```shell
mkdir -p .curve
mv client.secret_key .curve   # Make client CURVE secret key usable
mv server.key .curve          # Make server CURVE public key usable
yomiel --auth-mode curve URI  # Start yomiel with CURVE enabled
```

`yomiel` will search .curve/ dir for both the client secret key
and the server public key. To change the default behaviour, you can use:

    --curve-server-public-key-file
    --curve-client-key-file

### Authenticate and encrypt using SSH

**jomiel (server-side)**

- Make sure you have configured SSH server and it is running
- Make sure `jomiel` is running

**yomiel (client-side)**

```shell
yomiel --auth-mode ssh --ssh-server user@host:port URI
```

**Notes**

- Make sure you have installed either [pexpect][29] or [paramiko][30]
  (recommended)
- You can tell `yomiel` to use [paramiko][30] (--ssh-paramiko)

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

### Supported websites

The website coverage is currently very limited:

```shell
jomiel --plugin-list
```

The plugins can be found in the jomiel/plugin/ directory.

- `jomiel` is written in [Python][22] which is an easy language to learn
- Additional support can be implemented by adding new plugins

**Notes**

- Make sure the site is not dedicated to copyright infringement, be that
  they host the media or the link to it
- Make sure the site is not NSFW

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
[29]: https://pypi.org/project/pexpect/
[30]: https://pypi.org/project/paramiko/
[40]: https://en.wikipedia.org/wiki/Video_hosting_service
[41]: https://2.python-requests.org/
[42]: https://2.python-requests.org/en/master/user/advanced/#proxies
[43]: http://curvezmq.org
