// Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

// Regenerate lexer by running 'python setup.py antlr' at project root.
// If you make changes here be sure to update the documentation
// (and update the grammar in website/docs/advanced/override_grammar/*.md)
lexer grammar OverrideLexer;


// Re-usable fragments.
fragment CHAR: [a-zA-Z];
fragment DIGIT: [0-9];
fragment INT_UNSIGNED: '0' | [1-9] (('_')? DIGIT)*;
fragment ESC_BACKSLASH: '\\\\';  // escaped backslash

////////////////////////
// DEFAULT_MODE (KEY) //
////////////////////////

EQUAL: '=' WS? -> mode(VALUE_MODE);

TILDE: '~';
PLUS: '+';
AT: '@';
COLON: ':';
SLASH: '/';

KEY_ID: ID -> type(ID);
DOT_PATH: (ID | INT_UNSIGNED) ('.' (ID | INT_UNSIGNED))+;

////////////////
// VALUE_MODE //
////////////////

mode VALUE_MODE;

INTER_OPEN: '${' WS? -> pushMode(INTERPOLATION_MODE);
BRACE_OPEN: '{' WS? -> pushMode(VALUE_MODE);  // must keep track of braces to detect end of interpolation
BRACE_CLOSE: WS? '}' -> popMode;
QUOTE_OPEN_SINGLE: '\'' -> pushMode(QUOTED_SINGLE_MODE);
QUOTE_OPEN_DOUBLE: '"' -> pushMode(QUOTED_DOUBLE_MODE);

POPEN: WS? '(' WS?;  // whitespaces before to allow `func (x)`
COMMA: WS? ',' WS?;
PCLOSE: WS? ')';
BRACKET_OPEN: '[' WS?;
BRACKET_CLOSE: WS? ']';
VALUE_COLON: WS? ':' WS? -> type(COLON);
VALUE_EQUAL: WS? '=' WS? -> type(EQUAL);

// Numbers.

fragment POINT_FLOAT: INT_UNSIGNED '.' | INT_UNSIGNED? '.' DIGIT (('_')? DIGIT)*;
fragment EXPONENT_FLOAT: (INT_UNSIGNED | POINT_FLOAT) [eE] [+-]? DIGIT (('_')? DIGIT)*;
FLOAT: [+-]? (POINT_FLOAT | EXPONENT_FLOAT | [Ii][Nn][Ff] | [Nn][Aa][Nn]);
INT: [+-]? INT_UNSIGNED;

// Other reserved keywords.

BOOL:
      [Tt][Rr][Uu][Ee]      // TRUE
    | [Ff][Aa][Ll][Ss][Ee]; // FALSE

NULL: [Nn][Uu][Ll][Ll];

UNQUOTED_CHAR: [/\-\\+.$%*@?];  // other characters allowed in unquoted strings
ID: (CHAR|'_') (CHAR|DIGIT|'_')*;
// Note: when adding more characters to the ESC rule below, also add them to
// the `_ESC` string in `_internal/grammar/utils.py`.
ESC: (ESC_BACKSLASH | '\\(' | '\\)' | '\\[' | '\\]' | '\\{' | '\\}' |
      '\\:' | '\\=' | '\\,' | '\\ ' | '\\\t')+;
WS: [ \t]+;


////////////////////////
// INTERPOLATION_MODE //
////////////////////////

mode INTERPOLATION_MODE;

NESTED_INTER_OPEN: INTER_OPEN WS? -> type(INTER_OPEN), pushMode(INTERPOLATION_MODE);
INTER_COLON: WS? ':' WS? -> type(COLON), mode(VALUE_MODE);
INTER_CLOSE: WS? '}' -> popMode;

DOT: '.';
INTER_BRACKET_OPEN: '[' -> type(BRACKET_OPEN);
INTER_BRACKET_CLOSE: ']' -> type(BRACKET_CLOSE);
INTER_ID: ID -> type(ID);

// Interpolation key, may contain any non special character.
// Note that we can allow '$' because the parser does not support interpolations that
// are only part of a key name, i.e., "${foo${bar}}" is not allowed. As a result, it
// is ok to "consume" all '$' characters within the `INTER_KEY` token.
INTER_KEY: ~[\\{}()[\]:. \t'"]+;


////////////////////////
// QUOTED_SINGLE_MODE //
////////////////////////

mode QUOTED_SINGLE_MODE;

// This mode is very similar to `DEFAULT_MODE` except for the handling of quotes.

QSINGLE_INTER_OPEN: INTER_OPEN -> type(INTER_OPEN), pushMode(INTERPOLATION_MODE);
MATCHING_QUOTE_CLOSE: '\'' -> popMode;

ESC_QUOTE: '\\\'';
QSINGLE_ESC_BACKSLASH: ESC_BACKSLASH -> type(ESC);
ESC_INTER: '\\${';


SPECIAL_CHAR: [\\$];
ANY_STR: ~['\\$]+;


////////////////////////
// QUOTED_DOUBLE_MODE //
////////////////////////

mode QUOTED_DOUBLE_MODE;

// Same as `QUOTED_SINGLE_MODE` but for double quotes.

QDOUBLE_INTER_OPEN: INTER_OPEN -> type(INTER_OPEN), pushMode(INTERPOLATION_MODE);
QDOUBLE_CLOSE: '"' -> type(MATCHING_QUOTE_CLOSE), popMode;

QDOUBLE_ESC_QUOTE: '\\"' -> type(ESC_QUOTE);
QDOUBLE_ESC_BACKSLASH: ESC_BACKSLASH -> type(ESC);
QDOUBLE_ESC_INTER: ESC_INTER -> type(ESC_INTER);

QDOUBLE_SPECIAL_CHAR: SPECIAL_CHAR -> type(SPECIAL_CHAR);
QDOUBLE_STR: ~["\\$]+ -> type(ANY_STR);
