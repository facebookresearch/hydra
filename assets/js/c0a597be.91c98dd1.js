"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[6964],{3905:function(t,e,r){r.r(e),r.d(e,{MDXContext:function(){return c},MDXProvider:function(){return m},mdx:function(){return g},useMDXComponents:function(){return d},withMDXComponents:function(){return l}});var n=r(67294);function o(t,e,r){return e in t?Object.defineProperty(t,e,{value:r,enumerable:!0,configurable:!0,writable:!0}):t[e]=r,t}function i(){return i=Object.assign||function(t){for(var e=1;e<arguments.length;e++){var r=arguments[e];for(var n in r)Object.prototype.hasOwnProperty.call(r,n)&&(t[n]=r[n])}return t},i.apply(this,arguments)}function a(t,e){var r=Object.keys(t);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(t);e&&(n=n.filter((function(e){return Object.getOwnPropertyDescriptor(t,e).enumerable}))),r.push.apply(r,n)}return r}function u(t){for(var e=1;e<arguments.length;e++){var r=null!=arguments[e]?arguments[e]:{};e%2?a(Object(r),!0).forEach((function(e){o(t,e,r[e])})):Object.getOwnPropertyDescriptors?Object.defineProperties(t,Object.getOwnPropertyDescriptors(r)):a(Object(r)).forEach((function(e){Object.defineProperty(t,e,Object.getOwnPropertyDescriptor(r,e))}))}return t}function s(t,e){if(null==t)return{};var r,n,o=function(t,e){if(null==t)return{};var r,n,o={},i=Object.keys(t);for(n=0;n<i.length;n++)r=i[n],e.indexOf(r)>=0||(o[r]=t[r]);return o}(t,e);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(t);for(n=0;n<i.length;n++)r=i[n],e.indexOf(r)>=0||Object.prototype.propertyIsEnumerable.call(t,r)&&(o[r]=t[r])}return o}var c=n.createContext({}),l=function(t){return function(e){var r=d(e.components);return n.createElement(t,i({},e,{components:r}))}},d=function(t){var e=n.useContext(c),r=e;return t&&(r="function"==typeof t?t(e):u(u({},e),t)),r},m=function(t){var e=d(t.components);return n.createElement(c.Provider,{value:e},t.children)},p={inlineCode:"code",wrapper:function(t){var e=t.children;return n.createElement(n.Fragment,{},e)}},f=n.forwardRef((function(t,e){var r=t.components,o=t.mdxType,i=t.originalType,a=t.parentName,c=s(t,["components","mdxType","originalType","parentName"]),l=d(r),m=o,f=l["".concat(a,".").concat(m)]||l[m]||p[m]||i;return r?n.createElement(f,u(u({ref:e},c),{},{components:r})):n.createElement(f,u({ref:e},c))}));function g(t,e){var r=arguments,o=e&&e.mdxType;if("string"==typeof t||o){var i=r.length,a=new Array(i);a[0]=f;var u={};for(var s in e)hasOwnProperty.call(e,s)&&(u[s]=e[s]);u.originalType=t,u.mdxType="string"==typeof t?t:o,a[1]=u;for(var c=2;c<i;c++)a[c]=r[c];return n.createElement.apply(null,a)}return n.createElement.apply(null,r)}f.displayName="MDXCreateElement"},93899:function(t,e,r){r.d(e,{Z:function(){return s},T:function(){return c}});var n=r(87462),o=r(67294),i=r(39960),a=r(52263),u=r(80907);function s(t){return o.createElement(i.default,(0,n.Z)({},t,{to:(e=t.to,s=(0,u.useActiveVersion)(),(0,a.default)().siteConfig.customFields.githubLinkVersionToBaseUrl[null!=(r=null==s?void 0:s.name)?r:"current"]+e),target:"_blank"}));var e,r,s}function c(t){var e,r=null!=(e=t.text)?e:"Example (Click Here)";return o.createElement(s,t,o.createElement("span",null,"\xa0"),o.createElement("img",{src:"https://img.shields.io/badge/-"+r+"-informational",alt:"Example (Click Here)"}))}},82080:function(t,e,r){r.r(e),r.d(e,{frontMatter:function(){return s},contentTitle:function(){return c},metadata:function(){return l},toc:function(){return d},default:function(){return p}});var n=r(87462),o=r(63366),i=(r(67294),r(3905)),a=r(93899),u=["components"],s={id:"intro",title:"Introduction to Structured Configs",sidebar_label:"Introduction to Structured Configs"},c=void 0,l={unversionedId:"tutorials/structured_config/intro",id:"version-1.3/tutorials/structured_config/intro",title:"Introduction to Structured Configs",description:"This is an advanced tutorial that assumes that you are comfortable with the concepts introduced in the Basic Tutorial.",source:"@site/versioned_docs/version-1.3/tutorials/structured_config/0_intro.md",sourceDirName:"tutorials/structured_config",slug:"/tutorials/structured_config/intro",permalink:"/docs/1.3/tutorials/structured_config/intro",editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/versioned_docs/version-1.3/tutorials/structured_config/0_intro.md",tags:[],version:"1.3",lastUpdatedBy:"Shagun Sodhani",lastUpdatedAt:1694910069,formattedLastUpdatedAt:"9/17/2023",sidebarPosition:0,frontMatter:{id:"intro",title:"Introduction to Structured Configs",sidebar_label:"Introduction to Structured Configs"},sidebar:"docs",previous:{title:"Tab completion",permalink:"/docs/1.3/tutorials/basic/running_your_app/tab_completion"},next:{title:"Config Store API",permalink:"/docs/1.3/tutorials/structured_config/config_store"}},d=[{value:"Structured Configs supports:",id:"structured-configs-supports",children:[],level:4},{value:"Structured Configs Limitations:",id:"structured-configs-limitations",children:[],level:4},{value:"There are two primary patterns for using Structured configs with Hydra",id:"there-are-two-primary-patterns-for-using-structured-configs-with-hydra",children:[],level:4}],m={toc:d};function p(t){var e=t.components,r=(0,o.Z)(t,u);return(0,i.mdx)("wrapper",(0,n.Z)({},m,r,{components:e,mdxType:"MDXLayout"}),(0,i.mdx)("p",null,"This is an advanced tutorial that assumes that you are comfortable with the concepts introduced in the ",(0,i.mdx)("a",{parentName:"p",href:"/docs/1.3/tutorials/basic/your_first_app/simple_cli"},"Basic Tutorial"),".\nThe examples in this tutorial are available ",(0,i.mdx)(a.Z,{to:"examples/tutorials/structured_configs",mdxType:"GithubLink"},"here"),"."),(0,i.mdx)("p",null,"Structured Configs use Python ",(0,i.mdx)("a",{parentName:"p",href:"https://docs.python.org/3.7/library/dataclasses.html"},"dataclasses")," to\ndescribe your configuration structure and types. They enable:"),(0,i.mdx)("ul",null,(0,i.mdx)("li",{parentName:"ul"},(0,i.mdx)("strong",{parentName:"li"},"Runtime type checking")," as you compose or mutate your config "),(0,i.mdx)("li",{parentName:"ul"},(0,i.mdx)("strong",{parentName:"li"},"Static type checking")," when using static type checkers (mypy, PyCharm, etc.)")),(0,i.mdx)("h4",{id:"structured-configs-supports"},"Structured Configs supports:"),(0,i.mdx)("ul",null,(0,i.mdx)("li",{parentName:"ul"},"Primitive types (",(0,i.mdx)("inlineCode",{parentName:"li"},"int"),", ",(0,i.mdx)("inlineCode",{parentName:"li"},"bool"),", ",(0,i.mdx)("inlineCode",{parentName:"li"},"float"),", ",(0,i.mdx)("inlineCode",{parentName:"li"},"str"),", ",(0,i.mdx)("inlineCode",{parentName:"li"},"Enums"),", ",(0,i.mdx)("inlineCode",{parentName:"li"},"bytes"),", ",(0,i.mdx)("inlineCode",{parentName:"li"},"pathlib.Path"),") "),(0,i.mdx)("li",{parentName:"ul"},"Nesting of Structured Configs"),(0,i.mdx)("li",{parentName:"ul"},"Containers (List and Dict) containing primitives, Structured Configs, or other lists/dicts"),(0,i.mdx)("li",{parentName:"ul"},"Optional fields")),(0,i.mdx)("h4",{id:"structured-configs-limitations"},"Structured Configs Limitations:"),(0,i.mdx)("ul",null,(0,i.mdx)("li",{parentName:"ul"},(0,i.mdx)("inlineCode",{parentName:"li"},"Union")," types are only partially supported (see ",(0,i.mdx)("a",{parentName:"li",href:"https://omegaconf.readthedocs.io/en/latest/structured_config.html#union-types"},"OmegaConf docs on unions"),")"),(0,i.mdx)("li",{parentName:"ul"},"User methods are not supported")),(0,i.mdx)("p",null,"See the ",(0,i.mdx)("a",{parentName:"p",href:"https://omegaconf.readthedocs.io/en/latest/structured_config.html"},"OmegaConf docs on Structured Configs")," for more details."),(0,i.mdx)("h4",{id:"there-are-two-primary-patterns-for-using-structured-configs-with-hydra"},"There are two primary patterns for using Structured configs with Hydra"),(0,i.mdx)("ul",null,(0,i.mdx)("li",{parentName:"ul"},"As a ",(0,i.mdx)("a",{parentName:"li",href:"/docs/1.3/tutorials/structured_config/minimal_example"},"config"),", in place of configuration files (often a starting place)"),(0,i.mdx)("li",{parentName:"ul"},"As a ",(0,i.mdx)("a",{parentName:"li",href:"/docs/1.3/tutorials/structured_config/schema"},"config schema")," validating configuration files (better for complex use cases)")),(0,i.mdx)("p",null,"With both patterns, you still get everything Hydra has to offer (config composition, Command line overrides etc).\nThis tutorial covers both. ","*",(0,i.mdx)("strong",{parentName:"p"},"Read it in order"),"*","."),(0,i.mdx)("p",null,"Hydra supports OmegaConf's Structured Configs via the ",(0,i.mdx)("inlineCode",{parentName:"p"},"ConfigStore")," API.\nThis tutorial does not assume any knowledge of them.\nIt is recommended that you visit the ",(0,i.mdx)("a",{class:"external",href:"https://omegaconf.readthedocs.io/en/latest/structured_config.html",target:"_blank"},"OmegaConf Structured Configs page")," to learn more later."))}p.isMDXComponent=!0}}]);