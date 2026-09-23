# Changelog

All notable changes to `motionmcp-client-sdk` are recorded here. The format
follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the
project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- First public cut, version 0.1.0: `motionmcp_client.client` (capabilities,
  probe, `generate` with the 200 / 202-and-poll paths, `headers=` for an
  embedding application's identity) and `motionmcp_client.gltf_parser`
  (`parse_gltf`, `parse_gltf_samples`, `xyzw_to_rotmat`). Standard library on
  the wire, numpy in the parser, Python 3.9+.
