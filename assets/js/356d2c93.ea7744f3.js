"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[1572],{15680:(e,n,t)=>{t.r(n),t.d(n,{MDXContext:()=>d,MDXProvider:()=>m,mdx:()=>h,useMDXComponents:()=>u,withMDXComponents:()=>s});var i=t(96540);function a(e,n,t){return n in e?Object.defineProperty(e,n,{value:t,enumerable:!0,configurable:!0,writable:!0}):e[n]=t,e}function r(){return r=Object.assign||function(e){for(var n=1;n<arguments.length;n++){var t=arguments[n];for(var i in t)Object.prototype.hasOwnProperty.call(t,i)&&(e[i]=t[i])}return e},r.apply(this,arguments)}function l(e,n){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);n&&(i=i.filter((function(n){return Object.getOwnPropertyDescriptor(e,n).enumerable}))),t.push.apply(t,i)}return t}function o(e){for(var n=1;n<arguments.length;n++){var t=null!=arguments[n]?arguments[n]:{};n%2?l(Object(t),!0).forEach((function(n){a(e,n,t[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):l(Object(t)).forEach((function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(t,n))}))}return e}function p(e,n){if(null==e)return{};var t,i,a=function(e,n){if(null==e)return{};var t,i,a={},r=Object.keys(e);for(i=0;i<r.length;i++)t=r[i],n.indexOf(t)>=0||(a[t]=e[t]);return a}(e,n);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);for(i=0;i<r.length;i++)t=r[i],n.indexOf(t)>=0||Object.prototype.propertyIsEnumerable.call(e,t)&&(a[t]=e[t])}return a}var d=i.createContext({}),s=function(e){return function(n){var t=u(n.components);return i.createElement(e,r({},n,{components:t}))}},u=function(e){var n=i.useContext(d),t=n;return e&&(t="function"==typeof e?e(n):o(o({},n),e)),t},m=function(e){var n=u(e.components);return i.createElement(d.Provider,{value:n},e.children)},c="mdxType",g={inlineCode:"code",wrapper:function(e){var n=e.children;return i.createElement(i.Fragment,{},n)}},y=i.forwardRef((function(e,n){var t=e.components,a=e.mdxType,r=e.originalType,l=e.parentName,d=p(e,["components","mdxType","originalType","parentName"]),s=u(t),m=a,c=s["".concat(l,".").concat(m)]||s[m]||g[m]||r;return t?i.createElement(c,o(o({ref:n},d),{},{components:t})):i.createElement(c,o({ref:n},d))}));function h(e,n){var t=arguments,a=n&&n.mdxType;if("string"==typeof e||a){var r=t.length,l=new Array(r);l[0]=y;var o={};for(var p in n)hasOwnProperty.call(n,p)&&(o[p]=n[p]);o.originalType=e,o[c]="string"==typeof e?e:a,l[1]=o;for(var d=2;d<r;d++)l[d]=t[d];return i.createElement.apply(null,l)}return i.createElement.apply(null,t)}y.displayName="MDXCreateElement"},49595:(e,n,t)=>{t.d(n,{A:()=>d,C:()=>s});var i=t(58168),a=t(96540),r=t(75489),l=t(44586),o=t(48295);function p(e){const n=(0,o.ir)();return(0,l.default)().siteConfig.customFields.githubLinkVersionToBaseUrl[n?.name??"current"]+e}function d(e){return a.createElement(r.default,(0,i.A)({},e,{to:p(e.to),target:"_blank"}))}function s(e){const n=e.text??"Example (Click Here)";return a.createElement(d,e,a.createElement("span",null,"\xa0"),a.createElement("img",{src:"https://img.shields.io/badge/-"+n+"-informational",alt:"Example (Click Here)"}))}},86629:(e,n,t)=>{t.r(n),t.d(n,{assets:()=>d,contentTitle:()=>o,default:()=>c,frontMatter:()=>l,metadata:()=>p,toc:()=>s});var i=t(58168),a=(t(96540),t(15680)),r=t(49595);const l={id:"develop",title:"Plugin development",sidebar_label:"Plugin development"},o=void 0,p={unversionedId:"advanced/plugins/develop",id:"version-1.1/advanced/plugins/develop",title:"Plugin development",description:"If you develop plugins, please join the Plugin developer announcement chat channel.",source:"@site/versioned_docs/version-1.1/advanced/plugins/develop.md",sourceDirName:"advanced/plugins",slug:"/advanced/plugins/develop",permalink:"/docs/1.1/advanced/plugins/develop",draft:!1,editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/versioned_docs/version-1.1/advanced/plugins/develop.md",tags:[],version:"1.1",lastUpdatedBy:"jesszzzz",lastUpdatedAt:1743461536,formattedLastUpdatedAt:"Mar 31, 2025",frontMatter:{id:"develop",title:"Plugin development",sidebar_label:"Plugin development"},sidebar:"docs",previous:{title:"Plugins Overview",permalink:"/docs/1.1/advanced/plugins/overview"},next:{title:"Application packaging",permalink:"/docs/1.1/advanced/app_packaging"}},d={},s=[{value:"Plugin discovery process",id:"plugin-discovery-process",level:2},{value:"Getting started",id:"getting-started",level:2}],u={toc:s},m="wrapper";function c(e){let{components:n,...t}=e;return(0,a.mdx)(m,(0,i.A)({},u,t,{components:n,mdxType:"MDXLayout"}),(0,a.mdx)("admonition",{type:"info"},(0,a.mdx)("p",{parentName:"admonition"},"If you develop plugins, please join the ",(0,a.mdx)("a",{href:"https://hydra-framework.zulipchat.com/#narrow/stream/233935-Hydra-plugin.20dev.20announcements"},"Plugin developer announcement chat channel"),".")),(0,a.mdx)("p",null,"When developing Hydra plugins, keep the following things in mind:"),(0,a.mdx)("ul",null,(0,a.mdx)("li",{parentName:"ul"},"Hydra plugins can be either a standalone Python package, or a part of your existing Python package.\nIn both cases - They should be in the namespace module ",(0,a.mdx)("inlineCode",{parentName:"li"},"hydra_plugins")," (This is a top level module, Your plugin will ",(0,a.mdx)("strong",{parentName:"li"},"NOT")," be discovered if you place it in ",(0,a.mdx)("inlineCode",{parentName:"li"},"mylib.hydra_plugins"),")."),(0,a.mdx)("li",{parentName:"ul"},"Do ",(0,a.mdx)("strong",{parentName:"li"},"NOT")," place an ",(0,a.mdx)("inlineCode",{parentName:"li"},"__init__.py")," file in ",(0,a.mdx)("inlineCode",{parentName:"li"},"hydra_plugins")," (doing so may break other installed Hydra plugins).")),(0,a.mdx)("h2",{id:"plugin-discovery-process"},"Plugin discovery process"),(0,a.mdx)("p",null,"The plugin discovery process runs whenever Hydra starts. During plugin discovery, Hydra scans for plugins in all the submodules of ",(0,a.mdx)("inlineCode",{parentName:"p"},"hydra_plugins"),". Hydra will import each module and look for plugins defined in that module.\nAny module under ",(0,a.mdx)("inlineCode",{parentName:"p"},"hydra_plugins")," that is slow to import will slow down the startup of ",(0,a.mdx)("strong",{parentName:"p"},"ALL")," Hydra applications.\nPlugins with expensive imports can exclude individual files from Hydra's plugin discovery process by prefixing them with ",(0,a.mdx)("inlineCode",{parentName:"p"},"_")," (but not ",(0,a.mdx)("inlineCode",{parentName:"p"},"__"),").\nFor example, the file ",(0,a.mdx)("inlineCode",{parentName:"p"},"_my_plugin_lib.py")," would not be imported and scanned, while ",(0,a.mdx)("inlineCode",{parentName:"p"},"my_plugin_lib.py")," would be."),(0,a.mdx)("h2",{id:"getting-started"},"Getting started"),(0,a.mdx)("p",null,"The best way to get started developing a Hydra plugin is to base your new plugin on one of the example plugins:"),(0,a.mdx)("ul",null,(0,a.mdx)("li",{parentName:"ul"},"Copy the subtree of the relevant ",(0,a.mdx)(r.A,{to:"examples/plugins",mdxType:"GithubLink"},"example plugin")," into a standalone project."),(0,a.mdx)("li",{parentName:"ul"},"Edit ",(0,a.mdx)("inlineCode",{parentName:"li"},"setup.py"),", rename the plugin module, for example from ",(0,a.mdx)("inlineCode",{parentName:"li"},"hydra_plugins.example_xyz_plugin")," to ",(0,a.mdx)("inlineCode",{parentName:"li"},"hydra_plugins.my_xyz_plugin"),"."),(0,a.mdx)("li",{parentName:"ul"},"Install the new plugin (Run this in the plugin directory: ",(0,a.mdx)("inlineCode",{parentName:"li"},"pip install -e ."),")"),(0,a.mdx)("li",{parentName:"ul"},"Run the included example app and make sure that the plugin is discovered:")),(0,a.mdx)("pre",null,(0,a.mdx)("code",{parentName:"pre",className:"language-shell"},"$ python example/my_app.py --info plugins\nInstalled Hydra Plugins\n***********************\n        ...\n        Launcher:\n        ---------\n                MyLauncher\n        ...\n")),(0,a.mdx)("ul",null,(0,a.mdx)("li",{parentName:"ul"},"Run the example application to see that that your plugin is doing something."),(0,a.mdx)("li",{parentName:"ul"},(0,a.mdx)("em",{parentName:"li"},"[Optional]")," If you want the plugin be embedded in your existing application/library, move the ",(0,a.mdx)("inlineCode",{parentName:"li"},"hydra_plugins")," directory\nand make sure that it's included as a namespace module in your final Python package. See the ",(0,a.mdx)("inlineCode",{parentName:"li"},"setup.py"),"\nfile included with the example plugin for hints (typically this involves using ",(0,a.mdx)("inlineCode",{parentName:"li"},'find_namespace_packages(include=["hydra_plugins.*"])'),")."),(0,a.mdx)("li",{parentName:"ul"},"Hack on your plugin, Ensure that the recommended tests and any tests you want to add are passing.")))}c.isMDXComponent=!0}}]);