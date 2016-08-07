# yamlui

yamlui is a library to allow a user interface using pygame to be defined
in a set of yaml files.

Currently, only "Containers" and "Windows" are implemented.

## Examples

The examples directory contains some example UI definitions. When all of
them are usable, it will be good!

## Tests

At the moment, there is only a minimal test implemented. It can be run
using `PYTHONPATH="$PYTHONPATH:." python tests/minimal.py`, and will
render the UI defined by `examples/minimal.yaml`.
