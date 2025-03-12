"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[1473],{15680:(e,t,r)=>{r.r(t),r.d(t,{MDXContext:()=>l,MDXProvider:()=>m,mdx:()=>h,useMDXComponents:()=>d,withMDXComponents:()=>c});var n=r(96540);function o(e,t,r){return t in e?Object.defineProperty(e,t,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[t]=r,e}function i(){return i=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var r=arguments[t];for(var n in r)Object.prototype.hasOwnProperty.call(r,n)&&(e[n]=r[n])}return e},i.apply(this,arguments)}function a(e,t){var r=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);t&&(n=n.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),r.push.apply(r,n)}return r}function s(e){for(var t=1;t<arguments.length;t++){var r=null!=arguments[t]?arguments[t]:{};t%2?a(Object(r),!0).forEach((function(t){o(e,t,r[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(r)):a(Object(r)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(r,t))}))}return e}function u(e,t){if(null==e)return{};var r,n,o=function(e,t){if(null==e)return{};var r,n,o={},i=Object.keys(e);for(n=0;n<i.length;n++)r=i[n],t.indexOf(r)>=0||(o[r]=e[r]);return o}(e,t);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);for(n=0;n<i.length;n++)r=i[n],t.indexOf(r)>=0||Object.prototype.propertyIsEnumerable.call(e,r)&&(o[r]=e[r])}return o}var l=n.createContext({}),c=function(e){return function(t){var r=d(t.components);return n.createElement(e,i({},t,{components:r}))}},d=function(e){var t=n.useContext(l),r=t;return e&&(r="function"==typeof e?e(t):s(s({},t),e)),r},m=function(e){var t=d(e.components);return n.createElement(l.Provider,{value:t},e.children)},p="mdxType",f={inlineCode:"code",wrapper:function(e){var t=e.children;return n.createElement(n.Fragment,{},t)}},g=n.forwardRef((function(e,t){var r=e.components,o=e.mdxType,i=e.originalType,a=e.parentName,l=u(e,["components","mdxType","originalType","parentName"]),c=d(r),m=o,p=c["".concat(a,".").concat(m)]||c[m]||f[m]||i;return r?n.createElement(p,s(s({ref:t},l),{},{components:r})):n.createElement(p,s({ref:t},l))}));function h(e,t){var r=arguments,o=t&&t.mdxType;if("string"==typeof e||o){var i=r.length,a=new Array(i);a[0]=g;var s={};for(var u in t)hasOwnProperty.call(t,u)&&(s[u]=t[u]);s.originalType=e,s[p]="string"==typeof e?e:o,a[1]=s;for(var l=2;l<i;l++)a[l]=r[l];return n.createElement.apply(null,a)}return n.createElement.apply(null,r)}g.displayName="MDXCreateElement"},49595:(e,t,r)=>{r.d(t,{A:()=>l,C:()=>c});var n=r(58168),o=r(96540),i=r(75489),a=r(44586),s=r(48295);function u(e){const t=(0,s.ir)();return(0,a.default)().siteConfig.customFields.githubLinkVersionToBaseUrl[t?.name??"current"]+e}function l(e){return o.createElement(i.default,(0,n.A)({},e,{to:u(e.to),target:"_blank"}))}function c(e){const t=e.text??"Example (Click Here)";return o.createElement(l,e,o.createElement("span",null,"\xa0"),o.createElement("img",{src:"https://img.shields.io/badge/-"+t+"-informational",alt:"Example (Click Here)"}))}},51801:(e,t,r)=>{r.r(t),r.d(t,{assets:()=>l,contentTitle:()=>s,default:()=>p,frontMatter:()=>a,metadata:()=>u,toc:()=>c});var n=r(58168),o=(r(96540),r(15680)),i=r(49595);const a={id:"intro",title:"Introduction to Structured Configs",sidebar_label:"Introduction to Structured Configs"},s=void 0,u={unversionedId:"tutorials/structured_config/intro",id:"version-1.2/tutorials/structured_config/intro",title:"Introduction to Structured Configs",description:"This is an advanced tutorial that assumes that you are comfortable with the concepts introduced in the Basic Tutorial.",source:"@site/versioned_docs/version-1.2/tutorials/structured_config/0_intro.md",sourceDirName:"tutorials/structured_config",slug:"/tutorials/structured_config/intro",permalink:"/docs/1.2/tutorials/structured_config/intro",draft:!1,editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/versioned_docs/version-1.2/tutorials/structured_config/0_intro.md",tags:[],version:"1.2",lastUpdatedBy:"jesszzzz",lastUpdatedAt:1741814683,formattedLastUpdatedAt:"Mar 12, 2025",sidebarPosition:0,frontMatter:{id:"intro",title:"Introduction to Structured Configs",sidebar_label:"Introduction to Structured Configs"},sidebar:"docs",previous:{title:"Tab completion",permalink:"/docs/1.2/tutorials/basic/running_your_app/tab_completion"},next:{title:"Config Store API",permalink:"/docs/1.2/tutorials/structured_config/config_store"}},l={},c=[{value:"Structured Configs supports:",id:"structured-configs-supports",level:4},{value:"Structured Configs Limitations:",id:"structured-configs-limitations",level:4},{value:"There are two primary patterns for using Structured configs with Hydra",id:"there-are-two-primary-patterns-for-using-structured-configs-with-hydra",level:4}],d={toc:c},m="wrapper";function p(e){let{components:t,...r}=e;return(0,o.mdx)(m,(0,n.A)({},d,r,{components:t,mdxType:"MDXLayout"}),(0,o.mdx)("p",null,"This is an advanced tutorial that assumes that you are comfortable with the concepts introduced in the ",(0,o.mdx)("a",{parentName:"p",href:"/docs/1.2/tutorials/basic/your_first_app/simple_cli"},"Basic Tutorial"),".\nThe examples in this tutorial are available ",(0,o.mdx)(i.A,{to:"examples/tutorials/structured_configs",mdxType:"GithubLink"},"here"),"."),(0,o.mdx)("p",null,"Structured Configs use Python ",(0,o.mdx)("a",{parentName:"p",href:"https://docs.python.org/3.7/library/dataclasses.html"},"dataclasses")," to\ndescribe your configuration structure and types. They enable:"),(0,o.mdx)("ul",null,(0,o.mdx)("li",{parentName:"ul"},(0,o.mdx)("strong",{parentName:"li"},"Runtime type checking")," as you compose or mutate your config "),(0,o.mdx)("li",{parentName:"ul"},(0,o.mdx)("strong",{parentName:"li"},"Static type checking")," when using static type checkers (mypy, PyCharm, etc.)")),(0,o.mdx)("h4",{id:"structured-configs-supports"},"Structured Configs supports:"),(0,o.mdx)("ul",null,(0,o.mdx)("li",{parentName:"ul"},"Primitive types (",(0,o.mdx)("inlineCode",{parentName:"li"},"int"),", ",(0,o.mdx)("inlineCode",{parentName:"li"},"bool"),", ",(0,o.mdx)("inlineCode",{parentName:"li"},"float"),", ",(0,o.mdx)("inlineCode",{parentName:"li"},"str"),", ",(0,o.mdx)("inlineCode",{parentName:"li"},"Enums"),", ",(0,o.mdx)("inlineCode",{parentName:"li"},"bytes"),", ",(0,o.mdx)("inlineCode",{parentName:"li"},"pathlib.Path"),") "),(0,o.mdx)("li",{parentName:"ul"},"Nesting of Structured Configs"),(0,o.mdx)("li",{parentName:"ul"},"Containers (List and Dict) containing primitives, Structured Configs, or other lists/dicts"),(0,o.mdx)("li",{parentName:"ul"},"Optional fields")),(0,o.mdx)("h4",{id:"structured-configs-limitations"},"Structured Configs Limitations:"),(0,o.mdx)("ul",null,(0,o.mdx)("li",{parentName:"ul"},(0,o.mdx)("inlineCode",{parentName:"li"},"Union")," types are only partially supported (see ",(0,o.mdx)("a",{parentName:"li",href:"https://omegaconf.readthedocs.io/en/latest/structured_config.html#union-types"},"OmegaConf docs on unions"),")"),(0,o.mdx)("li",{parentName:"ul"},"User methods are not supported")),(0,o.mdx)("p",null,"See the ",(0,o.mdx)("a",{parentName:"p",href:"https://omegaconf.readthedocs.io/en/latest/structured_config.html"},"OmegaConf docs on Structured Configs")," for more details."),(0,o.mdx)("h4",{id:"there-are-two-primary-patterns-for-using-structured-configs-with-hydra"},"There are two primary patterns for using Structured configs with Hydra"),(0,o.mdx)("ul",null,(0,o.mdx)("li",{parentName:"ul"},"As a ",(0,o.mdx)("a",{parentName:"li",href:"/docs/1.2/tutorials/structured_config/minimal_example"},"config"),", in place of configuration files (often a starting place)"),(0,o.mdx)("li",{parentName:"ul"},"As a ",(0,o.mdx)("a",{parentName:"li",href:"/docs/1.2/tutorials/structured_config/schema"},"config schema")," validating configuration files (better for complex use cases)")),(0,o.mdx)("p",null,"With both patterns, you still get everything Hydra has to offer (config composition, Command line overrides etc).\nThis tutorial covers both. ","*",(0,o.mdx)("strong",{parentName:"p"},"Read it in order"),"*","."),(0,o.mdx)("p",null,"Hydra supports OmegaConf's Structured Configs via the ",(0,o.mdx)("inlineCode",{parentName:"p"},"ConfigStore")," API.\nThis tutorial does not assume any knowledge of them.\nIt is recommended that you visit the ",(0,o.mdx)("a",{class:"external",href:"https://omegaconf.readthedocs.io/en/latest/structured_config.html",target:"_blank"},"OmegaConf Structured Configs page")," to learn more later."))}p.isMDXComponent=!0}}]);