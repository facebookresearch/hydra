"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[3224],{15680:(e,r,n)=>{n.r(r),n.d(r,{MDXContext:()=>l,MDXProvider:()=>d,mdx:()=>h,useMDXComponents:()=>p,withMDXComponents:()=>m});var o=n(96540);function a(e,r,n){return r in e?Object.defineProperty(e,r,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[r]=n,e}function t(){return t=Object.assign||function(e){for(var r=1;r<arguments.length;r++){var n=arguments[r];for(var o in n)Object.prototype.hasOwnProperty.call(n,o)&&(e[o]=n[o])}return e},t.apply(this,arguments)}function i(e,r){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(e);r&&(o=o.filter((function(r){return Object.getOwnPropertyDescriptor(e,r).enumerable}))),n.push.apply(n,o)}return n}function c(e){for(var r=1;r<arguments.length;r++){var n=null!=arguments[r]?arguments[r]:{};r%2?i(Object(n),!0).forEach((function(r){a(e,r,n[r])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):i(Object(n)).forEach((function(r){Object.defineProperty(e,r,Object.getOwnPropertyDescriptor(n,r))}))}return e}function f(e,r){if(null==e)return{};var n,o,a=function(e,r){if(null==e)return{};var n,o,a={},t=Object.keys(e);for(o=0;o<t.length;o++)n=t[o],r.indexOf(n)>=0||(a[n]=e[n]);return a}(e,r);if(Object.getOwnPropertySymbols){var t=Object.getOwnPropertySymbols(e);for(o=0;o<t.length;o++)n=t[o],r.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(a[n]=e[n])}return a}var l=o.createContext({}),m=function(e){return function(r){var n=p(r.components);return o.createElement(e,t({},r,{components:n}))}},p=function(e){var r=o.useContext(l),n=r;return e&&(n="function"==typeof e?e(r):c(c({},r),e)),n},d=function(e){var r=p(e.components);return o.createElement(l.Provider,{value:r},e.children)},s="mdxType",u={inlineCode:"code",wrapper:function(e){var r=e.children;return o.createElement(o.Fragment,{},r)}},g=o.forwardRef((function(e,r){var n=e.components,a=e.mdxType,t=e.originalType,i=e.parentName,l=f(e,["components","mdxType","originalType","parentName"]),m=p(n),d=a,s=m["".concat(i,".").concat(d)]||m[d]||u[d]||t;return n?o.createElement(s,c(c({ref:r},l),{},{components:n})):o.createElement(s,c({ref:r},l))}));function h(e,r){var n=arguments,a=r&&r.mdxType;if("string"==typeof e||a){var t=n.length,i=new Array(t);i[0]=g;var c={};for(var f in r)hasOwnProperty.call(r,f)&&(c[f]=r[f]);c.originalType=e,c[s]="string"==typeof e?e:a,i[1]=c;for(var l=2;l<t;l++)i[l]=n[l];return o.createElement.apply(null,i)}return o.createElement.apply(null,n)}g.displayName="MDXCreateElement"},95915:(e,r,n)=>{n.r(r),n.d(r,{assets:()=>f,contentTitle:()=>i,default:()=>d,frontMatter:()=>t,metadata:()=>c,toc:()=>l});var o=n(58168),a=(n(96540),n(15680));const t={id:"fbcode-configerator-config-source",title:"Configerator Config Source Plugin"},i=void 0,c={unversionedId:"fb/fbcode-configerator-config-source",id:"fb/fbcode-configerator-config-source",title:"Configerator Config Source Plugin",description:"The ConfigeratorConfigSource plugin makes it possible for Hydra applications to consume a domain of configs from configerator.",source:"@site/docs/fb/configerator-config-source.md",sourceDirName:"fb",slug:"/fb/fbcode-configerator-config-source",permalink:"/docs/fb/fbcode-configerator-config-source",draft:!1,editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/docs/fb/configerator-config-source.md",tags:[],version:"current",lastUpdatedBy:"jesszzzz",lastUpdatedAt:1741814683,formattedLastUpdatedAt:"Mar 12, 2025",frontMatter:{id:"fbcode-configerator-config-source",title:"Configerator Config Source Plugin"}},f={},l=[{value:"Dependency",id:"dependency",level:3},{value:"Usage",id:"usage",level:3},{value:"Example:",id:"example",level:3},{value:"Example SearchPathPlugin",id:"example-searchpathplugin",level:4},{value:"Reading primary config from configerator",id:"reading-primary-config-from-configerator",level:4},{value:"Compose config with configerator",id:"compose-config-with-configerator",level:4}],m={toc:l},p="wrapper";function d(e){let{components:r,...n}=e;return(0,a.mdx)(p,(0,o.A)({},m,n,{components:r,mdxType:"MDXLayout"}),(0,a.mdx)("p",null,"The ConfigeratorConfigSource plugin makes it possible for Hydra applications to consume a domain of configs from configerator."),(0,a.mdx)("h3",{id:"dependency"},"Dependency"),(0,a.mdx)("p",null,"Add the following to your ",(0,a.mdx)("inlineCode",{parentName:"p"},"TARGET")," file"),(0,a.mdx)("pre",null,(0,a.mdx)("code",{parentName:"pre",className:"language-commandline"},"//fair_infra/fbcode_hydra_plugins/configerator_config_source:configerator_config_source\n")),(0,a.mdx)("h3",{id:"usage"},"Usage"),(0,a.mdx)("ol",null,(0,a.mdx)("li",{parentName:"ol"},"The Configerator Config Source plugin requires that you place the configs under a ",(0,a.mdx)("a",{parentName:"li",href:"https://fburl.com/wiki/n5cgchxe"},"domain"),".\nYou can find an example domain ",(0,a.mdx)("a",{parentName:"li",href:"https://fburl.com/diffusion/ms50g5hu"},"here"))),(0,a.mdx)("admonition",{type:"important"},(0,a.mdx)("p",{parentName:"admonition"},"Due to the limitations of Configerator APIs, matching the name of your domain and directory of configs is necessary for the plugin to extract information on the full config names.\nFor example, the config paths returned by Configerator API could look like ",(0,a.mdx)("inlineCode",{parentName:"p"},"fair_infra/hydra_plugins/configerator_config_source/example/db/mysql"),". The plugin needs to know where the directory of configs begins (",(0,a.mdx)("a",{parentName:"p",href:"https://fburl.com/diffusion/7c0c5tig"},(0,a.mdx)("inlineCode",{parentName:"a"},"example")),"), in order to determine the full config name (",(0,a.mdx)("inlineCode",{parentName:"p"},"db/mysql"),"). So in this case the domain should be named ",(0,a.mdx)("a",{parentName:"p",href:"https://fburl.com/diffusion/pyymoo1t"},(0,a.mdx)("inlineCode",{parentName:"a"},"example.cconf")))),(0,a.mdx)("ol",{start:2},(0,a.mdx)("li",{parentName:"ol"},"Create a ",(0,a.mdx)("a",{parentName:"li",href:"https://hydra.cc/docs/next/advanced/search_path"},"SearchPathPlugin")," to add the Configerator path to the list of search paths.\nThe path you add in your SearchPathPlugin should be the name of your domain of configs, such as in this ",(0,a.mdx)("a",{parentName:"li",href:"https://fburl.com/diffusion/ljggtux5"},"example SearchPathPlugin"))),(0,a.mdx)("admonition",{type:"info"},(0,a.mdx)("p",{parentName:"admonition"},"Adding a new search path will become much easier once ",(0,a.mdx)("a",{parentName:"p",href:"https://github.com/facebookresearch/hydra/issues/274"},"#274")," is resolved, which is planned for Hydra 1.1.")),(0,a.mdx)("h3",{id:"example"},"Example:"),(0,a.mdx)("h4",{id:"example-searchpathplugin"},"Example SearchPathPlugin"),(0,a.mdx)("p",null,(0,a.mdx)("a",{parentName:"p",href:"https://fburl.com/diffusion/vwa82fbg"},(0,a.mdx)("inlineCode",{parentName:"a"},"ConfigeratorExampleSearchPathPlugin"))," adds the example configerator domain to the search path of the example applications."),(0,a.mdx)("h4",{id:"reading-primary-config-from-configerator"},"Reading primary config from configerator"),(0,a.mdx)("p",null,"This example reads its primary config from configerator ",(0,a.mdx)("a",{parentName:"p",href:"https://fburl.com/diffusion/twk3smkj"},"here")," which has a default list defined."),(0,a.mdx)("pre",null,(0,a.mdx)("code",{parentName:"pre",className:"language-commandline"},"$ buck run //fair_infra/fbcode_hydra_plugins/configerator_config_source/example/primary_config:my_app \n...\nParsing buck files: finished in 1.1 sec\n...\n{'driver': 'mysql', 'user': 'alau'}\n")),(0,a.mdx)("h4",{id:"compose-config-with-configerator"},"Compose config with configerator"),(0,a.mdx)("p",null,"This example reads its primary config from local yaml file ",(0,a.mdx)("inlineCode",{parentName:"p"},"primary_config.yaml")," but reads config groups info from configerator."),(0,a.mdx)("pre",null,(0,a.mdx)("code",{parentName:"pre",className:"language-commandline"},"$ buck run //fair_infra/fbcode_hydra_plugins/configerator_config_source/example/config_group:my_app -- +db=mysql\n...\nParsing buck files: finished in 1.1 sec\n...\n{'foo': 'bar', 'driver': 'mysql', 'user': 'alau'}\n")))}d.isMDXComponent=!0}}]);