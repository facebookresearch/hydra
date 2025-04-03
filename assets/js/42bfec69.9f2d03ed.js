"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[8794],{15680:(t,e,r)=>{r.r(e),r.d(e,{MDXContext:()=>c,MDXProvider:()=>p,mdx:()=>h,useMDXComponents:()=>d,withMDXComponents:()=>l});var n=r(96540);function o(t,e,r){return e in t?Object.defineProperty(t,e,{value:r,enumerable:!0,configurable:!0,writable:!0}):t[e]=r,t}function i(){return i=Object.assign||function(t){for(var e=1;e<arguments.length;e++){var r=arguments[e];for(var n in r)Object.prototype.hasOwnProperty.call(r,n)&&(t[n]=r[n])}return t},i.apply(this,arguments)}function a(t,e){var r=Object.keys(t);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(t);e&&(n=n.filter((function(e){return Object.getOwnPropertyDescriptor(t,e).enumerable}))),r.push.apply(r,n)}return r}function s(t){for(var e=1;e<arguments.length;e++){var r=null!=arguments[e]?arguments[e]:{};e%2?a(Object(r),!0).forEach((function(e){o(t,e,r[e])})):Object.getOwnPropertyDescriptors?Object.defineProperties(t,Object.getOwnPropertyDescriptors(r)):a(Object(r)).forEach((function(e){Object.defineProperty(t,e,Object.getOwnPropertyDescriptor(r,e))}))}return t}function u(t,e){if(null==t)return{};var r,n,o=function(t,e){if(null==t)return{};var r,n,o={},i=Object.keys(t);for(n=0;n<i.length;n++)r=i[n],e.indexOf(r)>=0||(o[r]=t[r]);return o}(t,e);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(t);for(n=0;n<i.length;n++)r=i[n],e.indexOf(r)>=0||Object.prototype.propertyIsEnumerable.call(t,r)&&(o[r]=t[r])}return o}var c=n.createContext({}),l=function(t){return function(e){var r=d(e.components);return n.createElement(t,i({},e,{components:r}))}},d=function(t){var e=n.useContext(c),r=e;return t&&(r="function"==typeof t?t(e):s(s({},e),t)),r},p=function(t){var e=d(t.components);return n.createElement(c.Provider,{value:e},t.children)},m="mdxType",f={inlineCode:"code",wrapper:function(t){var e=t.children;return n.createElement(n.Fragment,{},e)}},g=n.forwardRef((function(t,e){var r=t.components,o=t.mdxType,i=t.originalType,a=t.parentName,c=u(t,["components","mdxType","originalType","parentName"]),l=d(r),p=o,m=l["".concat(a,".").concat(p)]||l[p]||f[p]||i;return r?n.createElement(m,s(s({ref:e},c),{},{components:r})):n.createElement(m,s({ref:e},c))}));function h(t,e){var r=arguments,o=e&&e.mdxType;if("string"==typeof t||o){var i=r.length,a=new Array(i);a[0]=g;var s={};for(var u in e)hasOwnProperty.call(e,u)&&(s[u]=e[u]);s.originalType=t,s[m]="string"==typeof t?t:o,a[1]=s;for(var c=2;c<i;c++)a[c]=r[c];return n.createElement.apply(null,a)}return n.createElement.apply(null,r)}g.displayName="MDXCreateElement"},44188:(t,e,r)=>{r.r(e),r.d(e,{assets:()=>c,contentTitle:()=>s,default:()=>m,frontMatter:()=>a,metadata:()=>u,toc:()=>l});var n=r(58168),o=(r(96540),r(15680)),i=r(49595);const a={id:"intro",title:"Introduction to Structured Configs",sidebar_label:"Introduction to Structured Configs"},s=void 0,u={unversionedId:"tutorials/structured_config/intro",id:"version-1.1/tutorials/structured_config/intro",title:"Introduction to Structured Configs",description:"This is an advanced tutorial that assumes that you are comfortable with the concepts introduced in the Basic Tutorial.",source:"@site/versioned_docs/version-1.1/tutorials/structured_config/0_intro.md",sourceDirName:"tutorials/structured_config",slug:"/tutorials/structured_config/intro",permalink:"/docs/1.1/tutorials/structured_config/intro",draft:!1,editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/versioned_docs/version-1.1/tutorials/structured_config/0_intro.md",tags:[],version:"1.1",lastUpdatedBy:"dependabot[bot]",lastUpdatedAt:1743717584,formattedLastUpdatedAt:"Apr 3, 2025",sidebarPosition:0,frontMatter:{id:"intro",title:"Introduction to Structured Configs",sidebar_label:"Introduction to Structured Configs"},sidebar:"docs",previous:{title:"Tab completion",permalink:"/docs/1.1/tutorials/basic/running_your_app/tab_completion"},next:{title:"Config Store API",permalink:"/docs/1.1/tutorials/structured_config/config_store"}},c={},l=[{value:"Structured Configs supports:",id:"structured-configs-supports",level:4},{value:"Structured Configs Limitations:",id:"structured-configs-limitations",level:4},{value:"There are two primary patterns for using Structured configs",id:"there-are-two-primary-patterns-for-using-structured-configs",level:4}],d={toc:l},p="wrapper";function m(t){let{components:e,...r}=t;return(0,o.mdx)(p,(0,n.A)({},d,r,{components:e,mdxType:"MDXLayout"}),(0,o.mdx)("p",null,"This is an advanced tutorial that assumes that you are comfortable with the concepts introduced in the ",(0,o.mdx)("a",{parentName:"p",href:"/docs/1.1/tutorials/basic/your_first_app/simple_cli"},"Basic Tutorial"),".\nThe examples in this tutorial are available ",(0,o.mdx)(i.A,{to:"examples/tutorials/structured_configs",mdxType:"GithubLink"},"here"),"."),(0,o.mdx)("p",null,"Structured Configs use Python ",(0,o.mdx)("a",{parentName:"p",href:"https://docs.python.org/3.7/library/dataclasses.html"},"dataclasses")," to\ndescribe your configuration structure and types. They enable:"),(0,o.mdx)("ul",null,(0,o.mdx)("li",{parentName:"ul"},(0,o.mdx)("strong",{parentName:"li"},"Runtime type checking")," as you compose or mutate your config "),(0,o.mdx)("li",{parentName:"ul"},(0,o.mdx)("strong",{parentName:"li"},"Static type checking")," when using static type checkers (mypy, PyCharm, etc.)")),(0,o.mdx)("h4",{id:"structured-configs-supports"},"Structured Configs supports:"),(0,o.mdx)("ul",null,(0,o.mdx)("li",{parentName:"ul"},"Primitive types (",(0,o.mdx)("inlineCode",{parentName:"li"},"int"),", ",(0,o.mdx)("inlineCode",{parentName:"li"},"bool"),", ",(0,o.mdx)("inlineCode",{parentName:"li"},"float"),", ",(0,o.mdx)("inlineCode",{parentName:"li"},"str"),", ",(0,o.mdx)("inlineCode",{parentName:"li"},"Enums"),") "),(0,o.mdx)("li",{parentName:"ul"},"Nesting of Structured Configs"),(0,o.mdx)("li",{parentName:"ul"},"Containers (List and Dict) containing primitives or Structured Configs"),(0,o.mdx)("li",{parentName:"ul"},"Optional fields")),(0,o.mdx)("h4",{id:"structured-configs-limitations"},"Structured Configs Limitations:"),(0,o.mdx)("ul",null,(0,o.mdx)("li",{parentName:"ul"},(0,o.mdx)("inlineCode",{parentName:"li"},"Union")," types are not supported (except ",(0,o.mdx)("inlineCode",{parentName:"li"},"Optional"),")"),(0,o.mdx)("li",{parentName:"ul"},"User methods are not supported")),(0,o.mdx)("h4",{id:"there-are-two-primary-patterns-for-using-structured-configs"},"There are two primary patterns for using Structured configs"),(0,o.mdx)("ul",null,(0,o.mdx)("li",{parentName:"ul"},"As a ",(0,o.mdx)("a",{parentName:"li",href:"/docs/1.1/tutorials/structured_config/minimal_example"},"config"),", in place of configuration files (often a starting place)"),(0,o.mdx)("li",{parentName:"ul"},"As a ",(0,o.mdx)("a",{parentName:"li",href:"/docs/1.1/tutorials/structured_config/schema"},"config schema")," validating configuration files (better for complex use cases)")),(0,o.mdx)("p",null,"With both patterns, you still get everything Hydra has to offer (config composition, Command line overrides etc).\nThis tutorial covers both. ","*",(0,o.mdx)("strong",{parentName:"p"},"Read it in order"),"*","."),(0,o.mdx)("p",null,"Hydra supports OmegaConf's Structured Configs via the ",(0,o.mdx)("inlineCode",{parentName:"p"},"ConfigStore")," API.\nThis tutorial does not assume any knowledge of them.\nIt is recommended that you visit the ",(0,o.mdx)("a",{class:"external",href:"https://omegaconf.readthedocs.io/en/latest/structured_config.html",target:"_blank"},"OmegaConf Structured Configs page")," to learn more later."))}m.isMDXComponent=!0},49595:(t,e,r)=>{r.d(e,{A:()=>c,C:()=>l});var n=r(58168),o=r(96540),i=r(75489),a=r(44586),s=r(48295);function u(t){const e=(0,s.ir)();return(0,a.default)().siteConfig.customFields.githubLinkVersionToBaseUrl[e?.name??"current"]+t}function c(t){return o.createElement(i.default,(0,n.A)({},t,{to:u(t.to),target:"_blank"}))}function l(t){const e=t.text??"Example (Click Here)";return o.createElement(c,t,o.createElement("span",null,"\xa0"),o.createElement("img",{src:"https://img.shields.io/badge/-"+e+"-informational",alt:"Example (Click Here)"}))}}}]);