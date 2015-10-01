Migration
=========

## Overview

Stronghold uses visibility columns to enforce row-level access control
to datastores. In order to migrate a datastore to Stronghold, it's
necessary to add these columns.

When migrating the data, a decision must be made as to which data
should be visible to which users. After this determination is made,
this script can be used to migrate the data.

## Example

Here's an example of a script using this library. It operates on the
index created by the <code>draft_lottery.py</code> program in the
<code>examples</code> directory. Both this script and that one require
the 'elasticsearch' python egg, which can be installed with the
following command:

    easy_install elasticsearch

The program itself has two levels of visibility: classified and
secret. In this case, we'll classify the final month of the draft
lottery secret, while allowing unrestricted access to the first 11
months.

```python
from elasticsearch import Elasticsearch
from ezbake.migration.elastic.visibility import EsMigrator
from ezbake.base.thriftapi.ttypes import Visibility

es = Elasticsearch()
migrator = EsMigrator(es, 'vtest')

unclassified = Visibility(formalVisibility='U')
secret = Visibility(formalVisibility='S')

# First 11 months are classified.
migrator.addVisibility('{"query":{"range":{"Mo.Number":{"lt":12}}}}',
                       'lottery',
                       visibility=unclassified)

# Last month is secret.
migrator.addVisibility('{"query":{"range":{"Mo.Number":{"gte":12}}}}',
                       'lottery',
                       visibility=secret)
                       

```