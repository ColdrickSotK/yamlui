# yamlui

yamlui is a library to allow a user interface using pygame to be defined
in a set of yaml files.

## Widgets

### Currently Implemented

* Window
* Container
* Label
* Button
* Textbox

### Planned

* Slider
* RadioButton
* CheckBox

...

## Examples

The examples directory contains some example UI definitions. When all of
them are usable, it will be good!

## Tests

At the moment, there is only a minimal test implemented. It can be run
using `PYTHONPATH="$PYTHONPATH:." python tests/minimal.py`, and will
render the UI defined by `examples/minimal.yaml`.

Style checks can be run with `tox -e pep8`. It seems you will need pretty
new versions of tox and pip for this to work.
