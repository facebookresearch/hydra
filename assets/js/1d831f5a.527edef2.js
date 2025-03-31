"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[9404],{15680:(e,n,t)=>{t.r(n),t.d(n,{MDXContext:()=>s,MDXProvider:()=>d,mdx:()=>f,useMDXComponents:()=>p,withMDXComponents:()=>u});var r=t(96540);function a(e,n,t){return n in e?Object.defineProperty(e,n,{value:t,enumerable:!0,configurable:!0,writable:!0}):e[n]=t,e}function i(){return i=Object.assign||function(e){for(var n=1;n<arguments.length;n++){var t=arguments[n];for(var r in t)Object.prototype.hasOwnProperty.call(t,r)&&(e[r]=t[r])}return e},i.apply(this,arguments)}function o(e,n){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);n&&(r=r.filter((function(n){return Object.getOwnPropertyDescriptor(e,n).enumerable}))),t.push.apply(t,r)}return t}function l(e){for(var n=1;n<arguments.length;n++){var t=null!=arguments[n]?arguments[n]:{};n%2?o(Object(t),!0).forEach((function(n){a(e,n,t[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):o(Object(t)).forEach((function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(t,n))}))}return e}function c(e,n){if(null==e)return{};var t,r,a=function(e,n){if(null==e)return{};var t,r,a={},i=Object.keys(e);for(r=0;r<i.length;r++)t=i[r],n.indexOf(t)>=0||(a[t]=e[t]);return a}(e,n);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);for(r=0;r<i.length;r++)t=i[r],n.indexOf(t)>=0||Object.prototype.propertyIsEnumerable.call(e,t)&&(a[t]=e[t])}return a}var s=r.createContext({}),u=function(e){return function(n){var t=p(n.components);return r.createElement(e,i({},n,{components:t}))}},p=function(e){var n=r.useContext(s),t=n;return e&&(t="function"==typeof e?e(n):l(l({},n),e)),t},d=function(e){var n=p(e.components);return r.createElement(s.Provider,{value:n},e.children)},m="mdxType",h={inlineCode:"code",wrapper:function(e){var n=e.children;return r.createElement(r.Fragment,{},n)}},g=r.forwardRef((function(e,n){var t=e.components,a=e.mdxType,i=e.originalType,o=e.parentName,s=c(e,["components","mdxType","originalType","parentName"]),u=p(t),d=a,m=u["".concat(o,".").concat(d)]||u[d]||h[d]||i;return t?r.createElement(m,l(l({ref:n},s),{},{components:t})):r.createElement(m,l({ref:n},s))}));function f(e,n){var t=arguments,a=n&&n.mdxType;if("string"==typeof e||a){var i=t.length,o=new Array(i);o[0]=g;var l={};for(var c in n)hasOwnProperty.call(n,c)&&(l[c]=n[c]);l.originalType=e,l[m]="string"==typeof e?e:a,o[1]=l;for(var s=2;s<i;s++)o[s]=t[s];return r.createElement.apply(null,o)}return r.createElement.apply(null,t)}g.displayName="MDXCreateElement"},49595:(e,n,t)=>{t.d(n,{A:()=>s,C:()=>u});var r=t(58168),a=t(96540),i=t(75489),o=t(44586),l=t(48295);function c(e){const n=(0,l.ir)();return(0,o.default)().siteConfig.customFields.githubLinkVersionToBaseUrl[n?.name??"current"]+e}function s(e){return a.createElement(i.default,(0,r.A)({},e,{to:c(e.to),target:"_blank"}))}function u(e){const n=e.text??"Example (Click Here)";return a.createElement(s,e,a.createElement("span",null,"\xa0"),a.createElement("img",{src:"https://img.shields.io/badge/-"+n+"-informational",alt:"Example (Click Here)"}))}},66115:(e,n,t)=>{t.r(n),t.d(n,{assets:()=>s,contentTitle:()=>l,default:()=>m,frontMatter:()=>o,metadata:()=>c,toc:()=>u});var r=t(58168),a=(t(96540),t(15680)),i=t(49595);const o={id:"overview",title:"Plugins Overview",sidebar_label:"Plugins Overview"},l=void 0,c={unversionedId:"advanced/plugins/overview",id:"advanced/plugins/overview",title:"Plugins Overview",description:"Hydra can be extended via plugins.",source:"@site/docs/advanced/plugins/intro.md",sourceDirName:"advanced/plugins",slug:"/advanced/plugins/overview",permalink:"/docs/advanced/plugins/overview",draft:!1,editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/docs/advanced/plugins/intro.md",tags:[],version:"current",lastUpdatedBy:"jesszzzz",lastUpdatedAt:1743461536,formattedLastUpdatedAt:"Mar 31, 2025",frontMatter:{id:"overview",title:"Plugins Overview",sidebar_label:"Plugins Overview"},sidebar:"docs",previous:{title:"Config Search Path",permalink:"/docs/advanced/search_path"},next:{title:"Plugin development",permalink:"/docs/advanced/plugins/develop"}},s={},u=[{value:"Plugin types",id:"plugin-types",level:2},{value:"Sweeper",id:"sweeper",level:3},{value:"Launcher",id:"launcher",level:3},{value:"SearchPathPlugin",id:"searchpathplugin",level:3},{value:"ConfigSource",id:"configsource",level:3}],p={toc:u},d="wrapper";function m(e){let{components:n,...t}=e;return(0,a.mdx)(d,(0,r.A)({},p,t,{components:n,mdxType:"MDXLayout"}),(0,a.mdx)("p",null,"Hydra can be extended via plugins.\nThe example plugins ",(0,a.mdx)(i.A,{to:"examples/plugins",mdxType:"GithubLink"},"here")," can help you get started with plugin development."),(0,a.mdx)("h2",{id:"plugin-types"},"Plugin types"),(0,a.mdx)("p",null,"Hydra has several plugin types:"),(0,a.mdx)("h3",{id:"sweeper"},"Sweeper"),(0,a.mdx)("p",null,"A sweeper is responsible for converting command line arguments list into multiple jobs.\nFor example, the basic built-in sweeper takes arguments like:"),(0,a.mdx)("pre",null,(0,a.mdx)("code",{parentName:"pre"},"batch_size=128 optimizer=nesterov,adam learning_rate=0.01,0.1 \n")),(0,a.mdx)("p",null,"And creates 4 jobs with the following parameters:"),(0,a.mdx)("pre",null,(0,a.mdx)("code",{parentName:"pre"},"batch_size=128 optimizer=nesterov learning_rate=0.01\nbatch_size=128 optimizer=nesterov learning_rate=0.1\nbatch_size=128 optimizer=adam learning_rate=0.01\nbatch_size=128 optimizer=adam learning_rate=0.1\n")),(0,a.mdx)("h3",{id:"launcher"},"Launcher"),(0,a.mdx)("p",null,"Launchers are responsible for launching a job to a specific environment.\nA Launcher takes a batch of argument lists like the one above and launches a job for each one.\nThe job uses those arguments to compose its configuration.\nThe basic launcher simply launches the job locally. "),(0,a.mdx)("h3",{id:"searchpathplugin"},"SearchPathPlugin"),(0,a.mdx)("p",null,"A config path plugin can manipulate the search path.\nThis can be used to influence the default Hydra configuration to be more appropriate to a specific environment,\nor just add new entries to the search path to make more configurations available to the Hydra app."),(0,a.mdx)("p",null,"SearchPathPlugin plugins are discovered automatically by Hydra and are being called to manipulate the search path before\nthe configuration is composed."),(0,a.mdx)("p",null,"Many other plugins also implement SearchPathPlugin to add their configuration to the config search path once they are installed. "),(0,a.mdx)("h3",{id:"configsource"},"ConfigSource"),(0,a.mdx)("p",null,"ConfigSource plugins can be used to allow Hydra to access configuration in non-standard locations when composing the config.\nThis can be used to enable access to an in-house private config store, or as a way to access configs from public sources like GitHub or"," ",(0,a.mdx)("a",{parentName:"p",href:"https://internalfb.com/sevmanager/view/3"},"S3"),"."))}m.isMDXComponent=!0}}]);