"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[540],{15680:(e,t,n)=>{n.r(t),n.d(t,{MDXContext:()=>c,MDXProvider:()=>s,mdx:()=>v,useMDXComponents:()=>m,withMDXComponents:()=>p});var a=n(96540);function r(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function i(){return i=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var a in n)Object.prototype.hasOwnProperty.call(n,a)&&(e[a]=n[a])}return e},i.apply(this,arguments)}function o(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);t&&(a=a.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,a)}return n}function d(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?o(Object(n),!0).forEach((function(t){r(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):o(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function l(e,t){if(null==e)return{};var n,a,r=function(e,t){if(null==e)return{};var n,a,r={},i=Object.keys(e);for(a=0;a<i.length;a++)n=i[a],t.indexOf(n)>=0||(r[n]=e[n]);return r}(e,t);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);for(a=0;a<i.length;a++)n=i[a],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(r[n]=e[n])}return r}var c=a.createContext({}),p=function(e){return function(t){var n=m(t.components);return a.createElement(e,i({},t,{components:n}))}},m=function(e){var t=a.useContext(c),n=t;return e&&(n="function"==typeof e?e(t):d(d({},t),e)),n},s=function(e){var t=m(e.components);return a.createElement(c.Provider,{value:t},e.children)},u="mdxType",g={inlineCode:"code",wrapper:function(e){var t=e.children;return a.createElement(a.Fragment,{},t)}},f=a.forwardRef((function(e,t){var n=e.components,r=e.mdxType,i=e.originalType,o=e.parentName,c=l(e,["components","mdxType","originalType","parentName"]),p=m(n),s=r,u=p["".concat(o,".").concat(s)]||p[s]||g[s]||i;return n?a.createElement(u,d(d({ref:t},c),{},{components:n})):a.createElement(u,d({ref:t},c))}));function v(e,t){var n=arguments,r=t&&t.mdxType;if("string"==typeof e||r){var i=n.length,o=new Array(i);o[0]=f;var d={};for(var l in t)hasOwnProperty.call(t,l)&&(d[l]=t[l]);d.originalType=e,d[u]="string"==typeof e?e:r,o[1]=d;for(var c=2;c<i;c++)o[c]=n[c];return a.createElement.apply(null,o)}return a.createElement.apply(null,n)}f.displayName="MDXCreateElement"},61596:(e,t,n)=>{n.r(t),n.d(t,{assets:()=>l,contentTitle:()=>o,default:()=>s,frontMatter:()=>i,metadata:()=>d,toc:()=>c});var a=n(58168),r=(n(96540),n(15680));const i={id:"adding_a_package_directive",title:"Adding an @package directive",hide_title:!0},o=void 0,d={unversionedId:"upgrades/0.11_to_1.0/adding_a_package_directive",id:"version-1.2/upgrades/0.11_to_1.0/adding_a_package_directive",title:"Adding an @package directive",description:"Adding an @package directive",source:"@site/versioned_docs/version-1.2/upgrades/0.11_to_1.0/adding_a_package_directive.md",sourceDirName:"upgrades/0.11_to_1.0",slug:"/upgrades/0.11_to_1.0/adding_a_package_directive",permalink:"/docs/1.2/upgrades/0.11_to_1.0/adding_a_package_directive",draft:!1,editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/versioned_docs/version-1.2/upgrades/0.11_to_1.0/adding_a_package_directive.md",tags:[],version:"1.2",lastUpdatedBy:"P\xe1draig Brady",lastUpdatedAt:1652825677,formattedLastUpdatedAt:"May 17, 2022",frontMatter:{id:"adding_a_package_directive",title:"Adding an @package directive",hide_title:!0},sidebar:"docs",previous:{title:"Config path changes",permalink:"/docs/1.2/upgrades/0.11_to_1.0/config_path_changes"},next:{title:"strict flag mode deprecation",permalink:"/docs/1.2/upgrades/0.11_to_1.0/strict_mode_flag_deprecated"}},l={},c=[{value:"Adding an @package directive",id:"adding-an-package-directive",level:2},{value:"Upgrade instructions:",id:"upgrade-instructions",level:2},{value:"Recommended (~10 seconds per config file):",id:"recommended-10-seconds-per-config-file",level:3},{value:"Alternative (not recommended):",id:"alternative-not-recommended",level:3},{value:"Example for <code>case 1</code>:",id:"example-for-case-1",level:3},{value:"Before",id:"before",level:4},{value:"After",id:"after",level:4},{value:"Example for <code>case 2</code>:",id:"example-for-case-2",level:3}],p={toc:c},m="wrapper";function s(e){let{components:t,...n}=e;return(0,r.mdx)(m,(0,a.A)({},p,n,{components:t,mdxType:"MDXLayout"}),(0,r.mdx)("h2",{id:"adding-an-package-directive"},"Adding an @package directive"),(0,r.mdx)("p",null,"Hydra 1.0 introduces the concept of a config ",(0,r.mdx)("inlineCode",{parentName:"p"},"package"),". A ",(0,r.mdx)("inlineCode",{parentName:"p"},"package")," is the common parent\npath of all nodes in the config file."),(0,r.mdx)("ul",null,(0,r.mdx)("li",{parentName:"ul"},"In Hydra 0.11, there was an implicit default of ",(0,r.mdx)("inlineCode",{parentName:"li"},"_global_"),' ("")'),(0,r.mdx)("li",{parentName:"ul"},"In Hydra 1.1 the default will be ",(0,r.mdx)("inlineCode",{parentName:"li"},"_group_")," (the name of the config group)."),(0,r.mdx)("li",{parentName:"ul"},"Hydra 1.0 maintains the implicit default of ",(0,r.mdx)("inlineCode",{parentName:"li"},"_global_")," and issues a warning for\nany config group file without a ",(0,r.mdx)("inlineCode",{parentName:"li"},"@package")," directive.")),(0,r.mdx)("p",null,"By adding an explicit ",(0,r.mdx)("inlineCode",{parentName:"p"},"@package")," to these configs now, you guarantee that your configs\nwill not break when you upgrade to Hydra 1.1."),(0,r.mdx)("p",null,"The ",(0,r.mdx)("inlineCode",{parentName:"p"},"@package")," directive is described in details ",(0,r.mdx)("a",{parentName:"p",href:"/docs/1.2/advanced/overriding_packages"},"here"),".  "),(0,r.mdx)("h2",{id:"upgrade-instructions"},"Upgrade instructions:"),(0,r.mdx)("h3",{id:"recommended-10-seconds-per-config-file"},"Recommended (~10 seconds per config file):"),(0,r.mdx)("p",null,(0,r.mdx)("inlineCode",{parentName:"p"},"Case 1"),": For config files where the common parent path matches the config group name:  "),(0,r.mdx)("ul",null,(0,r.mdx)("li",{parentName:"ul"},"Add ",(0,r.mdx)("inlineCode",{parentName:"li"},"# @package _group_")," to the top of every config group file"),(0,r.mdx)("li",{parentName:"ul"},"Remove the common parent path config file like in the example below.")),(0,r.mdx)("p",null,(0,r.mdx)("inlineCode",{parentName:"p"},"Case 2"),": For files without a common parent path:"),(0,r.mdx)("ul",null,(0,r.mdx)("li",{parentName:"ul"},"Add ",(0,r.mdx)("inlineCode",{parentName:"li"},"# @package _global_"),".")),(0,r.mdx)("h3",{id:"alternative-not-recommended"},"Alternative (not recommended):"),(0,r.mdx)("ul",null,(0,r.mdx)("li",{parentName:"ul"},"If you do not want to restructure the config at this time use ",(0,r.mdx)("inlineCode",{parentName:"li"},"Case 2")," for all your config files.")),(0,r.mdx)("h3",{id:"example-for-case-1"},"Example for ",(0,r.mdx)("inlineCode",{parentName:"h3"},"case 1"),":"),(0,r.mdx)("h4",{id:"before"},"Before"),(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="db/mysql.yaml"',title:'"db/mysql.yaml"'},"db:\n  driver: mysql\n  host: localhost\n  port: 3306\n")),(0,r.mdx)("h4",{id:"after"},"After"),(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="db/mysql.yaml"',title:'"db/mysql.yaml"'},"# @package _group_\ndriver: mysql\nhost: localhost\nport: 3306\n")),(0,r.mdx)("p",null,"The interpretations of the before and after files are identical."),(0,r.mdx)("h3",{id:"example-for-case-2"},"Example for ",(0,r.mdx)("inlineCode",{parentName:"h3"},"case 2"),":"),(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="env/prod.yaml"',title:'"env/prod.yaml"'},"# @package _global_\ndb:\n  driver: mysql\n  host: 10.0.0.11\n  port: 3306\n\nwebserver:\n  host: 10.0.0.11\n  port: 443\n")))}s.isMDXComponent=!0}}]);