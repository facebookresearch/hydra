"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[717],{15680:(e,t,n)=>{n.r(t),n.d(t,{MDXContext:()=>c,MDXProvider:()=>p,mdx:()=>h,useMDXComponents:()=>m,withMDXComponents:()=>s});var r=n(96540);function i(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function a(){return a=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var r in n)Object.prototype.hasOwnProperty.call(n,r)&&(e[r]=n[r])}return e},a.apply(this,arguments)}function o(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,r)}return n}function d(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?o(Object(n),!0).forEach((function(t){i(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):o(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function l(e,t){if(null==e)return{};var n,r,i=function(e,t){if(null==e)return{};var n,r,i={},a=Object.keys(e);for(r=0;r<a.length;r++)n=a[r],t.indexOf(n)>=0||(i[n]=e[n]);return i}(e,t);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);for(r=0;r<a.length;r++)n=a[r],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(i[n]=e[n])}return i}var c=r.createContext({}),s=function(e){return function(t){var n=m(t.components);return r.createElement(e,a({},t,{components:n}))}},m=function(e){var t=r.useContext(c),n=t;return e&&(n="function"==typeof e?e(t):d(d({},t),e)),n},p=function(e){var t=m(e.components);return r.createElement(c.Provider,{value:t},e.children)},f="mdxType",u={inlineCode:"code",wrapper:function(e){var t=e.children;return r.createElement(r.Fragment,{},t)}},g=r.forwardRef((function(e,t){var n=e.components,i=e.mdxType,a=e.originalType,o=e.parentName,c=l(e,["components","mdxType","originalType","parentName"]),s=m(n),p=i,f=s["".concat(o,".").concat(p)]||s[p]||u[p]||a;return n?r.createElement(f,d(d({ref:t},c),{},{components:n})):r.createElement(f,d({ref:t},c))}));function h(e,t){var n=arguments,i=t&&t.mdxType;if("string"==typeof e||i){var a=n.length,o=new Array(a);o[0]=g;var d={};for(var l in t)hasOwnProperty.call(t,l)&&(d[l]=t[l]);d.originalType=e,d[f]="string"==typeof e?e:i,o[1]=d;for(var c=2;c<a;c++)o[c]=n[c];return r.createElement.apply(null,o)}return r.createElement.apply(null,n)}g.displayName="MDXCreateElement"},72278:(e,t,n)=>{n.r(t),n.d(t,{assets:()=>l,contentTitle:()=>o,default:()=>p,frontMatter:()=>a,metadata:()=>d,toc:()=>c});var r=n(58168),i=(n(96540),n(15680));const a={id:"strict_mode_flag_deprecated",title:"strict flag mode deprecation",hide_title:!0},o=void 0,d={unversionedId:"upgrades/0.11_to_1.0/strict_mode_flag_deprecated",id:"version-1.2/upgrades/0.11_to_1.0/strict_mode_flag_deprecated",title:"strict flag mode deprecation",description:"strict flag mode deprecation",source:"@site/versioned_docs/version-1.2/upgrades/0.11_to_1.0/strict_mode_flag_deprecated.md",sourceDirName:"upgrades/0.11_to_1.0",slug:"/upgrades/0.11_to_1.0/strict_mode_flag_deprecated",permalink:"/docs/1.2/upgrades/0.11_to_1.0/strict_mode_flag_deprecated",draft:!1,editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/versioned_docs/version-1.2/upgrades/0.11_to_1.0/strict_mode_flag_deprecated.md",tags:[],version:"1.2",lastUpdatedBy:"jesszzzz",lastUpdatedAt:1741383139,formattedLastUpdatedAt:"Mar 7, 2025",frontMatter:{id:"strict_mode_flag_deprecated",title:"strict flag mode deprecation",hide_title:!0},sidebar:"docs",previous:{title:"Adding an @package directive",permalink:"/docs/1.2/upgrades/0.11_to_1.0/adding_a_package_directive"},next:{title:"Object instantiation changes",permalink:"/docs/1.2/upgrades/0.11_to_1.0/object_instantiation_changes"}},l={},c=[{value:"strict flag mode deprecation",id:"strict-flag-mode-deprecation",level:2},{value:"Alternatives to <code>strict=False</code>",id:"alternatives-to-strictfalse",level:2},{value:"Adding config fields through the command line",id:"adding-config-fields-through-the-command-line",level:3},{value:"Adding fields at runtime",id:"adding-fields-at-runtime",level:3},{value:"Field existence check",id:"field-existence-check",level:3}],s={toc:c},m="wrapper";function p(e){let{components:t,...n}=e;return(0,i.mdx)(m,(0,r.A)({},s,n,{components:t,mdxType:"MDXLayout"}),(0,i.mdx)("h2",{id:"strict-flag-mode-deprecation"},"strict flag mode deprecation"),(0,i.mdx)("p",null,"The strict mode is a flag added to ",(0,i.mdx)("inlineCode",{parentName:"p"},"@hydra.main()")," to enable two features:"),(0,i.mdx)("ul",null,(0,i.mdx)("li",{parentName:"ul"},"Command line error detection (overriding a field not in the config)"),(0,i.mdx)("li",{parentName:"ul"},"Runtime config access error detection (accessing/setting a field not in the config)")),(0,i.mdx)("p",null,"This flag is now deprecated, and the ability to turn it off will be removed in Hydra 1.1."),(0,i.mdx)("h2",{id:"alternatives-to-strictfalse"},"Alternatives to ",(0,i.mdx)("inlineCode",{parentName:"h2"},"strict=False")),(0,i.mdx)("p",null,"Below are a few common reasons for people disabling strict mode along with recommended alternatives."),(0,i.mdx)("h3",{id:"adding-config-fields-through-the-command-line"},"Adding config fields through the command line"),(0,i.mdx)("p",null,"With strict mode disabled; you can add fields not specified in config file through the command line.\nHydra 1.0 introduces the + prefix to command line overrides, enabling the addition of fields not in the config file."),(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="config.yaml"',title:'"config.yaml"'},"db:\n  driver: mysql\n")),(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:"{1,6}","{1,6}":!0},"$ python my_app.py +db.host=localhost\ndb:\n  driver: mysql\n  host: localhost\n")),(0,i.mdx)("h3",{id:"adding-fields-at-runtime"},"Adding fields at runtime"),(0,i.mdx)("p",null,"When strict mode is disabled, you can add fields to your config at runtime.\nStrict mode is implemented by setting the OmegaConf ",(0,i.mdx)("inlineCode",{parentName:"p"},"struct")," flag to True on the root of the config."),(0,i.mdx)("ul",null,(0,i.mdx)("li",{parentName:"ul"},"You can disable the struct flag a specific context using ",(0,i.mdx)("inlineCode",{parentName:"li"},"open_dict"),"."),(0,i.mdx)("li",{parentName:"ul"},"You can disable the struct flag permanently for your config using ",(0,i.mdx)("inlineCode",{parentName:"li"},"OmegaConf.set_struct(cfg, False)"),".")),(0,i.mdx)("p",null,"Learn more about OmegaConf struct flag ",(0,i.mdx)("a",{class:"external",href:"https://omegaconf.readthedocs.io/en/latest/usage.html#struct-flag",target:"_blank"},"here"),"."),(0,i.mdx)("h3",{id:"field-existence-check"},"Field existence check"),(0,i.mdx)("p",null,"With strict mode disabled, you can check if a field is in the config by comparing it to None:"),(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre",className:"language-python"},"if cfg.host is None:\n    # host is not in the config\n")),(0,i.mdx)("p",null,"This will no longer work because an exception will be thrown when the ",(0,i.mdx)("inlineCode",{parentName:"p"},"host")," field is accessed.",(0,i.mdx)("br",{parentName:"p"}),"\n","Use ",(0,i.mdx)("inlineCode",{parentName:"p"},"in")," or ",(0,i.mdx)("inlineCode",{parentName:"p"},"hasattr")," instead:"),(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre",className:"language-python"},'if "host" not in cfg:\n    # host is not in the config\n\nif not hasattr(cfg, "host"):\n    # host is not in the config\n')))}p.isMDXComponent=!0}}]);