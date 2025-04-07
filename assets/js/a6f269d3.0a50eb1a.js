"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[2870],{15680:(e,t,n)=>{n.r(t),n.d(t,{MDXContext:()=>p,MDXProvider:()=>m,mdx:()=>h,useMDXComponents:()=>s,withMDXComponents:()=>d});var a=n(96540);function r(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function o(){return o=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var a in n)Object.prototype.hasOwnProperty.call(n,a)&&(e[a]=n[a])}return e},o.apply(this,arguments)}function i(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);t&&(a=a.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,a)}return n}function c(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?i(Object(n),!0).forEach((function(t){r(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):i(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function l(e,t){if(null==e)return{};var n,a,r=function(e,t){if(null==e)return{};var n,a,r={},o=Object.keys(e);for(a=0;a<o.length;a++)n=o[a],t.indexOf(n)>=0||(r[n]=e[n]);return r}(e,t);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(e);for(a=0;a<o.length;a++)n=o[a],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(r[n]=e[n])}return r}var p=a.createContext({}),d=function(e){return function(t){var n=s(t.components);return a.createElement(e,o({},t,{components:n}))}},s=function(e){var t=a.useContext(p),n=t;return e&&(n="function"==typeof e?e(t):c(c({},t),e)),n},m=function(e){var t=s(e.components);return a.createElement(p.Provider,{value:t},e.children)},g="mdxType",u={inlineCode:"code",wrapper:function(e){var t=e.children;return a.createElement(a.Fragment,{},t)}},f=a.forwardRef((function(e,t){var n=e.components,r=e.mdxType,o=e.originalType,i=e.parentName,p=l(e,["components","mdxType","originalType","parentName"]),d=s(n),m=r,g=d["".concat(i,".").concat(m)]||d[m]||u[m]||o;return n?a.createElement(g,c(c({ref:t},p),{},{components:n})):a.createElement(g,c({ref:t},p))}));function h(e,t){var n=arguments,r=t&&t.mdxType;if("string"==typeof e||r){var o=n.length,i=new Array(o);i[0]=f;var c={};for(var l in t)hasOwnProperty.call(t,l)&&(c[l]=t[l]);c.originalType=e,c[g]="string"==typeof e?e:r,i[1]=c;for(var p=2;p<o;p++)i[p]=n[p];return a.createElement.apply(null,i)}return a.createElement.apply(null,n)}f.displayName="MDXCreateElement"},67884:(e,t,n)=>{n.r(t),n.d(t,{assets:()=>l,contentTitle:()=>i,default:()=>m,frontMatter:()=>o,metadata:()=>c,toc:()=>p});var a=n(58168),r=(n(96540),n(15680));const o={id:"config_path_changes",title:"Config path changes",hide_title:!0},i=void 0,c={unversionedId:"upgrades/0.11_to_1.0/config_path_changes",id:"version-1.2/upgrades/0.11_to_1.0/config_path_changes",title:"Config path changes",description:"Config path changes",source:"@site/versioned_docs/version-1.2/upgrades/0.11_to_1.0/config_path_changes.md",sourceDirName:"upgrades/0.11_to_1.0",slug:"/upgrades/0.11_to_1.0/config_path_changes",permalink:"/docs/1.2/upgrades/0.11_to_1.0/config_path_changes",draft:!1,editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/versioned_docs/version-1.2/upgrades/0.11_to_1.0/config_path_changes.md",tags:[],version:"1.2",lastUpdatedBy:"jesszzzz",lastUpdatedAt:1744041844,formattedLastUpdatedAt:"Apr 7, 2025",frontMatter:{id:"config_path_changes",title:"Config path changes",hide_title:!0},sidebar:"docs",previous:{title:"Automatic schema-matching",permalink:"/docs/1.2/upgrades/1.0_to_1.1/automatic_schema_matching"},next:{title:"Adding an @package directive",permalink:"/docs/1.2/upgrades/0.11_to_1.0/adding_a_package_directive"}},l={},p=[{value:"Config path changes",id:"config-path-changes",level:2},{value:"Migration examples",id:"migration-examples",level:2}],d={toc:p},s="wrapper";function m(e){let{components:t,...n}=e;return(0,r.mdx)(s,(0,a.A)({},d,n,{components:t,mdxType:"MDXLayout"}),(0,r.mdx)("h2",{id:"config-path-changes"},"Config path changes"),(0,r.mdx)("p",null,"Hydra 1.0 adds a new ",(0,r.mdx)("inlineCode",{parentName:"p"},"config_name")," parameter to ",(0,r.mdx)("inlineCode",{parentName:"p"},"@hydra.main()")," and changes the meaning of the ",(0,r.mdx)("inlineCode",{parentName:"p"},"config_path"),".\nPreviously, ",(0,r.mdx)("inlineCode",{parentName:"p"},"config_path")," encapsulated two things:"),(0,r.mdx)("ul",null,(0,r.mdx)("li",{parentName:"ul"},"Search path relative to the declaring python file."),(0,r.mdx)("li",{parentName:"ul"},"Optional config file (.yaml) to load.")),(0,r.mdx)("p",null,"Having both of those things in the same parameter does not work well if you consider configs that are not files\nsuch as Structured Configs. In addition, it prevents overriding just the ",(0,r.mdx)("inlineCode",{parentName:"p"},"config_name")," or just the ",(0,r.mdx)("inlineCode",{parentName:"p"},"config_path")),(0,r.mdx)("p",null,"A second change is that the ",(0,r.mdx)("inlineCode",{parentName:"p"},"config_name")," no longer requires a file extension. For configs files the ",(0,r.mdx)("inlineCode",{parentName:"p"},".yaml")," extension\nwill be added automatically when the file is loaded."),(0,r.mdx)("p",null,"This change is backward compatible, but support for the old style is deprecated and will be removed in the next major Hydra version."),(0,r.mdx)("h2",{id:"migration-examples"},"Migration examples"),(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-python",metastring:'title="Hydra 0.11"',title:'"Hydra','0.11"':!0},'@hydra.main(config_path="config.yaml")\n')),(0,r.mdx)("p",null,"Becomes: "),(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-python",metastring:'title="Hydra 1.0"',title:'"Hydra','1.0"':!0},'@hydra.main(config_name="config")\n')),(0,r.mdx)("p",null,"And"),(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-python",metastring:'title="Hydra 0.11"',title:'"Hydra','0.11"':!0},'@hydra.main(config_path="conf/config.yaml")\n')),(0,r.mdx)("p",null,"Becomes:"),(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-python",metastring:'title="Hydra 1.0"',title:'"Hydra','1.0"':!0},'@hydra.main(config_path="conf", config_name="config")\n')))}m.isMDXComponent=!0}}]);