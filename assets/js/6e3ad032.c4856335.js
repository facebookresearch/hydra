"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[331],{10184:(e,n,t)=>{t.r(n),t.d(n,{assets:()=>p,contentTitle:()=>l,default:()=>u,frontMatter:()=>i,metadata:()=>g,toc:()=>d});var r=t(58168),o=(t(96540),t(15680)),a=t(49595);const i={id:"logging",title:"Logging",sidebar_label:"Logging"},l=void 0,g={unversionedId:"tutorials/basic/running_your_app/logging",id:"version-1.2/tutorials/basic/running_your_app/logging",title:"Logging",description:"People often do not use Python logging due to the setup cost.",source:"@site/versioned_docs/version-1.2/tutorials/basic/running_your_app/4_logging.md",sourceDirName:"tutorials/basic/running_your_app",slug:"/tutorials/basic/running_your_app/logging",permalink:"/docs/1.2/tutorials/basic/running_your_app/logging",draft:!1,editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/versioned_docs/version-1.2/tutorials/basic/running_your_app/4_logging.md",tags:[],version:"1.2",lastUpdatedBy:"jesszzzz",lastUpdatedAt:1744041844,formattedLastUpdatedAt:"Apr 7, 2025",sidebarPosition:4,frontMatter:{id:"logging",title:"Logging",sidebar_label:"Logging"},sidebar:"docs",previous:{title:"Output/Working directory",permalink:"/docs/1.2/tutorials/basic/running_your_app/working_directory"},next:{title:"Debugging",permalink:"/docs/1.2/tutorials/basic/running_your_app/debugging"}},p={},d=[],s={toc:d},m="wrapper";function u(e){let{components:n,...t}=e;return(0,o.mdx)(m,(0,r.A)({},s,t,{components:n,mdxType:"MDXLayout"}),(0,o.mdx)(a.C,{to:"examples/tutorials/basic/running_your_hydra_app/4_logging/my_app.py",mdxType:"ExampleGithubLink"}),(0,o.mdx)("p",null,"People often do not use Python logging due to the setup cost.\nHydra solves this by configuring the Python logging for you."),(0,o.mdx)("p",null,"By default, Hydra logs at the INFO level to both the console and a log file in the automatic working directory."),(0,o.mdx)("p",null,"An example of logging with Hydra:"),(0,o.mdx)("pre",null,(0,o.mdx)("code",{parentName:"pre",className:"language-python"},'import logging\nfrom omegaconf import DictConfig\nimport hydra\n\n# A logger for this file\nlog = logging.getLogger(__name__)\n\n@hydra.main()\ndef my_app(_cfg: DictConfig) -> None:\n    log.info("Info level message")\n    log.debug("Debug level message")\n\nif __name__ == "__main__":\n    my_app()\n\n$ python my_app.py\n[2019-06-27 00:52:46,653][__main__][INFO] - Info level message\n\n')),(0,o.mdx)("p",null,"You can enable DEBUG level logging from the command line  by overriding ",(0,o.mdx)("inlineCode",{parentName:"p"},"hydra.verbose"),"."),(0,o.mdx)("p",null,(0,o.mdx)("inlineCode",{parentName:"p"},"hydra.verbose")," can be a Boolean, a String or a List:"),(0,o.mdx)("p",null,"Examples:"),(0,o.mdx)("ul",null,(0,o.mdx)("li",{parentName:"ul"},(0,o.mdx)("inlineCode",{parentName:"li"},"hydra.verbose=true")," : Sets the log level of ",(0,o.mdx)("strong",{parentName:"li"},"all")," loggers to ",(0,o.mdx)("inlineCode",{parentName:"li"},"DEBUG")),(0,o.mdx)("li",{parentName:"ul"},(0,o.mdx)("inlineCode",{parentName:"li"},"hydra.verbose=NAME")," : Sets the log level of the logger ",(0,o.mdx)("inlineCode",{parentName:"li"},"NAME")," to ",(0,o.mdx)("inlineCode",{parentName:"li"},"DEBUG"),".\nEquivalent to ",(0,o.mdx)("inlineCode",{parentName:"li"},"import logging; logging.getLogger(NAME).setLevel(logging.DEBUG)"),"."),(0,o.mdx)("li",{parentName:"ul"},(0,o.mdx)("inlineCode",{parentName:"li"},"hydra.verbose=[NAME1,NAME2]"),": Sets the log level of the loggers ",(0,o.mdx)("inlineCode",{parentName:"li"},"NAME1")," and ",(0,o.mdx)("inlineCode",{parentName:"li"},"NAME2")," to ",(0,o.mdx)("inlineCode",{parentName:"li"},"DEBUG"))),(0,o.mdx)("p",null,"Example output:"),(0,o.mdx)("pre",null,(0,o.mdx)("code",{parentName:"pre",className:"language-text"},"$ python my_app.py hydra.verbose=[__main__,hydra]\n[2019-09-29 13:06:00,880] - Installed Hydra Plugins\n[2019-09-29 13:06:00,880] - ***********************\n...\n[2019-09-29 13:06:00,896][__main__][INFO] - Info level message\n[2019-09-29 13:06:00,896][__main__][DEBUG] - Debug level message\n")),(0,o.mdx)("p",null,"You can disable the logging output by setting ",(0,o.mdx)("inlineCode",{parentName:"p"},"hydra/job_logging")," to ",(0,o.mdx)("inlineCode",{parentName:"p"},"disabled"),"   "),(0,o.mdx)("pre",null,(0,o.mdx)("code",{parentName:"pre",className:"language-commandline"},"$ python my_app.py hydra/job_logging=disabled\n<NO OUTPUT>\n")),(0,o.mdx)("p",null,"You can also set ",(0,o.mdx)("inlineCode",{parentName:"p"},"hydra/job_logging=none")," and ",(0,o.mdx)("inlineCode",{parentName:"p"},"hydra/hydra_logging=none")," if you do not want Hydra to configure the logging."),(0,o.mdx)("p",null,"Logging can be ",(0,o.mdx)("a",{parentName:"p",href:"/docs/1.2/configure_hydra/logging"},"customized"),"."))}u.isMDXComponent=!0},15680:(e,n,t)=>{t.r(n),t.d(n,{MDXContext:()=>p,MDXProvider:()=>m,mdx:()=>f,useMDXComponents:()=>s,withMDXComponents:()=>d});var r=t(96540);function o(e,n,t){return n in e?Object.defineProperty(e,n,{value:t,enumerable:!0,configurable:!0,writable:!0}):e[n]=t,e}function a(){return a=Object.assign||function(e){for(var n=1;n<arguments.length;n++){var t=arguments[n];for(var r in t)Object.prototype.hasOwnProperty.call(t,r)&&(e[r]=t[r])}return e},a.apply(this,arguments)}function i(e,n){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);n&&(r=r.filter((function(n){return Object.getOwnPropertyDescriptor(e,n).enumerable}))),t.push.apply(t,r)}return t}function l(e){for(var n=1;n<arguments.length;n++){var t=null!=arguments[n]?arguments[n]:{};n%2?i(Object(t),!0).forEach((function(n){o(e,n,t[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):i(Object(t)).forEach((function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(t,n))}))}return e}function g(e,n){if(null==e)return{};var t,r,o=function(e,n){if(null==e)return{};var t,r,o={},a=Object.keys(e);for(r=0;r<a.length;r++)t=a[r],n.indexOf(t)>=0||(o[t]=e[t]);return o}(e,n);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);for(r=0;r<a.length;r++)t=a[r],n.indexOf(t)>=0||Object.prototype.propertyIsEnumerable.call(e,t)&&(o[t]=e[t])}return o}var p=r.createContext({}),d=function(e){return function(n){var t=s(n.components);return r.createElement(e,a({},n,{components:t}))}},s=function(e){var n=r.useContext(p),t=n;return e&&(t="function"==typeof e?e(n):l(l({},n),e)),t},m=function(e){var n=s(e.components);return r.createElement(p.Provider,{value:n},e.children)},u="mdxType",c={inlineCode:"code",wrapper:function(e){var n=e.children;return r.createElement(r.Fragment,{},n)}},y=r.forwardRef((function(e,n){var t=e.components,o=e.mdxType,a=e.originalType,i=e.parentName,p=g(e,["components","mdxType","originalType","parentName"]),d=s(t),m=o,u=d["".concat(i,".").concat(m)]||d[m]||c[m]||a;return t?r.createElement(u,l(l({ref:n},p),{},{components:t})):r.createElement(u,l({ref:n},p))}));function f(e,n){var t=arguments,o=n&&n.mdxType;if("string"==typeof e||o){var a=t.length,i=new Array(a);i[0]=y;var l={};for(var g in n)hasOwnProperty.call(n,g)&&(l[g]=n[g]);l.originalType=e,l[u]="string"==typeof e?e:o,i[1]=l;for(var p=2;p<a;p++)i[p]=t[p];return r.createElement.apply(null,i)}return r.createElement.apply(null,t)}y.displayName="MDXCreateElement"},49595:(e,n,t)=>{t.d(n,{A:()=>p,C:()=>d});var r=t(58168),o=t(96540),a=t(75489),i=t(44586),l=t(48295);function g(e){const n=(0,l.ir)();return(0,i.default)().siteConfig.customFields.githubLinkVersionToBaseUrl[n?.name??"current"]+e}function p(e){return o.createElement(a.default,(0,r.A)({},e,{to:g(e.to),target:"_blank"}))}function d(e){const n=e.text??"Example (Click Here)";return o.createElement(p,e,o.createElement("span",null,"\xa0"),o.createElement("img",{src:"https://img.shields.io/badge/-"+n+"-informational",alt:"Example (Click Here)"}))}}}]);