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
KEY_SPECIAL: (CHAR|'_'|'$') (CHAR|DIGIT|'_'|'$')*;  // same as ID but allowing $
DOT_PATH: (KEY_SPECIAL | INT_UNSIGNED) ('.' (KEY_SPECIAL | INT_UNSIGNED))+;

////////////////
// VALUE_MODE //
////////////////

mode VALUE_MODE;

QUOTE_OPEN_SINGLE: '\'' -> pushMode(QUOTED_SINGLE_MODE);
QUOTE_OPEN_DOUBLE: '"' -> pushMode(QUOTED_DOUBLE_MODE);

POPEN: WS? '(' WS?;  // whitespaces before to allow `func (x)`
COMMA: WS? ',' WS?;
PCLOSE: WS? ')';
BRACKET_OPEN: '[' WS?;
BRACKET_CLOSE: WS? ']';
BRACE_OPEN: '{' WS?;
BRACE_CLOSE: WS? '}';
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

INTERPOLATION: '${' ~('}')+ '}';


////////////////////////
// QUOTED_SINGLE_MODE //
////////////////////////

mode QUOTED_SINGLE_MODE;

MATCHING_QUOTE_CLOSE: '\'' -> popMode;

ESC_QUOTE: '\\\'';
QSINGLE_ESC_BACKSLASH: ESC_BACKSLASH -> type(ESC);

QSINGLE_INTERPOLATION: INTERPOLATION -> type(INTERPOLATION);
SPECIAL_CHAR: [\\$];
ANY_STR: ~['\\$]+;


////////////////////////
// QUOTED_DOUBLE_MODE //
////////////////////////

mode QUOTED_DOUBLE_MODE;

// Same as `QUOTED_SINGLE_MODE` but for double quotes.

QDOUBLE_CLOSE: '"' -> type(MATCHING_QUOTE_CLOSE), popMode;

QDOUBLE_ESC_QUOTE: '\\"' -> type(ESC_QUOTE);
QDOUBLE_ESC_BACKSLASH: ESC_BACKSLASH -> type(ESC);

QDOUBLE_INTERPOLATION: INTERPOLATION -> type(INTERPOLATION);
QDOUBLE_SPECIAL_CHAR: SPECIAL_CHAR -> type(SPECIAL_CHAR);
QDOUBLE_STR: ~["\\$]+ -> type(ANY_STR);
