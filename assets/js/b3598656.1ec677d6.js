"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[5079],{15680:(e,t,n)=>{n.r(t),n.d(t,{MDXContext:()=>p,MDXProvider:()=>h,mdx:()=>g,useMDXComponents:()=>l,withMDXComponents:()=>s});var r=n(96540);function a(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function o(){return o=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var r in n)Object.prototype.hasOwnProperty.call(n,r)&&(e[r]=n[r])}return e},o.apply(this,arguments)}function i(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,r)}return n}function c(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?i(Object(n),!0).forEach((function(t){a(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):i(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function d(e,t){if(null==e)return{};var n,r,a=function(e,t){if(null==e)return{};var n,r,a={},o=Object.keys(e);for(r=0;r<o.length;r++)n=o[r],t.indexOf(n)>=0||(a[n]=e[n]);return a}(e,t);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(e);for(r=0;r<o.length;r++)n=o[r],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(a[n]=e[n])}return a}var p=r.createContext({}),s=function(e){return function(t){var n=l(t.components);return r.createElement(e,o({},t,{components:n}))}},l=function(e){var t=r.useContext(p),n=t;return e&&(n="function"==typeof e?e(t):c(c({},t),e)),n},h=function(e){var t=l(e.components);return r.createElement(p.Provider,{value:t},e.children)},u="mdxType",m={inlineCode:"code",wrapper:function(e){var t=e.children;return r.createElement(r.Fragment,{},t)}},f=r.forwardRef((function(e,t){var n=e.components,a=e.mdxType,o=e.originalType,i=e.parentName,p=d(e,["components","mdxType","originalType","parentName"]),s=l(n),h=a,u=s["".concat(i,".").concat(h)]||s[h]||m[h]||o;return n?r.createElement(u,c(c({ref:t},p),{},{components:n})):r.createElement(u,c({ref:t},p))}));function g(e,t){var n=arguments,a=t&&t.mdxType;if("string"==typeof e||a){var o=n.length,i=new Array(o);i[0]=f;var c={};for(var d in t)hasOwnProperty.call(t,d)&&(c[d]=t[d]);c.originalType=e,c[u]="string"==typeof e?e:a,i[1]=c;for(var p=2;p<o;p++)i[p]=n[p];return r.createElement.apply(null,i)}return r.createElement.apply(null,n)}f.displayName="MDXCreateElement"},60498:(e,t,n)=>{n.r(t),n.d(t,{assets:()=>d,contentTitle:()=>i,default:()=>h,frontMatter:()=>o,metadata:()=>c,toc:()=>p});var r=n(58168),a=(n(96540),n(15680));const o={id:"changes_to_hydra_main_config_path",title:"Changes to @hydra.main() and hydra.initialize()"},i=void 0,c={unversionedId:"upgrades/1.1_to_1.2/changes_to_hydra_main_config_path",id:"version-1.3/upgrades/1.1_to_1.2/changes_to_hydra_main_config_path",title:"Changes to @hydra.main() and hydra.initialize()",description:"Prior to Hydra 1.2, @hydra.main() and hydra.initialize() default config path was the directory containing the Python app (calling @hydra.main() or hydra.initialize()).",source:"@site/versioned_docs/version-1.3/upgrades/1.1_to_1.2/hydra_main_config_path.md",sourceDirName:"upgrades/1.1_to_1.2",slug:"/upgrades/1.1_to_1.2/changes_to_hydra_main_config_path",permalink:"/docs/1.3/upgrades/1.1_to_1.2/changes_to_hydra_main_config_path",draft:!1,editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/versioned_docs/version-1.3/upgrades/1.1_to_1.2/hydra_main_config_path.md",tags:[],version:"1.3",lastUpdatedBy:"dependabot[bot]",lastUpdatedAt:1742161400,formattedLastUpdatedAt:"Mar 16, 2025",frontMatter:{id:"changes_to_hydra_main_config_path",title:"Changes to @hydra.main() and hydra.initialize()"},sidebar:"docs",previous:{title:"version_base",permalink:"/docs/1.3/upgrades/version_base"},next:{title:"Changes to job's runtime working directory",permalink:"/docs/1.3/upgrades/1.1_to_1.2/changes_to_job_working_dir"}},d={},p=[],s={toc:p},l="wrapper";function h(e){let{components:t,...n}=e;return(0,a.mdx)(l,(0,r.A)({},s,n,{components:t,mdxType:"MDXLayout"}),(0,a.mdx)("p",null,"Prior to Hydra 1.2, ",(0,a.mdx)("strong",{parentName:"p"},"@hydra.main()")," and ",(0,a.mdx)("strong",{parentName:"p"},"hydra.initialize()")," default ",(0,a.mdx)("inlineCode",{parentName:"p"},"config path")," was the directory containing the Python app (calling ",(0,a.mdx)("strong",{parentName:"p"},"@hydra.main()")," or ",(0,a.mdx)("strong",{parentName:"p"},"hydra.initialize()"),").\nStarting with Hydra 1.1 we give ",(0,a.mdx)("a",{parentName:"p",href:"/docs/1.3/upgrades/1.0_to_1.1/changes_to_hydra_main_config_path"},"control over the default config path"),",\nand starting with Hydra 1.2, with ",(0,a.mdx)("a",{parentName:"p",href:"/docs/1.3/upgrades/version_base"},"version_base"),' >= "1.2", we choose a default config_path=None, indicating that no directory should be added to the config search path.'))}h.isMDXComponent=!0}}]);