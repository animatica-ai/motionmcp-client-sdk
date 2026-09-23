# motionmcp-client-sdk

A Python client for the [MMCP protocol](https://github.com/animatica-ai/motionmcp):
ask a motion server for a motion, read the glTF it answers with.

Two modules, on purpose small:

* `motionmcp_client.client` speaks the protocol over the standard library
  alone. No `requests`, no `httpx` -- it is built to run inside interpreters
  embedded in other applications, whose site-packages nobody owns.
* `motionmcp_client.gltf_parser` turns the server's glTF 2.0 document into
  plain arrays. numpy is its only dependency.

## Install

```
pip install motionmcp-client-sdk
```

From a checkout, `pip install .`; for development, `pip install -e ".[dev]"`
and `pytest`. Releases are tags `vX.Y.Z` on `main`, published to PyPI by
`.github/workflows/publish.yml`.

Python 3.9 or newer. numpy is pinned by interpreter version (1.x below
Python 3.13, 2.x from 3.13 on) to match the wheels of GUI toolkits that
embed alongside it.

## API

```python
from motionmcp_client import client, gltf_parser

caps = client.get_capabilities("http://127.0.0.1:8000")   # cached per URL per session
model = client.pick_model(caps, wanted="kimodo")           # a model id from the capabilities
segments = client.model_supported_segments(model)         # which body segments it drives

doc = client.generate("http://127.0.0.1:8000", request_body,
                      access_token=None,                    # Bearer token, if the server wants one
                      headers={"X-My-App": "1.0"},          # merged after the standard headers
                      on_progress=print)                    # 202 + polling on the async path
samples = gltf_parser.parse_gltf_samples(doc)              # one motion_data dict per sample
```

* `get_capabilities`, `cached_capabilities`, `clear_capabilities_cache`
* `probe_server` -> `ProbeResult`, `retarget_state`
* `pick_model`, `model_supported_segments`
* `generate` -- handles both the synchronous `200` and the `202 Accepted`
  plus polling pattern; raises `MmcpError` on any transport or server failure.
  `headers` lets an embedding application attach its own identity; it rides on
  the request that starts a generation and on nothing else.
* `parse_gltf`, `parse_gltf_samples`, `xyzw_to_rotmat`

## Vendoring

Applications that cannot `pip install` into their interpreter copy the
`motionmcp_client/` directory next to their own code and record the commit
it came from. The package has no import-time side effects and no
configuration, so a copy is the whole thing.

## Where it comes from

This client was cut out of Animatica's private core on 2026-09-24; the
history before that lives there. Issues and pull requests here.

## License

MIT. See `LICENSE`.
