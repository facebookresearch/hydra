"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[2729],{325:(e,r,t)=>{t.r(r),t.d(r,{assets:()=>p,contentTitle:()=>l,default:()=>g,frontMatter:()=>a,metadata:()=>i,toc:()=>s});var o=t(58168),n=(t(96540),t(15680));const a={id:"colorlog",title:"Colorlog plugin",sidebar_label:"Colorlog plugin"},l=void 0,i={unversionedId:"plugins/colorlog",id:"version-1.0/plugins/colorlog",title:"Colorlog plugin",description:"PyPI",source:"@site/versioned_docs/version-1.0/plugins/colorlog.md",sourceDirName:"plugins",slug:"/plugins/colorlog",permalink:"/docs/1.0/plugins/colorlog",draft:!1,editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/versioned_docs/version-1.0/plugins/colorlog.md",tags:[],version:"1.0",lastUpdatedBy:"jesszzzz",lastUpdatedAt:1741383139,formattedLastUpdatedAt:"Mar 7, 2025",frontMatter:{id:"colorlog",title:"Colorlog plugin",sidebar_label:"Colorlog plugin"},sidebar:"docs",previous:{title:"Customizing Application's help",permalink:"/docs/1.0/configure_hydra/app_help"},next:{title:"Joblib Launcher plugin",permalink:"/docs/1.0/plugins/joblib_launcher"}},p={},s=[{value:"Installation",id:"installation",level:3},{value:"Usage",id:"usage",level:3}],c={toc:s},d="wrapper";function g(e){let{components:r,...a}=e;return(0,n.mdx)(d,(0,o.A)({},c,a,{components:r,mdxType:"MDXLayout"}),(0,n.mdx)("p",null,(0,n.mdx)("a",{parentName:"p",href:"https://pypi.org/project/hydra-colorlog/"},(0,n.mdx)("img",{parentName:"a",src:"https://img.shields.io/pypi/v/hydra-colorlog",alt:"PyPI"})),"\n",(0,n.mdx)("img",{parentName:"p",src:"https://img.shields.io/pypi/l/hydra-colorlog",alt:"PyPI - License"}),"\n",(0,n.mdx)("img",{parentName:"p",src:"https://img.shields.io/pypi/pyversions/hydra-colorlog",alt:"PyPI - Python Version"}),"\n",(0,n.mdx)("a",{parentName:"p",href:"https://pypistats.org/packages/hydra-colorlog"},(0,n.mdx)("img",{parentName:"a",src:"https://img.shields.io/pypi/dm/hydra-colorlog.svg",alt:"PyPI - Downloads"})),"\n",(0,n.mdx)("a",{parentName:"p",href:"https://github.com/facebookresearch/hydra/tree/1.0_branch/plugins/hydra_colorlog/example"},(0,n.mdx)("img",{parentName:"a",src:"https://img.shields.io/badge/-Example%20application-informational",alt:"Example application"})),"\n",(0,n.mdx)("a",{parentName:"p",href:"https://github.com/facebookresearch/hydra/tree/1.0_branch/plugins/hydra_colorlog"},(0,n.mdx)("img",{parentName:"a",src:"https://img.shields.io/badge/-Plugin%20source-informational",alt:"Plugin source"}))),(0,n.mdx)("p",null,"Adds ",(0,n.mdx)("a",{class:"external",href:"https://github.com/borntyping/python-colorlog",target:"_blank"},"colorlog")," colored logs for ",(0,n.mdx)("inlineCode",{parentName:"p"},"hydra/job_logging")," and ",(0,n.mdx)("inlineCode",{parentName:"p"},"hydra/hydra_logging"),"."),(0,n.mdx)("h3",{id:"installation"},"Installation"),(0,n.mdx)("pre",null,(0,n.mdx)("code",{parentName:"pre",className:"language-commandline"},"pip install hydra_colorlog --upgrade\n")),(0,n.mdx)("h3",{id:"usage"},"Usage"),(0,n.mdx)("p",null,"Override ",(0,n.mdx)("inlineCode",{parentName:"p"},"hydra/job_logging")," and ",(0,n.mdx)("inlineCode",{parentName:"p"},"hydra/hydra_logging")," your config:"),(0,n.mdx)("pre",null,(0,n.mdx)("code",{parentName:"pre",className:"language-yaml"},"defaults:\n  - hydra/job_logging: colorlog\n  - hydra/hydra_logging: colorlog\n")),(0,n.mdx)("p",null,"See included ",(0,n.mdx)("a",{parentName:"p",href:"https://github.com/facebookresearch/hydra/tree/1.0_branch/plugins/hydra_colorlog/example"},"example"),"."),(0,n.mdx)("p",null,(0,n.mdx)("img",{alt:"Colored log output",src:t(93207).A,width:"693",height:"138"})))}g.isMDXComponent=!0},15680:(e,r,t)=>{t.r(r),t.d(r,{MDXContext:()=>s,MDXProvider:()=>g,mdx:()=>y,useMDXComponents:()=>d,withMDXComponents:()=>c});var o=t(96540);function n(e,r,t){return r in e?Object.defineProperty(e,r,{value:t,enumerable:!0,configurable:!0,writable:!0}):e[r]=t,e}function a(){return a=Object.assign||function(e){for(var r=1;r<arguments.length;r++){var t=arguments[r];for(var o in t)Object.prototype.hasOwnProperty.call(t,o)&&(e[o]=t[o])}return e},a.apply(this,arguments)}function l(e,r){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(e);r&&(o=o.filter((function(r){return Object.getOwnPropertyDescriptor(e,r).enumerable}))),t.push.apply(t,o)}return t}function i(e){for(var r=1;r<arguments.length;r++){var t=null!=arguments[r]?arguments[r]:{};r%2?l(Object(t),!0).forEach((function(r){n(e,r,t[r])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):l(Object(t)).forEach((function(r){Object.defineProperty(e,r,Object.getOwnPropertyDescriptor(t,r))}))}return e}function p(e,r){if(null==e)return{};var t,o,n=function(e,r){if(null==e)return{};var t,o,n={},a=Object.keys(e);for(o=0;o<a.length;o++)t=a[o],r.indexOf(t)>=0||(n[t]=e[t]);return n}(e,r);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);for(o=0;o<a.length;o++)t=a[o],r.indexOf(t)>=0||Object.prototype.propertyIsEnumerable.call(e,t)&&(n[t]=e[t])}return n}var s=o.createContext({}),c=function(e){return function(r){var t=d(r.components);return o.createElement(e,a({},r,{components:t}))}},d=function(e){var r=o.useContext(s),t=r;return e&&(t="function"==typeof e?e(r):i(i({},r),e)),t},g=function(e){var r=d(e.components);return o.createElement(s.Provider,{value:r},e.children)},m="mdxType",u={inlineCode:"code",wrapper:function(e){var r=e.children;return o.createElement(o.Fragment,{},r)}},h=o.forwardRef((function(e,r){var t=e.components,n=e.mdxType,a=e.originalType,l=e.parentName,s=p(e,["components","mdxType","originalType","parentName"]),c=d(t),g=n,m=c["".concat(l,".").concat(g)]||c[g]||u[g]||a;return t?o.createElement(m,i(i({ref:r},s),{},{components:t})):o.createElement(m,i({ref:r},s))}));function y(e,r){var t=arguments,n=r&&r.mdxType;if("string"==typeof e||n){var a=t.length,l=new Array(a);l[0]=h;var i={};for(var p in r)hasOwnProperty.call(r,p)&&(i[p]=r[p]);i.originalType=e,i[m]="string"==typeof e?e:n,l[1]=i;for(var s=2;s<a;s++)l[s]=t[s];return o.createElement.apply(null,l)}return o.createElement.apply(null,t)}h.displayName="MDXCreateElement"},93207:(e,r,t)=>{t.d(r,{A:()=>o});const o=t.p+"assets/images/colorlog-b20147697b9d16362f62a5d0bb58347f.png"}}]);