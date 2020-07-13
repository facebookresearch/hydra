---
id: command_line_syntax
title: Command-line syntax
---
You can modify your configuration via the command line. This includes:
- Modifying the the `Defaults List`
- Modifying the config object

Command line overrides matching a Config group are modifying the `Defaults List`;
The rest are manipulating the config object.

## Basic examples
### Modifying the Config Object
- Overriding a config value : `foo.bar=value`
- Appending a config value : `+foo.bar=value`
- Removing a config value : `~foo.bar`, `~foo.bar=value`

### Modifying the Defaults List
- Overriding selected Option: `db=mysql`
- Changing a package: `db@src_pkg:dst_pkg`
- Overriding selected Option and changing the package: `db@src_pkg:dst_pkg=mysql`
- Appending to defaults: `+db=mysql`
- Deleting from defaults: `~db`, `~db=mysql`

## Grammar
Hydra supports a rich [DSL](https://en.wikipedia.org/wiki/Domain-specific_language) in the command line.   
Below are the lexical rules, and [description](#Description) of the grammar.
You can see the full grammar [here](https://github.com/facebookresearch/hydra/tree/master/hydra/grammar/Override.g4).

```antlrv4
grammar Override;

override: (
      key '=' value?                             // key=value
    | '~' key ('=' value?)?                      // ~key | ~key=value
    | '+' key '=' value?                         // +key= | +key=value
) EOF;

key :
    packageOrGroup                              // key
    | packageOrGroup '@' package (':' package)? // group@pkg | group@pkg1:pkg2
    | packageOrGroup '@:' package               // group@:pkg2
;

packageOrGroup: package | ID ('/' ID)+;         // db, hydra/launcher
package: (ID | DOT_PATH);                       // db, hydra.launcher

value: element | choiceSweep;
element:
      primitive
    | listValue
    | dictValue
;
choiceSweep: element (',' element)+;            // value1,value2,value3

primitive:
    WS? (QUOTED_VALUE |                         // 'hello world', "hello world"
        ( ID                                    // foo_10
        | NULL                                  // null, NULL
        | INT                                   // 0, 10, -20, 1_000_000
        | FLOAT                                 // 3.14, -20.0, 1e-1, -10e3
        | BOOL                                  // true, TrUe, false, False
        | DOT_PATH                              // foo.bar
        | INTERPOLATION                         // ${foo.bar}, ${env:USER,me}
        | '/' | ':' | '-' | '\\'
        | '+' | '.' | '$'
        )+
    )
    WS?;

listValue: '[' (element(',' element)*)? ']';    // [], [1,2,3], [a,b,[1,2]]
dictValue: '{'                                  // {}, {a:10,b:20}
    (id_ws ':' element (',' id_ws ':' element)*)?
'}';

id_ws: WS? ID WS?;
```
## Description
### Key
Key is the component before the =. A few examples:
```shell script
foo.bar           # A config key
hydra/launcher    # A config group
group@pkg         # A config group assigned to the package pkg
group@pkg1:pkg2   # A config group changing the package from pkg1 to pkg2
```

### Quoted values
Hydra supports both double quotes and single quoted values.
Quoted strings can accept any value between the quotes.
To include a single quote in a single quoted string escape it : `\'`. Same for double quote in a double quoted string.

<div className="row">
<div className="col col--6">

```python title="Double quotes"
"hello there"
"escaped \"double quote\""
"1,2,3"
"{a:10} ${xyz}"
"'single quoted string'"
```

</div>

<div className="col  col--6">

```python title="Single quotes"
'hello there'
'escaped \'single quote\''
'1,2,3'
'{a:10} ${xyz}'
'"double quoted string"'
```
</div>
</div>

 
### Primitives
- `id` : oompa10, loompa_12
- `null`: null
- `int`: 10, -20, 0, 1_000_000.
- `float`: 3.14, -10e6, inf, -inf, nan.
- `bool`: true, false
- `dot_path`: foo.bar
- `interpolation`: ${foo.bar}, ${env:USER,me}

Constants (null, true, false, inf, nan) are case insensitive. 

**IMPORTANT** Always single-quote interpolations in the shell.

### Lists
```python
foo=[1,2,3]
nested=[a,[b,[c]]]
```
**IMPORTANT** Always single-quote overrides that contains lists in the shell.

### Dictionaries
```python
foo={a:10,b:20}
nested={a:10,b:{c:30,d:40}}
```
**IMPORTANT** Always single-quote overrides that contains dicts in the shell.
### Sweeper syntax

A choice sweep is comma separated list with two or more elements: 
```shell script
key=a,b                       # Simple sweep: ChoiceSweep(a, b)
key="a,b","c,d"               # Elements can be quoted strings, ChoiceSweep("a,b", "c,d")
key=[a,b],[c,d]               # Elements can be real lists, ChoiceSweep([a,b], [c,d])
key={a:10, b:20},{c:30,d:40}  # and even dictionaries: ChoiceSweep([a,b], [c,d]){a,b}}
```

**IMPORTANT** You may need to quote your choice sweep in the shell

## Working with your shell
All interprets command line inputs and may what is passed to the process.
A good way to determine what the shell is doing to your command is to `echo` it.
```shell script
# bash output
$ echo foo_{a:10,b:20} ${HOME} [b,c]*
foo_a:10 foo_b:20 /home/omry build_helpers
$ echo 'foo_{a:10,b:20}' '${HOME}' '[b,c]*'
foo_{a:10,b:20} ${HOME} [b,c]*
```

If in doubt, quote a command line element with a **single quote** (`'`).  

If you want to pass quotes to Hydra in a shell quoted string, it's best to pass double quotes.
```shell script
$ echo '"hello world"'
"hello world"
```

You can use some shell specific commands to change their behavior, but the cost will be that their behavior will change.
### Bash
You can disable braces expansion, filename generation (globing) and hist expansion. Please note that this will change
your shell behavior for the current session. 
```shell script
$ set +o braceexpand -o noglob +o histexpand
$ echo key1={a:10,b:20} key2=${HOME} key=[b]*
key1={a:10,b:20} key2=/home/omry key=[b]*
# does not help with () though:
$  echo key=choice(a,b,c)
bash: syntax error near unexpected token '('
$ echo 'key=choice(a,b,c)'
key=choice(a,b,c)
```

### Other shells
Send a PR to add information about your favorite shell here.