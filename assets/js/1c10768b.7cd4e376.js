"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[4429],{15680:(e,t,n)=>{n.r(t),n.d(t,{MDXContext:()=>p,MDXProvider:()=>m,mdx:()=>v,useMDXComponents:()=>c,withMDXComponents:()=>d});var r=n(96540);function o(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function i(){return i=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var r in n)Object.prototype.hasOwnProperty.call(n,r)&&(e[r]=n[r])}return e},i.apply(this,arguments)}function a(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,r)}return n}function s(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?a(Object(n),!0).forEach((function(t){o(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):a(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function l(e,t){if(null==e)return{};var n,r,o=function(e,t){if(null==e)return{};var n,r,o={},i=Object.keys(e);for(r=0;r<i.length;r++)n=i[r],t.indexOf(n)>=0||(o[n]=e[n]);return o}(e,t);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);for(r=0;r<i.length;r++)n=i[r],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(o[n]=e[n])}return o}var p=r.createContext({}),d=function(e){return function(t){var n=c(t.components);return r.createElement(e,i({},t,{components:n}))}},c=function(e){var t=r.useContext(p),n=t;return e&&(n="function"==typeof e?e(t):s(s({},t),e)),n},m=function(e){var t=c(e.components);return r.createElement(p.Provider,{value:t},e.children)},u="mdxType",f={inlineCode:"code",wrapper:function(e){var t=e.children;return r.createElement(r.Fragment,{},t)}},y=r.forwardRef((function(e,t){var n=e.components,o=e.mdxType,i=e.originalType,a=e.parentName,p=l(e,["components","mdxType","originalType","parentName"]),d=c(n),m=o,u=d["".concat(a,".").concat(m)]||d[m]||f[m]||i;return n?r.createElement(u,s(s({ref:t},p),{},{components:n})):r.createElement(u,s({ref:t},p))}));function v(e,t){var n=arguments,o=t&&t.mdxType;if("string"==typeof e||o){var i=n.length,a=new Array(i);a[0]=y;var s={};for(var l in t)hasOwnProperty.call(t,l)&&(s[l]=t[l]);s.originalType=e,s[u]="string"==typeof e?e:o,a[1]=s;for(var p=2;p<i;p++)a[p]=n[p];return r.createElement.apply(null,a)}return r.createElement.apply(null,n)}y.displayName="MDXCreateElement"},84081:(e,t,n)=>{n.r(t),n.d(t,{assets:()=>l,contentTitle:()=>a,default:()=>m,frontMatter:()=>i,metadata:()=>s,toc:()=>p});var r=n(58168),o=(n(96540),n(15680));const i={id:"testing",title:"Testing",sidebar_label:"Testing"},a=void 0,s={unversionedId:"development/testing",id:"version-1.0/development/testing",title:"Testing",description:"Hydra uses a test automation tool called nox to manage tests, linting, code coverage, etc.",source:"@site/versioned_docs/version-1.0/development/testing.md",sourceDirName:"development",slug:"/development/testing",permalink:"/docs/1.0/development/testing",draft:!1,editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/versioned_docs/version-1.0/development/testing.md",tags:[],version:"1.0",lastUpdatedBy:"jesszzzz",lastUpdatedAt:1741383139,formattedLastUpdatedAt:"Mar 7, 2025",frontMatter:{id:"testing",title:"Testing",sidebar_label:"Testing"},sidebar:"docs",previous:{title:"Overview",permalink:"/docs/1.0/development/overview"},next:{title:"Style Guide",permalink:"/docs/1.0/development/style_guide"}},l={},p=[{value:"With pytest",id:"with-pytest",level:2},{value:"With nox",id:"with-nox",level:2}],d={toc:p},c="wrapper";function m(e){let{components:t,...n}=e;return(0,o.mdx)(c,(0,r.A)({},d,n,{components:t,mdxType:"MDXLayout"}),(0,o.mdx)("p",null,"Hydra uses a test automation tool called ",(0,o.mdx)("a",{parentName:"p",href:"https://github.com/theacodes/nox"},"nox")," to manage tests, linting, code coverage, etc.\n",(0,o.mdx)("inlineCode",{parentName:"p"},"nox")," will run all the configured sessions. You can see the full list of nox sessions with ",(0,o.mdx)("inlineCode",{parentName:"p"},"nox -l")," and run specific sessions\nwith ",(0,o.mdx)("inlineCode",{parentName:"p"},"nox -s NAME")," (you may need to quote the session name in some cases)"),(0,o.mdx)("h2",{id:"with-pytest"},"With pytest"),(0,o.mdx)("p",null,"Run ",(0,o.mdx)("inlineCode",{parentName:"p"},"pytest")," at the repository root to run all the Hydra core tests.\nTo run the tests of individual plugins, use ",(0,o.mdx)("inlineCode",{parentName:"p"},"pytest plugins/NAME"),"."),(0,o.mdx)("admonition",{title:"NOTE",type:"info"},(0,o.mdx)("p",{parentName:"admonition"},"Some plugins support fewer versions of Python than the Hydra core.")),(0,o.mdx)("h2",{id:"with-nox"},"With nox"),(0,o.mdx)("p",null,"See ",(0,o.mdx)("inlineCode",{parentName:"p"},"nox -l"),". a few examples:"),(0,o.mdx)("ul",null,(0,o.mdx)("li",{parentName:"ul"},(0,o.mdx)("inlineCode",{parentName:"li"},"nox -s test_core")," will test Hydra core on all supported Python versions"),(0,o.mdx)("li",{parentName:"ul"},(0,o.mdx)("inlineCode",{parentName:"li"},'nox -s "test_core-3.6(pip install)"')," : Test on Python 3.6 with ",(0,o.mdx)("inlineCode",{parentName:"li"},"pip install")," as installation method"),(0,o.mdx)("li",{parentName:"ul"},(0,o.mdx)("inlineCode",{parentName:"li"},'nox -s "test_plugins-3.8(pip install -e)"')," : Test plugins on Python 3.8 with ",(0,o.mdx)("inlineCode",{parentName:"li"},"pip install -e")," as installation method")))}m.isMDXComponent=!0}}]);