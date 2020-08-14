// Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

// Regenerate lexer by running 'python setup.py antlr' at project root.
// If you make changes here be sure to update the documentation (and update the grammar in command_line_syntax.md)
lexer grammar OverrideLexer;


// Re-usable fragments.
fragment DIGIT: [0-9_];
fragment WS_: [ \t]+;

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

fragment CHAR: [a-zA-Z];
ID: (CHAR|'_') (CHAR|DIGIT|'_')*;
fragment LIST_INDEX: '0' | [1-9][0-9]*;
DOT_PATH: (ID | LIST_INDEX) ('.' (ID | LIST_INDEX))+;

WS: WS_ -> skip;

//////////
// ARGS //
//////////

mode ARGS;

PARENTHESIS_OPEN: WS_? '(' WS_?;  // whitespaces before to allow `func (x)`
COMMA: WS_? ',' WS_?;
PARENTHESIS_CLOSE: WS_? ')';
BRACKET_OPEN: '[' WS_?;
BRACKET_CLOSE: WS_? ']';
BRACE_OPEN: '{' WS_?;
BRACE_CLOSE: WS_? '}';
ARGS_COLON: WS_? ':' WS_? -> type(COLON);
ARGS_EQUAL: WS_? '=' WS_? -> type(EQUAL);

// Types
fragment NZ_DIGIT: [1-9];
fragment INT_PART: DIGIT+;
fragment FRACTION: '.' DIGIT+;
fragment POINT_FLOAT: INT_PART? FRACTION | INT_PART '.';
fragment EXPONENT: [eE] [+-]? DIGIT+;
fragment EXPONENT_FLOAT: ( INT_PART | POINT_FLOAT) EXPONENT;
FLOAT: [-]?(POINT_FLOAT | EXPONENT_FLOAT | [Ii][Nn][Ff] | [Nn][Aa][Nn]);
INT: [-]? ('0' | (NZ_DIGIT DIGIT*));

BOOL:
      [Tt][Rr][Uu][Ee]      // TRUE
    | [Ff][Aa][Ll][Ss][Ee]; // FALSE

NULL: [Nn][Uu][Ll][Ll];

OTHER_CHAR: [/\-\\+.$*];  // other characters allowed in unquoted strings
ARGS_ID: ID -> type(ID);
ARGS_DOT_PATH: DOT_PATH -> type(DOT_PATH);
ARGS_WS: WS_ -> type(WS);

QUOTED_VALUE:
      '\'' ('\\\''|.)*? '\'' // Single quotes, can contain escaped single quote : /'
    | '"' ('\\"'|.)*? '"' ;  // Double quotes, can contain escaped double quote : /"

INTERPOLATION:
    '${' (
          // interpolation
          (ID | DOT_PATH)
          // custom interpolation
        | ID ':' (ID | QUOTED_VALUE) (',' (ID | QUOTED_VALUE))*
    ) '}';