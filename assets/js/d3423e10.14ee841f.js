"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[5705],{15680:(e,t,n)=>{n.r(t),n.d(t,{MDXContext:()=>s,MDXProvider:()=>m,mdx:()=>v,useMDXComponents:()=>c,withMDXComponents:()=>p});var r=n(96540);function o(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function i(){return i=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var r in n)Object.prototype.hasOwnProperty.call(n,r)&&(e[r]=n[r])}return e},i.apply(this,arguments)}function l(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,r)}return n}function a(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?l(Object(n),!0).forEach((function(t){o(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):l(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function d(e,t){if(null==e)return{};var n,r,o=function(e,t){if(null==e)return{};var n,r,o={},i=Object.keys(e);for(r=0;r<i.length;r++)n=i[r],t.indexOf(n)>=0||(o[n]=e[n]);return o}(e,t);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);for(r=0;r<i.length;r++)n=i[r],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(o[n]=e[n])}return o}var s=r.createContext({}),p=function(e){return function(t){var n=c(t.components);return r.createElement(e,i({},t,{components:n}))}},c=function(e){var t=r.useContext(s),n=t;return e&&(n="function"==typeof e?e(t):a(a({},t),e)),n},m=function(e){var t=c(e.components);return r.createElement(s.Provider,{value:t},e.children)},u="mdxType",y={inlineCode:"code",wrapper:function(e){var t=e.children;return r.createElement(r.Fragment,{},t)}},f=r.forwardRef((function(e,t){var n=e.components,o=e.mdxType,i=e.originalType,l=e.parentName,s=d(e,["components","mdxType","originalType","parentName"]),p=c(n),m=o,u=p["".concat(l,".").concat(m)]||p[m]||y[m]||i;return n?r.createElement(u,a(a({ref:t},s),{},{components:n})):r.createElement(u,a({ref:t},s))}));function v(e,t){var n=arguments,o=t&&t.mdxType;if("string"==typeof e||o){var i=n.length,l=new Array(i);l[0]=f;var a={};for(var d in t)hasOwnProperty.call(t,d)&&(a[d]=t[d]);a.originalType=e,a[u]="string"==typeof e?e:o,l[1]=a;for(var s=2;s<i;s++)l[s]=n[s];return r.createElement.apply(null,l)}return r.createElement.apply(null,n)}f.displayName="MDXCreateElement"},70109:(e,t,n)=>{n.r(t),n.d(t,{assets:()=>d,contentTitle:()=>l,default:()=>m,frontMatter:()=>i,metadata:()=>a,toc:()=>s});var r=n(58168),o=(n(96540),n(15680));const i={id:"style_guide",title:"Style Guide",sidebar_label:"Style Guide"},l=void 0,a={unversionedId:"development/style_guide",id:"version-1.2/development/style_guide",title:"Style Guide",description:"The code need to pass verification by the following tools:",source:"@site/versioned_docs/version-1.2/development/style_guide.md",sourceDirName:"development",slug:"/development/style_guide",permalink:"/docs/1.2/development/style_guide",draft:!1,editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/versioned_docs/version-1.2/development/style_guide.md",tags:[],version:"1.2",lastUpdatedBy:"dependabot[bot]",lastUpdatedAt:1742161400,formattedLastUpdatedAt:"Mar 16, 2025",frontMatter:{id:"style_guide",title:"Style Guide",sidebar_label:"Style Guide"},sidebar:"docs",previous:{title:"Testing",permalink:"/docs/1.2/development/testing"},next:{title:"Documentation",permalink:"/docs/1.2/development/documentation"}},d={},s=[],p={toc:s},c="wrapper";function m(e){let{components:t,...n}=e;return(0,o.mdx)(c,(0,r.A)({},p,n,{components:t,mdxType:"MDXLayout"}),(0,o.mdx)("p",null,"The code need to pass verification by the following tools:"),(0,o.mdx)("ul",null,(0,o.mdx)("li",{parentName:"ul"},(0,o.mdx)("inlineCode",{parentName:"li"},"black .")," : Automatic code formatting for Python"),(0,o.mdx)("li",{parentName:"ul"},(0,o.mdx)("inlineCode",{parentName:"li"},"flake8")," : PEP8 compliance checker for Python, this includes copyright header verification"),(0,o.mdx)("li",{parentName:"ul"},(0,o.mdx)("inlineCode",{parentName:"li"},"isort .")," : Ensure imports are sorted properly"),(0,o.mdx)("li",{parentName:"ul"},(0,o.mdx)("inlineCode",{parentName:"li"},"mypy --strict .")," : Ensures code passes strict type checking"),(0,o.mdx)("li",{parentName:"ul"},(0,o.mdx)("inlineCode",{parentName:"li"},"yamllint .")," : Ensures that yaml files are syntactically correct and properly indented.")),(0,o.mdx)("p",null,"The easiest way to run the required verifications is: "),(0,o.mdx)("ul",null,(0,o.mdx)("li",{parentName:"ul"},(0,o.mdx)("inlineCode",{parentName:"li"},"nox -s lint")," : for the Hydra core"),(0,o.mdx)("li",{parentName:"ul"},(0,o.mdx)("inlineCode",{parentName:"li"},"nox -s lint_plugins")," : for the included plugins")),(0,o.mdx)("p",null,"isort is a bit tricky to run for plugins. the best way to get it to sort the plugins imports is with the FIX environment\nvariable:"),(0,o.mdx)("pre",null,(0,o.mdx)("code",{parentName:"pre"},"$ FIX=1 nox -s lint_plugins\n")),(0,o.mdx)("p",null,"It is also recommended that you install pre-commit hooks (use ",(0,o.mdx)("inlineCode",{parentName:"p"},"pre-commit install"),").\npre-commit will execute some of the above tests when you commit your code locally.\nYou can disable it by appending ",(0,o.mdx)("inlineCode",{parentName:"p"},"-n")," to your commit command: ",(0,o.mdx)("inlineCode",{parentName:"p"},"git commit -m wip -n")),(0,o.mdx)("p",null,"Pull requests that do not lint will fail the automated testing."))}m.isMDXComponent=!0}}]);