---
id: composition
title: Config composition
sidebar_label: Config composition
---

The product manager had an idea:
She wants my_app to support creating arbitrary database schemas, on all supported databases!
She also wants to have two kinds of UI - a full UI to create and view databases and a view only UI.
You are the fall guy. Before you even start, she tells you the 3 existing customers want 3 different database schemas, and that there are more customers lined up.
You area already sweating because it all sounds pretty complex.
You also got a feeling that this is only the beginning - who knows what idea she will have next?

To solve it with Hydra, we need more config groups.
Add a `schema` and a `ui` config group:
```text
├── conf
│   ├── config.yaml
│   ├── db
│   │   ├── mysql.yaml
│   │   └── postgresql.yaml
│   ├── schema
│   │   ├── school.yaml
│   │   ├── support.yaml
│   │   └── warehouse.yaml
│   └── ui
│       ├── full.yaml
│       └── view.yaml
└── my_app.py
```

At this point, we already have 2 supported databases, 3 schemas, and 2 ui modes.
This is a total of 12 combinations. adding another supported database will bring this to 18 combinations.
Creating 18 files is not a good idea, if you wanted to make a change such as renaming `db.user` to `db.username` you would have to do it 18 times!

Composition can come to the rescue.

Configuration file: `config.yaml`
```yaml
defaults:
  - db: mysql
  - ui: full
  - schema: ???
```

We see something new here: `schema: ???`. `???` is a special string in OmegaCong which indicates that this key is mandatory and is missing right now.
While we can decide on a default database, a default schema makes less sense so this will require that a schema is selected in the command line.
Another important thing to note is that the defaults is ordered. if there are two configurations that defines
the same value, the second one would win. If two configurations are contributing to the same dictionary the result would be a combined dictionary.

When running this, 
```yaml
$ python my_app.py schema=school
db:
  driver: mysql
  pass: secret
  user: omry
schema:
  database: school
  tables:
  - fields:
    - name: string
    - class: int
    name: students
  - fields:
    - profession: string
    - time: data
    - class: int
    name: exams
ui:
  windows:
    create_db: true
    view: true
```

In much the same way you can compose any of the other 11 configurations and by adding additional command line overrides you can 
create completely new configurations.