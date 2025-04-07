"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[8018],{15680:(e,n,t)=>{t.r(n),t.d(n,{MDXContext:()=>s,MDXProvider:()=>u,mdx:()=>h,useMDXComponents:()=>d,withMDXComponents:()=>m});var a=t(96540);function r(e,n,t){return n in e?Object.defineProperty(e,n,{value:t,enumerable:!0,configurable:!0,writable:!0}):e[n]=t,e}function i(){return i=Object.assign||function(e){for(var n=1;n<arguments.length;n++){var t=arguments[n];for(var a in t)Object.prototype.hasOwnProperty.call(t,a)&&(e[a]=t[a])}return e},i.apply(this,arguments)}function l(e,n){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);n&&(a=a.filter((function(n){return Object.getOwnPropertyDescriptor(e,n).enumerable}))),t.push.apply(t,a)}return t}function o(e){for(var n=1;n<arguments.length;n++){var t=null!=arguments[n]?arguments[n]:{};n%2?l(Object(t),!0).forEach((function(n){r(e,n,t[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):l(Object(t)).forEach((function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(t,n))}))}return e}function c(e,n){if(null==e)return{};var t,a,r=function(e,n){if(null==e)return{};var t,a,r={},i=Object.keys(e);for(a=0;a<i.length;a++)t=i[a],n.indexOf(t)>=0||(r[t]=e[t]);return r}(e,n);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);for(a=0;a<i.length;a++)t=i[a],n.indexOf(t)>=0||Object.prototype.propertyIsEnumerable.call(e,t)&&(r[t]=e[t])}return r}var s=a.createContext({}),m=function(e){return function(n){var t=d(n.components);return a.createElement(e,i({},n,{components:t}))}},d=function(e){var n=a.useContext(s),t=n;return e&&(t="function"==typeof e?e(n):o(o({},n),e)),t},u=function(e){var n=d(e.components);return a.createElement(s.Provider,{value:n},e.children)},p="mdxType",g={inlineCode:"code",wrapper:function(e){var n=e.children;return a.createElement(a.Fragment,{},n)}},f=a.forwardRef((function(e,n){var t=e.components,r=e.mdxType,i=e.originalType,l=e.parentName,s=c(e,["components","mdxType","originalType","parentName"]),m=d(t),u=r,p=m["".concat(l,".").concat(u)]||m[u]||g[u]||i;return t?a.createElement(p,o(o({ref:n},s),{},{components:t})):a.createElement(p,o({ref:n},s))}));function h(e,n){var t=arguments,r=n&&n.mdxType;if("string"==typeof e||r){var i=t.length,l=new Array(i);l[0]=f;var o={};for(var c in n)hasOwnProperty.call(n,c)&&(o[c]=n[c]);o.originalType=e,o[p]="string"==typeof e?e:r,l[1]=o;for(var s=2;s<i;s++)l[s]=t[s];return a.createElement.apply(null,l)}return a.createElement.apply(null,t)}f.displayName="MDXCreateElement"},49595:(e,n,t)=>{t.d(n,{A:()=>s,C:()=>m});var a=t(58168),r=t(96540),i=t(75489),l=t(44586),o=t(48295);function c(e){const n=(0,o.ir)();return(0,l.default)().siteConfig.customFields.githubLinkVersionToBaseUrl[n?.name??"current"]+e}function s(e){return r.createElement(i.default,(0,a.A)({},e,{to:c(e.to),target:"_blank"}))}function m(e){const n=e.text??"Example (Click Here)";return r.createElement(s,e,r.createElement("span",null,"\xa0"),r.createElement("img",{src:"https://img.shields.io/badge/-"+n+"-informational",alt:"Example (Click Here)"}))}},68926:(e,n,t)=>{t.r(n),t.d(n,{assets:()=>c,contentTitle:()=>l,default:()=>u,frontMatter:()=>i,metadata:()=>o,toc:()=>s});var a=t(58168),r=(t(96540),t(15680));t(49595);const i={id:"configuring_plugins",title:"Configuring Plugins"},l=void 0,o={unversionedId:"patterns/configuring_plugins",id:"version-1.1/patterns/configuring_plugins",title:"Configuring Plugins",description:"Hydra plugins usually come with sensible defaults which work with minimal configuration.",source:"@site/versioned_docs/version-1.1/patterns/configuring_plugins.md",sourceDirName:"patterns",slug:"/patterns/configuring_plugins",permalink:"/docs/1.1/patterns/configuring_plugins",draft:!1,editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/versioned_docs/version-1.1/patterns/configuring_plugins.md",tags:[],version:"1.1",lastUpdatedBy:"jesszzzz",lastUpdatedAt:1744041844,formattedLastUpdatedAt:"Apr 7, 2025",frontMatter:{id:"configuring_plugins",title:"Configuring Plugins"},sidebar:"docs",previous:{title:"Configuring Experiments",permalink:"/docs/1.1/patterns/configuring_experiments"},next:{title:"Selecting multiple configs from a Config Group",permalink:"/docs/1.1/patterns/select_multiple_configs_from_config_group"}},c={},s=[{value:"Overriding in primary config",id:"overriding-in-primary-config",level:3},{value:"Extending plugin default config",id:"extending-plugin-default-config",level:3}],m={toc:s},d="wrapper";function u(e){let{components:n,...t}=e;return(0,r.mdx)(d,(0,a.A)({},m,t,{components:n,mdxType:"MDXLayout"}),(0,r.mdx)("p",null,"Hydra plugins usually come with sensible defaults which work with minimal configuration.\nThere are two primary ways to customize the configuration of a plugin:"),(0,r.mdx)("ul",null,(0,r.mdx)("li",{parentName:"ul"},"Overriding it directly in your primary config"),(0,r.mdx)("li",{parentName:"ul"},"Extending the config and using it from your primary config.")),(0,r.mdx)("p",null,"The first method is the simpler, but it makes it harder to switch to a different plugin configuration.\nThe second method is a bit more complicated, but makes it easier to switch between different plugin configurations."),(0,r.mdx)("p",null,"The following methods apply to all Hydra plugins. In the following examples, we will configure an imaginary Launcher plugin\n",(0,r.mdx)("inlineCode",{parentName:"p"},"MoonLauncher"),". The Launcher has two modes: ",(0,r.mdx)("inlineCode",{parentName:"p"},"falcon9"),", which actually launches the application to the Moon and\n",(0,r.mdx)("inlineCode",{parentName:"p"},"sim")," which simulates a launch."),(0,r.mdx)("p",null,"The config schema for MoonLauncher looks like:"),(0,r.mdx)("div",{className:"row"},(0,r.mdx)("div",{className:"col col--6"},(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-python"},"@dataclass\nclass Falcon9Conf:\n  ton_fuel:  int = 10\n\n\n\n\n"))),(0,r.mdx)("div",{className:"col  col--6"},(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-python"},"@dataclass\nclass Simulation:\n  ton_fuel:  int = 10\n  window_size:\n    width: 1024\n    height: 768\n\n")))),(0,r.mdx)("h3",{id:"overriding-in-primary-config"},"Overriding in primary config"),(0,r.mdx)("p",null,"We can directly override Launcher config in primary config."),(0,r.mdx)("div",{className:"row"},(0,r.mdx)("div",{className:"col col--4"},(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="config.yaml"',title:'"config.yaml"'},"a: 1\n\nhydra:\n  launcher:\n    ton_fuel: 2\n\n\n\n\n\n\n\n\n\n"))),(0,r.mdx)("div",{className:"col col--4"},(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-commandline",metastring:'title="command-line override"',title:'"command-line','override"':!0},"hydra/launcher=falcon9\n\n\n")),(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="resulting launcher config"  {3}',title:'"resulting',launcher:!0,'config"':!0,"":!0,"{3}":!0},"hydra:\n  launcher:\n    ton_fuel: 2\n\n\n\n"))),(0,r.mdx)("div",{className:"col col--4"},(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-commandline",metastring:'title="command-line override"',title:'"command-line','override"':!0},"hydra/launcher=sim\n\n\n")),(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="resulting launcher config"  {3}',title:'"resulting',launcher:!0,'config"':!0,"":!0,"{3}":!0},"hydra:\n  launcher:\n    ton_fuel: 2\n    window_size:\n      width: 1024\n      height: 768\n")))),(0,r.mdx)("p",null,"This approach makes the assumption that the Launcher used has all the fields we are overriding.\nIf we wanted to override a field that exists in the Simulation Launcher but not in the Falcon9 Launcher,\nlike ",(0,r.mdx)("inlineCode",{parentName:"p"},"window_size.width"),", we would no longer be able to use the Falcon9 Launcher! The next section solves this problem."),(0,r.mdx)("h3",{id:"extending-plugin-default-config"},"Extending plugin default config"),(0,r.mdx)("p",null,"This section assumes that you are familiar with the contents of ",(0,r.mdx)("a",{parentName:"p",href:"/docs/1.1/patterns/extending_configs"},"Common Patterns/Extending Configs"),"."),(0,r.mdx)("p",null,"Extending plugin default config has several advantages:"),(0,r.mdx)("ul",null,(0,r.mdx)("li",{parentName:"ul"},"Separate configuration concerns, keep primary config clean."),(0,r.mdx)("li",{parentName:"ul"},"Easier to switch between different plugin configurations."),(0,r.mdx)("li",{parentName:"ul"},"Provides flexibility when a Plugin has different modes\nthat requires different schema.")),(0,r.mdx)("p",null,"Say that we want to override certain values for different Launcher mode:"),(0,r.mdx)("div",{className:"row"},(0,r.mdx)("div",{className:"col col--6"},(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="hydra/launcher/my_falcon9.yaml" {4}',title:'"hydra/launcher/my_falcon9.yaml"',"{4}":!0},"defaults:\n  - falcon9\n\nton_fuel: 2\n\n\n"))),(0,r.mdx)("div",{className:"col col--6"},(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="hydra/sweeper/my_sim.yaml" {5}',title:'"hydra/sweeper/my_sim.yaml"',"{5}":!0},"defaults:\n  - sim\n\nwindow_size:\n  width: 768\n\n")))),(0,r.mdx)("p",null,"We can easily user command-line overrides to get the configuration needed:"),(0,r.mdx)("div",{className:"row"},(0,r.mdx)("div",{className:"col col--6"},(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-commandline",metastring:'title="command-line override"',title:'"command-line','override"':!0},"hydra/launcher=my_falcon9\n\n\n")),(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="resulting launcher config"  {3}',title:'"resulting',launcher:!0,'config"':!0,"":!0,"{3}":!0},"hydra:\n  launcher:\n    ton_fuel: 2\n\n\n\n"))),(0,r.mdx)("div",{className:"col col--6"},(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-commandline",metastring:'title="command-line override"',title:'"command-line','override"':!0},"hydra/launcher=my_sim\n\n\n")),(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="resulting launcher config"  {5}',title:'"resulting',launcher:!0,'config"':!0,"":!0,"{5}":!0},"hydra:\n  launcher:\n    ton_fuel: 10\n    window_size:\n      width: 768\n      height: 768\n")))))}u.isMDXComponent=!0}}]);