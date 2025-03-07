"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[5869],{15680:(e,t,n)=>{n.r(t),n.d(t,{MDXContext:()=>l,MDXProvider:()=>m,mdx:()=>h,useMDXComponents:()=>p,withMDXComponents:()=>d});var r=n(96540);function a(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function o(){return o=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var r in n)Object.prototype.hasOwnProperty.call(n,r)&&(e[r]=n[r])}return e},o.apply(this,arguments)}function i(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,r)}return n}function s(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?i(Object(n),!0).forEach((function(t){a(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):i(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function c(e,t){if(null==e)return{};var n,r,a=function(e,t){if(null==e)return{};var n,r,a={},o=Object.keys(e);for(r=0;r<o.length;r++)n=o[r],t.indexOf(n)>=0||(a[n]=e[n]);return a}(e,t);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(e);for(r=0;r<o.length;r++)n=o[r],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(a[n]=e[n])}return a}var l=r.createContext({}),d=function(e){return function(t){var n=p(t.components);return r.createElement(e,o({},t,{components:n}))}},p=function(e){var t=r.useContext(l),n=t;return e&&(n="function"==typeof e?e(t):s(s({},t),e)),n},m=function(e){var t=p(e.components);return r.createElement(l.Provider,{value:t},e.children)},u="mdxType",g={inlineCode:"code",wrapper:function(e){var t=e.children;return r.createElement(r.Fragment,{},t)}},f=r.forwardRef((function(e,t){var n=e.components,a=e.mdxType,o=e.originalType,i=e.parentName,l=c(e,["components","mdxType","originalType","parentName"]),d=p(n),m=a,u=d["".concat(i,".").concat(m)]||d[m]||g[m]||o;return n?r.createElement(u,s(s({ref:t},l),{},{components:n})):r.createElement(u,s({ref:t},l))}));function h(e,t){var n=arguments,a=t&&t.mdxType;if("string"==typeof e||a){var o=n.length,i=new Array(o);i[0]=f;var s={};for(var c in t)hasOwnProperty.call(t,c)&&(s[c]=t[c]);s.originalType=e,s[u]="string"==typeof e?e:a,i[1]=s;for(var l=2;l<o;l++)i[l]=n[l];return r.createElement.apply(null,i)}return r.createElement.apply(null,n)}f.displayName="MDXCreateElement"},84128:(e,t,n)=>{n.r(t),n.d(t,{assets:()=>c,contentTitle:()=>i,default:()=>m,frontMatter:()=>o,metadata:()=>s,toc:()=>l});var r=n(58168),a=(n(96540),n(15680));const o={id:"object_instantiation_changes",title:"Object instantiation changes",hide_title:!0},i=void 0,s={unversionedId:"upgrades/0.11_to_1.0/object_instantiation_changes",id:"version-1.3/upgrades/0.11_to_1.0/object_instantiation_changes",title:"Object instantiation changes",description:"Object instantiation changes",source:"@site/versioned_docs/version-1.3/upgrades/0.11_to_1.0/object_instantiation_changes.md",sourceDirName:"upgrades/0.11_to_1.0",slug:"/upgrades/0.11_to_1.0/object_instantiation_changes",permalink:"/docs/1.3/upgrades/0.11_to_1.0/object_instantiation_changes",draft:!1,editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/versioned_docs/version-1.3/upgrades/0.11_to_1.0/object_instantiation_changes.md",tags:[],version:"1.3",lastUpdatedBy:"Jasha",lastUpdatedAt:1670537910,formattedLastUpdatedAt:"Dec 8, 2022",frontMatter:{id:"object_instantiation_changes",title:"Object instantiation changes",hide_title:!0},sidebar:"docs",previous:{title:"strict flag mode deprecation",permalink:"/docs/1.3/upgrades/0.11_to_1.0/strict_mode_flag_deprecated"}},c={},l=[{value:"Object instantiation changes",id:"object-instantiation-changes",level:2},{value:"Hydra configuration",id:"hydra-configuration",level:2}],d={toc:l},p="wrapper";function m(e){let{components:t,...n}=e;return(0,a.mdx)(p,(0,r.A)({},d,n,{components:t,mdxType:"MDXLayout"}),(0,a.mdx)("h2",{id:"object-instantiation-changes"},"Object instantiation changes"),(0,a.mdx)("p",null,"Hydra 1.0.0 is deprecating ObjectConf and the corresponding config structure to a simpler one without the params node.\nThis removes a level of nesting from command line and configs overrides."),(0,a.mdx)("div",{className:"row"},(0,a.mdx)("div",{className:"col col--6"},(0,a.mdx)("pre",null,(0,a.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="Hydra 0.11"',title:'"Hydra','0.11"':!0},"class: my_app.MySQLConnection\nparams:\n  host: localhost\n  user: root\n  password: 1234\n"))),(0,a.mdx)("div",{className:"col  col--6"},(0,a.mdx)("pre",null,(0,a.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="Hydra 1.0"',title:'"Hydra','1.0"':!0},"_target_: my_app.MySQLConnection\nhost: localhost\nuser: root\npassword: 1234\n\n")))),(0,a.mdx)("h2",{id:"hydra-configuration"},"Hydra configuration"),(0,a.mdx)("p",null,"Hydra plugins are configured using the same mechanism.\nThis means that this change will effect how all plugins are configured and overridden.\nThis is a breaking change for code overriding configs in such plugins, but luckily it's easy to fix."),(0,a.mdx)("p",null,"As an example, a Sweeper plugin override will change as follows:"),(0,a.mdx)("div",{className:"row"},(0,a.mdx)("div",{className:"col col--6"},(0,a.mdx)("pre",null,(0,a.mdx)("code",{parentName:"pre",className:"language-shell",metastring:'script title="Hydra 0.11"',script:!0,title:'"Hydra','0.11"':!0},"hydra.sweeper.params.max_batch_size=10\n"))),(0,a.mdx)("div",{className:"col  col--6"},(0,a.mdx)("pre",null,(0,a.mdx)("code",{parentName:"pre",className:"language-shell",metastring:'script title="Hydra 1.0"',script:!0,title:'"Hydra','1.0"':!0},"hydra.sweeper.max_batch_size=10\n")))))}m.isMDXComponent=!0}}]);