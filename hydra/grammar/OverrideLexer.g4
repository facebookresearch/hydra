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
ATCOLON: '@:';
SLASH: '/';

KEY_ID: ID -> type(ID);
DOT_PATH: (ID | INT_UNSIGNED) ('.' (ID | INT_UNSIGNED))+;

////////////////
// VALUE_MODE //
////////////////

mode VALUE_MODE;

INTER_OPEN: '${' -> pushMode(INTERPOLATION_MODE);
BRACE_OPEN: '{' WS? -> pushMode(VALUE_MODE);  // must keep track of braces to detect end of interpolation
BRACE_CLOSE: WS? '}' -> popMode;

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

UNQUOTED_CHAR: [/\-\\+.$%*];  // other characters allowed in unquoted strings
ID: (CHAR|'_') (CHAR|DIGIT|'_')*;
ESC: (ESC_BACKSLASH | '\\(' | '\\)' | '\\[' | '\\]' | '\\{' | '\\}' |
      '\\:' | '\\=' | '\\,' | '\\ ' | '\\\t')+;
WS: [ \t]+;

QUOTED_VALUE:
      '\'' ('\\\''|.)*? '\'' // Single quotes, can contain escaped single quote : /'
    | '"' ('\\"'|.)*? '"' ;  // Double quotes, can contain escaped double quote : /"

////////////////////////
// INTERPOLATION_MODE //
////////////////////////

mode INTERPOLATION_MODE;

NESTED_INTER_OPEN: INTER_OPEN -> type(INTER_OPEN), pushMode(INTERPOLATION_MODE);
INTER_COLON: ':' WS? -> type(COLON), mode(VALUE_MODE);
INTER_CLOSE: '}' -> popMode;

DOT: '.';
INTER_ID: ID -> type(ID);
LIST_INDEX: INT_UNSIGNED;
INTER_WS: WS -> skip;
