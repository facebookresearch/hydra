"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[4812],{15680:(e,r,n)=>{n.r(r),n.d(r,{MDXContext:()=>c,MDXProvider:()=>u,mdx:()=>h,useMDXComponents:()=>p,withMDXComponents:()=>s});var t=n(96540);function a(e,r,n){return r in e?Object.defineProperty(e,r,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[r]=n,e}function o(){return o=Object.assign||function(e){for(var r=1;r<arguments.length;r++){var n=arguments[r];for(var t in n)Object.prototype.hasOwnProperty.call(n,t)&&(e[t]=n[t])}return e},o.apply(this,arguments)}function i(e,r){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var t=Object.getOwnPropertySymbols(e);r&&(t=t.filter((function(r){return Object.getOwnPropertyDescriptor(e,r).enumerable}))),n.push.apply(n,t)}return n}function d(e){for(var r=1;r<arguments.length;r++){var n=null!=arguments[r]?arguments[r]:{};r%2?i(Object(n),!0).forEach((function(r){a(e,r,n[r])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):i(Object(n)).forEach((function(r){Object.defineProperty(e,r,Object.getOwnPropertyDescriptor(n,r))}))}return e}function l(e,r){if(null==e)return{};var n,t,a=function(e,r){if(null==e)return{};var n,t,a={},o=Object.keys(e);for(t=0;t<o.length;t++)n=o[t],r.indexOf(n)>=0||(a[n]=e[n]);return a}(e,r);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(e);for(t=0;t<o.length;t++)n=o[t],r.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(a[n]=e[n])}return a}var c=t.createContext({}),s=function(e){return function(r){var n=p(r.components);return t.createElement(e,o({},r,{components:n}))}},p=function(e){var r=t.useContext(c),n=r;return e&&(n="function"==typeof e?e(r):d(d({},r),e)),n},u=function(e){var r=p(e.components);return t.createElement(c.Provider,{value:r},e.children)},f="mdxType",m={inlineCode:"code",wrapper:function(e){var r=e.children;return t.createElement(t.Fragment,{},r)}},b=t.forwardRef((function(e,r){var n=e.components,a=e.mdxType,o=e.originalType,i=e.parentName,c=l(e,["components","mdxType","originalType","parentName"]),s=p(n),u=a,f=s["".concat(i,".").concat(u)]||s[u]||m[u]||o;return n?t.createElement(f,d(d({ref:r},c),{},{components:n})):t.createElement(f,d({ref:r},c))}));function h(e,r){var n=arguments,a=r&&r.mdxType;if("string"==typeof e||a){var o=n.length,i=new Array(o);i[0]=b;var d={};for(var l in r)hasOwnProperty.call(r,l)&&(d[l]=r[l]);d.originalType=e,d[f]="string"==typeof e?e:a,i[1]=d;for(var c=2;c<o;c++)i[c]=n[c];return t.createElement.apply(null,i)}return t.createElement.apply(null,n)}b.displayName="MDXCreateElement"},21814:(e,r,n)=>{n.r(r),n.d(r,{assets:()=>l,contentTitle:()=>i,default:()=>u,frontMatter:()=>o,metadata:()=>d,toc:()=>c});var t=n(58168),a=(n(96540),n(15680));const o={id:"fbcode",title:"Hydra at fbcode"},i=void 0,d={unversionedId:"fb/fbcode",id:"fb/fbcode",title:"Hydra at fbcode",description:"Differences in fbcode",source:"@site/docs/fb/fbcode.md",sourceDirName:"fb",slug:"/fb/fbcode",permalink:"/docs/fb/fbcode",draft:!1,editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/docs/fb/fbcode.md",tags:[],version:"current",lastUpdatedBy:"jesszzzz",lastUpdatedAt:1743461536,formattedLastUpdatedAt:"Mar 31, 2025",frontMatter:{id:"fbcode",title:"Hydra at fbcode"}},l={},c=[{value:"Differences in fbcode",id:"differences-in-fbcode",level:2},{value:"Open source plugins",id:"open-source-plugins",level:3},{value:"Supported:",id:"supported",level:4},{value:"Unsupported:",id:"unsupported",level:4},{value:"Facebook specified plugins",id:"facebook-specified-plugins",level:3},{value:"TARGETS",id:"targets",level:4}],s={toc:c},p="wrapper";function u(e){let{components:r,...n}=e;return(0,a.mdx)(p,(0,t.A)({},s,n,{components:r,mdxType:"MDXLayout"}),(0,a.mdx)("h2",{id:"differences-in-fbcode"},"Differences in fbcode"),(0,a.mdx)("h3",{id:"open-source-plugins"},"Open source plugins"),(0,a.mdx)("h4",{id:"supported"},"Supported:"),(0,a.mdx)("ul",null,(0,a.mdx)("li",{parentName:"ul"},"hydra_ax_sweeper"),(0,a.mdx)("li",{parentName:"ul"},"hydra_colorlog"),(0,a.mdx)("li",{parentName:"ul"},"hydra_nevergrad_sweeper")),(0,a.mdx)("h4",{id:"unsupported"},"Unsupported:"),(0,a.mdx)("ul",null,(0,a.mdx)("li",{parentName:"ul"},"joblib launcher: Joblib's Loki backend does not work correctly when executed from a par file.")),(0,a.mdx)("h3",{id:"facebook-specified-plugins"},"Facebook specified plugins"),(0,a.mdx)("ul",null,(0,a.mdx)("li",{parentName:"ul"},"fbcode_defaults : Changes configuration defaults to be appropriate for fbcode (e.g: Output directories are in ",(0,a.mdx)("inlineCode",{parentName:"li"},"fbcode/outputs")," and ",(0,a.mdx)("inlineCode",{parentName:"li"},"fbcode/multirun"),")"),(0,a.mdx)("li",{parentName:"ul"},"configerator_config_source: See ",(0,a.mdx)("a",{parentName:"li",href:"/docs/fb/fbcode-configerator-config-source"},"doc"),"  for more information.")),(0,a.mdx)("h4",{id:"targets"},"TARGETS"),(0,a.mdx)("p",null,"Hydra includes buck TARGETS you can use in fbcode. In general, if there is TARGET there are two options:"),(0,a.mdx)("ol",null,(0,a.mdx)("li",{parentName:"ol"},"You can depend on the TARGETS to use Hydra or a plugin."),(0,a.mdx)("li",{parentName:"ol"},"The TARGETS contains a runnable example.")),(0,a.mdx)("p",null,"targets are under ",(0,a.mdx)("inlineCode",{parentName:"p"},"github/facebookresearch/hydra"),":"),(0,a.mdx)("ul",null,(0,a.mdx)("li",{parentName:"ul"},(0,a.mdx)("a",{parentName:"li",href:"https://www.internalfb.com/intern/diffusion/FBS/browsedir/master/fbcode/github/facebookresearch/hydra"},":",(0,a.mdx)("inlineCode",{parentName:"a"},"hydra"))," : Primary target to use in most cases. Includes ",(0,a.mdx)("inlineCode",{parentName:"li"},"hydra_oss")," and the ",(0,a.mdx)("inlineCode",{parentName:"li"},"fbcode_defaults"),"."),(0,a.mdx)("li",{parentName:"ul"},(0,a.mdx)("inlineCode",{parentName:"li"},":hydra_oss")," : Vanilla Hydra without any Facebook specific targets."),(0,a.mdx)("li",{parentName:"ul"},(0,a.mdx)("a",{parentName:"li",href:"https://www.internalfb.com/intern/diffusion/FBS/browsedir/master/fbcode/github/facebookresearch/hydra/plugins"},(0,a.mdx)("inlineCode",{parentName:"a"},"plugins")),": Plugins that have a TARGETS file are runnable in fbcode."),(0,a.mdx)("li",{parentName:"ul"},(0,a.mdx)("a",{parentName:"li",href:"https://www.internalfb.com/intern/diffusion/FBS/browsedir/master/fbcode/github/facebookresearch/hydra/examples"},(0,a.mdx)("inlineCode",{parentName:"a"},"examples")),": Examples that have a TARGETS file are runnable in ",(0,a.mdx)("inlineCode",{parentName:"li"},"fbcode"),". All tutorials (in ",(0,a.mdx)("a",{parentName:"li",href:"https://www.internalfb.com/intern/diffusion/FBS/browsedir/master/fbcode/github/facebookresearch/hydra/examples"},(0,a.mdx)("inlineCode",{parentName:"a"},"examples/tutorials")),") are supported. An example TARGET file can be found ",(0,a.mdx)("a",{parentName:"li",href:"https://www.internalfb.com/intern/diffusion/FBS/browsedir/master/fbcode/github/facebookresearch/hydra/examples/tutorials/basic/your_first_hydra_app/5_composition"},"here"),".")))}u.isMDXComponent=!0}}]);