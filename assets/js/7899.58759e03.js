"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[7899],{27899:(t,e,s)=>{s.d(e,{D:()=>l,S:()=>c,a:()=>h,b:()=>a,c:()=>o,d:()=>B,p:()=>r,s:()=>P});var i=s(86079),n=function(){var t=function(t,e,s,i){for(s=s||{},i=t.length;i--;s[t[i]]=e);return s},e=[1,2],s=[1,3],i=[1,4],n=[2,4],r=[1,9],o=[1,11],a=[1,15],c=[1,16],l=[1,17],h=[1,18],u=[1,30],d=[1,19],p=[1,20],y=[1,21],f=[1,22],m=[1,23],g=[1,25],S=[1,26],_=[1,27],k=[1,28],T=[1,29],b=[1,32],E=[1,33],x=[1,34],C=[1,35],$=[1,31],v=[1,4,5,15,16,18,20,21,23,24,25,26,27,28,32,34,36,37,41,44,45,46,47,50],D=[1,4,5,13,14,15,16,18,20,21,23,24,25,26,27,28,32,34,36,37,41,44,45,46,47,50],A=[4,5,15,16,18,20,21,23,24,25,26,27,28,32,34,36,37,41,44,45,46,47,50],L={trace:function(){},yy:{},symbols_:{error:2,start:3,SPACE:4,NL:5,SD:6,document:7,line:8,statement:9,classDefStatement:10,cssClassStatement:11,idStatement:12,DESCR:13,"--\x3e":14,HIDE_EMPTY:15,scale:16,WIDTH:17,COMPOSIT_STATE:18,STRUCT_START:19,STRUCT_STOP:20,STATE_DESCR:21,AS:22,ID:23,FORK:24,JOIN:25,CHOICE:26,CONCURRENT:27,note:28,notePosition:29,NOTE_TEXT:30,direction:31,acc_title:32,acc_title_value:33,acc_descr:34,acc_descr_value:35,acc_descr_multiline_value:36,classDef:37,CLASSDEF_ID:38,CLASSDEF_STYLEOPTS:39,DEFAULT:40,class:41,CLASSENTITY_IDS:42,STYLECLASS:43,direction_tb:44,direction_bt:45,direction_rl:46,direction_lr:47,eol:48,";":49,EDGE_STATE:50,STYLE_SEPARATOR:51,left_of:52,right_of:53,$accept:0,$end:1},terminals_:{2:"error",4:"SPACE",5:"NL",6:"SD",13:"DESCR",14:"--\x3e",15:"HIDE_EMPTY",16:"scale",17:"WIDTH",18:"COMPOSIT_STATE",19:"STRUCT_START",20:"STRUCT_STOP",21:"STATE_DESCR",22:"AS",23:"ID",24:"FORK",25:"JOIN",26:"CHOICE",27:"CONCURRENT",28:"note",30:"NOTE_TEXT",32:"acc_title",33:"acc_title_value",34:"acc_descr",35:"acc_descr_value",36:"acc_descr_multiline_value",37:"classDef",38:"CLASSDEF_ID",39:"CLASSDEF_STYLEOPTS",40:"DEFAULT",41:"class",42:"CLASSENTITY_IDS",43:"STYLECLASS",44:"direction_tb",45:"direction_bt",46:"direction_rl",47:"direction_lr",49:";",50:"EDGE_STATE",51:"STYLE_SEPARATOR",52:"left_of",53:"right_of"},productions_:[0,[3,2],[3,2],[3,2],[7,0],[7,2],[8,2],[8,1],[8,1],[9,1],[9,1],[9,1],[9,2],[9,3],[9,4],[9,1],[9,2],[9,1],[9,4],[9,3],[9,6],[9,1],[9,1],[9,1],[9,1],[9,4],[9,4],[9,1],[9,2],[9,2],[9,1],[10,3],[10,3],[11,3],[31,1],[31,1],[31,1],[31,1],[48,1],[48,1],[12,1],[12,1],[12,3],[12,3],[29,1],[29,1]],performAction:function(t,e,s,i,n,r,o){var a=r.length-1;switch(n){case 3:return i.setRootDoc(r[a]),r[a];case 4:this.$=[];break;case 5:"nl"!=r[a]&&(r[a-1].push(r[a]),this.$=r[a-1]);break;case 6:case 7:case 11:this.$=r[a];break;case 8:this.$="nl";break;case 12:const t=r[a-1];t.description=i.trimColon(r[a]),this.$=t;break;case 13:this.$={stmt:"relation",state1:r[a-2],state2:r[a]};break;case 14:const e=i.trimColon(r[a]);this.$={stmt:"relation",state1:r[a-3],state2:r[a-1],description:e};break;case 18:this.$={stmt:"state",id:r[a-3],type:"default",description:"",doc:r[a-1]};break;case 19:var c=r[a],l=r[a-2].trim();if(r[a].match(":")){var h=r[a].split(":");c=h[0],l=[l,h[1]]}this.$={stmt:"state",id:c,type:"default",description:l};break;case 20:this.$={stmt:"state",id:r[a-3],type:"default",description:r[a-5],doc:r[a-1]};break;case 21:this.$={stmt:"state",id:r[a],type:"fork"};break;case 22:this.$={stmt:"state",id:r[a],type:"join"};break;case 23:this.$={stmt:"state",id:r[a],type:"choice"};break;case 24:this.$={stmt:"state",id:i.getDividerId(),type:"divider"};break;case 25:this.$={stmt:"state",id:r[a-1].trim(),note:{position:r[a-2].trim(),text:r[a].trim()}};break;case 28:this.$=r[a].trim(),i.setAccTitle(this.$);break;case 29:case 30:this.$=r[a].trim(),i.setAccDescription(this.$);break;case 31:case 32:this.$={stmt:"classDef",id:r[a-1].trim(),classes:r[a].trim()};break;case 33:this.$={stmt:"applyClass",id:r[a-1].trim(),styleClass:r[a].trim()};break;case 34:i.setDirection("TB"),this.$={stmt:"dir",value:"TB"};break;case 35:i.setDirection("BT"),this.$={stmt:"dir",value:"BT"};break;case 36:i.setDirection("RL"),this.$={stmt:"dir",value:"RL"};break;case 37:i.setDirection("LR"),this.$={stmt:"dir",value:"LR"};break;case 40:case 41:this.$={stmt:"state",id:r[a].trim(),type:"default",description:""};break;case 42:case 43:this.$={stmt:"state",id:r[a-2].trim(),classes:[r[a].trim()],type:"default",description:""}}},table:[{3:1,4:e,5:s,6:i},{1:[3]},{3:5,4:e,5:s,6:i},{3:6,4:e,5:s,6:i},t([1,4,5,15,16,18,21,23,24,25,26,27,28,32,34,36,37,41,44,45,46,47,50],n,{7:7}),{1:[2,1]},{1:[2,2]},{1:[2,3],4:r,5:o,8:8,9:10,10:12,11:13,12:14,15:a,16:c,18:l,21:h,23:u,24:d,25:p,26:y,27:f,28:m,31:24,32:g,34:S,36:_,37:k,41:T,44:b,45:E,46:x,47:C,50:$},t(v,[2,5]),{9:36,10:12,11:13,12:14,15:a,16:c,18:l,21:h,23:u,24:d,25:p,26:y,27:f,28:m,31:24,32:g,34:S,36:_,37:k,41:T,44:b,45:E,46:x,47:C,50:$},t(v,[2,7]),t(v,[2,8]),t(v,[2,9]),t(v,[2,10]),t(v,[2,11],{13:[1,37],14:[1,38]}),t(v,[2,15]),{17:[1,39]},t(v,[2,17],{19:[1,40]}),{22:[1,41]},t(v,[2,21]),t(v,[2,22]),t(v,[2,23]),t(v,[2,24]),{29:42,30:[1,43],52:[1,44],53:[1,45]},t(v,[2,27]),{33:[1,46]},{35:[1,47]},t(v,[2,30]),{38:[1,48],40:[1,49]},{42:[1,50]},t(D,[2,40],{51:[1,51]}),t(D,[2,41],{51:[1,52]}),t(v,[2,34]),t(v,[2,35]),t(v,[2,36]),t(v,[2,37]),t(v,[2,6]),t(v,[2,12]),{12:53,23:u,50:$},t(v,[2,16]),t(A,n,{7:54}),{23:[1,55]},{23:[1,56]},{22:[1,57]},{23:[2,44]},{23:[2,45]},t(v,[2,28]),t(v,[2,29]),{39:[1,58]},{39:[1,59]},{43:[1,60]},{23:[1,61]},{23:[1,62]},t(v,[2,13],{13:[1,63]}),{4:r,5:o,8:8,9:10,10:12,11:13,12:14,15:a,16:c,18:l,20:[1,64],21:h,23:u,24:d,25:p,26:y,27:f,28:m,31:24,32:g,34:S,36:_,37:k,41:T,44:b,45:E,46:x,47:C,50:$},t(v,[2,19],{19:[1,65]}),{30:[1,66]},{23:[1,67]},t(v,[2,31]),t(v,[2,32]),t(v,[2,33]),t(D,[2,42]),t(D,[2,43]),t(v,[2,14]),t(v,[2,18]),t(A,n,{7:68}),t(v,[2,25]),t(v,[2,26]),{4:r,5:o,8:8,9:10,10:12,11:13,12:14,15:a,16:c,18:l,20:[1,69],21:h,23:u,24:d,25:p,26:y,27:f,28:m,31:24,32:g,34:S,36:_,37:k,41:T,44:b,45:E,46:x,47:C,50:$},t(v,[2,20])],defaultActions:{5:[2,1],6:[2,2],44:[2,44],45:[2,45]},parseError:function(t,e){if(!e.recoverable){var s=new Error(t);throw s.hash=e,s}this.trace(t)},parse:function(t){var e=this,s=[0],i=[],n=[null],r=[],o=this.table,a="",c=0,l=0,h=r.slice.call(arguments,1),u=Object.create(this.lexer),d={yy:{}};for(var p in this.yy)Object.prototype.hasOwnProperty.call(this.yy,p)&&(d.yy[p]=this.yy[p]);u.setInput(t,d.yy),d.yy.lexer=u,d.yy.parser=this,void 0===u.yylloc&&(u.yylloc={});var y=u.yylloc;r.push(y);var f=u.options&&u.options.ranges;"function"==typeof d.yy.parseError?this.parseError=d.yy.parseError:this.parseError=Object.getPrototypeOf(this).parseError;for(var m,g,S,_,k,T,b,E,x,C={};;){if(g=s[s.length-1],this.defaultActions[g]?S=this.defaultActions[g]:(null==m&&(x=void 0,"number"!=typeof(x=i.pop()||u.lex()||1)&&(x instanceof Array&&(x=(i=x).pop()),x=e.symbols_[x]||x),m=x),S=o[g]&&o[g][m]),void 0===S||!S.length||!S[0]){var $="";for(k in E=[],o[g])this.terminals_[k]&&k>2&&E.push("'"+this.terminals_[k]+"'");$=u.showPosition?"Parse error on line "+(c+1)+":\n"+u.showPosition()+"\nExpecting "+E.join(", ")+", got '"+(this.terminals_[m]||m)+"'":"Parse error on line "+(c+1)+": Unexpected "+(1==m?"end of input":"'"+(this.terminals_[m]||m)+"'"),this.parseError($,{text:u.match,token:this.terminals_[m]||m,line:u.yylineno,loc:y,expected:E})}if(S[0]instanceof Array&&S.length>1)throw new Error("Parse Error: multiple actions possible at state: "+g+", token: "+m);switch(S[0]){case 1:s.push(m),n.push(u.yytext),r.push(u.yylloc),s.push(S[1]),m=null,l=u.yyleng,a=u.yytext,c=u.yylineno,y=u.yylloc;break;case 2:if(T=this.productions_[S[1]][1],C.$=n[n.length-T],C._$={first_line:r[r.length-(T||1)].first_line,last_line:r[r.length-1].last_line,first_column:r[r.length-(T||1)].first_column,last_column:r[r.length-1].last_column},f&&(C._$.range=[r[r.length-(T||1)].range[0],r[r.length-1].range[1]]),void 0!==(_=this.performAction.apply(C,[a,l,c,d.yy,S[1],n,r].concat(h))))return _;T&&(s=s.slice(0,-1*T*2),n=n.slice(0,-1*T),r=r.slice(0,-1*T)),s.push(this.productions_[S[1]][0]),n.push(C.$),r.push(C._$),b=o[s[s.length-2]][s[s.length-1]],s.push(b);break;case 3:return!0}}return!0}},I={EOF:1,parseError:function(t,e){if(!this.yy.parser)throw new Error(t);this.yy.parser.parseError(t,e)},setInput:function(t,e){return this.yy=e||this.yy||{},this._input=t,this._more=this._backtrack=this.done=!1,this.yylineno=this.yyleng=0,this.yytext=this.matched=this.match="",this.conditionStack=["INITIAL"],this.yylloc={first_line:1,first_column:0,last_line:1,last_column:0},this.options.ranges&&(this.yylloc.range=[0,0]),this.offset=0,this},input:function(){var t=this._input[0];return this.yytext+=t,this.yyleng++,this.offset++,this.match+=t,this.matched+=t,t.match(/(?:\r\n?|\n).*/g)?(this.yylineno++,this.yylloc.last_line++):this.yylloc.last_column++,this.options.ranges&&this.yylloc.range[1]++,this._input=this._input.slice(1),t},unput:function(t){var e=t.length,s=t.split(/(?:\r\n?|\n)/g);this._input=t+this._input,this.yytext=this.yytext.substr(0,this.yytext.length-e),this.offset-=e;var i=this.match.split(/(?:\r\n?|\n)/g);this.match=this.match.substr(0,this.match.length-1),this.matched=this.matched.substr(0,this.matched.length-1),s.length-1&&(this.yylineno-=s.length-1);var n=this.yylloc.range;return this.yylloc={first_line:this.yylloc.first_line,last_line:this.yylineno+1,first_column:this.yylloc.first_column,last_column:s?(s.length===i.length?this.yylloc.first_column:0)+i[i.length-s.length].length-s[0].length:this.yylloc.first_column-e},this.options.ranges&&(this.yylloc.range=[n[0],n[0]+this.yyleng-e]),this.yyleng=this.yytext.length,this},more:function(){return this._more=!0,this},reject:function(){return this.options.backtrack_lexer?(this._backtrack=!0,this):this.parseError("Lexical error on line "+(this.yylineno+1)+". You can only invoke reject() in the lexer when the lexer is of the backtracking persuasion (options.backtrack_lexer = true).\n"+this.showPosition(),{text:"",token:null,line:this.yylineno})},less:function(t){this.unput(this.match.slice(t))},pastInput:function(){var t=this.matched.substr(0,this.matched.length-this.match.length);return(t.length>20?"...":"")+t.substr(-20).replace(/\n/g,"")},upcomingInput:function(){var t=this.match;return t.length<20&&(t+=this._input.substr(0,20-t.length)),(t.substr(0,20)+(t.length>20?"...":"")).replace(/\n/g,"")},showPosition:function(){var t=this.pastInput(),e=new Array(t.length+1).join("-");return t+this.upcomingInput()+"\n"+e+"^"},test_match:function(t,e){var s,i,n;if(this.options.backtrack_lexer&&(n={yylineno:this.yylineno,yylloc:{first_line:this.yylloc.first_line,last_line:this.last_line,first_column:this.yylloc.first_column,last_column:this.yylloc.last_column},yytext:this.yytext,match:this.match,matches:this.matches,matched:this.matched,yyleng:this.yyleng,offset:this.offset,_more:this._more,_input:this._input,yy:this.yy,conditionStack:this.conditionStack.slice(0),done:this.done},this.options.ranges&&(n.yylloc.range=this.yylloc.range.slice(0))),(i=t[0].match(/(?:\r\n?|\n).*/g))&&(this.yylineno+=i.length),this.yylloc={first_line:this.yylloc.last_line,last_line:this.yylineno+1,first_column:this.yylloc.last_column,last_column:i?i[i.length-1].length-i[i.length-1].match(/\r?\n?/)[0].length:this.yylloc.last_column+t[0].length},this.yytext+=t[0],this.match+=t[0],this.matches=t,this.yyleng=this.yytext.length,this.options.ranges&&(this.yylloc.range=[this.offset,this.offset+=this.yyleng]),this._more=!1,this._backtrack=!1,this._input=this._input.slice(t[0].length),this.matched+=t[0],s=this.performAction.call(this,this.yy,this,e,this.conditionStack[this.conditionStack.length-1]),this.done&&this._input&&(this.done=!1),s)return s;if(this._backtrack){for(var r in n)this[r]=n[r];return!1}return!1},next:function(){if(this.done)return this.EOF;var t,e,s,i;this._input||(this.done=!0),this._more||(this.yytext="",this.match="");for(var n=this._currentRules(),r=0;r<n.length;r++)if((s=this._input.match(this.rules[n[r]]))&&(!e||s[0].length>e[0].length)){if(e=s,i=r,this.options.backtrack_lexer){if(!1!==(t=this.test_match(s,n[r])))return t;if(this._backtrack){e=!1;continue}return!1}if(!this.options.flex)break}return e?!1!==(t=this.test_match(e,n[i]))&&t:""===this._input?this.EOF:this.parseError("Lexical error on line "+(this.yylineno+1)+". Unrecognized text.\n"+this.showPosition(),{text:"",token:null,line:this.yylineno})},lex:function(){var t=this.next();return t||this.lex()},begin:function(t){this.conditionStack.push(t)},popState:function(){return this.conditionStack.length-1>0?this.conditionStack.pop():this.conditionStack[0]},_currentRules:function(){return this.conditionStack.length&&this.conditionStack[this.conditionStack.length-1]?this.conditions[this.conditionStack[this.conditionStack.length-1]].rules:this.conditions.INITIAL.rules},topState:function(t){return(t=this.conditionStack.length-1-Math.abs(t||0))>=0?this.conditionStack[t]:"INITIAL"},pushState:function(t){this.begin(t)},stateStackSize:function(){return this.conditionStack.length},options:{"case-insensitive":!0},performAction:function(t,e,s,i){switch(s){case 0:return 40;case 1:case 39:return 44;case 2:case 40:return 45;case 3:case 41:return 46;case 4:case 42:return 47;case 5:case 6:case 8:case 9:case 10:case 11:case 51:case 53:case 59:break;case 7:case 74:return 5;case 12:case 29:return this.pushState("SCALE"),16;case 13:case 30:return 17;case 14:case 20:case 31:case 46:case 49:this.popState();break;case 15:return this.begin("acc_title"),32;case 16:return this.popState(),"acc_title_value";case 17:return this.begin("acc_descr"),34;case 18:return this.popState(),"acc_descr_value";case 19:this.begin("acc_descr_multiline");break;case 21:return"acc_descr_multiline_value";case 22:return this.pushState("CLASSDEF"),37;case 23:return this.popState(),this.pushState("CLASSDEFID"),"DEFAULT_CLASSDEF_ID";case 24:return this.popState(),this.pushState("CLASSDEFID"),38;case 25:return this.popState(),39;case 26:return this.pushState("CLASS"),41;case 27:return this.popState(),this.pushState("CLASS_STYLE"),42;case 28:return this.popState(),43;case 32:this.pushState("STATE");break;case 33:case 36:return this.popState(),e.yytext=e.yytext.slice(0,-8).trim(),24;case 34:case 37:return this.popState(),e.yytext=e.yytext.slice(0,-8).trim(),25;case 35:case 38:return this.popState(),e.yytext=e.yytext.slice(0,-10).trim(),26;case 43:this.pushState("STATE_STRING");break;case 44:return this.pushState("STATE_ID"),"AS";case 45:case 61:return this.popState(),"ID";case 47:return"STATE_DESCR";case 48:return 18;case 50:return this.popState(),this.pushState("struct"),19;case 52:return this.popState(),20;case 54:return this.begin("NOTE"),28;case 55:return this.popState(),this.pushState("NOTE_ID"),52;case 56:return this.popState(),this.pushState("NOTE_ID"),53;case 57:this.popState(),this.pushState("FLOATING_NOTE");break;case 58:return this.popState(),this.pushState("FLOATING_NOTE_ID"),"AS";case 60:return"NOTE_TEXT";case 62:return this.popState(),this.pushState("NOTE_TEXT"),23;case 63:return this.popState(),e.yytext=e.yytext.substr(2).trim(),30;case 64:return this.popState(),e.yytext=e.yytext.slice(0,-8).trim(),30;case 65:case 66:return 6;case 67:return 15;case 68:return 50;case 69:return 23;case 70:return e.yytext=e.yytext.trim(),13;case 71:return 14;case 72:return 27;case 73:return 51;case 75:return"INVALID"}},rules:[/^(?:default\b)/i,/^(?:.*direction\s+TB[^\n]*)/i,/^(?:.*direction\s+BT[^\n]*)/i,/^(?:.*direction\s+RL[^\n]*)/i,/^(?:.*direction\s+LR[^\n]*)/i,/^(?:%%(?!\{)[^\n]*)/i,/^(?:[^\}]%%[^\n]*)/i,/^(?:[\n]+)/i,/^(?:[\s]+)/i,/^(?:((?!\n)\s)+)/i,/^(?:#[^\n]*)/i,/^(?:%[^\n]*)/i,/^(?:scale\s+)/i,/^(?:\d+)/i,/^(?:\s+width\b)/i,/^(?:accTitle\s*:\s*)/i,/^(?:(?!\n||)*[^\n]*)/i,/^(?:accDescr\s*:\s*)/i,/^(?:(?!\n||)*[^\n]*)/i,/^(?:accDescr\s*\{\s*)/i,/^(?:[\}])/i,/^(?:[^\}]*)/i,/^(?:classDef\s+)/i,/^(?:DEFAULT\s+)/i,/^(?:\w+\s+)/i,/^(?:[^\n]*)/i,/^(?:class\s+)/i,/^(?:(\w+)+((,\s*\w+)*))/i,/^(?:[^\n]*)/i,/^(?:scale\s+)/i,/^(?:\d+)/i,/^(?:\s+width\b)/i,/^(?:state\s+)/i,/^(?:.*<<fork>>)/i,/^(?:.*<<join>>)/i,/^(?:.*<<choice>>)/i,/^(?:.*\[\[fork\]\])/i,/^(?:.*\[\[join\]\])/i,/^(?:.*\[\[choice\]\])/i,/^(?:.*direction\s+TB[^\n]*)/i,/^(?:.*direction\s+BT[^\n]*)/i,/^(?:.*direction\s+RL[^\n]*)/i,/^(?:.*direction\s+LR[^\n]*)/i,/^(?:["])/i,/^(?:\s*as\s+)/i,/^(?:[^\n\{]*)/i,/^(?:["])/i,/^(?:[^"]*)/i,/^(?:[^\n\s\{]+)/i,/^(?:\n)/i,/^(?:\{)/i,/^(?:%%(?!\{)[^\n]*)/i,/^(?:\})/i,/^(?:[\n])/i,/^(?:note\s+)/i,/^(?:left of\b)/i,/^(?:right of\b)/i,/^(?:")/i,/^(?:\s*as\s*)/i,/^(?:["])/i,/^(?:[^"]*)/i,/^(?:[^\n]*)/i,/^(?:\s*[^:\n\s\-]+)/i,/^(?:\s*:[^:\n;]+)/i,/^(?:[\s\S]*?end note\b)/i,/^(?:stateDiagram\s+)/i,/^(?:stateDiagram-v2\s+)/i,/^(?:hide empty description\b)/i,/^(?:\[\*\])/i,/^(?:[^:\n\s\-\{]+)/i,/^(?:\s*:[^:\n;]+)/i,/^(?:-->)/i,/^(?:--)/i,/^(?::::)/i,/^(?:$)/i,/^(?:.)/i],conditions:{LINE:{rules:[9,10],inclusive:!1},struct:{rules:[9,10,22,26,32,39,40,41,42,51,52,53,54,68,69,70,71,72],inclusive:!1},FLOATING_NOTE_ID:{rules:[61],inclusive:!1},FLOATING_NOTE:{rules:[58,59,60],inclusive:!1},NOTE_TEXT:{rules:[63,64],inclusive:!1},NOTE_ID:{rules:[62],inclusive:!1},NOTE:{rules:[55,56,57],inclusive:!1},CLASS_STYLE:{rules:[28],inclusive:!1},CLASS:{rules:[27],inclusive:!1},CLASSDEFID:{rules:[25],inclusive:!1},CLASSDEF:{rules:[23,24],inclusive:!1},acc_descr_multiline:{rules:[20,21],inclusive:!1},acc_descr:{rules:[18],inclusive:!1},acc_title:{rules:[16],inclusive:!1},SCALE:{rules:[13,14,30,31],inclusive:!1},ALIAS:{rules:[],inclusive:!1},STATE_ID:{rules:[45],inclusive:!1},STATE_STRING:{rules:[46,47],inclusive:!1},FORK_STATE:{rules:[],inclusive:!1},STATE:{rules:[9,10,33,34,35,36,37,38,43,44,48,49,50],inclusive:!1},ID:{rules:[9,10],inclusive:!1},INITIAL:{rules:[0,1,2,3,4,5,6,7,8,10,11,12,15,17,19,22,26,29,32,50,54,65,66,67,68,69,70,71,73,74,75],inclusive:!0}}};function O(){this.yy={}}return L.lexer=I,O.prototype=L,L.Parser=O,new O}();n.parser=n;const r=n,o="TB",a="state",c="relation",l="default",h="divider",u="[*]",d="start",p=u,y="color",f="fill";let m="LR",g=[],S={};let _={root:{relations:[],states:{},documents:{}}},k=_.root,T=0,b=0;const E=t=>JSON.parse(JSON.stringify(t)),x=(t,e,s)=>{if(e.stmt===c)x(t,e.state1,!0),x(t,e.state2,!1);else if(e.stmt===a&&("[*]"===e.id?(e.id=s?t.id+"_start":t.id+"_end",e.start=s):e.id=e.id.trim()),e.doc){const t=[];let s,n=[];for(s=0;s<e.doc.length;s++)if(e.doc[s].type===h){const i=E(e.doc[s]);i.doc=E(n),t.push(i),n=[]}else n.push(e.doc[s]);if(t.length>0&&n.length>0){const s={stmt:a,id:(0,i.I)(),type:"divider",doc:E(n)};t.push(E(s)),e.doc=t}e.doc.forEach((t=>x(e,t,!0)))}},C=function(t,e=l,s=null,n=null,r=null,o=null,a=null,c=null){const h=null==t?void 0:t.trim();if(void 0===k.states[h]?(i.l.info("Adding state ",h,n),k.states[h]={id:h,descriptions:[],type:e,doc:s,note:r,classes:[],styles:[],textStyles:[]}):(k.states[h].doc||(k.states[h].doc=s),k.states[h].type||(k.states[h].type=e)),n&&(i.l.info("Setting state description",h,n),"string"==typeof n&&I(h,n.trim()),"object"==typeof n&&n.forEach((t=>I(h,t.trim())))),r&&(k.states[h].note=r,k.states[h].note.text=i.e.sanitizeText(k.states[h].note.text,(0,i.c)())),o){i.l.info("Setting state classes",h,o);("string"==typeof o?[o]:o).forEach((t=>N(h,t.trim())))}if(a){i.l.info("Setting state styles",h,a);("string"==typeof a?[a]:a).forEach((t=>R(h,t.trim())))}if(c){i.l.info("Setting state styles",h,a);("string"==typeof c?[c]:c).forEach((t=>w(h,t.trim())))}},$=function(t){_={root:{relations:[],states:{},documents:{}}},k=_.root,T=0,S={},t||(0,i.v)()},v=function(t){return k.states[t]};function D(t=""){let e=t;return t===u&&(T++,e=`${d}${T}`),e}function A(t="",e=l){return t===u?d:e}const L=function(t,e,s){if("object"==typeof t)!function(t,e,s){let n=D(t.id.trim()),r=A(t.id.trim(),t.type),o=D(e.id.trim()),a=A(e.id.trim(),e.type);C(n,r,t.doc,t.description,t.note,t.classes,t.styles,t.textStyles),C(o,a,e.doc,e.description,e.note,e.classes,e.styles,e.textStyles),k.relations.push({id1:n,id2:o,relationTitle:i.e.sanitizeText(s,(0,i.c)())})}(t,e,s);else{const n=D(t.trim()),r=A(t),o=function(t=""){let e=t;return t===p&&(T++,e=`end${T}`),e}(e.trim()),a=function(t="",e=l){return t===p?"end":e}(e);C(n,r),C(o,a),k.relations.push({id1:n,id2:o,title:i.e.sanitizeText(s,(0,i.c)())})}},I=function(t,e){const s=k.states[t],n=e.startsWith(":")?e.replace(":","").trim():e;s.descriptions.push(i.e.sanitizeText(n,(0,i.c)()))},O=function(t,e=""){void 0===S[t]&&(S[t]={id:t,styles:[],textStyles:[]});const s=S[t];null!=e&&e.split(",").forEach((t=>{const e=t.replace(/([^;]*);/,"$1").trim();if(t.match(y)){const t=e.replace(f,"bgFill").replace(y,f);s.textStyles.push(t)}s.styles.push(e)}))},N=function(t,e){t.split(",").forEach((function(t){let s=v(t);if(void 0===s){const e=t.trim();C(e),s=v(e)}s.classes.push(e)}))},R=function(t,e){const s=v(t);void 0!==s&&s.textStyles.push(e)},w=function(t,e){const s=v(t);void 0!==s&&s.textStyles.push(e)},B={getConfig:()=>(0,i.c)().state,addState:C,clear:$,getState:v,getStates:function(){return k.states},getRelations:function(){return k.relations},getClasses:function(){return S},getDirection:()=>m,addRelation:L,getDividerId:()=>(b++,"divider-id-"+b),setDirection:t=>{m=t},cleanupLabel:function(t){return":"===t.substring(0,1)?t.substr(2).trim():t.trim()},lineType:{LINE:0,DOTTED_LINE:1},relationType:{AGGREGATION:0,EXTENSION:1,COMPOSITION:2,DEPENDENCY:3},logDocuments:function(){i.l.info("Documents = ",_)},getRootDoc:()=>g,setRootDoc:t=>{i.l.info("Setting root doc",t),g=t},getRootDocV2:()=>(x({id:"root"},{id:"root",doc:g},!0),{id:"root",doc:g}),extract:t=>{let e;e=t.doc?t.doc:t,i.l.info(e),$(!0),i.l.info("Extract",e),e.forEach((t=>{switch(t.stmt){case a:C(t.id.trim(),t.type,t.doc,t.description,t.note,t.classes,t.styles,t.textStyles);break;case c:L(t.state1,t.state2,t.description);break;case"classDef":O(t.id.trim(),t.classes);break;case"applyClass":N(t.id.trim(),t.styleClass)}}))},trimColon:t=>t&&":"===t[0]?t.substr(1).trim():t.trim(),getAccTitle:i.g,setAccTitle:i.s,getAccDescription:i.a,setAccDescription:i.b,addStyleClass:O,setCssClass:N,addDescription:I,setDiagramTitle:i.q,getDiagramTitle:i.t},P=t=>`\ndefs #statediagram-barbEnd {\n    fill: ${t.transitionColor};\n    stroke: ${t.transitionColor};\n  }\ng.stateGroup text {\n  fill: ${t.nodeBorder};\n  stroke: none;\n  font-size: 10px;\n}\ng.stateGroup text {\n  fill: ${t.textColor};\n  stroke: none;\n  font-size: 10px;\n\n}\ng.stateGroup .state-title {\n  font-weight: bolder;\n  fill: ${t.stateLabelColor};\n}\n\ng.stateGroup rect {\n  fill: ${t.mainBkg};\n  stroke: ${t.nodeBorder};\n}\n\ng.stateGroup line {\n  stroke: ${t.lineColor};\n  stroke-width: 1;\n}\n\n.transition {\n  stroke: ${t.transitionColor};\n  stroke-width: 1;\n  fill: none;\n}\n\n.stateGroup .composit {\n  fill: ${t.background};\n  border-bottom: 1px\n}\n\n.stateGroup .alt-composit {\n  fill: #e0e0e0;\n  border-bottom: 1px\n}\n\n.state-note {\n  stroke: ${t.noteBorderColor};\n  fill: ${t.noteBkgColor};\n\n  text {\n    fill: ${t.noteTextColor};\n    stroke: none;\n    font-size: 10px;\n  }\n}\n\n.stateLabel .box {\n  stroke: none;\n  stroke-width: 0;\n  fill: ${t.mainBkg};\n  opacity: 0.5;\n}\n\n.edgeLabel .label rect {\n  fill: ${t.labelBackgroundColor};\n  opacity: 0.5;\n}\n.edgeLabel .label text {\n  fill: ${t.transitionLabelColor||t.tertiaryTextColor};\n}\n.label div .edgeLabel {\n  color: ${t.transitionLabelColor||t.tertiaryTextColor};\n}\n\n.stateLabel text {\n  fill: ${t.stateLabelColor};\n  font-size: 10px;\n  font-weight: bold;\n}\n\n.node circle.state-start {\n  fill: ${t.specialStateColor};\n  stroke: ${t.specialStateColor};\n}\n\n.node .fork-join {\n  fill: ${t.specialStateColor};\n  stroke: ${t.specialStateColor};\n}\n\n.node circle.state-end {\n  fill: ${t.innerEndBackground};\n  stroke: ${t.background};\n  stroke-width: 1.5\n}\n.end-state-inner {\n  fill: ${t.compositeBackground||t.background};\n  // stroke: ${t.background};\n  stroke-width: 1.5\n}\n\n.node rect {\n  fill: ${t.stateBkg||t.mainBkg};\n  stroke: ${t.stateBorder||t.nodeBorder};\n  stroke-width: 1px;\n}\n.node polygon {\n  fill: ${t.mainBkg};\n  stroke: ${t.stateBorder||t.nodeBorder};;\n  stroke-width: 1px;\n}\n#statediagram-barbEnd {\n  fill: ${t.lineColor};\n}\n\n.statediagram-cluster rect {\n  fill: ${t.compositeTitleBackground};\n  stroke: ${t.stateBorder||t.nodeBorder};\n  stroke-width: 1px;\n}\n\n.cluster-label, .nodeLabel {\n  color: ${t.stateLabelColor};\n}\n\n.statediagram-cluster rect.outer {\n  rx: 5px;\n  ry: 5px;\n}\n.statediagram-state .divider {\n  stroke: ${t.stateBorder||t.nodeBorder};\n}\n\n.statediagram-state .title-state {\n  rx: 5px;\n  ry: 5px;\n}\n.statediagram-cluster.statediagram-cluster .inner {\n  fill: ${t.compositeBackground||t.background};\n}\n.statediagram-cluster.statediagram-cluster-alt .inner {\n  fill: ${t.altBackground?t.altBackground:"#efefef"};\n}\n\n.statediagram-cluster .inner {\n  rx:0;\n  ry:0;\n}\n\n.statediagram-state rect.basic {\n  rx: 5px;\n  ry: 5px;\n}\n.statediagram-state rect.divider {\n  stroke-dasharray: 10,10;\n  fill: ${t.altBackground?t.altBackground:"#efefef"};\n}\n\n.note-edge {\n  stroke-dasharray: 5;\n}\n\n.statediagram-note rect {\n  fill: ${t.noteBkgColor};\n  stroke: ${t.noteBorderColor};\n  stroke-width: 1px;\n  rx: 0;\n  ry: 0;\n}\n.statediagram-note rect {\n  fill: ${t.noteBkgColor};\n  stroke: ${t.noteBorderColor};\n  stroke-width: 1px;\n  rx: 0;\n  ry: 0;\n}\n\n.statediagram-note text {\n  fill: ${t.noteTextColor};\n}\n\n.statediagram-note .nodeLabel {\n  color: ${t.noteTextColor};\n}\n.statediagram .edgeLabel {\n  color: red; // ${t.noteTextColor};\n}\n\n#dependencyStart, #dependencyEnd {\n  fill: ${t.lineColor};\n  stroke: ${t.lineColor};\n  stroke-width: 1;\n}\n\n.statediagramTitleText {\n  text-anchor: middle;\n  font-size: 18px;\n  fill: ${t.textColor};\n}\n`}}]);