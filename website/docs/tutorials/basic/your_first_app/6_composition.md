---
id: composition
title: Putting it all together
---

[![Example](https://img.shields.io/badge/-Example-informational)](https://github.com/facebookresearch/hydra/tree/master/examples/tutorials/basic/your_first_hydra_app/6_composition)

As software gets more complex, we resort to modularity and composition to keep it manageable. 
We can do the same with configs: suppose we want our working example to support multiple databases, with
multiple schemas per database, and different UIs. We wouldn't write a separate class
for each permutation of db, schema and UI, so we shouldn't write separate configs either. We use 
the same solution in configuration as in writing the underlying software: composition. 

To do this in Hydra, we first add a `schema` and a `ui` config group:

``` text title="Directory layout"
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

```yaml title="config.yaml"
defaults:
  - db: mysql
  - ui: full
  - schema: school
```

The resulting configuration would be a composition of `mysql`, `full` ui and the `school` database schema (which we are seeing for the first time here):
```yaml
$ python my_app.py
db:
  driver: mysql
  user: omry
  pass: secret
ui:
  windows:
    create_db: true
    view: true
schema:
  database: school
  tables:
  - name: students
    fields:
    - name: string
    - class: int
  - name: exams
    fields:
    - profession: string
    - time: data
    - class: int
```

### Summary
 - The addition of each new db, schema, or ui only requires a single file
 - Each config group can have a default specified in the `defaults` list
 - Any combination can be composed by selecting the desired option from each config group in the `defaults` list or the command line.

Stay tuned to see how to run all of the combinations automatically ([Multi-run](/tutorials/basic/running_your_app/2_multirun.md)).