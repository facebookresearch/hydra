"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[2070],{15680:(e,t,r)=>{r.r(t),r.d(t,{MDXContext:()=>s,MDXProvider:()=>f,mdx:()=>b,useMDXComponents:()=>u,withMDXComponents:()=>p});var n=r(96540);function o(e,t,r){return t in e?Object.defineProperty(e,t,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[t]=r,e}function a(){return a=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var r=arguments[t];for(var n in r)Object.prototype.hasOwnProperty.call(r,n)&&(e[n]=r[n])}return e},a.apply(this,arguments)}function l(e,t){var r=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);t&&(n=n.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),r.push.apply(r,n)}return r}function i(e){for(var t=1;t<arguments.length;t++){var r=null!=arguments[t]?arguments[t]:{};t%2?l(Object(r),!0).forEach((function(t){o(e,t,r[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(r)):l(Object(r)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(r,t))}))}return e}function c(e,t){if(null==e)return{};var r,n,o=function(e,t){if(null==e)return{};var r,n,o={},a=Object.keys(e);for(n=0;n<a.length;n++)r=a[n],t.indexOf(r)>=0||(o[r]=e[r]);return o}(e,t);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);for(n=0;n<a.length;n++)r=a[n],t.indexOf(r)>=0||Object.prototype.propertyIsEnumerable.call(e,r)&&(o[r]=e[r])}return o}var s=n.createContext({}),p=function(e){return function(t){var r=u(t.components);return n.createElement(e,a({},t,{components:r}))}},u=function(e){var t=n.useContext(s),r=t;return e&&(r="function"==typeof e?e(t):i(i({},t),e)),r},f=function(e){var t=u(e.components);return n.createElement(s.Provider,{value:t},e.children)},m="mdxType",d={inlineCode:"code",wrapper:function(e){var t=e.children;return n.createElement(n.Fragment,{},t)}},y=n.forwardRef((function(e,t){var r=e.components,o=e.mdxType,a=e.originalType,l=e.parentName,s=c(e,["components","mdxType","originalType","parentName"]),p=u(r),f=o,m=p["".concat(l,".").concat(f)]||p[f]||d[f]||a;return r?n.createElement(m,i(i({ref:t},s),{},{components:r})):n.createElement(m,i({ref:t},s))}));function b(e,t){var r=arguments,o=t&&t.mdxType;if("string"==typeof e||o){var a=r.length,l=new Array(a);l[0]=y;var i={};for(var c in t)hasOwnProperty.call(t,c)&&(i[c]=t[c]);i.originalType=e,i[m]="string"==typeof e?e:o,l[1]=i;for(var s=2;s<a;s++)l[s]=r[s];return n.createElement.apply(null,l)}return n.createElement.apply(null,r)}y.displayName="MDXCreateElement"},74822:(e,t,r)=>{r.r(t),r.d(t,{assets:()=>c,contentTitle:()=>l,default:()=>f,frontMatter:()=>a,metadata:()=>i,toc:()=>s});var n=r(58168),o=(r(96540),r(15680));const a={id:"internal-fb-cluster",title:"Hydra on the internet FB Cluster"},l=void 0,i={unversionedId:"fb/internal-fb-cluster",id:"fb/internal-fb-cluster",title:"Hydra on the internet FB Cluster",description:"Support for launching jobs to the AI cluster is currently still experimental and is expected to evolve over",source:"@site/docs/fb/ai-cluster.md",sourceDirName:"fb",slug:"/fb/internal-fb-cluster",permalink:"/docs/fb/internal-fb-cluster",draft:!1,editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/docs/fb/ai-cluster.md",tags:[],version:"current",lastUpdatedBy:"jesszzzz",lastUpdatedAt:1722609481,formattedLastUpdatedAt:"Aug 2, 2024",frontMatter:{id:"internal-fb-cluster",title:"Hydra on the internet FB Cluster"}},c={},s=[{value:"flow-cli",id:"flow-cli",level:2}],p={toc:s},u="wrapper";function f(e){let{components:t,...r}=e;return(0,o.mdx)(u,(0,n.A)({},p,r,{components:t,mdxType:"MDXLayout"}),(0,o.mdx)("p",null,"Support for launching jobs to the AI cluster is currently still experimental and is expected to evolve over\nthe coming months."),(0,o.mdx)("h2",{id:"flow-cli"},"flow-cli"),(0,o.mdx)("p",null,"flow-cli integration is hacky at the moment.\nSee the sample f6.sample_projects.classy_hydra_project.workflow.main for details."),(0,o.mdx)("pre",null,(0,o.mdx)("code",{parentName:"pre",className:"language-bash",metastring:'title="Example run"',title:'"Example','run"':!0},'$ CFG=\'{"config": {"overrides": ["trainer=multi_gpu","trainer.max_epochs=90","+lr_scheduler=multi_step"]}}\'\n$ ENTITLEMENT=cv_images_gpu_prod\n$ TEAM=team_computer_vision\n$ WORKFLOW=f6.sample_projects.classy_hydra_project.workflow.main\n$ flow-cli canary $WORKFLOW --run-as-secure-group $TEAM --parameters-json=$CFG --entitlement $ENTITLEMENT\n')))}f.isMDXComponent=!0}}]);