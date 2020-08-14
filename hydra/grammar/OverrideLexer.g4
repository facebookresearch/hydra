// Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

// Regenerate lexer by running 'python setup.py antlr' at project root.
// If you make changes here be sure to update the documentation (and update the grammar in command_line_syntax.md)
lexer grammar OverrideLexer;


// Re-usable fragments.
fragment CHAR: [a-zA-Z];
fragment DIGIT: [0-9];
fragment INT_UNSIGNED: '0' | [1-9] (('_')? DIGIT)*;
fragment WS_: [ \t]+;
fragment ESC_BACKSLASH_: '\\\\';  // escaped backslash

/////////
// KEY //
/////////

mode KEY;

EQUAL: '=' WS_? -> mode(ARGS);

TILDE: '~';
PLUS: '+';
AT: '@';
COLON: ':';
ATCOLON: '@:';
SLASH: '/';

ID: (CHAR|'_') (CHAR|DIGIT|'_')*;
DOT_PATH: (ID | INT_UNSIGNED) ('.' (ID | INT_UNSIGNED))+;

WS: WS_ -> skip;

///////////////////
// INTERPOLATION //
///////////////////

mode INTERPOLATION;

INTERPOLATION_OPEN: '${' -> pushMode(INTERPOLATION);
INTER_COLON: ':' WS_? -> type(COLON), mode(ARGS);
INTERPOLATION_CLOSE: '}' -> popMode;

DOT: '.';
INTER_ID: ID -> type(ID);
LIST_INDEX: INT_UNSIGNED;
INTER_WS: WS_ -> skip;

//////////
// ARGS //
//////////

mode ARGS;

// Special characters.

ARGS_INTER_OPEN: INTERPOLATION_OPEN -> type(INTERPOLATION_OPEN), pushMode(INTERPOLATION);
BRACE_OPEN: '{' WS_? -> pushMode(ARGS);  // must keep track of braces to detect end of interpolation
BRACE_CLOSE: WS_? '}' -> popMode;

PARENTHESIS_OPEN: WS_? '(' WS_?;  // whitespaces before to allow `func (x)`
COMMA: WS_? ',' WS_?;
PARENTHESIS_CLOSE: WS_? ')';
BRACKET_OPEN: '[' WS_?;
BRACKET_CLOSE: WS_? ']';
ARGS_COLON: WS_? ':' WS_? -> type(COLON);
ARGS_EQUAL: WS_? '=' WS_? -> type(EQUAL);

// Numbers.

fragment POINT_FLOAT: INT_UNSIGNED? '.' DIGIT (('_')? DIGIT)* | INT_UNSIGNED '.';
fragment EXPONENT_FLOAT: (INT_UNSIGNED | POINT_FLOAT) [eE] [+-]? INT_UNSIGNED;
FLOAT: [+-]? (POINT_FLOAT | EXPONENT_FLOAT | [Ii][Nn][Ff] | [Nn][Aa][Nn]);
INT: [+-]? INT_UNSIGNED;

// Other reserved keywords.

BOOL:
      [Tt][Rr][Uu][Ee]      // TRUE
    | [Ff][Aa][Ll][Ss][Ee]; // FALSE

NULL: [Nn][Uu][Ll][Ll];

// Strings.

OTHER_CHAR: [/\-\\+.$*];  // other characters allowed in unquoted strings
ARGS_ID: ID -> type(ID);
ESC: (ESC_BACKSLASH_ | '\\,' | '\\ ' | '\\\t')+;

ARGS_WS: WS_ -> type(WS);

QUOTED_VALUE:
      '\'' ('\\\''|.)*? '\'' // Single quotes, can contain escaped single quote : /'
    | '"' ('\\"'|.)*? '"' ;  // Double quotes, can contain escaped double quote : /"
