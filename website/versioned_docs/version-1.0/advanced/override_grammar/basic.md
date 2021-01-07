---
id: basic
hide_title: true
sidebar_label: Basic Override syntax
---
## Basic Override syntax
You can manipulate your configuration with overrides (via the command line or the Compose API). This includes:
- Modifying the the `Defaults List`
- Modifying the config object

Overrides matching a config group are modifying the `Defaults List`;
The rest are manipulating the config object.

## Basic examples
### Modifying the Config Object
- Overriding a config value : `foo.bar=value`
- Appending a config value : `+foo.bar=value`
- Removing a config value : `~foo.bar`, `~foo.bar=value`

### Modifying the Defaults List
- Overriding selected Option: `db=mysql`
- Appending to defaults: `+db=mysql`
- Deleting from defaults: `~db`, `~db=mysql`

## Grammar
Hydra supports a rich [DSL](https://en.wikipedia.org/wiki/Domain-specific_language) in the command line.
Below are the parser rules from grammar.
You can see the full grammar on GitHub
([lexer](https://github.com/facebookresearch/hydra/tree/master/hydra/grammar/OverrideLexer.g4) and
[parser](https://github.com/facebookresearch/hydra/tree/master/hydra/grammar/OverrideParser.g4)).

```antlr4 title="OverrideParser.g4"
// High-level command-line override.

override: (
      key EQUAL value?                           // key=value, key= (for empty value)
    | TILDE key (EQUAL value?)?                  // ~key | ~key=value
    | PLUS key EQUAL value?                      // +key= | +key=value
) EOF;

// Keys.

key : packageOrGroup (AT package)?;              // key | group@pkg

packageOrGroup: package | ID (SLASH ID)+;        // db, hydra/launcher
package: (ID | DOT_PATH);                        // db, hydra.launcher

// Elements (that may be swept over).

value: element | simpleChoiceSweep;

element:
      primitive
    | listValue
    | dictValue
    | function
;

simpleChoiceSweep:
      element (COMMA element)+                   // value1,value2,value3
;

// Functions.

argName: ID EQUAL;
function: ID POPEN (argName? element (COMMA argName? element )* )? PCLOSE;

// Data structures.

listValue: BRACKET_OPEN                          // [], [1,2,3], [a,b,[1,2]]
    (element(COMMA element)*)?
BRACKET_CLOSE;

dictValue: BRACE_OPEN (dictKeyValuePair (COMMA dictKeyValuePair)*)? BRACE_CLOSE;  // {}, {a:10,b:20}
dictKeyValuePair: ID COLON element;

// Primitive types.

primitive:
      QUOTED_VALUE                               // 'hello world', "hello world"
    | (   ID                                     // foo_10
        | NULL                                   // null, NULL
        | INT                                    // 0, 10, -20, 1_000_000
        | FLOAT                                  // 3.14, -20.0, 1e-1, -10e3
        | BOOL                                   // true, TrUe, false, False
        | INTERPOLATION                          // ${foo.bar}, ${env:USER,me}
        | UNQUOTED_CHAR                          // /, -, \, +, ., $, %, *, @
        | COLON                                  // :
        | ESC                                    // \\, \(, \), \[, \], \{, \}, \:, \=, \ , \\t, \,
        | WS                                     // whitespaces
    )+;
```

## Elements
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

### Whitespaces in unquoted values
Unquoted Override values can contain non leading or trailing whitespaces.
For example, `msg=hello world` is a legal override (key is `msg` and value is the string `hello world`).
Normally, your shell will interpret values with whitespaces as being multiple parameters (`key=a b` would be interpreted as `key=a` and `b`).
To prevent this you can quote them with a single quote. For example:

```shell
$ python my_app.py 'msg=hello world'
```

Note that trailing and leading whitespace are ignored, the above is equivalent to:

```shell
$ python my_app.py 'msg=    hello world    '
```

### Escaped characters in unquoted values
Some otherwise special characters may be included in unquoted values by escaping them with a `\`.
These characters are: `\()[]{}:=, \t` (the last two ones being the whitespace and tab characters).

As an example, in the following `dir` is set to the string `job{a=1,b=2,c=3}`:

```shell
$ python my_app.py 'dir=job\{a\=1\,b\=2\,c\=3\}'
```

### Primitives
- `id` : oompa10, loompa_12
- `null`: null
- `int`: 10, -20, 0, 1_000_000.
- `float`: 3.14, -10e6, inf, -inf, nan.
- `bool`: true, false
- `dot_path`: foo.bar
- `interpolation`: ${foo.bar}, ${env:USER,me}

Constants (null, true, false, inf, nan) are case insensitive.

:::important
Always single-quote interpolations in the shell.
:::

## Dictionaries and Lists

### Lists
```python
foo=[1,2,3]
nested=[a,[b,[c]]]
```

### Dictionaries
```python
foo={a:10,b:20}
nested={a:10,b:{c:30,d:40}}
```

Dictionaries are merged, not assigned. The following example illustrates the point:
<div className="row">
<div className="col col--6">

```yaml title="Input config"
db:
  driver: mysql
  user: ???
  pass: ???
```

</div>

<div className="col  col--6">


```yaml title="db={user:root,pass:1234}"
db:
  driver: mysql
  user: root
  pass: 1234
```

</div>
</div>


:::important
Always single-quote overrides that contains dicts and lists in the shell.
:::

### Sweeper syntax
A choice sweep is comma separated list with two or more elements:
```shell script
key=a,b                       # Simple sweep: ChoiceSweep(a, b)
key="a,b","c,d"               # Elements can be quoted strings, ChoiceSweep("a,b", "c,d")
key=[a,b],[c,d]               # Elements can be real lists, ChoiceSweep([a,b], [c,d])
key={a:10, b:20},{c:30,d:40}  # And dictionaries: ChoiceSweep({a:10, b:20}, {c:30,d:40})
```
More sweeping options are described in the [Extended Grammar page](extended).

:::important
You may need to quote your choice sweep in the shell.
:::


### Functions
Hydra supports several functions in the command line.
See the [Extended Grammar page](extended) for more information.

## Working with your shell
All shells interprets command line inputs and may change what is passed to the process.
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
$ echo key=choice(a,b,c)
bash: syntax error near unexpected token '('
$ echo 'key=choice(a,b,c)'
key=choice(a,b,c)
```

### Other shells
Send a PR to add information about your favorite shell here.
