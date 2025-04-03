"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[1646],{15680:(e,n,a)=>{a.r(n),a.d(n,{MDXContext:()=>m,MDXProvider:()=>p,mdx:()=>h,useMDXComponents:()=>c,withMDXComponents:()=>s});var r=a(96540);function t(e,n,a){return n in e?Object.defineProperty(e,n,{value:a,enumerable:!0,configurable:!0,writable:!0}):e[n]=a,e}function i(){return i=Object.assign||function(e){for(var n=1;n<arguments.length;n++){var a=arguments[n];for(var r in a)Object.prototype.hasOwnProperty.call(a,r)&&(e[r]=a[r])}return e},i.apply(this,arguments)}function o(e,n){var a=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);n&&(r=r.filter((function(n){return Object.getOwnPropertyDescriptor(e,n).enumerable}))),a.push.apply(a,r)}return a}function l(e){for(var n=1;n<arguments.length;n++){var a=null!=arguments[n]?arguments[n]:{};n%2?o(Object(a),!0).forEach((function(n){t(e,n,a[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(a)):o(Object(a)).forEach((function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(a,n))}))}return e}function d(e,n){if(null==e)return{};var a,r,t=function(e,n){if(null==e)return{};var a,r,t={},i=Object.keys(e);for(r=0;r<i.length;r++)a=i[r],n.indexOf(a)>=0||(t[a]=e[a]);return t}(e,n);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);for(r=0;r<i.length;r++)a=i[r],n.indexOf(a)>=0||Object.prototype.propertyIsEnumerable.call(e,a)&&(t[a]=e[a])}return t}var m=r.createContext({}),s=function(e){return function(n){var a=c(n.components);return r.createElement(e,i({},n,{components:a}))}},c=function(e){var n=r.useContext(m),a=n;return e&&(a="function"==typeof e?e(n):l(l({},n),e)),a},p=function(e){var n=c(e.components);return r.createElement(m.Provider,{value:n},e.children)},u="mdxType",f={inlineCode:"code",wrapper:function(e){var n=e.children;return r.createElement(r.Fragment,{},n)}},g=r.forwardRef((function(e,n){var a=e.components,t=e.mdxType,i=e.originalType,o=e.parentName,m=d(e,["components","mdxType","originalType","parentName"]),s=c(a),p=t,u=s["".concat(o,".").concat(p)]||s[p]||f[p]||i;return a?r.createElement(u,l(l({ref:n},m),{},{components:a})):r.createElement(u,l({ref:n},m))}));function h(e,n){var a=arguments,t=n&&n.mdxType;if("string"==typeof e||t){var i=a.length,o=new Array(i);o[0]=g;var l={};for(var d in n)hasOwnProperty.call(n,d)&&(l[d]=n[d]);l.originalType=e,l[u]="string"==typeof e?e:t,o[1]=l;for(var m=2;m<i;m++)o[m]=a[m];return r.createElement.apply(null,o)}return r.createElement.apply(null,a)}g.displayName="MDXCreateElement"},80374:(e,n,a)=>{a.r(n),a.d(n,{assets:()=>d,contentTitle:()=>o,default:()=>p,frontMatter:()=>i,metadata:()=>l,toc:()=>m});var r=a(58168),t=(a(96540),a(15680));const i={id:"hydra-command-line-flags",title:"Hydra's command line flags"},o=void 0,l={unversionedId:"advanced/hydra-command-line-flags",id:"version-1.3/advanced/hydra-command-line-flags",title:"Hydra's command line flags",description:"Hydra is using the command line for two things:",source:"@site/versioned_docs/version-1.3/advanced/hydra-command-line-flags.md",sourceDirName:"advanced",slug:"/advanced/hydra-command-line-flags",permalink:"/docs/1.3/advanced/hydra-command-line-flags",draft:!1,editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/versioned_docs/version-1.3/advanced/hydra-command-line-flags.md",tags:[],version:"1.3",lastUpdatedBy:"dependabot[bot]",lastUpdatedAt:1743717584,formattedLastUpdatedAt:"Apr 3, 2025",frontMatter:{id:"hydra-command-line-flags",title:"Hydra's command line flags"},sidebar:"docs",previous:{title:"Terminology",permalink:"/docs/1.3/advanced/terminology"},next:{title:"Basic Override syntax",permalink:"/docs/1.3/advanced/override_grammar/basic"}},d={},m=[],s={toc:m},c="wrapper";function p(e){let{components:n,...a}=e;return(0,t.mdx)(c,(0,r.A)({},s,a,{components:n,mdxType:"MDXLayout"}),(0,t.mdx)("p",null,"Hydra is using the command line for two things:"),(0,t.mdx)("ul",null,(0,t.mdx)("li",{parentName:"ul"},"Controlling Hydra"),(0,t.mdx)("li",{parentName:"ul"},"Configuring your application (See ",(0,t.mdx)("a",{parentName:"li",href:"/docs/1.3/advanced/override_grammar/basic"},"Override Grammar"),")")),(0,t.mdx)("p",null,"Arguments prefixed by - or -- control Hydra; the rest are used to configure the application."),(0,t.mdx)("p",null,"Information about Hydra:"),(0,t.mdx)("ul",null,(0,t.mdx)("li",{parentName:"ul"},(0,t.mdx)("strong",{parentName:"li"},"--hydra-help"),": Shows Hydra specific flags"),(0,t.mdx)("li",{parentName:"ul"},(0,t.mdx)("strong",{parentName:"li"},"--version"),": Show Hydra's version and exit")),(0,t.mdx)("p",null,"Information provided by the Hydra app:"),(0,t.mdx)("ul",null,(0,t.mdx)("li",{parentName:"ul"},(0,t.mdx)("strong",{parentName:"li"},"--help,-h"),": Shows the application's help. This can be ",(0,t.mdx)("a",{parentName:"li",href:"/docs/1.3/configure_hydra/app_help"},"customized"),".")),(0,t.mdx)("p",null,"Debugging assistance:"),(0,t.mdx)("ul",null,(0,t.mdx)("li",{parentName:"ul"},(0,t.mdx)("strong",{parentName:"li"},"--cfg,-c"),": Show config instead of running. Takes as parameter one of ",(0,t.mdx)("inlineCode",{parentName:"li"},"job"),", ",(0,t.mdx)("inlineCode",{parentName:"li"},"hydra")," or ",(0,t.mdx)("inlineCode",{parentName:"li"},"all"),"."),(0,t.mdx)("li",{parentName:"ul"},(0,t.mdx)("strong",{parentName:"li"},"--resolve"),": Used in conjunction with the ",(0,t.mdx)("inlineCode",{parentName:"li"},"--cfg")," flag; resolve interpolations in the config before printing it."),(0,t.mdx)("li",{parentName:"ul"},(0,t.mdx)("strong",{parentName:"li"},"--package,-p"),": Used in conjunction with --cfg to select a specific config package to show."),(0,t.mdx)("li",{parentName:"ul"},(0,t.mdx)("strong",{parentName:"li"},"--info,-i"),": Print Hydra information. This includes installed plugins, Config Search Path, Defaults List, generated config and more.")),(0,t.mdx)("p",null,"Running Hydra applications:"),(0,t.mdx)("ul",null,(0,t.mdx)("li",{parentName:"ul"},(0,t.mdx)("strong",{parentName:"li"},"--run,-r"),": Run is the default mode and is not normally needed."),(0,t.mdx)("li",{parentName:"ul"},(0,t.mdx)("strong",{parentName:"li"},"--multirun,-m"),": Run multiple jobs with the configured launcher and sweeper. See ",(0,t.mdx)("a",{parentName:"li",href:"/docs/1.3/tutorials/basic/running_your_app/multi-run"},"Multi-run"),".",(0,t.mdx)("br",null),(0,t.mdx)("br",null)),(0,t.mdx)("li",{parentName:"ul"},(0,t.mdx)("strong",{parentName:"li"},"--config-path,-cp"),": Overrides the ",(0,t.mdx)("inlineCode",{parentName:"li"},"config_path")," specified in ",(0,t.mdx)("inlineCode",{parentName:"li"},"hydra.main()"),". The ",(0,t.mdx)("inlineCode",{parentName:"li"},"config_path")," is absolute or relative to the Python file declaring ",(0,t.mdx)("inlineCode",{parentName:"li"},"@hydra.main()"),"."),(0,t.mdx)("li",{parentName:"ul"},(0,t.mdx)("strong",{parentName:"li"},"--config-name,-cn"),": Overrides the ",(0,t.mdx)("inlineCode",{parentName:"li"},"config_name")," specified in ",(0,t.mdx)("inlineCode",{parentName:"li"},"hydra.main()"),"."),(0,t.mdx)("li",{parentName:"ul"},(0,t.mdx)("strong",{parentName:"li"},"--config-dir,-cd"),": Adds an additional config directory to the ",(0,t.mdx)("a",{parentName:"li",href:"/docs/1.3/advanced/search_path"},"config search path"),".",(0,t.mdx)("br",{parentName:"li"}),"This is useful for installed apps that want to allow their users to provide additional configs.")),(0,t.mdx)("p",null,"Misc:"),(0,t.mdx)("ul",null,(0,t.mdx)("li",{parentName:"ul"},(0,t.mdx)("strong",{parentName:"li"},"--shell-completion,-sc"),": Install or Uninstall ",(0,t.mdx)("a",{parentName:"li",href:"/docs/1.3/tutorials/basic/running_your_app/tab_completion"},"shell tab completion"),".")))}p.isMDXComponent=!0}}]);