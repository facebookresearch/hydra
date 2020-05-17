---
id: composition
title: Putting it all together
---

The product manager had an idea:
She wants my_app to support 3 schemas on 2 different databases and 2 kinds of UI for start. More will come later.

This is easy using config groups.  Each new schema, database, or UI will add a single config file to the corresponding 
config group.
Compare this to the common alternative of creating a separate config file for each combination.
The number of config files would then grow combinatorially.
Not only that, but if you wanted to make a change such as renaming `db.user` to `db.username` you would have to do it
 12 times instead of once!

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

### Summary
 - The addition of each new db, schema, or ui only requires a single file
 - Each config group can have a default specified in the `defaults` list
 - Any combination can be composed by selecting the desired option from each config group in the `defaults` list or the command line.

Stay tuned to see how to run all of the combinations automatically ([Multi-run](/tutorials/basic/6_multirun.md)).
