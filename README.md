# beanhub-extract
The simple library for extracting all kind of bank account transaction export files, mostly for [beanhub-import](https://github.com/LaunchPlatform/beanhub-import) to ingest and generate transactions

**Note**: This project is still in early stage, still subject to rapid major changes

## Why?

Have you ever wondered why each of us has to write our own different Beancount importers for the same bank again and again?
Why we cannot use the same exporter for the same bank CSV file?
One of the biggest problems of the original Beancount importer design is that the transaction generation logic is coupled with the extract logic, making it hard to reuse.
We are addressing the problem by creating a library only for extracting bank-exported CSV files into standardized transaction structures to be processed later.
Ideally, you should be able to import this library and use it to import standardized transactions from CSV files exported from any bank in the world.

## Install

```bash
pip install beanhub-extract
```

## Example

Extracting transactions from the CSV file is easy.
Simply create the extractor class and make a function call on the instance object, which will return a transaction object generator.
Like this:

```python
from beanhub_extract.extractors.mercury import MercuryExtractor

with open("/path/to/my-mercury.csv", "rt") as fo:
    extractor = MercuryExtractor(fo)
    for txn in extractor():
        print(txn)
        # process your transaction here

```

## Sponsor

<p align="center">
  <a href="https://beanhub.io"><img src="https://github.com/LaunchPlatform/beanhub-extract/raw/master/assets/beanhub.svg?raw=true" alt="BeanHub logo" /></a>
</p>

A modern accounting book service based on the most popular open source version control system [Git](https://git-scm.com/) and text-based double entry accounting book software [Beancount](https://beancount.github.io/docs/index.html).

## Transaction data object

We defined a standardized transaction data object to accommodate a transaction statement's most commonly used columns.
The data object type is a simple immutable Python `dataclasses.dataclass` class.
It's defined in the [beanhub_extract/data_types.py](beanhub_extract/data_types.py) file.

## Supported Formats

Currently, we only support a few banks for our own benefit.
If you find any particular bank CSV file or format missing and want this library to support it, please feel free to open a PR.

### [Mercury](https://mercury.com/) - `mercury`

To export the CSV file, please visit the [Transactions](https://app.mercury.com/transactions) page and click "Add Filter" to limit the time range of your export, then click the "Export All" button on the right-hand side.
