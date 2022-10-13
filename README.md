![](docs/logo.png)

# dvcli

An experiment in creating an all-in-one CLI application for using and administrating Dataverse

See also community mailing list: https://groups.google.com/forum/#!topic/dataverse-community/etN5URWos44

## Installation

This tool requires Python v3.8 or newer.

For now, being an experiment without any releases, simply:

```
pip install git+https://github.com/gdcc/dvcli.git
```

## Plugins

A list of available plugins, which extend `dvcli` in fields beyond core scope:

- Kubernetes: https://github.com/poikilotherm/dvcli-plugin-k8s

## Development

- (Optional) Install [`pre-commit`](https://pre-commit.com) if not already present on your system.
- `git clone` this repository
- (Optional) Install commit hooks for [`pre-commit`](https://pre-commit.com) via `pre-commit install`
- Install [`poetry`](https://python-poetry.org/docs/#installation) as your build system
- Run `poetry install` (creates a virtual environment for you, too)
- Run `poetry run dvcli`
- When hacking on the files, there is no need to re-run the install, only when changing dependencies.

## Configuration

All parameters, options etc for any command can be given via:

1. Defaults (within the app)
2. YAML configuration file in operating system locations
3. YAML configuration file at any arbitrary location (use `--config` or `DVCLI_CONFIG=...`)
4. Environment variable with prefix `DVCLI_`
5. Commandline option.

The order of appearance above corresponds to the priority of the source, lowest
to highest. Values are merged according to their priority. Key hashes in YAML files
are merged, but not arrays or hash values (so no deep merge).

## Ideas

- Can be extended by others using a standard python plugin mechanism via entry points.
  More extensive documentation to come, you can take a look at this codebase as an example.
- Create a command to set database configuration options in an idempotent manner.
- Maybe add a XML generator for JVM options to ease their configuration?
