"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[195],{15680:(e,n,r)=>{r.r(n),r.d(n,{MDXContext:()=>s,MDXProvider:()=>u,mdx:()=>y,useMDXComponents:()=>d,withMDXComponents:()=>c});var t=r(96540);function o(e,n,r){return n in e?Object.defineProperty(e,n,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[n]=r,e}function a(){return a=Object.assign||function(e){for(var n=1;n<arguments.length;n++){var r=arguments[n];for(var t in r)Object.prototype.hasOwnProperty.call(r,t)&&(e[t]=r[t])}return e},a.apply(this,arguments)}function i(e,n){var r=Object.keys(e);if(Object.getOwnPropertySymbols){var t=Object.getOwnPropertySymbols(e);n&&(t=t.filter((function(n){return Object.getOwnPropertyDescriptor(e,n).enumerable}))),r.push.apply(r,t)}return r}function p(e){for(var n=1;n<arguments.length;n++){var r=null!=arguments[n]?arguments[n]:{};n%2?i(Object(r),!0).forEach((function(n){o(e,n,r[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(r)):i(Object(r)).forEach((function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(r,n))}))}return e}function l(e,n){if(null==e)return{};var r,t,o=function(e,n){if(null==e)return{};var r,t,o={},a=Object.keys(e);for(t=0;t<a.length;t++)r=a[t],n.indexOf(r)>=0||(o[r]=e[r]);return o}(e,n);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);for(t=0;t<a.length;t++)r=a[t],n.indexOf(r)>=0||Object.prototype.propertyIsEnumerable.call(e,r)&&(o[r]=e[r])}return o}var s=t.createContext({}),c=function(e){return function(n){var r=d(n.components);return t.createElement(e,a({},n,{components:r}))}},d=function(e){var n=t.useContext(s),r=n;return e&&(r="function"==typeof e?e(n):p(p({},n),e)),r},u=function(e){var n=d(e.components);return t.createElement(s.Provider,{value:n},e.children)},m="mdxType",f={inlineCode:"code",wrapper:function(e){var n=e.children;return t.createElement(t.Fragment,{},n)}},h=t.forwardRef((function(e,n){var r=e.components,o=e.mdxType,a=e.originalType,i=e.parentName,s=l(e,["components","mdxType","originalType","parentName"]),c=d(r),u=o,m=c["".concat(i,".").concat(u)]||c[u]||f[u]||a;return r?t.createElement(m,p(p({ref:n},s),{},{components:r})):t.createElement(m,p({ref:n},s))}));function y(e,n){var r=arguments,o=n&&n.mdxType;if("string"==typeof e||o){var a=r.length,i=new Array(a);i[0]=h;var p={};for(var l in n)hasOwnProperty.call(n,l)&&(p[l]=n[l]);p.originalType=e,p[m]="string"==typeof e?e:o,i[1]=p;for(var s=2;s<a;s++)i[s]=r[s];return t.createElement.apply(null,i)}return t.createElement.apply(null,r)}h.displayName="MDXCreateElement"},82743:(e,n,r)=>{r.r(n),r.d(n,{assets:()=>l,contentTitle:()=>i,default:()=>u,frontMatter:()=>a,metadata:()=>p,toc:()=>s});var t=r(58168),o=(r(96540),r(15680));const a={id:"app_help",title:"Customizing Application's help",sidebar_label:"Customizing Application's help"},i=void 0,p={unversionedId:"configure_hydra/app_help",id:"version-0.11/configure_hydra/app_help",title:"Customizing Application's help",description:"Hydra provides two different help options:",source:"@site/versioned_docs/version-0.11/configure_hydra/app_help.md",sourceDirName:"configure_hydra",slug:"/configure_hydra/app_help",permalink:"/docs/0.11/configure_hydra/app_help",draft:!1,editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/versioned_docs/version-0.11/configure_hydra/app_help.md",tags:[],version:"0.11",lastUpdatedBy:"jesszzzz",lastUpdatedAt:1744041844,formattedLastUpdatedAt:"Apr 7, 2025",frontMatter:{id:"app_help",title:"Customizing Application's help",sidebar_label:"Customizing Application's help"},sidebar:"docs",previous:{title:"Customizing working directory pattern",permalink:"/docs/0.11/configure_hydra/workdir"},next:{title:"Colorlog plugin",permalink:"/docs/0.11/plugins/colorlog"}},l={},s=[],c={toc:s},d="wrapper";function u(e){let{components:n,...r}=e;return(0,o.mdx)(d,(0,t.A)({},c,r,{components:n,mdxType:"MDXLayout"}),(0,o.mdx)("p",null,"Hydra provides two different help options:"),(0,o.mdx)("ul",null,(0,o.mdx)("li",{parentName:"ul"},(0,o.mdx)("inlineCode",{parentName:"li"},"--help")," : Application specific help"),(0,o.mdx)("li",{parentName:"ul"},(0,o.mdx)("inlineCode",{parentName:"li"},"--hydra-help")," Hydra specific help. ")),(0,o.mdx)("p",null,"Example output of ",(0,o.mdx)("inlineCode",{parentName:"p"},"--help"),":"),(0,o.mdx)("pre",null,(0,o.mdx)("code",{parentName:"pre",className:"language-text"},"$ python my_app.py --help\nmy_app is powered by Hydra.\n\n== Configuration groups ==\nCompose your configuration from those groups (group=option)\n\ndb: mysql, postgresql\n\n\n== Config ==\nOverride anything in the config (foo.bar=value)\n\ndb:\n  driver: mysql\n  pass: secret\n  user: omry\n\n\nPowered by Hydra (https://hydra.cc)\nUse --hydra-help to view Hydra specific help\n")),(0,o.mdx)("p",null,"This output is generated from the following default configuration.\nYou can override the individual components like ",(0,o.mdx)("inlineCode",{parentName:"p"},"hydra.help.app_name")," or the whole template. "),(0,o.mdx)("pre",null,(0,o.mdx)("code",{parentName:"pre",className:"language-yaml"},"hydra:\n  help:\n    # App name, override to match the name your app is known by\n    app_name: ${hydra.job.name}\n\n    # Help header, customize to describe your app to your users\n    header: |\n      ${hydra.help.app_name} is powered by Hydra.\n\n    footer: |\n      Powered by Hydra (https://hydra.cc)\n      Use --hydra-help to view Hydra specific help\n\n    # Basic Hydra flags:\n    #   $FLAGS_HELP\n    #\n    # Config groups, choose one of:\n    #   $APP_CONFIG_GROUPS: All config groups that does not start with hydra/.\n    #   $HYDRA_CONFIG_GROUPS: All the Hydra config groups (starts with hydra/)\n    #\n    # Configuration generated with overrides:\n    #   $CONFIG : Generated config\n    #\n    template: |\n      ${hydra.help.header}\n      == Configuration groups ==\n      Compose your configuration from those groups (group=option)\n\n      $APP_CONFIG_GROUPS\n\n      == Config ==\n      Override anything in the config (foo.bar=value)\n\n      $CONFIG\n\n      ${hydra.help.footer}\n")))}u.isMDXComponent=!0}}]);