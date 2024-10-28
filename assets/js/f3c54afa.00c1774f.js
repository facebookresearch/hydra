"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[1307],{15680:(e,r,t)=>{t.r(r),t.d(r,{MDXContext:()=>l,MDXProvider:()=>u,mdx:()=>v,useMDXComponents:()=>m,withMDXComponents:()=>p});var n=t(96540);function a(e,r,t){return r in e?Object.defineProperty(e,r,{value:t,enumerable:!0,configurable:!0,writable:!0}):e[r]=t,e}function o(){return o=Object.assign||function(e){for(var r=1;r<arguments.length;r++){var t=arguments[r];for(var n in t)Object.prototype.hasOwnProperty.call(t,n)&&(e[n]=t[n])}return e},o.apply(this,arguments)}function i(e,r){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);r&&(n=n.filter((function(r){return Object.getOwnPropertyDescriptor(e,r).enumerable}))),t.push.apply(t,n)}return t}function s(e){for(var r=1;r<arguments.length;r++){var t=null!=arguments[r]?arguments[r]:{};r%2?i(Object(t),!0).forEach((function(r){a(e,r,t[r])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):i(Object(t)).forEach((function(r){Object.defineProperty(e,r,Object.getOwnPropertyDescriptor(t,r))}))}return e}function d(e,r){if(null==e)return{};var t,n,a=function(e,r){if(null==e)return{};var t,n,a={},o=Object.keys(e);for(n=0;n<o.length;n++)t=o[n],r.indexOf(t)>=0||(a[t]=e[t]);return a}(e,r);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(e);for(n=0;n<o.length;n++)t=o[n],r.indexOf(t)>=0||Object.prototype.propertyIsEnumerable.call(e,t)&&(a[t]=e[t])}return a}var l=n.createContext({}),p=function(e){return function(r){var t=m(r.components);return n.createElement(e,o({},r,{components:t}))}},m=function(e){var r=n.useContext(l),t=r;return e&&(t="function"==typeof e?e(r):s(s({},r),e)),t},u=function(e){var r=m(e.components);return n.createElement(l.Provider,{value:r},e.children)},c={inlineCode:"code",wrapper:function(e){var r=e.children;return n.createElement(n.Fragment,{},r)}},g=n.forwardRef((function(e,r){var t=e.components,a=e.mdxType,o=e.originalType,i=e.parentName,l=d(e,["components","mdxType","originalType","parentName"]),p=m(t),u=a,g=p["".concat(i,".").concat(u)]||p[u]||c[u]||o;return t?n.createElement(g,s(s({ref:r},l),{},{components:t})):n.createElement(g,s({ref:r},l))}));function v(e,r){var t=arguments,a=r&&r.mdxType;if("string"==typeof e||a){var o=t.length,i=new Array(o);i[0]=g;var s={};for(var d in r)hasOwnProperty.call(r,d)&&(s[d]=r[d]);s.originalType=e,s.mdxType="string"==typeof e?e:a,i[1]=s;for(var l=2;l<o;l++)i[l]=t[l];return n.createElement.apply(null,i)}return n.createElement.apply(null,t)}g.displayName="MDXCreateElement"},38822:(e,r,t)=>{t.r(r),t.d(r,{contentTitle:()=>d,default:()=>u,frontMatter:()=>s,metadata:()=>l,toc:()=>p});var n=t(58168),a=t(98587),o=(t(96540),t(15680)),i=["components"],s={id:"intro",title:"Introduction",sidebar_label:"Introduction"},d=void 0,l={unversionedId:"upgrades/intro",id:"version-1.1/upgrades/intro",title:"Introduction",description:"Upgrading to a new Hydra version is usually an easy process.",source:"@site/versioned_docs/version-1.1/upgrades/intro.md",sourceDirName:"upgrades",slug:"/upgrades/intro",permalink:"/docs/1.1/upgrades/intro",editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/versioned_docs/version-1.1/upgrades/intro.md",tags:[],version:"1.1",lastUpdatedBy:"dependabot[bot]",lastUpdatedAt:1730135614,formattedLastUpdatedAt:"10/28/2024",frontMatter:{id:"intro",title:"Introduction",sidebar_label:"Introduction"},sidebar:"version-1.1/docs",previous:{title:"Release process",permalink:"/docs/1.1/development/release"},next:{title:"Changes to @hydra.main() and hydra.initialize()",permalink:"/docs/1.1/upgrades/1.0_to_1.1/changes_to_hydra_main_config_path"}},p=[{value:"Major version upgrades",id:"major-version-upgrades",children:[],level:2},{value:"Patch version upgrades",id:"patch-version-upgrades",children:[],level:2},{value:"Dev release upgrades",id:"dev-release-upgrades",children:[],level:2}],m={toc:p};function u(e){var r=e.components,t=(0,a.A)(e,i);return(0,o.mdx)("wrapper",(0,n.A)({},m,t,{components:r,mdxType:"MDXLayout"}),(0,o.mdx)("p",null,"Upgrading to a new Hydra version is usually an easy process."),(0,o.mdx)("div",{className:"admonition admonition-info alert alert--info"},(0,o.mdx)("div",{parentName:"div",className:"admonition-heading"},(0,o.mdx)("h5",{parentName:"div"},(0,o.mdx)("span",{parentName:"h5",className:"admonition-icon"},(0,o.mdx)("svg",{parentName:"span",xmlns:"http://www.w3.org/2000/svg",width:"14",height:"16",viewBox:"0 0 14 16"},(0,o.mdx)("path",{parentName:"svg",fillRule:"evenodd",d:"M7 2.3c3.14 0 5.7 2.56 5.7 5.7s-2.56 5.7-5.7 5.7A5.71 5.71 0 0 1 1.3 8c0-3.14 2.56-5.7 5.7-5.7zM7 1C3.14 1 0 4.14 0 8s3.14 7 7 7 7-3.14 7-7-3.14-7-7-7zm1 3H6v5h2V4zm0 6H6v2h2v-2z"}))),"NOTE")),(0,o.mdx)("div",{parentName:"div",className:"admonition-content"},(0,o.mdx)("p",{parentName:"div"},"Hydra versioning has only major versions and patch versions. A bump of the first two version digits is considered a major release.\nA major release may have multiple followup patch releases that will fix bugs without introducing new functionality."))),(0,o.mdx)("h2",{id:"major-version-upgrades"},"Major version upgrades"),(0,o.mdx)("p",null,"Hydra will typically provide helpful warnings about required changes, sometimes pointing to an upgrade page that provides more details about the required changes."),(0,o.mdx)("p",null,"For a smooth upgrade experience, please follow these simple rules:"),(0,o.mdx)("ul",null,(0,o.mdx)("li",{parentName:"ul"},(0,o.mdx)("strong",{parentName:"li"},"Upgrade to the latest patch version first"),".\ne.g: If you are upgrading from 1.0 to 1.1, be sure to upgrade to the latest 1.0 version first (1.0.6)."),(0,o.mdx)("li",{parentName:"ul"},(0,o.mdx)("strong",{parentName:"li"},"Address ALL runtime warnings issued by Hydra."),(0,o.mdx)("br",{parentName:"li"}),"A warning in one version is likely to become a far less friendly error in the next major version."),(0,o.mdx)("li",{parentName:"ul"},(0,o.mdx)("strong",{parentName:"li"},"Do not skip major versions"),".",(0,o.mdx)("br",{parentName:"li"}),"e.g: If you are upgrading from Hydra 1.0 to Hydra 1.2 - Do it by",(0,o.mdx)("ul",{parentName:"li"},(0,o.mdx)("li",{parentName:"ul"},"Upgrading from 1.0 to 1.1, addressing all the warnings."),(0,o.mdx)("li",{parentName:"ul"},"Upgrading from 1.1 to 1.2, addressing all the warnings.")))),(0,o.mdx)("h2",{id:"patch-version-upgrades"},"Patch version upgrades"),(0,o.mdx)("p",null,"Patch releases normally contains only bug fixes and are thus safe and easy to upgrade (e.g. ",(0,o.mdx)("strong",{parentName:"p"},"1.0.3")," to ",(0,o.mdx)("strong",{parentName:"p"},"1.0.6"),").",(0,o.mdx)("br",{parentName:"p"}),"\n","In rare cases, patch releases will introduce new warnings. Be sure to address them before upgrading to the next major version."),(0,o.mdx)("h2",{id:"dev-release-upgrades"},"Dev release upgrades"),(0,o.mdx)("p",null,"Development releases are subject to breaking changes without notice. Please be aware that upgrading to a new development release\nis more likely to introduce some breakage. No attempt will be made to make upgrading between development releases easy."))}u.isMDXComponent=!0}}]);