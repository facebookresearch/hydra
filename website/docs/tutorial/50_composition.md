---
id: composition
title: Config composition
sidebar_label: Config composition
---

The product manager had an idea:
She wants my_app to support creating arbitrary database schemas, on all supported databases!
She also wants to have two kinds of UI - a full UI to create and view databases and a view only UI.
You are the fall guy. Before you even start, she tells you there are already 3 database schema you need to support, and more are coming soon.
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
The defaults is ordered. if there are two configurations that defines the same value, the second one would win. If two configurations are contributing to the same dictionary the result would be a combined dictionary.
We also see something new here: `schema: ???`. `???` is a special string which indicates that this key is mandatory and is missing right now.
You decided that mysql is the default database, but there is no good choice for a default schema here. This will require that the schema is 
specified in the command line. If it's not, an exception will be thrown when it's accessed. 

When running this, we will compose a configuration with mysql, full ui and the `school` database schema (which we are seeing for the first time here):
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