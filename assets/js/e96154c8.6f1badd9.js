"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[1736],{15680:(e,t,n)=>{n.r(t),n.d(t,{MDXContext:()=>d,MDXProvider:()=>c,mdx:()=>y,useMDXComponents:()=>u,withMDXComponents:()=>p});var r=n(96540);function a(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function o(){return o=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var r in n)Object.prototype.hasOwnProperty.call(n,r)&&(e[r]=n[r])}return e},o.apply(this,arguments)}function i(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,r)}return n}function l(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?i(Object(n),!0).forEach((function(t){a(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):i(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function s(e,t){if(null==e)return{};var n,r,a=function(e,t){if(null==e)return{};var n,r,a={},o=Object.keys(e);for(r=0;r<o.length;r++)n=o[r],t.indexOf(n)>=0||(a[n]=e[n]);return a}(e,t);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(e);for(r=0;r<o.length;r++)n=o[r],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(a[n]=e[n])}return a}var d=r.createContext({}),p=function(e){return function(t){var n=u(t.components);return r.createElement(e,o({},t,{components:n}))}},u=function(e){var t=r.useContext(d),n=t;return e&&(n="function"==typeof e?e(t):l(l({},t),e)),n},c=function(e){var t=u(e.components);return r.createElement(d.Provider,{value:t},e.children)},m="mdxType",f={inlineCode:"code",wrapper:function(e){var t=e.children;return r.createElement(r.Fragment,{},t)}},g=r.forwardRef((function(e,t){var n=e.components,a=e.mdxType,o=e.originalType,i=e.parentName,d=s(e,["components","mdxType","originalType","parentName"]),p=u(n),c=a,m=p["".concat(i,".").concat(c)]||p[c]||f[c]||o;return n?r.createElement(m,l(l({ref:t},d),{},{components:n})):r.createElement(m,l({ref:t},d))}));function y(e,t){var n=arguments,a=t&&t.mdxType;if("string"==typeof e||a){var o=n.length,i=new Array(o);i[0]=g;var l={};for(var s in t)hasOwnProperty.call(t,s)&&(l[s]=t[s]);l.originalType=e,l[m]="string"==typeof e?e:a,i[1]=l;for(var d=2;d<o;d++)i[d]=n[d];return r.createElement.apply(null,i)}return r.createElement.apply(null,n)}g.displayName="MDXCreateElement"},62361:(e,t,n)=>{n.r(t),n.d(t,{assets:()=>s,contentTitle:()=>i,default:()=>c,frontMatter:()=>o,metadata:()=>l,toc:()=>d});var r=n(58168),a=(n(96540),n(15680));const o={id:"defaults_list_interpolation",title:"Defaults List interpolation"},i=void 0,l={unversionedId:"upgrades/1.0_to_1.1/defaults_list_interpolation",id:"upgrades/1.0_to_1.1/defaults_list_interpolation",title:"Defaults List interpolation",description:"The defaults lists are used to compose the final config object.",source:"@site/docs/upgrades/1.0_to_1.1/defaults_list_interpolation_changes.md",sourceDirName:"upgrades/1.0_to_1.1",slug:"/upgrades/1.0_to_1.1/defaults_list_interpolation",permalink:"/docs/upgrades/1.0_to_1.1/defaults_list_interpolation",draft:!1,editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/docs/upgrades/1.0_to_1.1/defaults_list_interpolation_changes.md",tags:[],version:"current",lastUpdatedBy:"Omry Yadan",lastUpdatedAt:1609806448,formattedLastUpdatedAt:"Jan 5, 2021",frontMatter:{id:"defaults_list_interpolation",title:"Defaults List interpolation"},sidebar:"docs",previous:{title:"Defaults List Overrides",permalink:"/docs/upgrades/1.0_to_1.1/defaults_list_override"},next:{title:"Changes to Package Header",permalink:"/docs/upgrades/1.0_to_1.1/changes_to_package_header"}},s={},d=[{value:"Migration examples",id:"migration-examples",level:2}],p={toc:d},u="wrapper";function c(e){let{components:t,...n}=e;return(0,a.mdx)(u,(0,r.A)({},p,n,{components:t,mdxType:"MDXLayout"}),(0,a.mdx)("p",null,"The defaults lists are used to compose the final config object.\nHydra supports a limited form of interpolation in the defaults list.\nThe interpolation style described there is deprecated in favor of a cleaner style more\nappropriate to recursive default lists."),(0,a.mdx)("h2",{id:"migration-examples"},"Migration examples"),(0,a.mdx)("p",null,"For example, the following snippet from Hydra 1.0 or older: "),(0,a.mdx)("pre",null,(0,a.mdx)("code",{parentName:"pre",className:"language-yaml"},"defaults:\n  - dataset: imagenet\n  - model: alexnet\n  - dataset_model: ${defaults.0.dataset}_${defaults.1.model}\n")),(0,a.mdx)("p",null,"Changes to this in Hydra 1.1 or newer:"),(0,a.mdx)("pre",null,(0,a.mdx)("code",{parentName:"pre",className:"language-yaml"},"defaults:\n  - dataset: imagenet\n  - model: alexnet\n  - dataset_model: ${dataset}_${model}\n")),(0,a.mdx)("p",null,"The new style is more compact and does not require specifying the exact index of the element in the defaults list.\nThis is enables interpolating using config group values that are coming from recursive defaults."),(0,a.mdx)("p",null,"Note that:"),(0,a.mdx)("ul",null,(0,a.mdx)("li",{parentName:"ul"},"This is non-standard interpolation support that is unique to the defaults list"),(0,a.mdx)("li",{parentName:"ul"},"interpolation keys in the defaults list can not access values from the composed config because it does not yet\nexist when Hydra is processing the defaults list")),(0,a.mdx)("p",null,"The Defaults List is described ",(0,a.mdx)("a",{parentName:"p",href:"/docs/advanced/defaults_list"},"here"),"."),(0,a.mdx)("admonition",{type:"warning"},(0,a.mdx)("p",{parentName:"admonition"},"Support for the old style will be removed in Hydra 1.2.")))}c.isMDXComponent=!0}}]);