"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[5815],{15680:(e,a,t)=>{t.r(a),t.d(a,{MDXContext:()=>c,MDXProvider:()=>p,mdx:()=>h,useMDXComponents:()=>m,withMDXComponents:()=>s});var r=t(96540);function n(e,a,t){return a in e?Object.defineProperty(e,a,{value:t,enumerable:!0,configurable:!0,writable:!0}):e[a]=t,e}function o(){return o=Object.assign||function(e){for(var a=1;a<arguments.length;a++){var t=arguments[a];for(var r in t)Object.prototype.hasOwnProperty.call(t,r)&&(e[r]=t[r])}return e},o.apply(this,arguments)}function i(e,a){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);a&&(r=r.filter((function(a){return Object.getOwnPropertyDescriptor(e,a).enumerable}))),t.push.apply(t,r)}return t}function l(e){for(var a=1;a<arguments.length;a++){var t=null!=arguments[a]?arguments[a]:{};a%2?i(Object(t),!0).forEach((function(a){n(e,a,t[a])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):i(Object(t)).forEach((function(a){Object.defineProperty(e,a,Object.getOwnPropertyDescriptor(t,a))}))}return e}function d(e,a){if(null==e)return{};var t,r,n=function(e,a){if(null==e)return{};var t,r,n={},o=Object.keys(e);for(r=0;r<o.length;r++)t=o[r],a.indexOf(t)>=0||(n[t]=e[t]);return n}(e,a);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(e);for(r=0;r<o.length;r++)t=o[r],a.indexOf(t)>=0||Object.prototype.propertyIsEnumerable.call(e,t)&&(n[t]=e[t])}return n}var c=r.createContext({}),s=function(e){return function(a){var t=m(a.components);return r.createElement(e,o({},a,{components:t}))}},m=function(e){var a=r.useContext(c),t=a;return e&&(t="function"==typeof e?e(a):l(l({},a),e)),t},p=function(e){var a=m(e.components);return r.createElement(c.Provider,{value:a},e.children)},u="mdxType",g={inlineCode:"code",wrapper:function(e){var a=e.children;return r.createElement(r.Fragment,{},a)}},y=r.forwardRef((function(e,a){var t=e.components,n=e.mdxType,o=e.originalType,i=e.parentName,c=d(e,["components","mdxType","originalType","parentName"]),s=m(t),p=n,u=s["".concat(i,".").concat(p)]||s[p]||g[p]||o;return t?r.createElement(u,l(l({ref:a},c),{},{components:t})):r.createElement(u,l({ref:a},c))}));function h(e,a){var t=arguments,n=a&&a.mdxType;if("string"==typeof e||n){var o=t.length,i=new Array(o);i[0]=y;var l={};for(var d in a)hasOwnProperty.call(a,d)&&(l[d]=a[d]);l.originalType=e,l[u]="string"==typeof e?e:n,i[1]=l;for(var c=2;c<o;c++)i[c]=t[c];return r.createElement.apply(null,i)}return r.createElement.apply(null,t)}y.displayName="MDXCreateElement"},98051:(e,a,t)=>{t.r(a),t.d(a,{assets:()=>d,contentTitle:()=>i,default:()=>p,frontMatter:()=>o,metadata:()=>l,toc:()=>c});var r=t(58168),n=(t(96540),t(15680));const o={id:"changes_to_package_header",title:"Changes to Package Header"},i=void 0,l={unversionedId:"upgrades/1.0_to_1.1/changes_to_package_header",id:"version-1.1/upgrades/1.0_to_1.1/changes_to_package_header",title:"Changes to Package Header",description:"Hydra 1.0 introduced the package header and required everyone to specify it in their configs.",source:"@site/versioned_docs/version-1.1/upgrades/1.0_to_1.1/changes_to_package_header.md",sourceDirName:"upgrades/1.0_to_1.1",slug:"/upgrades/1.0_to_1.1/changes_to_package_header",permalink:"/docs/1.1/upgrades/1.0_to_1.1/changes_to_package_header",draft:!1,editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/versioned_docs/version-1.1/upgrades/1.0_to_1.1/changes_to_package_header.md",tags:[],version:"1.1",lastUpdatedBy:"dependabot[bot]",lastUpdatedAt:1743717584,formattedLastUpdatedAt:"Apr 3, 2025",frontMatter:{id:"changes_to_package_header",title:"Changes to Package Header"},sidebar:"docs",previous:{title:"Defaults List interpolation",permalink:"/docs/1.1/upgrades/1.0_to_1.1/defaults_list_interpolation"},next:{title:"Automatic schema-matching",permalink:"/docs/1.1/upgrades/1.0_to_1.1/automatic_schema_matching"}},d={},c=[{value:"Migration",id:"migration",level:3},{value:"Compatibility with both Hydra 1.0 and 1.1",id:"compatibility-with-both-hydra-10-and-11",level:3}],s={toc:c},m="wrapper";function p(e){let{components:a,...t}=e;return(0,n.mdx)(m,(0,r.A)({},s,t,{components:a,mdxType:"MDXLayout"}),(0,n.mdx)("p",null,"Hydra 1.0 introduced the package header and required everyone to specify it in their configs.\nThis was done to facilitate a transition from a model where the packages are global\nto a model where - by default - package are derived from the config group."),(0,n.mdx)("p",null,"e.g: Change of the default package for ",(0,n.mdx)("inlineCode",{parentName:"p"},"server/db/mysql.yaml")," from ",(0,n.mdx)("inlineCode",{parentName:"p"},"_global_")," to ",(0,n.mdx)("inlineCode",{parentName:"p"},"server.db"),"."),(0,n.mdx)("p",null,"Hydra 1.1 completes this transition. "),(0,n.mdx)("ul",null,(0,n.mdx)("li",{parentName:"ul"},"If a package header is not specified, the config will have the default package as described above."),(0,n.mdx)("li",{parentName:"ul"},"_","group","_"," and ","_","name","_"," in package header are deprecated (You can still use a literal package header).")),(0,n.mdx)("admonition",{type:"info"},(0,n.mdx)("p",{parentName:"admonition"},"Another important change in Hydra 1.1 is the\n",(0,n.mdx)("a",{parentName:"p",href:"/docs/1.1/upgrades/1.0_to_1.1/default_composition_order"},"Changes to default composition order"),".")),(0,n.mdx)("h3",{id:"migration"},"Migration"),(0,n.mdx)("p",null,"If your header is ",(0,n.mdx)("inlineCode",{parentName:"p"},"# @package _group_"),", remove the header."),(0,n.mdx)("div",{className:"row"},(0,n.mdx)("div",{className:"col col--6"},(0,n.mdx)("pre",null,(0,n.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="db/mysql.yaml in Hydra 1.0"',title:'"db/mysql.yaml',in:!0,Hydra:!0,'1.0"':!0},"# @package _group_\nhost: localhost\n"))),(0,n.mdx)("div",{className:"col  col--6"},(0,n.mdx)("pre",null,(0,n.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="db/mysql.yaml in Hydra 1.1"',title:'"db/mysql.yaml',in:!0,Hydra:!0,'1.1"':!0},"host: localhost\n\n")))),(0,n.mdx)("p",null,"If your header is using ",(0,n.mdx)("inlineCode",{parentName:"p"},"_group_")," or ",(0,n.mdx)("inlineCode",{parentName:"p"},"_name_")," to specify a package other than the default package,\nSpecify the literal package:"),(0,n.mdx)("div",{className:"row"},(0,n.mdx)("div",{className:"col col--6"},(0,n.mdx)("pre",null,(0,n.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="db/mysql.yaml in Hydra 1.0"',title:'"db/mysql.yaml',in:!0,Hydra:!0,'1.0"':!0},"# @package _group_._name_\nhost: localhost\n"))),(0,n.mdx)("div",{className:"col  col--6"},(0,n.mdx)("pre",null,(0,n.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="db/mysql.yaml in Hydra 1.1"',title:'"db/mysql.yaml',in:!0,Hydra:!0,'1.1"':!0},"# @package db.mysql\nhost: localhost\n")))),(0,n.mdx)("h3",{id:"compatibility-with-both-hydra-10-and-11"},"Compatibility with both Hydra 1.0 and 1.1"),(0,n.mdx)("p",null,"If your configs should be compatible with both Hydra 1.0 and Hydra 1.1, use literal package headers."),(0,n.mdx)("div",{className:"row"},(0,n.mdx)("div",{className:"col col--6"},(0,n.mdx)("pre",null,(0,n.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="db/mysql.yaml in Hydra 1.0"',title:'"db/mysql.yaml',in:!0,Hydra:!0,'1.0"':!0},"# @package _group_\nhost: localhost\n"))),(0,n.mdx)("div",{className:"col  col--6"},(0,n.mdx)("pre",null,(0,n.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="db/mysql.yaml in Hydra 1.1"',title:'"db/mysql.yaml',in:!0,Hydra:!0,'1.1"':!0},"# @package db\nhost: localhost\n")))))}p.isMDXComponent=!0}}]);