"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[3226],{15680:(e,n,t)=>{t.r(n),t.d(n,{MDXContext:()=>p,MDXProvider:()=>m,mdx:()=>h,useMDXComponents:()=>u,withMDXComponents:()=>s});var i=t(96540);function a(e,n,t){return n in e?Object.defineProperty(e,n,{value:t,enumerable:!0,configurable:!0,writable:!0}):e[n]=t,e}function l(){return l=Object.assign||function(e){for(var n=1;n<arguments.length;n++){var t=arguments[n];for(var i in t)Object.prototype.hasOwnProperty.call(t,i)&&(e[i]=t[i])}return e},l.apply(this,arguments)}function r(e,n){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);n&&(i=i.filter((function(n){return Object.getOwnPropertyDescriptor(e,n).enumerable}))),t.push.apply(t,i)}return t}function o(e){for(var n=1;n<arguments.length;n++){var t=null!=arguments[n]?arguments[n]:{};n%2?r(Object(t),!0).forEach((function(n){a(e,n,t[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):r(Object(t)).forEach((function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(t,n))}))}return e}function d(e,n){if(null==e)return{};var t,i,a=function(e,n){if(null==e)return{};var t,i,a={},l=Object.keys(e);for(i=0;i<l.length;i++)t=l[i],n.indexOf(t)>=0||(a[t]=e[t]);return a}(e,n);if(Object.getOwnPropertySymbols){var l=Object.getOwnPropertySymbols(e);for(i=0;i<l.length;i++)t=l[i],n.indexOf(t)>=0||Object.prototype.propertyIsEnumerable.call(e,t)&&(a[t]=e[t])}return a}var p=i.createContext({}),s=function(e){return function(n){var t=u(n.components);return i.createElement(e,l({},n,{components:t}))}},u=function(e){var n=i.useContext(p),t=n;return e&&(t="function"==typeof e?e(n):o(o({},n),e)),t},m=function(e){var n=u(e.components);return i.createElement(p.Provider,{value:n},e.children)},c={inlineCode:"code",wrapper:function(e){var n=e.children;return i.createElement(i.Fragment,{},n)}},g=i.forwardRef((function(e,n){var t=e.components,a=e.mdxType,l=e.originalType,r=e.parentName,p=d(e,["components","mdxType","originalType","parentName"]),s=u(t),m=a,g=s["".concat(r,".").concat(m)]||s[m]||c[m]||l;return t?i.createElement(g,o(o({ref:n},p),{},{components:t})):i.createElement(g,o({ref:n},p))}));function h(e,n){var t=arguments,a=n&&n.mdxType;if("string"==typeof e||a){var l=t.length,r=new Array(l);r[0]=g;var o={};for(var d in n)hasOwnProperty.call(n,d)&&(o[d]=n[d]);o.originalType=e,o.mdxType="string"==typeof e?e:a,r[1]=o;for(var p=2;p<l;p++)r[p]=t[p];return i.createElement.apply(null,r)}return i.createElement.apply(null,t)}g.displayName="MDXCreateElement"},49595:(e,n,t)=>{t.d(n,{A:()=>d,C:()=>p});var i=t(58168),a=t(96540),l=t(75489),r=t(44586),o=t(74098);function d(e){return a.createElement(l.default,(0,i.A)({},e,{to:(n=e.to,d=(0,o.useActiveVersion)(),(0,r.default)().siteConfig.customFields.githubLinkVersionToBaseUrl[null!=(t=null==d?void 0:d.name)?t:"current"]+n),target:"_blank"}));var n,t,d}function p(e){var n,t=null!=(n=e.text)?n:"Example (Click Here)";return a.createElement(d,e,a.createElement("span",null,"\xa0"),a.createElement("img",{src:"https://img.shields.io/badge/-"+t+"-informational",alt:"Example (Click Here)"}))}},4179:(e,n,t)=>{t.r(n),t.d(n,{contentTitle:()=>p,default:()=>c,frontMatter:()=>d,metadata:()=>s,toc:()=>u});var i=t(58168),a=t(98587),l=(t(96540),t(15680)),r=t(49595),o=["components"],d={id:"develop",title:"Plugin development",sidebar_label:"Plugin development"},p=void 0,s={unversionedId:"advanced/plugins/develop",id:"advanced/plugins/develop",title:"Plugin development",description:"If you develop plugins, please join the Plugin developer announcement chat channel.",source:"@site/docs/advanced/plugins/develop.md",sourceDirName:"advanced/plugins",slug:"/advanced/plugins/develop",permalink:"/docs/advanced/plugins/develop",editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/docs/advanced/plugins/develop.md",tags:[],version:"current",lastUpdatedBy:"Shicong Huang",lastUpdatedAt:1726517222,formattedLastUpdatedAt:"9/16/2024",frontMatter:{id:"develop",title:"Plugin development",sidebar_label:"Plugin development"},sidebar:"docs",previous:{title:"Plugins Overview",permalink:"/docs/advanced/plugins/overview"},next:{title:"Application packaging",permalink:"/docs/advanced/app_packaging"}},u=[{value:"Automatic Plugin discovery process",id:"automatic-plugin-discovery-process",children:[],level:2},{value:"Plugin registration via the <code>Plugins.register</code> method",id:"plugin-registration-via-the-pluginsregister-method",children:[],level:2},{value:"Getting started",id:"getting-started",children:[],level:2}],m={toc:u};function c(e){var n=e.components,t=(0,a.A)(e,o);return(0,l.mdx)("wrapper",(0,i.A)({},m,t,{components:n,mdxType:"MDXLayout"}),(0,l.mdx)("div",{className:"admonition admonition-info alert alert--info"},(0,l.mdx)("div",{parentName:"div",className:"admonition-heading"},(0,l.mdx)("h5",{parentName:"div"},(0,l.mdx)("span",{parentName:"h5",className:"admonition-icon"},(0,l.mdx)("svg",{parentName:"span",xmlns:"http://www.w3.org/2000/svg",width:"14",height:"16",viewBox:"0 0 14 16"},(0,l.mdx)("path",{parentName:"svg",fillRule:"evenodd",d:"M7 2.3c3.14 0 5.7 2.56 5.7 5.7s-2.56 5.7-5.7 5.7A5.71 5.71 0 0 1 1.3 8c0-3.14 2.56-5.7 5.7-5.7zM7 1C3.14 1 0 4.14 0 8s3.14 7 7 7 7-3.14 7-7-3.14-7-7-7zm1 3H6v5h2V4zm0 6H6v2h2v-2z"}))),"info")),(0,l.mdx)("div",{parentName:"div",className:"admonition-content"},(0,l.mdx)("p",{parentName:"div"},"If you develop plugins, please join the ",(0,l.mdx)("a",{href:"https://hydra-framework.zulipchat.com/#narrow/stream/233935-Hydra-plugin.20dev.20announcements"},"Plugin developer announcement chat channel"),"."))),(0,l.mdx)("p",null,"Hydra plugins must be registered before they can be used. There are two ways to register a plugin:"),(0,l.mdx)("ul",null,(0,l.mdx)("li",{parentName:"ul"},"via the automatic plugin discovery process, which discovers plugins located in the ",(0,l.mdx)("inlineCode",{parentName:"li"},"hydra_plugins")," namespace package"),(0,l.mdx)("li",{parentName:"ul"},"by calling the ",(0,l.mdx)("inlineCode",{parentName:"li"},"register")," method on Hydra's ",(0,l.mdx)("inlineCode",{parentName:"li"},"Plugins")," singleton class")),(0,l.mdx)("h2",{id:"automatic-plugin-discovery-process"},"Automatic Plugin discovery process"),(0,l.mdx)("p",null,"If you create a Plugin and want it to be discovered automatically by Hydra, keep the following things in mind:"),(0,l.mdx)("ul",null,(0,l.mdx)("li",{parentName:"ul"},"Hydra plugins can be either a standalone Python package, or a part of your existing Python package.\nIn both cases - They should be in the namespace module ",(0,l.mdx)("inlineCode",{parentName:"li"},"hydra_plugins")," (This is a top level module, Your plugin will ",(0,l.mdx)("strong",{parentName:"li"},"NOT")," be discovered if you place it in ",(0,l.mdx)("inlineCode",{parentName:"li"},"mylib.hydra_plugins"),")."),(0,l.mdx)("li",{parentName:"ul"},"Do ",(0,l.mdx)("strong",{parentName:"li"},"NOT")," place an ",(0,l.mdx)("inlineCode",{parentName:"li"},"__init__.py")," file in ",(0,l.mdx)("inlineCode",{parentName:"li"},"hydra_plugins")," (doing so may break other installed Hydra plugins).")),(0,l.mdx)("p",null,"The plugin discovery process runs whenever Hydra starts. During plugin discovery, Hydra scans for plugins in all the submodules of ",(0,l.mdx)("inlineCode",{parentName:"p"},"hydra_plugins"),". Hydra will import each module and look for plugins defined in that module.\nAny module under ",(0,l.mdx)("inlineCode",{parentName:"p"},"hydra_plugins")," that is slow to import will slow down the startup of ",(0,l.mdx)("strong",{parentName:"p"},"ALL")," Hydra applications.\nPlugins with expensive imports can exclude individual files from Hydra's plugin discovery process by prefixing them with ",(0,l.mdx)("inlineCode",{parentName:"p"},"_")," (but not ",(0,l.mdx)("inlineCode",{parentName:"p"},"__"),").\nFor example, the file ",(0,l.mdx)("inlineCode",{parentName:"p"},"_my_plugin_lib.py")," would not be imported and scanned, while ",(0,l.mdx)("inlineCode",{parentName:"p"},"my_plugin_lib.py")," would be."),(0,l.mdx)("h2",{id:"plugin-registration-via-the-pluginsregister-method"},"Plugin registration via the ",(0,l.mdx)("inlineCode",{parentName:"h2"},"Plugins.register")," method"),(0,l.mdx)("p",null,"Plugins can be manually registered by calling the ",(0,l.mdx)("inlineCode",{parentName:"p"},"register")," method on the instance of Hydra's ",(0,l.mdx)("inlineCode",{parentName:"p"},"Plugins")," singleton class."),(0,l.mdx)("pre",null,(0,l.mdx)("code",{parentName:"pre",className:"language-python"},'from hydra.core.plugins import Plugins\nfrom hydra.plugins.plugin import Plugin\n\nclass MyPlugin(Plugin):\n  ...\n\ndef register_my_plugin() -> None:\n    """Hydra users should call this function before invoking @hydra.main"""\n    Plugins.instance().register(MyPlugin)\n')),(0,l.mdx)("h2",{id:"getting-started"},"Getting started"),(0,l.mdx)("p",null,"The best way to get started developing a Hydra plugin is to base your new plugin on one of the example plugins:"),(0,l.mdx)("ul",null,(0,l.mdx)("li",{parentName:"ul"},"Copy the subtree of the relevant ",(0,l.mdx)(r.A,{to:"examples/plugins",mdxType:"GithubLink"},"example plugin")," into a standalone project."),(0,l.mdx)("li",{parentName:"ul"},"Edit ",(0,l.mdx)("inlineCode",{parentName:"li"},"setup.py"),", rename the plugin module, for example from ",(0,l.mdx)("inlineCode",{parentName:"li"},"hydra_plugins.example_xyz_plugin")," to ",(0,l.mdx)("inlineCode",{parentName:"li"},"hydra_plugins.my_xyz_plugin"),"."),(0,l.mdx)("li",{parentName:"ul"},"Install the new plugin (Run this in the plugin directory: ",(0,l.mdx)("inlineCode",{parentName:"li"},"pip install -e ."),")"),(0,l.mdx)("li",{parentName:"ul"},"Run the included example app and make sure that the plugin is discovered:")),(0,l.mdx)("pre",null,(0,l.mdx)("code",{parentName:"pre",className:"language-shell"},"$ python example/my_app.py --info plugins\nInstalled Hydra Plugins\n***********************\n        ...\n        Launcher:\n        ---------\n                MyLauncher\n        ...\n")),(0,l.mdx)("ul",null,(0,l.mdx)("li",{parentName:"ul"},"Run the example application to see that that your plugin is doing something."),(0,l.mdx)("li",{parentName:"ul"},(0,l.mdx)("em",{parentName:"li"},"[Optional]")," If you want the plugin be embedded in your existing application/library, move the ",(0,l.mdx)("inlineCode",{parentName:"li"},"hydra_plugins")," directory\nand make sure that it's included as a namespace module in your final Python package. See the ",(0,l.mdx)("inlineCode",{parentName:"li"},"setup.py"),"\nfile included with the example plugin for hints (typically this involves using ",(0,l.mdx)("inlineCode",{parentName:"li"},'find_namespace_packages(include=["hydra_plugins.*"])'),")."),(0,l.mdx)("li",{parentName:"ul"},"Hack on your plugin, Ensure that the recommended tests and any tests you want to add are passing.")))}c.isMDXComponent=!0}}]);