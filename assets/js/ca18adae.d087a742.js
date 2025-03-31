"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[5921],{18:(e,t,r)=>{r.r(t),r.d(t,{assets:()=>d,contentTitle:()=>i,default:()=>h,frontMatter:()=>o,metadata:()=>c,toc:()=>p});var n=r(58168),a=(r(96540),r(15680));const o={id:"changes_to_hydra_main_config_path",title:"Changes to @hydra.main() and hydra.initialize()"},i=void 0,c={unversionedId:"upgrades/1.1_to_1.2/changes_to_hydra_main_config_path",id:"upgrades/1.1_to_1.2/changes_to_hydra_main_config_path",title:"Changes to @hydra.main() and hydra.initialize()",description:"Prior to Hydra 1.2, @hydra.main() and hydra.initialize() default config path was the directory containing the Python app (calling @hydra.main() or hydra.initialize()).",source:"@site/docs/upgrades/1.1_to_1.2/hydra_main_config_path.md",sourceDirName:"upgrades/1.1_to_1.2",slug:"/upgrades/1.1_to_1.2/changes_to_hydra_main_config_path",permalink:"/docs/upgrades/1.1_to_1.2/changes_to_hydra_main_config_path",draft:!1,editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/docs/upgrades/1.1_to_1.2/hydra_main_config_path.md",tags:[],version:"current",lastUpdatedBy:"jesszzzz",lastUpdatedAt:1743461536,formattedLastUpdatedAt:"Mar 31, 2025",frontMatter:{id:"changes_to_hydra_main_config_path",title:"Changes to @hydra.main() and hydra.initialize()"},sidebar:"docs",previous:{title:"version_base",permalink:"/docs/upgrades/version_base"},next:{title:"Changes to job's runtime working directory",permalink:"/docs/upgrades/1.1_to_1.2/changes_to_job_working_dir"}},d={},p=[],s={toc:p},l="wrapper";function h(e){let{components:t,...r}=e;return(0,a.mdx)(l,(0,n.A)({},s,r,{components:t,mdxType:"MDXLayout"}),(0,a.mdx)("p",null,"Prior to Hydra 1.2, ",(0,a.mdx)("strong",{parentName:"p"},"@hydra.main()")," and ",(0,a.mdx)("strong",{parentName:"p"},"hydra.initialize()")," default ",(0,a.mdx)("inlineCode",{parentName:"p"},"config path")," was the directory containing the Python app (calling ",(0,a.mdx)("strong",{parentName:"p"},"@hydra.main()")," or ",(0,a.mdx)("strong",{parentName:"p"},"hydra.initialize()"),").\nStarting with Hydra 1.1 we give ",(0,a.mdx)("a",{parentName:"p",href:"/docs/upgrades/1.0_to_1.1/changes_to_hydra_main_config_path"},"control over the default config path"),",\nand starting with Hydra 1.2, with ",(0,a.mdx)("a",{parentName:"p",href:"/docs/upgrades/version_base"},"version_base"),' >= "1.2", we choose a default config_path=None, indicating that no directory should be added to the config search path.'))}h.isMDXComponent=!0},15680:(e,t,r)=>{r.r(t),r.d(t,{MDXContext:()=>p,MDXProvider:()=>h,mdx:()=>g,useMDXComponents:()=>l,withMDXComponents:()=>s});var n=r(96540);function a(e,t,r){return t in e?Object.defineProperty(e,t,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[t]=r,e}function o(){return o=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var r=arguments[t];for(var n in r)Object.prototype.hasOwnProperty.call(r,n)&&(e[n]=r[n])}return e},o.apply(this,arguments)}function i(e,t){var r=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);t&&(n=n.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),r.push.apply(r,n)}return r}function c(e){for(var t=1;t<arguments.length;t++){var r=null!=arguments[t]?arguments[t]:{};t%2?i(Object(r),!0).forEach((function(t){a(e,t,r[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(r)):i(Object(r)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(r,t))}))}return e}function d(e,t){if(null==e)return{};var r,n,a=function(e,t){if(null==e)return{};var r,n,a={},o=Object.keys(e);for(n=0;n<o.length;n++)r=o[n],t.indexOf(r)>=0||(a[r]=e[r]);return a}(e,t);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(e);for(n=0;n<o.length;n++)r=o[n],t.indexOf(r)>=0||Object.prototype.propertyIsEnumerable.call(e,r)&&(a[r]=e[r])}return a}var p=n.createContext({}),s=function(e){return function(t){var r=l(t.components);return n.createElement(e,o({},t,{components:r}))}},l=function(e){var t=n.useContext(p),r=t;return e&&(r="function"==typeof e?e(t):c(c({},t),e)),r},h=function(e){var t=l(e.components);return n.createElement(p.Provider,{value:t},e.children)},u="mdxType",m={inlineCode:"code",wrapper:function(e){var t=e.children;return n.createElement(n.Fragment,{},t)}},f=n.forwardRef((function(e,t){var r=e.components,a=e.mdxType,o=e.originalType,i=e.parentName,p=d(e,["components","mdxType","originalType","parentName"]),s=l(r),h=a,u=s["".concat(i,".").concat(h)]||s[h]||m[h]||o;return r?n.createElement(u,c(c({ref:t},p),{},{components:r})):n.createElement(u,c({ref:t},p))}));function g(e,t){var r=arguments,a=t&&t.mdxType;if("string"==typeof e||a){var o=r.length,i=new Array(o);i[0]=f;var c={};for(var d in t)hasOwnProperty.call(t,d)&&(c[d]=t[d]);c.originalType=e,c[u]="string"==typeof e?e:a,i[1]=c;for(var p=2;p<o;p++)i[p]=r[p];return n.createElement.apply(null,i)}return n.createElement.apply(null,r)}f.displayName="MDXCreateElement"}}]);