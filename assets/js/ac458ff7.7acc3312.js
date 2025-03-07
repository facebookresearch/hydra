"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[7821],{4488:(e,t,n)=>{n.r(t),n.d(t,{assets:()=>c,contentTitle:()=>o,default:()=>h,frontMatter:()=>i,metadata:()=>d,toc:()=>s});var r=n(58168),a=(n(96540),n(15680));const i={id:"changes_to_hydra_main_config_path",title:"Changes to @hydra.main() and hydra.initialize()"},o=void 0,d={unversionedId:"upgrades/1.0_to_1.1/changes_to_hydra_main_config_path",id:"version-1.1/upgrades/1.0_to_1.1/changes_to_hydra_main_config_path",title:"Changes to @hydra.main() and hydra.initialize()",description:"Prior to Hydra 1.1, @hydra.main() and hydra.initialize() default config path was the directory containing the Python app (calling @hydra.main() or hydra.initialize()).",source:"@site/versioned_docs/version-1.1/upgrades/1.0_to_1.1/hydra_main_config_path.md",sourceDirName:"upgrades/1.0_to_1.1",slug:"/upgrades/1.0_to_1.1/changes_to_hydra_main_config_path",permalink:"/docs/1.1/upgrades/1.0_to_1.1/changes_to_hydra_main_config_path",draft:!1,editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/versioned_docs/version-1.1/upgrades/1.0_to_1.1/hydra_main_config_path.md",tags:[],version:"1.1",lastUpdatedBy:"jesszzzz",lastUpdatedAt:1741383139,formattedLastUpdatedAt:"Mar 7, 2025",frontMatter:{id:"changes_to_hydra_main_config_path",title:"Changes to @hydra.main() and hydra.initialize()"},sidebar:"docs",previous:{title:"Introduction",permalink:"/docs/1.1/upgrades/intro"},next:{title:"Changes to default composition order",permalink:"/docs/1.1/upgrades/1.0_to_1.1/default_composition_order"}},c={},s=[{value:"Dedicated config directory",id:"dedicated-config-directory",level:3},{value:"No config directory",id:"no-config-directory",level:3},{value:"Using the application directory",id:"using-the-application-directory",level:3}],p={toc:s},l="wrapper";function h(e){let{components:t,...n}=e;return(0,a.mdx)(l,(0,r.A)({},p,n,{components:t,mdxType:"MDXLayout"}),(0,a.mdx)("p",null,"Prior to Hydra 1.1, ",(0,a.mdx)("strong",{parentName:"p"},"@hydra.main()")," and ",(0,a.mdx)("strong",{parentName:"p"},"hydra.initialize()")," default ",(0,a.mdx)("inlineCode",{parentName:"p"},"config path")," was the directory containing the Python app (calling ",(0,a.mdx)("strong",{parentName:"p"},"@hydra.main()")," or ",(0,a.mdx)("strong",{parentName:"p"},"hydra.initialize()"),")."),(0,a.mdx)("p",null,"This can cause unexpected behavior:"),(0,a.mdx)("ul",null,(0,a.mdx)("li",{parentName:"ul"},"Sibling directories are interpreted as config groups, which can lead to surprising results (See ",(0,a.mdx)("a",{parentName:"li",href:"https://github.com/facebookresearch/hydra/issues/1533"},"#1533"),")."),(0,a.mdx)("li",{parentName:"ul"},"The subtree added automatically can have many files/directories - which will cause ",(0,a.mdx)("strong",{parentName:"li"},"--help")," to be very slow as it's scanning for all config groups/config files (See ",(0,a.mdx)("a",{parentName:"li",href:"https://github.com/facebookresearch/hydra/issues/759"},"#759"),").")),(0,a.mdx)("p",null,"To address these issues, Hydra 1.1 issues a warning if the config_path is not specified.",(0,a.mdx)("br",{parentName:"p"}),"\n","Your options are as follows:"),(0,a.mdx)("h3",{id:"dedicated-config-directory"},"Dedicated config directory"),(0,a.mdx)("p",null,'For applications with config files, specify a directory like "conf" to use a dedicated config directory relative to the application.'),(0,a.mdx)("pre",null,(0,a.mdx)("code",{parentName:"pre",className:"language-python"},'@hydra.main(config_path="conf")\n# or:\nhydra.initialize(config_path="conf")\n')),(0,a.mdx)("h3",{id:"no-config-directory"},"No config directory"),(0,a.mdx)("p",null,"For applications that do not define config files next to the Python script (typically applications using only Structured Configs), it is recommended that\nyou pass ",(0,a.mdx)("inlineCode",{parentName:"p"},"None")," as the config_path, indicating that no directory should be added to the config search path.\nThis will become the default in Hydra 1.2."),(0,a.mdx)("pre",null,(0,a.mdx)("code",{parentName:"pre",className:"language-python"},"@hydra.main(config_path=None)\n# or:\nhydra.initialize(config_path=None)\n")),(0,a.mdx)("h3",{id:"using-the-application-directory"},"Using the application directory"),(0,a.mdx)("p",null,"Use the directory/module of the Python script.\nThis was the default behavior up to Hydra 1.0.",(0,a.mdx)("br",{parentName:"p"}),"\n","This is not recommended as it can cause the surprising behavior outlined above."),(0,a.mdx)("pre",null,(0,a.mdx)("code",{parentName:"pre",className:"language-python"},'@hydra.main(config_path=".")\n# or:\nhydra.initialize(config_path=".")\n')))}h.isMDXComponent=!0},15680:(e,t,n)=>{n.r(t),n.d(t,{MDXContext:()=>s,MDXProvider:()=>h,mdx:()=>y,useMDXComponents:()=>l,withMDXComponents:()=>p});var r=n(96540);function a(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function i(){return i=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var r in n)Object.prototype.hasOwnProperty.call(n,r)&&(e[r]=n[r])}return e},i.apply(this,arguments)}function o(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,r)}return n}function d(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?o(Object(n),!0).forEach((function(t){a(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):o(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function c(e,t){if(null==e)return{};var n,r,a=function(e,t){if(null==e)return{};var n,r,a={},i=Object.keys(e);for(r=0;r<i.length;r++)n=i[r],t.indexOf(n)>=0||(a[n]=e[n]);return a}(e,t);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);for(r=0;r<i.length;r++)n=i[r],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(a[n]=e[n])}return a}var s=r.createContext({}),p=function(e){return function(t){var n=l(t.components);return r.createElement(e,i({},t,{components:n}))}},l=function(e){var t=r.useContext(s),n=t;return e&&(n="function"==typeof e?e(t):d(d({},t),e)),n},h=function(e){var t=l(e.components);return r.createElement(s.Provider,{value:t},e.children)},u="mdxType",m={inlineCode:"code",wrapper:function(e){var t=e.children;return r.createElement(r.Fragment,{},t)}},f=r.forwardRef((function(e,t){var n=e.components,a=e.mdxType,i=e.originalType,o=e.parentName,s=c(e,["components","mdxType","originalType","parentName"]),p=l(n),h=a,u=p["".concat(o,".").concat(h)]||p[h]||m[h]||i;return n?r.createElement(u,d(d({ref:t},s),{},{components:n})):r.createElement(u,d({ref:t},s))}));function y(e,t){var n=arguments,a=t&&t.mdxType;if("string"==typeof e||a){var i=n.length,o=new Array(i);o[0]=f;var d={};for(var c in t)hasOwnProperty.call(t,c)&&(d[c]=t[c]);d.originalType=e,d[u]="string"==typeof e?e:a,o[1]=d;for(var s=2;s<i;s++)o[s]=n[s];return r.createElement.apply(null,o)}return r.createElement.apply(null,n)}f.displayName="MDXCreateElement"}}]);