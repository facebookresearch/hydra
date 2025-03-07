"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[4569],{15680:(t,e,r)=>{r.r(e),r.d(e,{MDXContext:()=>l,MDXProvider:()=>m,mdx:()=>h,useMDXComponents:()=>d,withMDXComponents:()=>c});var n=r(96540);function o(t,e,r){return e in t?Object.defineProperty(t,e,{value:r,enumerable:!0,configurable:!0,writable:!0}):t[e]=r,t}function i(){return i=Object.assign||function(t){for(var e=1;e<arguments.length;e++){var r=arguments[e];for(var n in r)Object.prototype.hasOwnProperty.call(r,n)&&(t[n]=r[n])}return t},i.apply(this,arguments)}function a(t,e){var r=Object.keys(t);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(t);e&&(n=n.filter((function(e){return Object.getOwnPropertyDescriptor(t,e).enumerable}))),r.push.apply(r,n)}return r}function s(t){for(var e=1;e<arguments.length;e++){var r=null!=arguments[e]?arguments[e]:{};e%2?a(Object(r),!0).forEach((function(e){o(t,e,r[e])})):Object.getOwnPropertyDescriptors?Object.defineProperties(t,Object.getOwnPropertyDescriptors(r)):a(Object(r)).forEach((function(e){Object.defineProperty(t,e,Object.getOwnPropertyDescriptor(r,e))}))}return t}function u(t,e){if(null==t)return{};var r,n,o=function(t,e){if(null==t)return{};var r,n,o={},i=Object.keys(t);for(n=0;n<i.length;n++)r=i[n],e.indexOf(r)>=0||(o[r]=t[r]);return o}(t,e);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(t);for(n=0;n<i.length;n++)r=i[n],e.indexOf(r)>=0||Object.prototype.propertyIsEnumerable.call(t,r)&&(o[r]=t[r])}return o}var l=n.createContext({}),c=function(t){return function(e){var r=d(e.components);return n.createElement(t,i({},e,{components:r}))}},d=function(t){var e=n.useContext(l),r=e;return t&&(r="function"==typeof t?t(e):s(s({},e),t)),r},m=function(t){var e=d(t.components);return n.createElement(l.Provider,{value:e},t.children)},p="mdxType",f={inlineCode:"code",wrapper:function(t){var e=t.children;return n.createElement(n.Fragment,{},e)}},g=n.forwardRef((function(t,e){var r=t.components,o=t.mdxType,i=t.originalType,a=t.parentName,l=u(t,["components","mdxType","originalType","parentName"]),c=d(r),m=o,p=c["".concat(a,".").concat(m)]||c[m]||f[m]||i;return r?n.createElement(p,s(s({ref:e},l),{},{components:r})):n.createElement(p,s({ref:e},l))}));function h(t,e){var r=arguments,o=e&&e.mdxType;if("string"==typeof t||o){var i=r.length,a=new Array(i);a[0]=g;var s={};for(var u in e)hasOwnProperty.call(e,u)&&(s[u]=e[u]);s.originalType=t,s[p]="string"==typeof t?t:o,a[1]=s;for(var l=2;l<i;l++)a[l]=r[l];return n.createElement.apply(null,a)}return n.createElement.apply(null,r)}g.displayName="MDXCreateElement"},49595:(t,e,r)=>{r.d(e,{A:()=>l,C:()=>c});var n=r(58168),o=r(96540),i=r(75489),a=r(44586),s=r(48295);function u(t){const e=(0,s.ir)();return(0,a.default)().siteConfig.customFields.githubLinkVersionToBaseUrl[e?.name??"current"]+t}function l(t){return o.createElement(i.default,(0,n.A)({},t,{to:u(t.to),target:"_blank"}))}function c(t){const e=t.text??"Example (Click Here)";return o.createElement(l,t,o.createElement("span",null,"\xa0"),o.createElement("img",{src:"https://img.shields.io/badge/-"+e+"-informational",alt:"Example (Click Here)"}))}},51290:(t,e,r)=>{r.r(e),r.d(e,{assets:()=>l,contentTitle:()=>s,default:()=>p,frontMatter:()=>a,metadata:()=>u,toc:()=>c});var n=r(58168),o=(r(96540),r(15680)),i=r(49595);const a={id:"intro",title:"Introduction to Structured Configs",sidebar_label:"Introduction to Structured Configs"},s=void 0,u={unversionedId:"tutorials/structured_config/intro",id:"tutorials/structured_config/intro",title:"Introduction to Structured Configs",description:"This is an advanced tutorial that assumes that you are comfortable with the concepts introduced in the Basic Tutorial.",source:"@site/docs/tutorials/structured_config/0_intro.md",sourceDirName:"tutorials/structured_config",slug:"/tutorials/structured_config/intro",permalink:"/docs/tutorials/structured_config/intro",draft:!1,editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/docs/tutorials/structured_config/0_intro.md",tags:[],version:"current",lastUpdatedBy:"jesszzzz",lastUpdatedAt:1741383139,formattedLastUpdatedAt:"Mar 7, 2025",sidebarPosition:0,frontMatter:{id:"intro",title:"Introduction to Structured Configs",sidebar_label:"Introduction to Structured Configs"},sidebar:"docs",previous:{title:"Tab completion",permalink:"/docs/tutorials/basic/running_your_app/tab_completion"},next:{title:"Config Store API",permalink:"/docs/tutorials/structured_config/config_store"}},l={},c=[{value:"Structured Configs supports:",id:"structured-configs-supports",level:4},{value:"Structured Configs Limitations:",id:"structured-configs-limitations",level:4},{value:"There are two primary patterns for using Structured configs with Hydra",id:"there-are-two-primary-patterns-for-using-structured-configs-with-hydra",level:4}],d={toc:c},m="wrapper";function p(t){let{components:e,...r}=t;return(0,o.mdx)(m,(0,n.A)({},d,r,{components:e,mdxType:"MDXLayout"}),(0,o.mdx)("p",null,"This is an advanced tutorial that assumes that you are comfortable with the concepts introduced in the ",(0,o.mdx)("a",{parentName:"p",href:"/docs/tutorials/basic/your_first_app/simple_cli"},"Basic Tutorial"),".\nThe examples in this tutorial are available ",(0,o.mdx)(i.A,{to:"examples/tutorials/structured_configs",mdxType:"GithubLink"},"here"),"."),(0,o.mdx)("p",null,"Structured Configs use Python ",(0,o.mdx)("a",{parentName:"p",href:"https://docs.python.org/3.8/library/dataclasses.html"},"dataclasses")," to\ndescribe your configuration structure and types. They enable:"),(0,o.mdx)("ul",null,(0,o.mdx)("li",{parentName:"ul"},(0,o.mdx)("strong",{parentName:"li"},"Runtime type checking")," as you compose or mutate your config "),(0,o.mdx)("li",{parentName:"ul"},(0,o.mdx)("strong",{parentName:"li"},"Static type checking")," when using static type checkers (mypy, PyCharm, etc.)")),(0,o.mdx)("h4",{id:"structured-configs-supports"},"Structured Configs supports:"),(0,o.mdx)("ul",null,(0,o.mdx)("li",{parentName:"ul"},"Primitive types (",(0,o.mdx)("inlineCode",{parentName:"li"},"int"),", ",(0,o.mdx)("inlineCode",{parentName:"li"},"bool"),", ",(0,o.mdx)("inlineCode",{parentName:"li"},"float"),", ",(0,o.mdx)("inlineCode",{parentName:"li"},"str"),", ",(0,o.mdx)("inlineCode",{parentName:"li"},"Enums"),", ",(0,o.mdx)("inlineCode",{parentName:"li"},"bytes"),", ",(0,o.mdx)("inlineCode",{parentName:"li"},"pathlib.Path"),") "),(0,o.mdx)("li",{parentName:"ul"},"Nesting of Structured Configs"),(0,o.mdx)("li",{parentName:"ul"},"Containers (List and Dict) containing primitives, Structured Configs, or other lists/dicts"),(0,o.mdx)("li",{parentName:"ul"},"Optional fields")),(0,o.mdx)("h4",{id:"structured-configs-limitations"},"Structured Configs Limitations:"),(0,o.mdx)("ul",null,(0,o.mdx)("li",{parentName:"ul"},(0,o.mdx)("inlineCode",{parentName:"li"},"Union")," types are only partially supported (see ",(0,o.mdx)("a",{parentName:"li",href:"https://omegaconf.readthedocs.io/en/latest/structured_config.html#union-types"},"OmegaConf docs on unions"),")"),(0,o.mdx)("li",{parentName:"ul"},"User methods are not supported")),(0,o.mdx)("p",null,"See the ",(0,o.mdx)("a",{parentName:"p",href:"https://omegaconf.readthedocs.io/en/latest/structured_config.html"},"OmegaConf docs on Structured Configs")," for more details."),(0,o.mdx)("h4",{id:"there-are-two-primary-patterns-for-using-structured-configs-with-hydra"},"There are two primary patterns for using Structured configs with Hydra"),(0,o.mdx)("ul",null,(0,o.mdx)("li",{parentName:"ul"},"As a ",(0,o.mdx)("a",{parentName:"li",href:"/docs/tutorials/structured_config/minimal_example"},"config"),", in place of configuration files (often a starting place)"),(0,o.mdx)("li",{parentName:"ul"},"As a ",(0,o.mdx)("a",{parentName:"li",href:"/docs/tutorials/structured_config/schema"},"config schema")," validating configuration files (better for complex use cases)")),(0,o.mdx)("p",null,"With both patterns, you still get everything Hydra has to offer (config composition, Command line overrides etc).\nThis tutorial covers both. ","*",(0,o.mdx)("strong",{parentName:"p"},"Read it in order"),"*","."),(0,o.mdx)("p",null,"Hydra supports OmegaConf's Structured Configs via the ",(0,o.mdx)("inlineCode",{parentName:"p"},"ConfigStore")," API.\nThis tutorial does not assume any knowledge of them.\nIt is recommended that you visit the ",(0,o.mdx)("a",{class:"external",href:"https://omegaconf.readthedocs.io/en/latest/structured_config.html",target:"_blank"},"OmegaConf Structured Configs page")," to learn more later."))}p.isMDXComponent=!0}}]);