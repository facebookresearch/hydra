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
;

simpleChoiceSweep:
      element (',' element)+                      // value1,value2,value3
    | castSimpleChoiceSweep                       // float(1,2,3)
    | sortSimpleChoiceSweep                       // sort(a,b,c)
    | shuffleSimpleChoiceSweep                    // shuffle(a,b,c)
;

choiceSweep:
    'choice' '(' (
          (element | simpleChoiceSweep)                     // choice(a), choice(a,c)
        | 'list' '=' '[' (element | simpleChoiceSweep) ']'  // choice(list=[a,b,c])
    ) ')'
    | castChoiceSweep                                       // str(choice(1,2))
    | taggedChoiceSweep                                     // tag(log,choice(1,10,100))
    | sortChoiceSweep                                       // sort(choice(a,b))
    | shuffleChoiceSweep                                    // shuffle(choice(a,b))
;

rangeSweep:                                         // range(start,stop,[step])
    'range' '('                                     // range(1,10), range(1,10,2)
        ('start' '=')? number ','                   // range(start=1,stop=10,step=2)
        ('stop' '=')? number
        (',' ('step' '=')? number)?')'
    | castRangeSweep                                // float(range(1,10)) TODO: test
    | taggedRangeSweep                              // tag(a,b,range(1,10))
    | sortRangeSweep                                // sort(range(10,1))
    | shuffleRangeSweep                             // shuffle(range(1,10))
;

intervalSweep:                                      // interval(start,end)
    'interval' '('
        ('start' '=' )? number ','
        ('end' '='   )? number
    ')'
    | castIntervalSweep
    | taggedIntervalSweep
;



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
    | castList                                      // str([1,2,3])
    | sortList                                      // sort([1,2,3])
    | shuffleList                                   // shuffle([1,2,3])
;

dictValue:
      '{' (ID ':' element (',' ID ':' element)*)? '}'   // {}, {a:10,b:20}
    | castDict
;

castType: 'int' | 'float' | 'str' | 'bool';
castPrimitive:          castType '(' primitive         ')';
castList:               castType '(' listValue         ')';
castDict:               castType '(' dictValue         ')';
castChoiceSweep:        castType '(' choiceSweep       ')';
castSimpleChoiceSweep:  castType '(' simpleChoiceSweep ')';
castRangeSweep:         castType '(' rangeSweep        ')';
castIntervalSweep:      castType '(' intervalSweep     ')';


sortList : 'sort' '(' ('list' '=')? listValue (',' 'reverse' '=' BOOL)? ')';
sortSimpleChoiceSweep : 'sort' '(' ('sweep' '=')? simpleChoiceSweep (',' 'reverse' '=' BOOL)? ')';
sortChoiceSweep : 'sort' '(' ('sweep' '=')? choiceSweep (',' 'reverse' '=' BOOL)? ')';
sortRangeSweep : 'sort' '(' ('range' '=')? rangeSweep (',' 'reverse' '=' BOOL)? ')';

shuffleList : 'shuffle' '(' ('list' '=')? listValue ')';
shuffleSimpleChoiceSweep: 'shuffle' '(' simpleChoiceSweep ')';
shuffleChoiceSweep: 'shuffle' '(' ('sweep' '=')? choiceSweep ')';
shuffleRangeSweep: 'shuffle' '(' ('sweep' '=')? rangeSweep ')';


taggedChoiceSweep: 'tag' '(' (tagList ',')? ('sweep' '=')? choiceSweep ')';
taggedRangeSweep: 'tag' '(' (tagList ',')? ('sweep' '=')? rangeSweep ')';
taggedIntervalSweep: 'tag' '(' (tagList ',')? ('sweep' '=')? intervalSweep ')';

tagList: ID (',' ID)* | 'tags' '=' '[' (ID (',' ID)*)? ']';

// sorted sweeps and lists


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


// Testing support
cast:
      castPrimitive
    | castList
    | castDict
    | castChoiceSweep
    | castSimpleChoiceSweep
    | castRangeSweep
    | castIntervalSweep
;

sort : sortList | sortChoiceSweep | sortSimpleChoiceSweep | sortRangeSweep;
shuffle : shuffleList | shuffleSimpleChoiceSweep | shuffleChoiceSweep | shuffleRangeSweep;