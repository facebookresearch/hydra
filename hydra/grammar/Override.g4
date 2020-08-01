// Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

// Regenerate parser by running 'python setup.py antlr' at project root.
// If you make changes here be sure to update the documentation (and update the grammar in command_line_syntax.md)
grammar Override;

override: (
      key '=' value?                             // key=value, key= (for empty value)
    | '~' key ('=' value?)?                      // ~key | ~key=value
    | '+' key '=' value?                         // +key= | +key=value
) EOF;

key :
    packageOrGroup                              // key
    | packageOrGroup '@' package (':' package)? // group@pkg | group@pkg1:pkg2
    | packageOrGroup '@:' package               // group@:pkg2
;

packageOrGroup: package | ID ('/' ID)+;         // db, hydra/launcher
package: (ID | DOT_PATH);                       // db, hydra.launcher

value: element | sweep;

element:
      primitive
    | listValue
    | dictValue
;

sweep:
      choiceSweep                               // choice(a,b,c)
    | simpleChoiceSweep                         // a,b,c
    | rangeSweep                                // range(1,10), range(0,3,0.5)
    | intervalSweep                             // interval(0,3)
    | castSweep
    | sortSweep
;


simpleChoiceSweep:
    element (',' element)+                        // value1,value2,value3
;

choiceSweep:
    'choice' '(' (
          (element | simpleChoiceSweep)                     // choice(a), choice(a,c)
        | 'list' '=' '[' (element | simpleChoiceSweep) ']'  // choice(list=[a,b,c])
    ) ')'
    | taggedChoiceSweep                             // tag(log,choice(1,10,100))
;

rangeSweep:                                         // range(start,stop,[step])
    'range' '('                                     // range(1,10), range(1,10,2)
        ('start' '=')? number ','                   // range(start=1,stop=10,step=2)
        ('stop' '=')? number
        (',' ('step' '=')? number)?')'
    | taggedRangeSweep
;

intervalSweep:                                      // interval(start,end)
    'interval' '('
        ('start' '=' )? number ','
        ('end' '='   )? number
    ')'
    | taggedIntervalSweep
;

taggedSweep:
    taggedChoiceSweep
    | taggedRangeSweep
    | taggedIntervalSweep
;

taggedChoiceSweep:
    'tag' '(' (tagList ',')? ('sweep' '=')? choiceSweep ')';

taggedRangeSweep:
    'tag' '(' (tagList ',')? ('sweep' '=')? rangeSweep ')';

taggedIntervalSweep:
    'tag' '(' (tagList ',')? ('sweep' '=')? intervalSweep ')';

tagList: ID (',' ID)* | 'tags' '=' '[' (ID (',' ID)*)? ']';

primitive:
      castPrimitive
    | QUOTED_VALUE                                 // 'hello world', "hello world"
    | (   ID                                        // foo_10
        | NULL                                      // null, NULL
        | INT                                       // 0, 10, -20, 1_000_000
        | FLOAT                                     // 3.14, -20.0, 1e-1, -10e3
        | BOOL                                      // true, TrUe, false, False
        | DOT_PATH                                  // foo.bar
        | INTERPOLATION                             // ${foo.bar}, ${env:USER,me}
        | '/' | ':' | '-' | '\\'
        | '+' | '.' | '$' | '*'
        | '='
    )+;


number: INT | FLOAT;

listValue:
      '[' (element(',' element)*)? ']'              // [], [1,2,3], [a,b,[1,2]]
    | sortList                                      // sort([1,2,3])
    | castList                                      // str([1,2,3])
;

dictValue:
      '{' (ID ':' element (',' ID ':' element)*)? '}'   // {}, {a:10,b:20}
    | castDict
;

cast : castPrimitive | castSweep | castList | castDict;
castSweep : ('int' | 'float' | 'str' | 'bool') '(' sweep ')';
castPrimitive : ('int' | 'float' | 'str' | 'bool') '(' primitive ')';
castList : ('int' | 'float' | 'str' | 'bool') '(' listValue ')';
castDict : ('int' | 'float' | 'str' | 'bool') '(' dictValue ')';

ordering: sort | shuffle;

sort : sortList | sortSweep;
sortList : 'sort' '(' ('list' '=')? listValue (',' 'reverse' '=' BOOL)? ')';
sortSweep : 'sort' '(' ('sweep' '=')? sweep (',' 'reverse' '=' BOOL)? ')';


shuffle:
    'shuffle' '('
          primitive (',' primitive)+
        | 'list' '=' '[' (primitive (',' primitive)*)? ']'
    ')'
;


// Types
fragment DIGIT: [0-9_];
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

fragment CHAR: [a-zA-Z];
ID : (CHAR|'_') (CHAR|DIGIT|'_')*;
fragment LIST_INDEX: '0' | [1-9][0-9]*;
DOT_PATH: (ID | LIST_INDEX) ('.' (ID | LIST_INDEX))+;

WS: (' ' | '\t')+ -> channel(HIDDEN);

QUOTED_VALUE:
      '\'' ('\\\''|.)*? '\''  // Single quoted string. can contain escaped single quote : /'
    | '"' ('\\"'|.)*? '"' ;   // Double quoted string. can contain escaped double quote : /"

INTERPOLATION:
    '${' (
          // interpolation
          (ID | DOT_PATH)
          // custom interpolation
        | ID ':' (ID | QUOTED_VALUE) (',' (ID | QUOTED_VALUE))*
    ) '}';

