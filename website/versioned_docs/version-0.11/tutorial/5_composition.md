---
id: composition
title: Config composition
sidebar_label: Config composition
---

As software gets more complex, we resort to modularity and composition to keep it manageable. 
We can do the same with configs: suppose we want our working example to support multiple databases, with
multiple schemas per database, and different UIs. We wouldn't write a separate class
for each permutation of db, schema and UI, so we shouldn't write separate configs either. We use 
the same solution in configuration as in writing the underlying software: composition. 

To do this in Hydra, we first add a `schema` and a `ui` config group:
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

With these configs, we already have 12 possible combinations. Without composition we would need 12 separate configs, 
and a single change (such as renaming `db.user` to `db.username`) would need to be done separately in every one of them. 

This is a maintainability nightmare -- but composition can come to the rescue.

Configuration file: `config.yaml`
```yaml
defaults:
  - db: mysql
  - ui: full
  - schema: school
```
The defaults are ordered:
 * If there are two configurations that defines the same value, the second one would win. 
 * If two configurations are contributing to the same dictionary the result would be the combined dictionary.

When running this, we will compose a configuration with `mysql`, `full` ui and the `school` database schema (which we are seeing for the first time here):
```yaml
$ python my_app.py
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

In much the same way you can compose any of the other 11 configurations by adding appropriate overrides such as `db=postgresql`.
