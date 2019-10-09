# jomiel - HOWTO

## Use a proxy

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

## Authenticate and encrypt using CURVE

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

## Authenticate and encrypt using SSH

**jomiel (server-side)**

- Have SSH configured and running
- Have `jomiel` running

**yomiel (client-side)**

```shell
yomiel --auth-mode ssh --ssh-server user@host:port URI
```

**Notes**

- Have either  [pexpect][29] or [paramiko][30] (recommended) installed
- Use --ssh-paramiko to tell `yomiel` to use it
