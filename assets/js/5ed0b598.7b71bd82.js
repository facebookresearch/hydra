"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[4673],{15680:(e,n,t)=>{t.r(n),t.d(n,{MDXContext:()=>d,MDXProvider:()=>c,mdx:()=>y,useMDXComponents:()=>u,withMDXComponents:()=>m});var a=t(96540);function r(e,n,t){return n in e?Object.defineProperty(e,n,{value:t,enumerable:!0,configurable:!0,writable:!0}):e[n]=t,e}function i(){return i=Object.assign||function(e){for(var n=1;n<arguments.length;n++){var t=arguments[n];for(var a in t)Object.prototype.hasOwnProperty.call(t,a)&&(e[a]=t[a])}return e},i.apply(this,arguments)}function o(e,n){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);n&&(a=a.filter((function(n){return Object.getOwnPropertyDescriptor(e,n).enumerable}))),t.push.apply(t,a)}return t}function l(e){for(var n=1;n<arguments.length;n++){var t=null!=arguments[n]?arguments[n]:{};n%2?o(Object(t),!0).forEach((function(n){r(e,n,t[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):o(Object(t)).forEach((function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(t,n))}))}return e}function s(e,n){if(null==e)return{};var t,a,r=function(e,n){if(null==e)return{};var t,a,r={},i=Object.keys(e);for(a=0;a<i.length;a++)t=i[a],n.indexOf(t)>=0||(r[t]=e[t]);return r}(e,n);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);for(a=0;a<i.length;a++)t=i[a],n.indexOf(t)>=0||Object.prototype.propertyIsEnumerable.call(e,t)&&(r[t]=e[t])}return r}var d=a.createContext({}),m=function(e){return function(n){var t=u(n.components);return a.createElement(e,i({},n,{components:t}))}},u=function(e){var n=a.useContext(d),t=n;return e&&(t="function"==typeof e?e(n):l(l({},n),e)),t},c=function(e){var n=u(e.components);return a.createElement(d.Provider,{value:n},e.children)},p="mdxType",f={inlineCode:"code",wrapper:function(e){var n=e.children;return a.createElement(a.Fragment,{},n)}},h=a.forwardRef((function(e,n){var t=e.components,r=e.mdxType,i=e.originalType,o=e.parentName,d=s(e,["components","mdxType","originalType","parentName"]),m=u(t),c=r,p=m["".concat(o,".").concat(c)]||m[c]||f[c]||i;return t?a.createElement(p,l(l({ref:n},d),{},{components:t})):a.createElement(p,l({ref:n},d))}));function y(e,n){var t=arguments,r=n&&n.mdxType;if("string"==typeof e||r){var i=t.length,o=new Array(i);o[0]=h;var l={};for(var s in n)hasOwnProperty.call(n,s)&&(l[s]=n[s]);l.originalType=e,l[p]="string"==typeof e?e:r,o[1]=l;for(var d=2;d<i;d++)o[d]=t[d];return a.createElement.apply(null,o)}return a.createElement.apply(null,t)}h.displayName="MDXCreateElement"},49227:(e,n,t)=>{t.r(n),t.d(n,{assets:()=>d,contentTitle:()=>l,default:()=>p,frontMatter:()=>o,metadata:()=>s,toc:()=>m});var a=t(58168),r=(t(96540),t(15680)),i=t(49595);const o={id:"documentation",title:"Documentation",sidebar_label:"Documentation"},l=void 0,s={unversionedId:"development/documentation",id:"version-1.0/development/documentation",title:"Documentation",description:"NEWS Entries",source:"@site/versioned_docs/version-1.0/development/documentation.md",sourceDirName:"development",slug:"/development/documentation",permalink:"/docs/1.0/development/documentation",draft:!1,editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/versioned_docs/version-1.0/development/documentation.md",tags:[],version:"1.0",lastUpdatedBy:"jesszzzz",lastUpdatedAt:1741383139,formattedLastUpdatedAt:"Mar 7, 2025",frontMatter:{id:"documentation",title:"Documentation",sidebar_label:"Documentation"},sidebar:"docs",previous:{title:"Style Guide",permalink:"/docs/1.0/development/style_guide"},next:{title:"Release process",permalink:"/docs/1.0/development/release"}},d={},m=[{value:"NEWS Entries",id:"news-entries",level:2},{value:"Contents of a NEWS entry",id:"contents-of-a-news-entry",level:3},{value:"Website setup",id:"website-setup",level:2},{value:"Install",id:"install",level:3},{value:"Local Development",id:"local-development",level:3}],u={toc:m},c="wrapper";function p(e){let{components:n,...t}=e;return(0,r.mdx)(c,(0,a.A)({},u,t,{components:n,mdxType:"MDXLayout"}),(0,r.mdx)("h2",{id:"news-entries"},"NEWS Entries"),(0,r.mdx)("p",null,"The ",(0,r.mdx)(i.A,{to:"NEWS.md",mdxType:"GithubLink"},"NEWS.md")," file is managed using ",(0,r.mdx)("inlineCode",{parentName:"p"},"towncrier")," and all non-trivial changes\nmust be accompanied by a news entry."),(0,r.mdx)("p",null,"To add an entry to the news file, first, you need to have created an issue\ndescribing the change you want to make. A Pull Request itself ",(0,r.mdx)("em",{parentName:"p"},"may")," function as\nsuch, but it is preferred to have a dedicated issue (for example, in case the\nPR ends up rejected due to code quality reasons)."),(0,r.mdx)("p",null,"Once you have an issue or pull request, you take the number, and you create a\nfile inside the ",(0,r.mdx)("inlineCode",{parentName:"p"},"news/")," directory named after that issue number with one of the following extensions:"),(0,r.mdx)("ul",null,(0,r.mdx)("li",{parentName:"ul"},(0,r.mdx)("inlineCode",{parentName:"li"},"api_change")," : API Change (Renames, deprecations, and removals)"),(0,r.mdx)("li",{parentName:"ul"},(0,r.mdx)("inlineCode",{parentName:"li"},"feature")," : Addition of a new feature"),(0,r.mdx)("li",{parentName:"ul"},(0,r.mdx)("inlineCode",{parentName:"li"},"bugfix")," : Fixing of a bug"),(0,r.mdx)("li",{parentName:"ul"},(0,r.mdx)("inlineCode",{parentName:"li"},"docs")," : Addition or updates to documentation"),(0,r.mdx)("li",{parentName:"ul"},(0,r.mdx)("inlineCode",{parentName:"li"},"plugin")," : Addition of changes to a plugin"),(0,r.mdx)("li",{parentName:"ul"},(0,r.mdx)("inlineCode",{parentName:"li"},"config")," : Changes or addition to the configuration structure"),(0,r.mdx)("li",{parentName:"ul"},(0,r.mdx)("inlineCode",{parentName:"li"},"maintenance")," : Changes that improve the maintainability of the code")),(0,r.mdx)("p",null,"If your issue or PR number is ",(0,r.mdx)("inlineCode",{parentName:"p"},"1234")," and this change is fixing a bug, you would\ncreate a file ",(0,r.mdx)("inlineCode",{parentName:"p"},"news/1234.bugfix"),". PRs can span multiple categories by creating\nmultiple files (for instance, if you added a feature and deprecated/removed the\nold feature at the same time, you would create ",(0,r.mdx)("inlineCode",{parentName:"p"},"news/NNNN.feature")," and\n",(0,r.mdx)("inlineCode",{parentName:"p"},"news/NNNN.api_change"),"). Likewise, if a PR touches multiple issues/PRs, you may\ncreate a file for each of them with the exact same contents, and Towncrier will\ndeduplicate them."),(0,r.mdx)("h3",{id:"contents-of-a-news-entry"},"Contents of a NEWS entry"),(0,r.mdx)("p",null,"The contents of this file are markdown formatted text that will be used\nas the content of the news file entry. You do not need to reference the issue\nor PR numbers here as towncrier will automatically add a reference to all of\nthe affected issues when rendering the news file."),(0,r.mdx)("p",null,"To maintain a consistent style in the ",(0,r.mdx)("inlineCode",{parentName:"p"},"NEWS.md"),' file, it is\npreferred to keep the news entry to the point, in sentence case, shorter than\n80 characters and in an imperative tone -- an entry should complete the sentence\n"This change will ...". In rare cases, where one line is not enough, use a\nsummary line in an imperative tone followed by a blank line separating it\nfrom a description of the feature/change in one or more paragraphs, each wrapped\nat 80 characters. Remember that a news entry is meant for end users and should\nonly contain details relevant to an end user.'),(0,r.mdx)("h2",{id:"website-setup"},"Website setup"),(0,r.mdx)("p",null,"The website is built using ",(0,r.mdx)("a",{parentName:"p",href:"https://v2.docusaurus.io/"},"Docusaurus 2"),".",(0,r.mdx)("br",{parentName:"p"}),"\n","Run the following commands from the ",(0,r.mdx)("inlineCode",{parentName:"p"},"website")," directory."),(0,r.mdx)("h3",{id:"install"},"Install"),(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre"},"$ yarn\n")),(0,r.mdx)("h3",{id:"local-development"},"Local Development"),(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre"},"$ yarn start\n")),(0,r.mdx)("p",null,"This command starts a local development server and opens up a browser window. Most changes are reflected live without having to restart the server."),(0,r.mdx)("p",null,"For more details, refer ",(0,r.mdx)(i.A,{to:"website/README.md",mdxType:"GithubLink"},"here"),"."))}p.isMDXComponent=!0},49595:(e,n,t)=>{t.d(n,{A:()=>d,C:()=>m});var a=t(58168),r=t(96540),i=t(75489),o=t(44586),l=t(48295);function s(e){const n=(0,l.ir)();return(0,o.default)().siteConfig.customFields.githubLinkVersionToBaseUrl[n?.name??"current"]+e}function d(e){return r.createElement(i.default,(0,a.A)({},e,{to:s(e.to),target:"_blank"}))}function m(e){const n=e.text??"Example (Click Here)";return r.createElement(d,e,r.createElement("span",null,"\xa0"),r.createElement("img",{src:"https://img.shields.io/badge/-"+n+"-informational",alt:"Example (Click Here)"}))}}}]);