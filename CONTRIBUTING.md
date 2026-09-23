# Contributing

* `main` is what is released; `develop` is where work lands. Open pull
  requests against `develop`.
* `pip install -e ".[dev]"` then `pytest` -- the suite runs without a server.
* The client speaks the protocol and nothing else: no application identity,
  no configuration, no import-time side effects. An embedding application
  passes what it needs as arguments (`headers=`, `access_token=`).
* Keep the wire module on the standard library. numpy stays confined to the
  parser.
