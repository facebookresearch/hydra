"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[854],{15680:(e,t,r)=>{r.r(t),r.d(t,{MDXContext:()=>p,MDXProvider:()=>u,mdx:()=>g,useMDXComponents:()=>l,withMDXComponents:()=>d});var n=r(96540);function a(e,t,r){return t in e?Object.defineProperty(e,t,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[t]=r,e}function o(){return o=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var r=arguments[t];for(var n in r)Object.prototype.hasOwnProperty.call(r,n)&&(e[n]=r[n])}return e},o.apply(this,arguments)}function i(e,t){var r=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);t&&(n=n.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),r.push.apply(r,n)}return r}function c(e){for(var t=1;t<arguments.length;t++){var r=null!=arguments[t]?arguments[t]:{};t%2?i(Object(r),!0).forEach((function(t){a(e,t,r[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(r)):i(Object(r)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(r,t))}))}return e}function s(e,t){if(null==e)return{};var r,n,a=function(e,t){if(null==e)return{};var r,n,a={},o=Object.keys(e);for(n=0;n<o.length;n++)r=o[n],t.indexOf(r)>=0||(a[r]=e[r]);return a}(e,t);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(e);for(n=0;n<o.length;n++)r=o[n],t.indexOf(r)>=0||Object.prototype.propertyIsEnumerable.call(e,r)&&(a[r]=e[r])}return a}var p=n.createContext({}),d=function(e){return function(t){var r=l(t.components);return n.createElement(e,o({},t,{components:r}))}},l=function(e){var t=n.useContext(p),r=t;return e&&(r="function"==typeof e?e(t):c(c({},t),e)),r},u=function(e){var t=l(e.components);return n.createElement(p.Provider,{value:t},e.children)},h="mdxType",f={inlineCode:"code",wrapper:function(e){var t=e.children;return n.createElement(n.Fragment,{},t)}},m=n.forwardRef((function(e,t){var r=e.components,a=e.mdxType,o=e.originalType,i=e.parentName,p=s(e,["components","mdxType","originalType","parentName"]),d=l(r),u=a,h=d["".concat(i,".").concat(u)]||d[u]||f[u]||o;return r?n.createElement(h,c(c({ref:t},p),{},{components:r})):n.createElement(h,c({ref:t},p))}));function g(e,t){var r=arguments,a=t&&t.mdxType;if("string"==typeof e||a){var o=r.length,i=new Array(o);i[0]=m;var c={};for(var s in t)hasOwnProperty.call(t,s)&&(c[s]=t[s]);c.originalType=e,c[h]="string"==typeof e?e:a,i[1]=c;for(var p=2;p<o;p++)i[p]=r[p];return n.createElement.apply(null,i)}return n.createElement.apply(null,r)}m.displayName="MDXCreateElement"},64884:(e,t,r)=>{r.r(t),r.d(t,{assets:()=>s,contentTitle:()=>i,default:()=>u,frontMatter:()=>o,metadata:()=>c,toc:()=>p});var n=r(58168),a=(r(96540),r(15680));const o={id:"search_path",title:"Config Search Path"},i=void 0,c={unversionedId:"advanced/search_path",id:"version-1.0/advanced/search_path",title:"Config Search Path",description:"The Config Search Path is a list of paths that are searched in order to find configs. It is similar to",source:"@site/versioned_docs/version-1.0/advanced/search_path.md",sourceDirName:"advanced",slug:"/advanced/search_path",permalink:"/docs/1.0/advanced/search_path",draft:!1,editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/versioned_docs/version-1.0/advanced/search_path.md",tags:[],version:"1.0",lastUpdatedBy:"Omry Yadan",lastUpdatedAt:1599148883,formattedLastUpdatedAt:"Sep 3, 2020",frontMatter:{id:"search_path",title:"Config Search Path"},sidebar:"docs",previous:{title:"Overriding packages",permalink:"/docs/1.0/advanced/overriding_packages"},next:{title:"Hydra plugins",permalink:"/docs/1.0/advanced/plugins"}},s={},p=[],d={toc:p},l="wrapper";function u(e){let{components:t,...r}=e;return(0,a.mdx)(l,(0,n.A)({},d,r,{components:t,mdxType:"MDXLayout"}),(0,a.mdx)("p",null,"The Config Search Path is a list of paths that are searched in order to find configs. It is similar to\nthe Python PYTHONPATH."),(0,a.mdx)("ul",null,(0,a.mdx)("li",{parentName:"ul"},"When a config is requested, The first matching config in the search path is used."),(0,a.mdx)("li",{parentName:"ul"},"Each search path element has a schema prefix such as file:// or pkg:// that is corresponding to a ConfigSourcePlugin."),(0,a.mdx)("li",{parentName:"ul"},(0,a.mdx)("inlineCode",{parentName:"li"},"SearchPathPlugin")," can manipulate the search path.")),(0,a.mdx)("p",null,"You can inspect the search path and the configurations loaded by Hydra by turning on verbose logging for the ",(0,a.mdx)("inlineCode",{parentName:"p"},"hydra")," logger:"),(0,a.mdx)("pre",null,(0,a.mdx)("code",{parentName:"pre",className:"language-text"},"$ python my_app.py hydra.verbose=hydra\n")))}u.isMDXComponent=!0}}]);