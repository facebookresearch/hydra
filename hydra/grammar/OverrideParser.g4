// Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

// Regenerate parser by running 'python setup.py antlr' at project root.
// If you make changes here be sure to update the documentation
// (and update the grammar in website/docs/advanced/override_grammar/*.md)
parser grammar OverrideParser;
options {tokenVocab = OverrideLexer;}

// High-level command-line override.

override: (
      key EQUAL value?                           // key=value, key= (for empty value)
    | TILDE key (EQUAL value?)?                  // ~key | ~key=value
    | PLUS key EQUAL value?                      // +key= | +key=value
) EOF;

// Keys.

key :
    packageOrGroup                               // key
    | packageOrGroup AT package (COLON package)? // group@pkg | group@pkg1:pkg2
    | packageOrGroup ATCOLON package             // group@:pkg2
;

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
