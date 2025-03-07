"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[1370],{15680:(e,n,r)=>{r.r(n),r.d(n,{MDXContext:()=>u,MDXProvider:()=>m,mdx:()=>y,useMDXComponents:()=>d,withMDXComponents:()=>p});var t=r(96540);function a(e,n,r){return n in e?Object.defineProperty(e,n,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[n]=r,e}function o(){return o=Object.assign||function(e){for(var n=1;n<arguments.length;n++){var r=arguments[n];for(var t in r)Object.prototype.hasOwnProperty.call(r,t)&&(e[t]=r[t])}return e},o.apply(this,arguments)}function l(e,n){var r=Object.keys(e);if(Object.getOwnPropertySymbols){var t=Object.getOwnPropertySymbols(e);n&&(t=t.filter((function(n){return Object.getOwnPropertyDescriptor(e,n).enumerable}))),r.push.apply(r,t)}return r}function c(e){for(var n=1;n<arguments.length;n++){var r=null!=arguments[n]?arguments[n]:{};n%2?l(Object(r),!0).forEach((function(n){a(e,n,r[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(r)):l(Object(r)).forEach((function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(r,n))}))}return e}function i(e,n){if(null==e)return{};var r,t,a=function(e,n){if(null==e)return{};var r,t,a={},o=Object.keys(e);for(t=0;t<o.length;t++)r=o[t],n.indexOf(r)>=0||(a[r]=e[r]);return a}(e,n);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(e);for(t=0;t<o.length;t++)r=o[t],n.indexOf(r)>=0||Object.prototype.propertyIsEnumerable.call(e,r)&&(a[r]=e[r])}return a}var u=t.createContext({}),p=function(e){return function(n){var r=d(n.components);return t.createElement(e,o({},n,{components:r}))}},d=function(e){var n=t.useContext(u),r=n;return e&&(r="function"==typeof e?e(n):c(c({},n),e)),r},m=function(e){var n=d(e.components);return t.createElement(u.Provider,{value:n},e.children)},s="mdxType",f={inlineCode:"code",wrapper:function(e){var n=e.children;return t.createElement(t.Fragment,{},n)}},h=t.forwardRef((function(e,n){var r=e.components,a=e.mdxType,o=e.originalType,l=e.parentName,u=i(e,["components","mdxType","originalType","parentName"]),p=d(r),m=a,s=p["".concat(l,".").concat(m)]||p[m]||f[m]||o;return r?t.createElement(s,c(c({ref:n},u),{},{components:r})):t.createElement(s,c({ref:n},u))}));function y(e,n){var r=arguments,a=n&&n.mdxType;if("string"==typeof e||a){var o=r.length,l=new Array(o);l[0]=h;var c={};for(var i in n)hasOwnProperty.call(n,i)&&(c[i]=n[i]);c.originalType=e,c[s]="string"==typeof e?e:a,l[1]=c;for(var u=2;u<o;u++)l[u]=r[u];return t.createElement.apply(null,l)}return t.createElement.apply(null,r)}h.displayName="MDXCreateElement"},18640:(e,n,r)=>{r.r(n),r.d(n,{assets:()=>i,contentTitle:()=>l,default:()=>m,frontMatter:()=>o,metadata:()=>c,toc:()=>u});var t=r(58168),a=(r(96540),r(15680));const o={id:"flow-launcher",title:"Flow Launcher"},l=void 0,c={unversionedId:"fb/flow-launcher",id:"fb/flow-launcher",title:"Flow Launcher",description:"The Flow Launcher plugin provides a way to launch application via flow.",source:"@site/docs/fb/flow-launcher.md",sourceDirName:"fb",slug:"/fb/flow-launcher",permalink:"/docs/fb/flow-launcher",draft:!1,editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/docs/fb/flow-launcher.md",tags:[],version:"current",lastUpdatedBy:"jesszzzz",lastUpdatedAt:1722609481,formattedLastUpdatedAt:"Aug 2, 2024",frontMatter:{id:"flow-launcher",title:"Flow Launcher"}},i={},u=[{value:"Dependency",id:"dependency",level:2},{value:"Usage",id:"usage",level:2}],p={toc:u},d="wrapper";function m(e){let{components:n,...r}=e;return(0,a.mdx)(d,(0,t.A)({},p,r,{components:n,mdxType:"MDXLayout"}),(0,a.mdx)("p",null,"The Flow Launcher plugin provides a way to launch application via ",(0,a.mdx)("inlineCode",{parentName:"p"},"flow"),"."),(0,a.mdx)("h2",{id:"dependency"},"Dependency"),(0,a.mdx)("p",null,"To use the Flow Launcher, add the following to your ",(0,a.mdx)("inlineCode",{parentName:"p"},"TARGETS")),(0,a.mdx)("pre",null,(0,a.mdx)("code",{parentName:"pre",className:"language-commandline"},"//github/facebookresearch/hydra/plugins/hydra_flow_launcher:hydra_flow_launcher\n")),(0,a.mdx)("h2",{id:"usage"},"Usage"),(0,a.mdx)("p",null,"Add hydra/launcher=flow to your command line. Alternatively, override hydra/launcher in your config:"),(0,a.mdx)("pre",null,(0,a.mdx)("code",{parentName:"pre",className:"language-commandline"},"defaults:\n  - hydra/launcher: flow\n")),(0,a.mdx)("details",null,(0,a.mdx)("summary",null,"Discover Flow Launcher's config"),(0,a.mdx)("pre",null,(0,a.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="$ buck run @mode/opt  //path:my_app -- --cfg hydra -p hydra.launcher"',title:'"$',buck:!0,run:!0,"@mode/opt":!0,"":!0,"//path:my_app":!0,"--":!0,"--cfg":!0,hydra:!0,"-p":!0,'hydra.launcher"':!0},"\n# @package hydra.launcher\n_target_: hydra_plugins.flow_launcher_plugin.flow_launcher.FlowLauncher\nmode: flow\nowner: ${oc.env:USER}\nentitlement: gpu_pnb_fair\npkg_version: fblearner.flow.canary:19e63cbf9945467281cf681bc8902c50\ndriver_path: ''\nresource_requirements:\n  gpu: 0\n  cpu: 1\n  memory: 10g\n  region: null\n  capabilities: []\n  percent_cpu: null\nrun_as_secure_group: fair_research_and_engineering\nretries: 2\ntags: []\n"))),(0,a.mdx)("p",null,"The Launcher currently support both ",(0,a.mdx)("inlineCode",{parentName:"p"},"par")," and ",(0,a.mdx)("inlineCode",{parentName:"p"},"xar")," style. You can override ",(0,a.mdx)("inlineCode",{parentName:"p"},"resource_requirements")," just like how you would via ",(0,a.mdx)("inlineCode",{parentName:"p"},"flow-cli"),"."),(0,a.mdx)("admonition",{title:"NOTE",type:"info"},(0,a.mdx)("p",{parentName:"admonition"},"Flow launcher only supports ",(0,a.mdx)("inlineCode",{parentName:"p"},"@mode/opt"),".")),(0,a.mdx)("p",null,"To run the example application:"),(0,a.mdx)("pre",null,(0,a.mdx)("code",{parentName:"pre",className:"language-commandline"},"buck run @mode/opt  //github/facebookresearch/hydra/plugins/hydra_flow_launcher/example:my_app -- --multirun\n")))}m.isMDXComponent=!0}}]);