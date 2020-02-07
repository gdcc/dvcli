# dvcli
An experiment in creating an all-in-one CLI application for using and administrating Dataverse

## Installation

For now, being an experiment without any releases, simply:

- `git clone` this repository
- Create a virtualenv or use [asdf](https://asdf-vm.io) to create non-system python env
- Run `pip install --editable .` from the cloned repo root to install
- Run `dvcli`
- When hacking on the files, you can simply run the tool again - the choosen
  installation method enables magically using it without reinstall.

## Ideas

- Can be extended by others using https://github.com/click-contrib/click-plugins.
  Adding support here is easy. That way we can split efforts but still have a
  common ground.
