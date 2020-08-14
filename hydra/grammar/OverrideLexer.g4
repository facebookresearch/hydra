// Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

// Regenerate lexer by running 'python setup.py antlr' at project root.
// If you make changes here be sure to update the documentation
// (and update the grammar in website/docs/advanced/override_grammar/*.md)
lexer grammar OverrideLexer;


// Re-usable fragments.
fragment DIGIT: [0-9];
fragment INT_UNSIGNED: '0' | [1-9] (('_')? DIGIT)*;

/////////
// KEY //
/////////

EQUAL: '=' WS? -> mode(VALUE_MODE);

TILDE: '~';
PLUS: '+';
AT: '@';
COLON: ':';
ATCOLON: '@:';
SLASH: '/';

fragment CHAR: [a-zA-Z];
ID: (CHAR|'_') (CHAR|DIGIT|'_')*;
fragment LIST_INDEX: '0' | [1-9][0-9]*;
DOT_PATH: (ID | LIST_INDEX) ('.' (ID | LIST_INDEX))+;

///////////
// VALUE //
///////////

mode VALUE_MODE;

POPEN: WS? '(' WS?;  // whitespaces before to allow `func (x)`
COMMA: WS? ',' WS?;
PCLOSE: WS? ')';
BRACKET_OPEN: '[' WS?;
BRACKET_CLOSE: WS? ']';
BRACE_OPEN: '{' WS?;
BRACE_CLOSE: WS? '}';
VALUE_COLON: WS? ':' WS? -> type(COLON);
VALUE_EQUAL: WS? '=' WS? -> type(EQUAL);

// Types

fragment POINT_FLOAT: INT_UNSIGNED '.' | INT_UNSIGNED? '.' DIGIT (('_')? DIGIT)*;
fragment EXPONENT_FLOAT: (INT_UNSIGNED | POINT_FLOAT) [eE] [+-]? INT_UNSIGNED;
FLOAT: [+-]? (POINT_FLOAT | EXPONENT_FLOAT | [Ii][Nn][Ff] | [Nn][Aa][Nn]);
INT: [+-]? INT_UNSIGNED;

BOOL:
      [Tt][Rr][Uu][Ee]      // TRUE
    | [Ff][Aa][Ll][Ss][Ee]; // FALSE

NULL: [Nn][Uu][Ll][Ll];

UNQUOTED_CHAR: [/\-\\+.$*];  // other characters allowed in unquoted strings
VALUE_ID: ID -> type(ID);
VALUE_DOT_PATH: DOT_PATH -> type(DOT_PATH);
WS: [ \t]+;

QUOTED_VALUE:
      '\'' ('\\\''|.)*? '\'' // Single quotes, can contain escaped single quote : /'
    | '"' ('\\"'|.)*? '"' ;  // Double quotes, can contain escaped double quote : /"

INTERPOLATION: '${' ~('}')+ '}';