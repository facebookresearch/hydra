"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[1629],{15680:(e,t,r)=>{r.r(t),r.d(t,{MDXContext:()=>c,MDXProvider:()=>l,mdx:()=>b,useMDXComponents:()=>u,withMDXComponents:()=>d});var n=r(96540);function o(e,t,r){return t in e?Object.defineProperty(e,t,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[t]=r,e}function a(){return a=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var r=arguments[t];for(var n in r)Object.prototype.hasOwnProperty.call(r,n)&&(e[n]=r[n])}return e},a.apply(this,arguments)}function i(e,t){var r=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);t&&(n=n.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),r.push.apply(r,n)}return r}function p(e){for(var t=1;t<arguments.length;t++){var r=null!=arguments[t]?arguments[t]:{};t%2?i(Object(r),!0).forEach((function(t){o(e,t,r[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(r)):i(Object(r)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(r,t))}))}return e}function s(e,t){if(null==e)return{};var r,n,o=function(e,t){if(null==e)return{};var r,n,o={},a=Object.keys(e);for(n=0;n<a.length;n++)r=a[n],t.indexOf(r)>=0||(o[r]=e[r]);return o}(e,t);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);for(n=0;n<a.length;n++)r=a[n],t.indexOf(r)>=0||Object.prototype.propertyIsEnumerable.call(e,r)&&(o[r]=e[r])}return o}var c=n.createContext({}),d=function(e){return function(t){var r=u(t.components);return n.createElement(e,a({},t,{components:r}))}},u=function(e){var t=n.useContext(c),r=t;return e&&(r="function"==typeof e?e(t):p(p({},t),e)),r},l=function(e){var t=u(e.components);return n.createElement(c.Provider,{value:t},e.children)},m="mdxType",y={inlineCode:"code",wrapper:function(e){var t=e.children;return n.createElement(n.Fragment,{},t)}},f=n.forwardRef((function(e,t){var r=e.components,o=e.mdxType,a=e.originalType,i=e.parentName,c=s(e,["components","mdxType","originalType","parentName"]),d=u(r),l=o,m=d["".concat(i,".").concat(l)]||d[l]||y[l]||a;return r?n.createElement(m,p(p({ref:t},c),{},{components:r})):n.createElement(m,p({ref:t},c))}));function b(e,t){var r=arguments,o=t&&t.mdxType;if("string"==typeof e||o){var a=r.length,i=new Array(a);i[0]=f;var p={};for(var s in t)hasOwnProperty.call(t,s)&&(p[s]=t[s]);p.originalType=e,p[m]="string"==typeof e?e:o,i[1]=p;for(var c=2;c<a;c++)i[c]=r[c];return n.createElement.apply(null,i)}return n.createElement.apply(null,r)}f.displayName="MDXCreateElement"},59031:(e,t,r)=>{r.r(t),r.d(t,{assets:()=>s,contentTitle:()=>i,default:()=>l,frontMatter:()=>a,metadata:()=>p,toc:()=>c});var n=r(58168),o=(r(96540),r(15680));const a={id:"jupyter_notebooks",title:"Hydra in Jupyter Notebooks"},i=void 0,p={unversionedId:"advanced/jupyter_notebooks",id:"version-1.1/advanced/jupyter_notebooks",title:"Hydra in Jupyter Notebooks",description:"Hydra supports config composition inside Jupyter notebooks via the Compose API.",source:"@site/versioned_docs/version-1.1/advanced/jupyter_notebooks.md",sourceDirName:"advanced",slug:"/advanced/jupyter_notebooks",permalink:"/docs/1.1/advanced/jupyter_notebooks",draft:!1,editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/versioned_docs/version-1.1/advanced/jupyter_notebooks.md",tags:[],version:"1.1",lastUpdatedBy:"Will Price",lastUpdatedAt:1631697e3,formattedLastUpdatedAt:"Sep 15, 2021",frontMatter:{id:"jupyter_notebooks",title:"Hydra in Jupyter Notebooks"},sidebar:"docs",previous:{title:"Application packaging",permalink:"/docs/1.1/advanced/app_packaging"},next:{title:"Hydra in Unit Tests",permalink:"/docs/1.1/advanced/unit_testing"}},s={},c=[],d={toc:c},u="wrapper";function l(e){let{components:t,...r}=e;return(0,o.mdx)(u,(0,n.A)({},d,r,{components:t,mdxType:"MDXLayout"}),(0,o.mdx)("p",null,"Hydra supports config composition inside Jupyter notebooks via the ",(0,o.mdx)("a",{parentName:"p",href:"/docs/1.1/advanced/compose_api"},"Compose API"),".  "),(0,o.mdx)("p",null,"Run the Notebook in a the Binder to see a live demo, or open the Notebook source on GitHub."),(0,o.mdx)("p",null,(0,o.mdx)("a",{parentName:"p",href:"https://mybinder.org/v2/gh/facebookresearch/hydra/main?filepath=examples%252jupyter_notebooks"},(0,o.mdx)("img",{parentName:"a",src:"https://mybinder.org/badge_logo.svg",alt:"Binder"})),"\n",(0,o.mdx)("a",{parentName:"p",href:"https://github.com/facebookresearch/hydra//tree/main/examples/jupyter_notebooks/"},(0,o.mdx)("img",{parentName:"a",src:"https://img.shields.io/badge/-Notebooks%20source-informational",alt:"Notebook source"}))))}l.isMDXComponent=!0}}]);