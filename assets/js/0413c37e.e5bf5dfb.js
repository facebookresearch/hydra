"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[9101],{8074:(e,n,t)=>{t.r(n),t.d(n,{assets:()=>p,contentTitle:()=>a,default:()=>c,frontMatter:()=>o,metadata:()=>l,toc:()=>u});var r=t(58168),i=(t(96540),t(15680));const o={id:"debugging",title:"Debugging",sidebar_label:"Debugging"},a=void 0,l={unversionedId:"tutorials/basic/running_your_app/debugging",id:"version-1.2/tutorials/basic/running_your_app/debugging",title:"Debugging",description:"Hydra provides a few options to improve debuggability.",source:"@site/versioned_docs/version-1.2/tutorials/basic/running_your_app/5_debugging.md",sourceDirName:"tutorials/basic/running_your_app",slug:"/tutorials/basic/running_your_app/debugging",permalink:"/docs/1.2/tutorials/basic/running_your_app/debugging",draft:!1,editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/versioned_docs/version-1.2/tutorials/basic/running_your_app/5_debugging.md",tags:[],version:"1.2",lastUpdatedBy:"jesszzzz",lastUpdatedAt:1741383139,formattedLastUpdatedAt:"Mar 7, 2025",sidebarPosition:5,frontMatter:{id:"debugging",title:"Debugging",sidebar_label:"Debugging"},sidebar:"docs",previous:{title:"Logging",permalink:"/docs/1.2/tutorials/basic/running_your_app/logging"},next:{title:"Tab completion",permalink:"/docs/1.2/tutorials/basic/running_your_app/tab_completion"}},p={},u=[{value:"Printing the configuration",id:"printing-the-configuration",level:3},{value:"Info",id:"info",level:3}],d={toc:u},s="wrapper";function c(e){let{components:n,...t}=e;return(0,i.mdx)(s,(0,r.A)({},d,t,{components:n,mdxType:"MDXLayout"}),(0,i.mdx)("p",null,"Hydra provides a few options to improve debuggability."),(0,i.mdx)("h3",{id:"printing-the-configuration"},"Printing the configuration"),(0,i.mdx)("p",null,"Print the config for your app without running your function by adding ",(0,i.mdx)("inlineCode",{parentName:"p"},"--cfg")," or ",(0,i.mdx)("inlineCode",{parentName:"p"},"-c")," to the command line."),(0,i.mdx)("p",null,"The ",(0,i.mdx)("inlineCode",{parentName:"p"},"--cfg")," option takes one argument indicating which part of the config to print:"),(0,i.mdx)("ul",null,(0,i.mdx)("li",{parentName:"ul"},(0,i.mdx)("inlineCode",{parentName:"li"},"job"),": Your config"),(0,i.mdx)("li",{parentName:"ul"},(0,i.mdx)("inlineCode",{parentName:"li"},"hydra"),": Hydra's config"),(0,i.mdx)("li",{parentName:"ul"},(0,i.mdx)("inlineCode",{parentName:"li"},"all"),": The full config, which is a union of ",(0,i.mdx)("inlineCode",{parentName:"li"},"job")," and ",(0,i.mdx)("inlineCode",{parentName:"li"},"hydra"),".")),(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre",className:"language-yaml"},"# A normal run:\n$ python my_app.py\nMySQL connecting to localhost with user=root and password=1234\n\n# just show the config without running your function:\n$ python my_app.py --cfg job\ndb:\n  host: localhost\n  user: root\n  password: 1234\n")),(0,i.mdx)("p",null,"The printed config includes any modifications done via the command line:"),(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:"{3}","{3}":!0},"$ python my_app.py db.host=10.0.0.1 --cfg job\ndb:\n  host: 10.0.0.1\n  user: root\n  password: 1234\n")),(0,i.mdx)("p",null,"You can use --package or -p to display a subset of the configuration:"),(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre",className:"language-yaml"},"python my_app.py --cfg hydra --package hydra.job\n# @package hydra.job\nname: my_app\nconfig_name: config\n...\n")),(0,i.mdx)("p",null,"By default, config interpolations are not resolved. To print resolved config use the ",(0,i.mdx)("inlineCode",{parentName:"p"},"--resolve")," flag in addition to the ",(0,i.mdx)("inlineCode",{parentName:"p"},"--cfg")," flag"),(0,i.mdx)("h3",{id:"info"},"Info"),(0,i.mdx)("p",null,"The ",(0,i.mdx)("inlineCode",{parentName:"p"},"--info")," flag can provide information about various aspects of Hydra and your application:"),(0,i.mdx)("ul",null,(0,i.mdx)("li",{parentName:"ul"},(0,i.mdx)("inlineCode",{parentName:"li"},"--info all"),": Default behavior, prints everything"),(0,i.mdx)("li",{parentName:"ul"},(0,i.mdx)("inlineCode",{parentName:"li"},"--info config"),": Prints information useful to understanding the config composition:",(0,i.mdx)("br",{parentName:"li"}),"Config Search Path, Defaults Tree, Defaults List and the final config."),(0,i.mdx)("li",{parentName:"ul"},(0,i.mdx)("inlineCode",{parentName:"li"},"--info defaults"),": Prints the Final Defaults List"),(0,i.mdx)("li",{parentName:"ul"},(0,i.mdx)("inlineCode",{parentName:"li"},"--info defaults-tree"),": Prints the Defaults Tree"),(0,i.mdx)("li",{parentName:"ul"},(0,i.mdx)("inlineCode",{parentName:"li"},"--info plugins"),": Prints information about installed plugins")))}c.isMDXComponent=!0},15680:(e,n,t)=>{t.r(n),t.d(n,{MDXContext:()=>u,MDXProvider:()=>c,mdx:()=>y,useMDXComponents:()=>s,withMDXComponents:()=>d});var r=t(96540);function i(e,n,t){return n in e?Object.defineProperty(e,n,{value:t,enumerable:!0,configurable:!0,writable:!0}):e[n]=t,e}function o(){return o=Object.assign||function(e){for(var n=1;n<arguments.length;n++){var t=arguments[n];for(var r in t)Object.prototype.hasOwnProperty.call(t,r)&&(e[r]=t[r])}return e},o.apply(this,arguments)}function a(e,n){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);n&&(r=r.filter((function(n){return Object.getOwnPropertyDescriptor(e,n).enumerable}))),t.push.apply(t,r)}return t}function l(e){for(var n=1;n<arguments.length;n++){var t=null!=arguments[n]?arguments[n]:{};n%2?a(Object(t),!0).forEach((function(n){i(e,n,t[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):a(Object(t)).forEach((function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(t,n))}))}return e}function p(e,n){if(null==e)return{};var t,r,i=function(e,n){if(null==e)return{};var t,r,i={},o=Object.keys(e);for(r=0;r<o.length;r++)t=o[r],n.indexOf(t)>=0||(i[t]=e[t]);return i}(e,n);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(e);for(r=0;r<o.length;r++)t=o[r],n.indexOf(t)>=0||Object.prototype.propertyIsEnumerable.call(e,t)&&(i[t]=e[t])}return i}var u=r.createContext({}),d=function(e){return function(n){var t=s(n.components);return r.createElement(e,o({},n,{components:t}))}},s=function(e){var n=r.useContext(u),t=n;return e&&(t="function"==typeof e?e(n):l(l({},n),e)),t},c=function(e){var n=s(e.components);return r.createElement(u.Provider,{value:n},e.children)},m="mdxType",g={inlineCode:"code",wrapper:function(e){var n=e.children;return r.createElement(r.Fragment,{},n)}},f=r.forwardRef((function(e,n){var t=e.components,i=e.mdxType,o=e.originalType,a=e.parentName,u=p(e,["components","mdxType","originalType","parentName"]),d=s(t),c=i,m=d["".concat(a,".").concat(c)]||d[c]||g[c]||o;return t?r.createElement(m,l(l({ref:n},u),{},{components:t})):r.createElement(m,l({ref:n},u))}));function y(e,n){var t=arguments,i=n&&n.mdxType;if("string"==typeof e||i){var o=t.length,a=new Array(o);a[0]=f;var l={};for(var p in n)hasOwnProperty.call(n,p)&&(l[p]=n[p]);l.originalType=e,l[m]="string"==typeof e?e:i,a[1]=l;for(var u=2;u<o;u++)a[u]=t[u];return r.createElement.apply(null,a)}return r.createElement.apply(null,t)}f.displayName="MDXCreateElement"}}]);