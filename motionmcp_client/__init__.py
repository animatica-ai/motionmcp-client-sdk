"""A client for the MMCP protocol: request a motion, read back a glTF.

:mod:`motionmcp_client.client` speaks the protocol over the standard library
alone -- no ``requests``, no ``httpx`` -- because the interpreters this runs
in are embedded in other applications and we do not own their site-packages.
:mod:`motionmcp_client.gltf_parser` turns the server's glTF 2.0 answer into
plain arrays; numpy is its only dependency.
"""

__version__ = "0.1.0"
