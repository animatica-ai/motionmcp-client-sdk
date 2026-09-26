# Changelog

All notable changes to `motionmcp-client-sdk` are recorded here. The format
follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the
project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- GLB (`model/gltf-binary`) responses in `generate`, on the synchronous path
  and after a 202 alike, unpacked into
  the same glTF JSON document by the new `motionmcp_client.glb.glb_to_gltf`;
  the `Accept` header on `/generate` now advertises it.
- `MmcpError.details["retry_after"]` (seconds, from the `Retry-After` header)
  and `details["request_id"]` (from `X-Request-ID`, or `X-Job-Id` if that is
  absent) on HTTP failures. `details["status"]` is now present on every HTTP
  failure, also when the server's envelope brought its own `details` (never
  overwriting a `status` the server named).
- `tests/fake_server.py`, a real `ThreadingHTTPServer`-backed fake server for
  wire-level client tests.
- `ruff` and `mypy` as a separate `lint` job in CI.

### Changed
- `get_capabilities`/`cached_capabilities` cache key is now
  `(server_url, access_token)` instead of `(server_url, bool(access_token))`,
  so two accounts against the same server no longer share a cache entry.
- HTTP error handling is the same for `get_capabilities`, `generate` and the
  polling after a 202; the server's error envelope (`code`/`message`/`details`)
  is now read on every HTTP failure, not only on the initial `generate` request.
- As a result, `get_capabilities` and the polling after a 202 can now raise
  `MmcpError` with the code from the server's envelope (e.g. `forbidden`)
  where they used to raise `http_error` every time. `probe_server` still
  reports such a server as `"http_error"`: any code it has no status for but
  that carries an HTTP status in `details` counts as an HTTP failure, and only
  transport-level codes fall back to `"unreachable"`.
- HTTP 401 always maps to `code="auth_required"`, whatever code the server's
  envelope carried. The message is the envelope's when the server sent one;
  only without an envelope message is it the neutral
  "Authentication required (HTTP 401)."
- Docstrings in `motionmcp_client/client.py` no longer reference the private
  core this package was cut from.

### Fixed
- mypy findings in `motionmcp_client/client.py`.

### Removed
- The "Vendoring" section of the README. How a consumer lays this package
  into its interpreter is the consumer's concern, not this library's.

## [0.1.0] - 2026-09-24

### Added
- First public cut: `motionmcp_client.client` (capabilities,
  probe, `generate` with the 200 / 202-and-poll paths, `headers=` for an
  embedding application's identity) and `motionmcp_client.gltf_parser`
  (`parse_gltf`, `parse_gltf_samples`, `xyzw_to_rotmat`). Standard library on
  the wire, numpy in the parser, Python 3.9+.
