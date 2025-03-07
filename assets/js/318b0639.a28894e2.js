"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[1707],{15680:(e,t,n)=>{n.r(t),n.d(t,{MDXContext:()=>d,MDXProvider:()=>m,mdx:()=>y,useMDXComponents:()=>c,withMDXComponents:()=>s});var r=n(96540);function o(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function a(){return a=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var r in n)Object.prototype.hasOwnProperty.call(n,r)&&(e[r]=n[r])}return e},a.apply(this,arguments)}function i(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,r)}return n}function p(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?i(Object(n),!0).forEach((function(t){o(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):i(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function l(e,t){if(null==e)return{};var n,r,o=function(e,t){if(null==e)return{};var n,r,o={},a=Object.keys(e);for(r=0;r<a.length;r++)n=a[r],t.indexOf(n)>=0||(o[n]=e[n]);return o}(e,t);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);for(r=0;r<a.length;r++)n=a[r],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(o[n]=e[n])}return o}var d=r.createContext({}),s=function(e){return function(t){var n=c(t.components);return r.createElement(e,a({},t,{components:n}))}},c=function(e){var t=r.useContext(d),n=t;return e&&(n="function"==typeof e?e(t):p(p({},t),e)),n},m=function(e){var t=c(e.components);return r.createElement(d.Provider,{value:t},e.children)},u="mdxType",v={inlineCode:"code",wrapper:function(e){var t=e.children;return r.createElement(r.Fragment,{},t)}},f=r.forwardRef((function(e,t){var n=e.components,o=e.mdxType,a=e.originalType,i=e.parentName,d=l(e,["components","mdxType","originalType","parentName"]),s=c(n),m=o,u=s["".concat(i,".").concat(m)]||s[m]||v[m]||a;return n?r.createElement(u,p(p({ref:t},d),{},{components:n})):r.createElement(u,p({ref:t},d))}));function y(e,t){var n=arguments,o=t&&t.mdxType;if("string"==typeof e||o){var a=n.length,i=new Array(a);i[0]=f;var p={};for(var l in t)hasOwnProperty.call(t,l)&&(p[l]=t[l]);p.originalType=e,p[u]="string"==typeof e?e:o,i[1]=p;for(var d=2;d<a;d++)i[d]=n[d];return r.createElement.apply(null,i)}return r.createElement.apply(null,n)}f.displayName="MDXCreateElement"},23959:(e,t,n)=>{n.r(t),n.d(t,{assets:()=>l,contentTitle:()=>i,default:()=>m,frontMatter:()=>a,metadata:()=>p,toc:()=>d});var r=n(58168),o=(n(96540),n(15680));const a={id:"overview",title:"Developer Guide Overview"},i=void 0,p={unversionedId:"development/overview",id:"version-1.1/development/overview",title:"Developer Guide Overview",description:"This guide assumes you have checked-out the repository.",source:"@site/versioned_docs/version-1.1/development/overview.md",sourceDirName:"development",slug:"/development/overview",permalink:"/docs/1.1/development/overview",draft:!1,editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/versioned_docs/version-1.1/development/overview.md",tags:[],version:"1.1",lastUpdatedBy:"Omry Yadan",lastUpdatedAt:1623349300,formattedLastUpdatedAt:"Jun 10, 2021",frontMatter:{id:"overview",title:"Developer Guide Overview"},sidebar:"docs",previous:{title:"Callbacks",permalink:"/docs/1.1/experimental/callbacks"},next:{title:"Testing",permalink:"/docs/1.1/development/testing"}},l={},d=[{value:"Environment setup",id:"environment-setup",level:2}],s={toc:d},c="wrapper";function m(e){let{components:t,...n}=e;return(0,o.mdx)(c,(0,r.A)({},s,n,{components:t,mdxType:"MDXLayout"}),(0,o.mdx)("p",null,"This guide assumes you have checked-out the ",(0,o.mdx)("a",{parentName:"p",href:"https://github.com/facebookresearch/hydra"},"repository"),".\nIt is recommended that you install Hydra in a virtual environment like ",(0,o.mdx)("a",{parentName:"p",href:"https://docs.conda.io/en/latest/"},"conda")," or ",(0,o.mdx)("a",{parentName:"p",href:"https://virtualenv.pypa.io/en/latest/"},"virtualenv"),"."),(0,o.mdx)("h2",{id:"environment-setup"},"Environment setup"),(0,o.mdx)("p",null,"Install ",(0,o.mdx)("a",{parentName:"p",href:"https://docs.conda.io/en/latest/miniconda.html"},"Miniconda")," and create an empty Conda environment with:"),(0,o.mdx)("pre",null,(0,o.mdx)("code",{parentName:"pre"},"conda create -n hydra38 python=3.8 -qy\n")),(0,o.mdx)("admonition",{title:"NOTE",type:"info"},(0,o.mdx)("p",{parentName:"admonition"},"The core Hydra framework supports Python 3.6 or newer. You may need to create additional environments for different Python versions if CI detect issues on a supported version of Python.")),(0,o.mdx)("p",null,"Activate the environment:"),(0,o.mdx)("pre",null,(0,o.mdx)("code",{parentName:"pre"},"conda activate hydra38\n")),(0,o.mdx)("p",null,"From the source tree, install Hydra in development mode with the following commands:"),(0,o.mdx)("pre",null,(0,o.mdx)("code",{parentName:"pre",className:"language-bash"},"# install development dependencies\npip install -r requirements/dev.txt\n# install Hydra in development (editable) mode\npip install -e .\n")))}m.isMDXComponent=!0}}]);