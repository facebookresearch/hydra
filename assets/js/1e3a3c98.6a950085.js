"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[5504],{15680:(e,r,t)=>{t.r(r),t.d(r,{MDXContext:()=>s,MDXProvider:()=>g,mdx:()=>h,useMDXComponents:()=>d,withMDXComponents:()=>c});var n=t(96540);function o(e,r,t){return r in e?Object.defineProperty(e,r,{value:t,enumerable:!0,configurable:!0,writable:!0}):e[r]=t,e}function l(){return l=Object.assign||function(e){for(var r=1;r<arguments.length;r++){var t=arguments[r];for(var n in t)Object.prototype.hasOwnProperty.call(t,n)&&(e[n]=t[n])}return e},l.apply(this,arguments)}function a(e,r){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);r&&(n=n.filter((function(r){return Object.getOwnPropertyDescriptor(e,r).enumerable}))),t.push.apply(t,n)}return t}function i(e){for(var r=1;r<arguments.length;r++){var t=null!=arguments[r]?arguments[r]:{};r%2?a(Object(t),!0).forEach((function(r){o(e,r,t[r])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):a(Object(t)).forEach((function(r){Object.defineProperty(e,r,Object.getOwnPropertyDescriptor(t,r))}))}return e}function p(e,r){if(null==e)return{};var t,n,o=function(e,r){if(null==e)return{};var t,n,o={},l=Object.keys(e);for(n=0;n<l.length;n++)t=l[n],r.indexOf(t)>=0||(o[t]=e[t]);return o}(e,r);if(Object.getOwnPropertySymbols){var l=Object.getOwnPropertySymbols(e);for(n=0;n<l.length;n++)t=l[n],r.indexOf(t)>=0||Object.prototype.propertyIsEnumerable.call(e,t)&&(o[t]=e[t])}return o}var s=n.createContext({}),c=function(e){return function(r){var t=d(r.components);return n.createElement(e,l({},r,{components:t}))}},d=function(e){var r=n.useContext(s),t=r;return e&&(t="function"==typeof e?e(r):i(i({},r),e)),t},g=function(e){var r=d(e.components);return n.createElement(s.Provider,{value:r},e.children)},m="mdxType",u={inlineCode:"code",wrapper:function(e){var r=e.children;return n.createElement(n.Fragment,{},r)}},y=n.forwardRef((function(e,r){var t=e.components,o=e.mdxType,l=e.originalType,a=e.parentName,s=p(e,["components","mdxType","originalType","parentName"]),c=d(t),g=o,m=c["".concat(a,".").concat(g)]||c[g]||u[g]||l;return t?n.createElement(m,i(i({ref:r},s),{},{components:t})):n.createElement(m,i({ref:r},s))}));function h(e,r){var t=arguments,o=r&&r.mdxType;if("string"==typeof e||o){var l=t.length,a=new Array(l);a[0]=y;var i={};for(var p in r)hasOwnProperty.call(r,p)&&(i[p]=r[p]);i.originalType=e,i[m]="string"==typeof e?e:o,a[1]=i;for(var s=2;s<l;s++)a[s]=t[s];return n.createElement.apply(null,a)}return n.createElement.apply(null,t)}y.displayName="MDXCreateElement"},17940:(e,r,t)=>{t.r(r),t.d(r,{assets:()=>s,contentTitle:()=>i,default:()=>y,frontMatter:()=>a,metadata:()=>p,toc:()=>c});var n=t(58168),o=(t(96540),t(15680)),l=t(49595);const a={id:"colorlog",title:"Colorlog plugin",sidebar_label:"Colorlog plugin"},i=void 0,p={unversionedId:"plugins/colorlog",id:"version-1.1/plugins/colorlog",title:"Colorlog plugin",description:"PyPI",source:"@site/versioned_docs/version-1.1/plugins/colorlog.md",sourceDirName:"plugins",slug:"/plugins/colorlog",permalink:"/docs/1.1/plugins/colorlog",draft:!1,editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/versioned_docs/version-1.1/plugins/colorlog.md",tags:[],version:"1.1",lastUpdatedBy:"Omry Yadan",lastUpdatedAt:1623349300,formattedLastUpdatedAt:"Jun 10, 2021",frontMatter:{id:"colorlog",title:"Colorlog plugin",sidebar_label:"Colorlog plugin"},sidebar:"docs",previous:{title:"Customizing Application's help",permalink:"/docs/1.1/configure_hydra/app_help"},next:{title:"Joblib Launcher plugin",permalink:"/docs/1.1/plugins/joblib_launcher"}},s={},c=[{value:"Installation",id:"installation",level:3},{value:"Usage",id:"usage",level:3}],d=(g="GithubLink",function(e){return console.warn("Component "+g+" was not imported, exported, or provided by MDXProvider as global scope"),(0,o.mdx)("div",e)});var g;const m={toc:c},u="wrapper";function y(e){let{components:r,...a}=e;return(0,o.mdx)(u,(0,n.A)({},m,a,{components:r,mdxType:"MDXLayout"}),(0,o.mdx)("p",null,(0,o.mdx)("a",{parentName:"p",href:"https://pypi.org/project/hydra-colorlog/"},(0,o.mdx)("img",{parentName:"a",src:"https://img.shields.io/pypi/v/hydra-colorlog",alt:"PyPI"})),"\n",(0,o.mdx)("img",{parentName:"p",src:"https://img.shields.io/pypi/l/hydra-colorlog",alt:"PyPI - License"}),"\n",(0,o.mdx)("img",{parentName:"p",src:"https://img.shields.io/pypi/pyversions/hydra-colorlog",alt:"PyPI - Python Version"}),"\n",(0,o.mdx)("a",{parentName:"p",href:"https://pypistats.org/packages/hydra-colorlog"},(0,o.mdx)("img",{parentName:"a",src:"https://img.shields.io/pypi/dm/hydra-colorlog.svg",alt:"PyPI - Downloads"})),(0,o.mdx)(l.C,{text:"Example application",to:"plugins/hydra_colorlog/example",mdxType:"ExampleGithubLink"}),(0,o.mdx)(l.C,{text:"Plugin source",to:"plugins/hydra_colorlog",mdxType:"ExampleGithubLink"})),(0,o.mdx)("p",null,"Adds ",(0,o.mdx)("a",{class:"external",href:"https://github.com/borntyping/python-colorlog",target:"_blank"},"colorlog")," colored logs for ",(0,o.mdx)("inlineCode",{parentName:"p"},"hydra/job_logging")," and ",(0,o.mdx)("inlineCode",{parentName:"p"},"hydra/hydra_logging"),"."),(0,o.mdx)("h3",{id:"installation"},"Installation"),(0,o.mdx)("pre",null,(0,o.mdx)("code",{parentName:"pre",className:"language-commandline"},"pip install hydra_colorlog --upgrade\n")),(0,o.mdx)("h3",{id:"usage"},"Usage"),(0,o.mdx)("p",null,"Override ",(0,o.mdx)("inlineCode",{parentName:"p"},"hydra/job_logging")," and ",(0,o.mdx)("inlineCode",{parentName:"p"},"hydra/hydra_logging")," in your config:"),(0,o.mdx)("pre",null,(0,o.mdx)("code",{parentName:"pre",className:"language-yaml"},"defaults:\n  - override hydra/job_logging: colorlog\n  - override hydra/hydra_logging: colorlog\n")),(0,o.mdx)("p",null,"There are several standard approaches for configuring plugins. Check ",(0,o.mdx)("a",{parentName:"p",href:"/docs/1.1/patterns/configuring_plugins"},"this page")," for more information."),(0,o.mdx)("p",null,"See included ",(0,o.mdx)(d,{to:"plugins/hydra_colorlog/example",mdxType:"GithubLink"},"example application"),"."),(0,o.mdx)("p",null,(0,o.mdx)("img",{alt:"Colored log output",src:t(91276).A,width:"693",height:"138"})))}y.isMDXComponent=!0},49595:(e,r,t)=>{t.d(r,{A:()=>s,C:()=>c});var n=t(58168),o=t(96540),l=t(75489),a=t(44586),i=t(48295);function p(e){const r=(0,i.ir)();return(0,a.default)().siteConfig.customFields.githubLinkVersionToBaseUrl[r?.name??"current"]+e}function s(e){return o.createElement(l.default,(0,n.A)({},e,{to:p(e.to),target:"_blank"}))}function c(e){const r=e.text??"Example (Click Here)";return o.createElement(s,e,o.createElement("span",null,"\xa0"),o.createElement("img",{src:"https://img.shields.io/badge/-"+r+"-informational",alt:"Example (Click Here)"}))}},91276:(e,r,t)=>{t.d(r,{A:()=>n});const n=t.p+"assets/images/colorlog-b20147697b9d16362f62a5d0bb58347f.png"}}]);