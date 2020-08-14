// Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

// Regenerate parser by running 'python setup.py antlr' at project root.
// If you make changes here be sure to update the documentation (and update the grammar in command_line_syntax.md)
parser grammar OverrideParser;
options {tokenVocab = OverrideLexer;}

override: (
      key EQUAL value?                           // key=value, key= (for empty value)
    | TILDE key (EQUAL value?)?                  // ~key | ~key=value
    | PLUS key EQUAL value?                      // +key= | +key=value
) EOF;

key :
    packageOrGroup                               // key
    | packageOrGroup AT package (COLON package)? // group@pkg | group@pkg1:pkg2
    | packageOrGroup ATCOLON package             // group@:pkg2
;

packageOrGroup: package | ID (SLASH ID)+;        // db, hydra/launcher
package: (ID | DOT_PATH);                        // db, hydra.launcher

value: element | simpleChoiceSweep;

element:
      primitive
    | listValue
    | dictValue
    | function
;

argName: ID EQUAL;
function: ID PARENTHESIS_OPEN
    (argName? element (COMMA argName? element )* )?
PARENTHESIS_CLOSE;

simpleChoiceSweep:
      element (COMMA element)+                   // value1,value2,value3
;
sequence: element (COMMA element)*;

primitive:
      QUOTED_VALUE                               // 'hello world', "hello world"
    | (   ID                                     // foo_10
        | NULL                                   // null, NULL
        | INT                                    // 0, 10, -20, 1_000_000
        | FLOAT                                  // 3.14, -20.0, 1e-1, -10e3
        | BOOL                                   // true, TrUe, false, False
        | INTERPOLATION                          // ${foo.bar}, ${env:USER,me}
        | OTHER_CHAR                             // /, -, \, +, ., $, *
        | COLON                                  // :
        | ESC                                    // \\, \, \ , \\t
        | WS                                     // whitespaces
    )+;

listValue: BRACKET_OPEN sequence? BRACKET_CLOSE;                          // [], [1,2,3], [a,b,[1,2]]
dictValue: BRACE_OPEN (keyValuePair (COMMA keyValuePair)*)? BRACE_CLOSE;  // {}, {a:10,b:20}
keyValuePair: ID COLON element;