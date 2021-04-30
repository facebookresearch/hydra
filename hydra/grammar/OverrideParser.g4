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
    | PLUS PLUS? key EQUAL value?                // +key= | +key=value | ++key=value
) EOF;
// Key:
key : packageOrGroup (AT package)?;              // key | group@pkg

packageOrGroup: package | ID (SLASH ID)+;        // db, hydra/launcher
package: ( | ID | DOT_PATH);                     // db, hydra.launcher, or the empty (for _global_ package)

// Elements (that may be swept over).

value: element | simpleChoiceSweep;


// Composite text expression (may contain interpolations).



// Elements.

element:
      primitive
    | quotedValue
    | listContainer
    | dictContainer
    | function
;

simpleChoiceSweep:
      element (COMMA element)+                   // value1,value2,value3
;

// Functions.

argName: ID EQUAL;
function: ID POPEN (argName? element (COMMA argName? element )* )? PCLOSE;

// Data structures.

listContainer: BRACKET_OPEN sequence? BRACKET_CLOSE;                         // [], [1,2,3], [a,b,[1,2]]
dictContainer: BRACE_OPEN (dictKeyValuePair (COMMA dictKeyValuePair)*)? BRACE_CLOSE;  // {}, {a:10,b:20}
dictKeyValuePair: dictKey COLON element;
sequence: (element (COMMA element?)*) | (COMMA element?)+;


// Interpolations.

interpolation: interpolationNode | interpolationResolver;

interpolationNode:
      INTER_OPEN
      DOT*                                                     // relative interpolation?
      (configKey | BRACKET_OPEN configKey BRACKET_CLOSE)       // foo, [foo]
      (DOT configKey | BRACKET_OPEN configKey BRACKET_CLOSE)*  // .foo, [foo], .foo[bar], [foo].bar[baz]
      INTER_CLOSE;
interpolationResolver: INTER_OPEN resolverName COLON sequence? BRACE_CLOSE;
configKey: interpolation | ID | INTER_KEY;
resolverName: (interpolation | ID) (DOT (interpolation | ID))* ;  // oc.env, myfunc, ns.${x}, ns1.ns2.f


// Primitive types.

// Ex: "hello world", 'hello ${world}'
quotedValue:
    (QUOTE_OPEN_SINGLE | QUOTE_OPEN_DOUBLE)
    (interpolation | ESC | ESC_INTER | ESC_QUOTE | SPECIAL_CHAR | ANY_STR)*
    MATCHING_QUOTE_CLOSE;

primitive:
    (   ID                                     // foo_10
      | NULL                                   // null, NULL
      | INT                                    // 0, 10, -20, 1_000_000
      | FLOAT                                  // 3.14, -20.0, 1e-1, -10e3
      | BOOL                                   // true, TrUe, false, False
      | UNQUOTED_CHAR                          // /, -, \, +, ., $, %, *, @
      | COLON                                  // :
      | ESC                                    // \\, \(, \), \[, \], \{, \}, \:, \=, \ , \\t, \,
      | WS                                     // whitespaces
      | interpolation
    )+;

// Same as `primitive` except that `COLON` and interpolations are not allowed.
dictKey:
    (   ID                                     // foo_10
      | NULL                                   // null, NULL
      | INT                                    // 0, 10, -20, 1_000_000
      | FLOAT                                  // 3.14, -20.0, 1e-1, -10e3
      | BOOL                                   // true, TrUe, false, False
      | UNQUOTED_CHAR                          // /, -, \, +, ., $, %, *, @
      | ESC                                    // \\, \(, \), \[, \], \{, \}, \:, \=, \ , \\t, \,
      | WS                                     // whitespaces
    )+;
