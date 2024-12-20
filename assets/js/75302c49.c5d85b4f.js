"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[3478],{15680:(e,n,t)=>{t.r(n),t.d(n,{MDXContext:()=>c,MDXProvider:()=>u,mdx:()=>f,useMDXComponents:()=>s,withMDXComponents:()=>d});var a=t(96540);function r(e,n,t){return n in e?Object.defineProperty(e,n,{value:t,enumerable:!0,configurable:!0,writable:!0}):e[n]=t,e}function i(){return i=Object.assign||function(e){for(var n=1;n<arguments.length;n++){var t=arguments[n];for(var a in t)Object.prototype.hasOwnProperty.call(t,a)&&(e[a]=t[a])}return e},i.apply(this,arguments)}function p(e,n){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);n&&(a=a.filter((function(n){return Object.getOwnPropertyDescriptor(e,n).enumerable}))),t.push.apply(t,a)}return t}function o(e){for(var n=1;n<arguments.length;n++){var t=null!=arguments[n]?arguments[n]:{};n%2?p(Object(t),!0).forEach((function(n){r(e,n,t[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):p(Object(t)).forEach((function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(t,n))}))}return e}function l(e,n){if(null==e)return{};var t,a,r=function(e,n){if(null==e)return{};var t,a,r={},i=Object.keys(e);for(a=0;a<i.length;a++)t=i[a],n.indexOf(t)>=0||(r[t]=e[t]);return r}(e,n);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);for(a=0;a<i.length;a++)t=i[a],n.indexOf(t)>=0||Object.prototype.propertyIsEnumerable.call(e,t)&&(r[t]=e[t])}return r}var c=a.createContext({}),d=function(e){return function(n){var t=s(n.components);return a.createElement(e,i({},n,{components:t}))}},s=function(e){var n=a.useContext(c),t=n;return e&&(t="function"==typeof e?e(n):o(o({},n),e)),t},u=function(e){var n=s(e.components);return a.createElement(c.Provider,{value:n},e.children)},m={inlineCode:"code",wrapper:function(e){var n=e.children;return a.createElement(a.Fragment,{},n)}},g=a.forwardRef((function(e,n){var t=e.components,r=e.mdxType,i=e.originalType,p=e.parentName,c=l(e,["components","mdxType","originalType","parentName"]),d=s(t),u=r,g=d["".concat(p,".").concat(u)]||d[u]||m[u]||i;return t?a.createElement(g,o(o({ref:n},c),{},{components:t})):a.createElement(g,o({ref:n},c))}));function f(e,n){var t=arguments,r=n&&n.mdxType;if("string"==typeof e||r){var i=t.length,p=new Array(i);p[0]=g;var o={};for(var l in n)hasOwnProperty.call(n,l)&&(o[l]=n[l]);o.originalType=e,o.mdxType="string"==typeof e?e:r,p[1]=o;for(var c=2;c<i;c++)p[c]=t[c];return a.createElement.apply(null,p)}return a.createElement.apply(null,t)}g.displayName="MDXCreateElement"},49595:(e,n,t)=>{t.d(n,{A:()=>l,C:()=>c});var a=t(58168),r=t(96540),i=t(75489),p=t(44586),o=t(74098);function l(e){return r.createElement(i.default,(0,a.A)({},e,{to:(n=e.to,l=(0,o.useActiveVersion)(),(0,p.default)().siteConfig.customFields.githubLinkVersionToBaseUrl[null!=(t=null==l?void 0:l.name)?t:"current"]+n),target:"_blank"}));var n,t,l}function c(e){var n,t=null!=(n=e.text)?n:"Example (Click Here)";return r.createElement(l,e,r.createElement("span",null,"\xa0"),r.createElement("img",{src:"https://img.shields.io/badge/-"+t+"-informational",alt:"Example (Click Here)"}))}},26942:(e,n,t)=>{t.r(n),t.d(n,{contentTitle:()=>c,default:()=>m,frontMatter:()=>l,metadata:()=>d,toc:()=>s});var a=t(58168),r=t(98587),i=(t(96540),t(15680)),p=t(49595),o=["components"],l={id:"app_packaging",title:"Application packaging",sidebar_label:"Application packaging"},c=void 0,d={unversionedId:"advanced/app_packaging",id:"version-1.3/advanced/app_packaging",title:"Application packaging",description:"You can package your Hydra application along with its configuration.",source:"@site/versioned_docs/version-1.3/advanced/packaging.md",sourceDirName:"advanced",slug:"/advanced/app_packaging",permalink:"/docs/1.3/advanced/app_packaging",editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/versioned_docs/version-1.3/advanced/packaging.md",tags:[],version:"1.3",lastUpdatedBy:"dependabot[bot]",lastUpdatedAt:1734709105,formattedLastUpdatedAt:"12/20/2024",frontMatter:{id:"app_packaging",title:"Application packaging",sidebar_label:"Application packaging"},sidebar:"docs",previous:{title:"Plugin development",permalink:"/docs/1.3/advanced/plugins/develop"},next:{title:"Decorating the main function",permalink:"/docs/1.3/advanced/decorating_main"}},s=[],u={toc:s};function m(e){var n=e.components,t=(0,r.A)(e,o);return(0,i.mdx)("wrapper",(0,a.A)({},u,t,{components:n,mdxType:"MDXLayout"}),(0,i.mdx)(p.C,{to:"examples/advanced/hydra_app_example",mdxType:"ExampleGithubLink"}),(0,i.mdx)("p",null,"You can package your Hydra application along with its configuration.\nAn example ",(0,i.mdx)(p.A,{to:"examples/advanced/hydra_app_example",mdxType:"GithubLink"},"standalone application")," is included in the repo."),(0,i.mdx)("p",null,"Run it with:"),(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre",className:"language-yaml"},"$ python examples/advanced/hydra_app_example/hydra_app/main.py\ndataset:\n  name: imagenet\n  path: /datasets/imagenet\n")),(0,i.mdx)("p",null,"Install it with:"),(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre",className:"language-text"},"$ pip install examples/advanced/hydra_app_example\n...\nSuccessfully installed hydra-app-0.1\n")),(0,i.mdx)("p",null,"Once installed, run the installed app with:"),(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre",className:"language-yaml"},"$ hydra_app\ndataset:\n  name: imagenet\n  path: /datasets/imagenet\n")),(0,i.mdx)("p",null,"The installed app will use the packaged configuration files."))}m.isMDXComponent=!0}}]);