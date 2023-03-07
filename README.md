# WhyLabs API scripts

# Prerequisites

1. poetry - https://python-poetry.org/
2. whylabs api key - https://docs.whylabs.ai/docs/whylabs-api/
3. whylabs org id - https://docs.whylabs.ai/docs/whylabs-capabilities#integration-examples
4. whylabs project (dataset/model) id

# How-to

1. clone this repo
2. run a script through poetry

```shell
$ poetry run python <script_name>
```

```shell
$ poetry run python update_column_schema.py --help
Usage: update_column_schema.py [OPTIONS]

  Gets current schema of a column and updates it to the values passed in.
...
```