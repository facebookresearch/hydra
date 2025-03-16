"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[5071],{15680:(e,n,t)=>{t.r(n),t.d(n,{MDXContext:()=>p,MDXProvider:()=>d,mdx:()=>y,useMDXComponents:()=>c,withMDXComponents:()=>s});var a=t(96540);function r(e,n,t){return n in e?Object.defineProperty(e,n,{value:t,enumerable:!0,configurable:!0,writable:!0}):e[n]=t,e}function i(){return i=Object.assign||function(e){for(var n=1;n<arguments.length;n++){var t=arguments[n];for(var a in t)Object.prototype.hasOwnProperty.call(t,a)&&(e[a]=t[a])}return e},i.apply(this,arguments)}function l(e,n){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);n&&(a=a.filter((function(n){return Object.getOwnPropertyDescriptor(e,n).enumerable}))),t.push.apply(t,a)}return t}function m(e){for(var n=1;n<arguments.length;n++){var t=null!=arguments[n]?arguments[n]:{};n%2?l(Object(t),!0).forEach((function(n){r(e,n,t[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):l(Object(t)).forEach((function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(t,n))}))}return e}function o(e,n){if(null==e)return{};var t,a,r=function(e,n){if(null==e)return{};var t,a,r={},i=Object.keys(e);for(a=0;a<i.length;a++)t=i[a],n.indexOf(t)>=0||(r[t]=e[t]);return r}(e,n);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);for(a=0;a<i.length;a++)t=i[a],n.indexOf(t)>=0||Object.prototype.propertyIsEnumerable.call(e,t)&&(r[t]=e[t])}return r}var p=a.createContext({}),s=function(e){return function(n){var t=c(n.components);return a.createElement(e,i({},n,{components:t}))}},c=function(e){var n=a.useContext(p),t=n;return e&&(t="function"==typeof e?e(n):m(m({},n),e)),t},d=function(e){var n=c(e.components);return a.createElement(p.Provider,{value:n},e.children)},u="mdxType",g={inlineCode:"code",wrapper:function(e){var n=e.children;return a.createElement(a.Fragment,{},n)}},x=a.forwardRef((function(e,n){var t=e.components,r=e.mdxType,i=e.originalType,l=e.parentName,p=o(e,["components","mdxType","originalType","parentName"]),s=c(t),d=r,u=s["".concat(l,".").concat(d)]||s[d]||g[d]||i;return t?a.createElement(u,m(m({ref:n},p),{},{components:t})):a.createElement(u,m({ref:n},p))}));function y(e,n){var t=arguments,r=n&&n.mdxType;if("string"==typeof e||r){var i=t.length,l=new Array(i);l[0]=x;var m={};for(var o in n)hasOwnProperty.call(n,o)&&(m[o]=n[o]);m.originalType=e,m[u]="string"==typeof e?e:r,l[1]=m;for(var p=2;p<i;p++)l[p]=t[p];return a.createElement.apply(null,l)}return a.createElement.apply(null,t)}x.displayName="MDXCreateElement"},17561:(e,n,t)=>{t.r(n),t.d(n,{assets:()=>p,contentTitle:()=>m,default:()=>u,frontMatter:()=>l,metadata:()=>o,toc:()=>s});var a=t(58168),r=(t(96540),t(15680)),i=t(49595);const l={id:"configuring_experiments",title:"Configuring Experiments"},m=void 0,o={unversionedId:"patterns/configuring_experiments",id:"version-1.2/patterns/configuring_experiments",title:"Configuring Experiments",description:"Problem",source:"@site/versioned_docs/version-1.2/patterns/configuring_experiments.md",sourceDirName:"patterns",slug:"/patterns/configuring_experiments",permalink:"/docs/1.2/patterns/configuring_experiments",draft:!1,editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/versioned_docs/version-1.2/patterns/configuring_experiments.md",tags:[],version:"1.2",lastUpdatedBy:"dependabot[bot]",lastUpdatedAt:1742161400,formattedLastUpdatedAt:"Mar 16, 2025",frontMatter:{id:"configuring_experiments",title:"Configuring Experiments"},sidebar:"docs",previous:{title:"Extending Configs",permalink:"/docs/1.2/patterns/extending_configs"},next:{title:"Configuring Plugins",permalink:"/docs/1.2/patterns/configuring_plugins"}},p={},s=[{value:"Problem",id:"problem",level:3},{value:"Solution",id:"solution",level:3},{value:"Example",id:"example",level:3},{value:"Sweeping over experiments",id:"sweeping-over-experiments",level:3}],c={toc:s},d="wrapper";function u(e){let{components:n,...t}=e;return(0,r.mdx)(d,(0,a.A)({},c,t,{components:n,mdxType:"MDXLayout"}),(0,r.mdx)(i.C,{text:"Example application",to:"examples/patterns/configuring_experiments",mdxType:"ExampleGithubLink"}),(0,r.mdx)("h3",{id:"problem"},"Problem"),(0,r.mdx)("p",null,"A common problem is maintaining multiple configurations of an application.  This can get especially\ntedious when the configuration differences span multiple dimensions.\nThis pattern shows how to cleanly support multiple configurations, with each configuration file only specifying\nthe changes to the master (default) configuration."),(0,r.mdx)("h3",{id:"solution"},"Solution"),(0,r.mdx)("p",null,"Create a config file specifying the overrides to the default configuration, and then call it via the command line.\ne.g. ",(0,r.mdx)("inlineCode",{parentName:"p"},"$ python my_app.py +experiment=fast_mode"),"."),(0,r.mdx)("p",null,"To avoid clutter, we place the experiment config files in dedicated config group called ",(0,r.mdx)("em",{parentName:"p"},"experiment"),"."),(0,r.mdx)("h3",{id:"example"},"Example"),(0,r.mdx)("p",null,"In this example, we will create configurations for each of the server and database pairings that we want to benchmark."),(0,r.mdx)("p",null,"The default configuration is:"),(0,r.mdx)("div",{className:"row"},(0,r.mdx)("div",{className:"col col--4"},(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="config.yaml"',title:'"config.yaml"'},"defaults:\n  - db: mysql\n  - server: apache\n\n\n\n\n\n"))),(0,r.mdx)("div",{className:"col col--4"},(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="db/mysql.yaml"',title:'"db/mysql.yaml"'},"name: mysql\n")),(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="server/apache.yaml"',title:'"server/apache.yaml"'},"name: apache\nport: 80\n"))),(0,r.mdx)("div",{className:"col col--4"},(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="db/sqlite.yaml"',title:'"db/sqlite.yaml"'},"name: sqlite\n")),(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="server/nginx.yaml"',title:'"server/nginx.yaml"'},"name: nginx\nport: 80\n")))),(0,r.mdx)("div",{className:"row"},(0,r.mdx)("div",{className:"col col--6"},(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-text",metastring:'title="Directory structure"',title:'"Directory','structure"':!0},"\u251c\u2500\u2500 config.yaml\n\u251c\u2500\u2500 db\n\u2502   \u251c\u2500\u2500 mysql.yaml\n\u2502   \u2514\u2500\u2500 sqlite.yaml\n\u2514\u2500\u2500 server\n    \u251c\u2500\u2500 apache.yaml\n    \u2514\u2500\u2500 nginx.yaml\n"))),(0,r.mdx)("div",{className:"col col--6"},(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="$ python my_app.py"',title:'"$',python:!0,'my_app.py"':!0},"db:\n  name: mysql\nserver:\n  name: apache\n  port: 80\n\n\n")))),(0,r.mdx)("p",null,"The benchmark config files specify the deltas from the default configuration:"),(0,r.mdx)("div",{className:"row"},(0,r.mdx)("div",{className:"col col--6"},(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="experiment/aplite.yaml"',title:'"experiment/aplite.yaml"'},"# @package _global_\ndefaults:\n  - override /db: sqlite\n  \n  \nserver:\n  port: 8080\n"))),(0,r.mdx)("div",{className:"col col--6"},(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="experiment/nglite.yaml"',title:'"experiment/nglite.yaml"'},"# @package _global_\ndefaults:\n  - override /db: sqlite\n  - override /server: nginx\n  \nserver:\n  port: 8080\n")))),(0,r.mdx)("div",{className:"row"},(0,r.mdx)("div",{className:"col col--6"},(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="$ python my_app.py +experiment=aplite"',title:'"$',python:!0,"my_app.py":!0,"+experiment":'aplite"'},"db:\n  name: sqlite\nserver:\n  name: apache\n  port: 8080\n"))),(0,r.mdx)("div",{className:"col col--6"},(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="$ python my_app.py +experiment=nglite"',title:'"$',python:!0,"my_app.py":!0,"+experiment":'nglite"'},"db:\n  name: sqlite\nserver:\n  name: nginx\n  port: 8080\n")))),(0,r.mdx)("p",null,"Key concepts:"),(0,r.mdx)("ul",null,(0,r.mdx)("li",{parentName:"ul"},(0,r.mdx)("strong",{parentName:"li"},"#"," @package ","_","global","_"),(0,r.mdx)("br",{parentName:"li"}),"Changes specified in this config should be interpreted as relative to the ","_","global","_"," package.",(0,r.mdx)("br",{parentName:"li"}),"We could instead place ",(0,r.mdx)("em",{parentName:"li"},"nglite.yaml")," and ",(0,r.mdx)("em",{parentName:"li"},"aplite.yaml")," next to ",(0,r.mdx)("em",{parentName:"li"},"config.yaml")," and omit this line."),(0,r.mdx)("li",{parentName:"ul"},(0,r.mdx)("strong",{parentName:"li"},"The overrides of /db and /server are absolute paths."),(0,r.mdx)("br",{parentName:"li"}),"This is necessary because they are outside of the experiment directory. ")),(0,r.mdx)("p",null,"Running the experiments from the command line requires prefixing the experiment choice with a ",(0,r.mdx)("inlineCode",{parentName:"p"},"+"),".\nThe experiment config group is an addition, not an override."),(0,r.mdx)("h3",{id:"sweeping-over-experiments"},"Sweeping over experiments"),(0,r.mdx)("p",null,"This approach also enables sweeping over those experiments to easily compare their results:"),(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-text",metastring:'title="$ python my_app.py --multirun +experiment=aplite,nglite"',title:'"$',python:!0,"my_app.py":!0,"--multirun":!0,"+experiment":'aplite,nglite"'},"[HYDRA] Launching 2 jobs locally\n[HYDRA]        #0 : +experiment=aplite\ndb:\n  name: sqlite\nserver:\n  name: apache\n  port: 8080\n\n[HYDRA]        #1 : +experiment=nglite\ndb:\n  name: sqlite\nserver:\n  name: nginx\n  port: 8080\n")),(0,r.mdx)("p",null,"To run all the experiments, use the ",(0,r.mdx)("a",{parentName:"p",href:"/docs/1.2/advanced/override_grammar/extended#glob-choice-sweep"},"glob")," syntax:"),(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-text",metastring:"title=\"$ python my_app.py --multirun '+experiment=glob(*)'\"",title:'"$',python:!0,"my_app.py":!0,"--multirun":!0,"'+experiment":"glob(*)'\""},"[HYDRA]        #0 : +experiment=aplite\n...\n[HYDRA]        #1 : +experiment=nglite\n...\n")))}u.isMDXComponent=!0},49595:(e,n,t)=>{t.d(n,{A:()=>p,C:()=>s});var a=t(58168),r=t(96540),i=t(75489),l=t(44586),m=t(48295);function o(e){const n=(0,m.ir)();return(0,l.default)().siteConfig.customFields.githubLinkVersionToBaseUrl[n?.name??"current"]+e}function p(e){return r.createElement(i.default,(0,a.A)({},e,{to:o(e.to),target:"_blank"}))}function s(e){const n=e.text??"Example (Click Here)";return r.createElement(p,e,r.createElement("span",null,"\xa0"),r.createElement("img",{src:"https://img.shields.io/badge/-"+n+"-informational",alt:"Example (Click Here)"}))}}}]);