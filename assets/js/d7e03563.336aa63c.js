"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[3742],{12115:(e,t,n)=>{n.r(t),n.d(t,{assets:()=>s,contentTitle:()=>l,default:()=>d,frontMatter:()=>i,metadata:()=>g,toc:()=>c});var r=n(58168),o=(n(96540),n(15680)),a=n(49595);const i={id:"logging",title:"Customizing logging",sidebar_label:"Customizing logging"},l=void 0,g={unversionedId:"configure_hydra/logging",id:"configure_hydra/logging",title:"Customizing logging",description:"Hydra is configuring Python standard logging library with the dictConfig method. You can learn more about it here.",source:"@site/docs/configure_hydra/logging.md",sourceDirName:"configure_hydra",slug:"/configure_hydra/logging",permalink:"/docs/configure_hydra/logging",draft:!1,editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/docs/configure_hydra/logging.md",tags:[],version:"current",lastUpdatedBy:"jesszzzz",lastUpdatedAt:1741814683,formattedLastUpdatedAt:"Mar 12, 2025",frontMatter:{id:"logging",title:"Customizing logging",sidebar_label:"Customizing logging"},sidebar:"docs",previous:{title:"Job Configuration",permalink:"/docs/configure_hydra/job"},next:{title:"Customizing working directory pattern",permalink:"/docs/configure_hydra/workdir"}},s={},c=[],u={toc:c},m="wrapper";function d(e){let{components:t,...n}=e;return(0,o.mdx)(m,(0,r.A)({},u,n,{components:t,mdxType:"MDXLayout"}),(0,o.mdx)(a.C,{text:"Example application",to:"examples/configure_hydra/logging",mdxType:"ExampleGithubLink"}),(0,o.mdx)("p",null,"Hydra is configuring Python standard logging library with the dictConfig method. You can learn more about it ",(0,o.mdx)("a",{parentName:"p",href:"https://docs.python.org/3/howto/logging.html"},"here"),".\nThere are two logging configurations, one for Hydra itself and one for the executed jobs."),(0,o.mdx)("p",null,"This example demonstrates how to customize the logging behavior of your Hydra app, by making the following changes\nto the default logging behavior:"),(0,o.mdx)("ul",null,(0,o.mdx)("li",{parentName:"ul"},"Outputs only to stdout (no log file)"),(0,o.mdx)("li",{parentName:"ul"},"Output a simpler log line pattern")),(0,o.mdx)("pre",null,(0,o.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="config.yaml"',title:'"config.yaml"'},"defaults:\n  - override hydra/job_logging: custom\n")),(0,o.mdx)("pre",null,(0,o.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="hydra/job_logging/custom.yaml"',title:'"hydra/job_logging/custom.yaml"'},"version: 1\nformatters:\n  simple:\n    format: '[%(levelname)s] - %(message)s'\nhandlers:\n  console:\n    class: logging.StreamHandler\n    formatter: simple\n    stream: ext://sys.stdout\nroot:\n  handlers: [console]\n\ndisable_existing_loggers: false\n")),(0,o.mdx)("p",null,"This is what the default logging looks like:"),(0,o.mdx)("pre",null,(0,o.mdx)("code",{parentName:"pre"},"$ python my_app.py hydra/job_logging=default\n[2020-08-24 13:43:26,761][__main__][INFO] - Info level message\n")),(0,o.mdx)("p",null,"And this is what the custom logging looks like:"),(0,o.mdx)("pre",null,(0,o.mdx)("code",{parentName:"pre",className:"language-text"},"$ python my_app.py \n[INFO] - Info level message\n")))}d.isMDXComponent=!0},15680:(e,t,n)=>{n.r(t),n.d(t,{MDXContext:()=>s,MDXProvider:()=>m,mdx:()=>y,useMDXComponents:()=>u,withMDXComponents:()=>c});var r=n(96540);function o(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function a(){return a=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var r in n)Object.prototype.hasOwnProperty.call(n,r)&&(e[r]=n[r])}return e},a.apply(this,arguments)}function i(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,r)}return n}function l(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?i(Object(n),!0).forEach((function(t){o(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):i(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function g(e,t){if(null==e)return{};var n,r,o=function(e,t){if(null==e)return{};var n,r,o={},a=Object.keys(e);for(r=0;r<a.length;r++)n=a[r],t.indexOf(n)>=0||(o[n]=e[n]);return o}(e,t);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);for(r=0;r<a.length;r++)n=a[r],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(o[n]=e[n])}return o}var s=r.createContext({}),c=function(e){return function(t){var n=u(t.components);return r.createElement(e,a({},t,{components:n}))}},u=function(e){var t=r.useContext(s),n=t;return e&&(n="function"==typeof e?e(t):l(l({},t),e)),n},m=function(e){var t=u(e.components);return r.createElement(s.Provider,{value:t},e.children)},d="mdxType",p={inlineCode:"code",wrapper:function(e){var t=e.children;return r.createElement(r.Fragment,{},t)}},f=r.forwardRef((function(e,t){var n=e.components,o=e.mdxType,a=e.originalType,i=e.parentName,s=g(e,["components","mdxType","originalType","parentName"]),c=u(n),m=o,d=c["".concat(i,".").concat(m)]||c[m]||p[m]||a;return n?r.createElement(d,l(l({ref:t},s),{},{components:n})):r.createElement(d,l({ref:t},s))}));function y(e,t){var n=arguments,o=t&&t.mdxType;if("string"==typeof e||o){var a=n.length,i=new Array(a);i[0]=f;var l={};for(var g in t)hasOwnProperty.call(t,g)&&(l[g]=t[g]);l.originalType=e,l[d]="string"==typeof e?e:o,i[1]=l;for(var s=2;s<a;s++)i[s]=n[s];return r.createElement.apply(null,i)}return r.createElement.apply(null,n)}f.displayName="MDXCreateElement"},49595:(e,t,n)=>{n.d(t,{A:()=>s,C:()=>c});var r=n(58168),o=n(96540),a=n(75489),i=n(44586),l=n(48295);function g(e){const t=(0,l.ir)();return(0,i.default)().siteConfig.customFields.githubLinkVersionToBaseUrl[t?.name??"current"]+e}function s(e){return o.createElement(a.default,(0,r.A)({},e,{to:g(e.to),target:"_blank"}))}function c(e){const t=e.text??"Example (Click Here)";return o.createElement(s,e,o.createElement("span",null,"\xa0"),o.createElement("img",{src:"https://img.shields.io/badge/-"+t+"-informational",alt:"Example (Click Here)"}))}}}]);