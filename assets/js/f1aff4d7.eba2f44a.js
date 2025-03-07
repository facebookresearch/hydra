"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[7780],{5911:(e,n,t)=>{t.r(n),t.d(n,{assets:()=>p,contentTitle:()=>o,default:()=>s,frontMatter:()=>a,metadata:()=>l,toc:()=>u});var r=t(58168),i=(t(96540),t(15680));const a={id:"debugging",title:"Debugging",sidebar_label:"Debugging"},o=void 0,l={unversionedId:"tutorials/basic/running_your_app/debugging",id:"tutorials/basic/running_your_app/debugging",title:"Debugging",description:"Hydra provides a few options to improve debuggability.",source:"@site/docs/tutorials/basic/running_your_app/5_debugging.md",sourceDirName:"tutorials/basic/running_your_app",slug:"/tutorials/basic/running_your_app/debugging",permalink:"/docs/tutorials/basic/running_your_app/debugging",draft:!1,editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/docs/tutorials/basic/running_your_app/5_debugging.md",tags:[],version:"current",lastUpdatedBy:"Jasha10",lastUpdatedAt:1620854337,formattedLastUpdatedAt:"May 12, 2021",sidebarPosition:5,frontMatter:{id:"debugging",title:"Debugging",sidebar_label:"Debugging"},sidebar:"docs",previous:{title:"Logging",permalink:"/docs/tutorials/basic/running_your_app/logging"},next:{title:"Tab completion",permalink:"/docs/tutorials/basic/running_your_app/tab_completion"}},p={},u=[{value:"Printing the configuration",id:"printing-the-configuration",level:3},{value:"Info",id:"info",level:3}],d={toc:u},c="wrapper";function s(e){let{components:n,...t}=e;return(0,i.mdx)(c,(0,r.A)({},d,t,{components:n,mdxType:"MDXLayout"}),(0,i.mdx)("p",null,"Hydra provides a few options to improve debuggability."),(0,i.mdx)("h3",{id:"printing-the-configuration"},"Printing the configuration"),(0,i.mdx)("p",null,"Print the config for your app without running your function by adding ",(0,i.mdx)("inlineCode",{parentName:"p"},"--cfg")," or ",(0,i.mdx)("inlineCode",{parentName:"p"},"-c")," to the command line."),(0,i.mdx)("p",null,"The ",(0,i.mdx)("inlineCode",{parentName:"p"},"--cfg")," option takes one argument indicating which part of the config to print:"),(0,i.mdx)("ul",null,(0,i.mdx)("li",{parentName:"ul"},(0,i.mdx)("inlineCode",{parentName:"li"},"job"),": Your config"),(0,i.mdx)("li",{parentName:"ul"},(0,i.mdx)("inlineCode",{parentName:"li"},"hydra"),": Hydra's config"),(0,i.mdx)("li",{parentName:"ul"},(0,i.mdx)("inlineCode",{parentName:"li"},"all"),": The full config, which is a union of ",(0,i.mdx)("inlineCode",{parentName:"li"},"job")," and ",(0,i.mdx)("inlineCode",{parentName:"li"},"hydra"),".")),(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre",className:"language-yaml"},"# A normal run:\n$ python my_app.py\nMySQL connecting to localhost with user=root and password=1234\n\n# just show the config without running your function:\n$ python my_app.py --cfg job\ndb:\n  host: localhost\n  user: root\n  password: 1234\n")),(0,i.mdx)("p",null,"The printed config includes any modifications done via the command line:"),(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:"{3}","{3}":!0},"$ python my_app.py db.host=10.0.0.1 --cfg job\ndb:\n  host: 10.0.0.1\n  user: root\n  password: 1234\n")),(0,i.mdx)("p",null,"You can use --package or -p to display a subset of the configuration:"),(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre",className:"language-yaml"},"python my_app.py --cfg hydra --package hydra.job\n# @package hydra.job\nname: my_app\nconfig_name: config\n...\n")),(0,i.mdx)("p",null,"By default, config interpolations are not resolved. To print resolved config use the ",(0,i.mdx)("inlineCode",{parentName:"p"},"--resolve")," flag in addition to the ",(0,i.mdx)("inlineCode",{parentName:"p"},"--cfg")," flag"),(0,i.mdx)("h3",{id:"info"},"Info"),(0,i.mdx)("p",null,"The ",(0,i.mdx)("inlineCode",{parentName:"p"},"--info")," flag can provide information about various aspects of Hydra and your application:"),(0,i.mdx)("ul",null,(0,i.mdx)("li",{parentName:"ul"},(0,i.mdx)("inlineCode",{parentName:"li"},"--info all"),": Default behavior, prints everything"),(0,i.mdx)("li",{parentName:"ul"},(0,i.mdx)("inlineCode",{parentName:"li"},"--info config"),": Prints information useful to understanding the config composition:",(0,i.mdx)("br",{parentName:"li"}),"Config Search Path, Defaults Tree, Defaults List and the final config."),(0,i.mdx)("li",{parentName:"ul"},(0,i.mdx)("inlineCode",{parentName:"li"},"--info defaults"),": Prints the Final Defaults List"),(0,i.mdx)("li",{parentName:"ul"},(0,i.mdx)("inlineCode",{parentName:"li"},"--info defaults-tree"),": Prints the Defaults Tree"),(0,i.mdx)("li",{parentName:"ul"},(0,i.mdx)("inlineCode",{parentName:"li"},"--info plugins"),": Prints information about installed plugins")))}s.isMDXComponent=!0},15680:(e,n,t)=>{t.r(n),t.d(n,{MDXContext:()=>u,MDXProvider:()=>s,mdx:()=>y,useMDXComponents:()=>c,withMDXComponents:()=>d});var r=t(96540);function i(e,n,t){return n in e?Object.defineProperty(e,n,{value:t,enumerable:!0,configurable:!0,writable:!0}):e[n]=t,e}function a(){return a=Object.assign||function(e){for(var n=1;n<arguments.length;n++){var t=arguments[n];for(var r in t)Object.prototype.hasOwnProperty.call(t,r)&&(e[r]=t[r])}return e},a.apply(this,arguments)}function o(e,n){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);n&&(r=r.filter((function(n){return Object.getOwnPropertyDescriptor(e,n).enumerable}))),t.push.apply(t,r)}return t}function l(e){for(var n=1;n<arguments.length;n++){var t=null!=arguments[n]?arguments[n]:{};n%2?o(Object(t),!0).forEach((function(n){i(e,n,t[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):o(Object(t)).forEach((function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(t,n))}))}return e}function p(e,n){if(null==e)return{};var t,r,i=function(e,n){if(null==e)return{};var t,r,i={},a=Object.keys(e);for(r=0;r<a.length;r++)t=a[r],n.indexOf(t)>=0||(i[t]=e[t]);return i}(e,n);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);for(r=0;r<a.length;r++)t=a[r],n.indexOf(t)>=0||Object.prototype.propertyIsEnumerable.call(e,t)&&(i[t]=e[t])}return i}var u=r.createContext({}),d=function(e){return function(n){var t=c(n.components);return r.createElement(e,a({},n,{components:t}))}},c=function(e){var n=r.useContext(u),t=n;return e&&(t="function"==typeof e?e(n):l(l({},n),e)),t},s=function(e){var n=c(e.components);return r.createElement(u.Provider,{value:n},e.children)},m="mdxType",g={inlineCode:"code",wrapper:function(e){var n=e.children;return r.createElement(r.Fragment,{},n)}},f=r.forwardRef((function(e,n){var t=e.components,i=e.mdxType,a=e.originalType,o=e.parentName,u=p(e,["components","mdxType","originalType","parentName"]),d=c(t),s=i,m=d["".concat(o,".").concat(s)]||d[s]||g[s]||a;return t?r.createElement(m,l(l({ref:n},u),{},{components:t})):r.createElement(m,l({ref:n},u))}));function y(e,n){var t=arguments,i=n&&n.mdxType;if("string"==typeof e||i){var a=t.length,o=new Array(a);o[0]=f;var l={};for(var p in n)hasOwnProperty.call(n,p)&&(l[p]=n[p]);l.originalType=e,l[m]="string"==typeof e?e:i,o[1]=l;for(var u=2;u<a;u++)o[u]=t[u];return r.createElement.apply(null,o)}return r.createElement.apply(null,t)}f.displayName="MDXCreateElement"}}]);