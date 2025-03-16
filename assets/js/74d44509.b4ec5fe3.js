"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[5170],{15680:(e,t,n)=>{n.r(t),n.d(t,{MDXContext:()=>l,MDXProvider:()=>p,mdx:()=>h,useMDXComponents:()=>f,withMDXComponents:()=>u});var r=n(96540);function a(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function i(){return i=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var r in n)Object.prototype.hasOwnProperty.call(n,r)&&(e[r]=n[r])}return e},i.apply(this,arguments)}function o(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,r)}return n}function c(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?o(Object(n),!0).forEach((function(t){a(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):o(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function s(e,t){if(null==e)return{};var n,r,a=function(e,t){if(null==e)return{};var n,r,a={},i=Object.keys(e);for(r=0;r<i.length;r++)n=i[r],t.indexOf(n)>=0||(a[n]=e[n]);return a}(e,t);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);for(r=0;r<i.length;r++)n=i[r],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(a[n]=e[n])}return a}var l=r.createContext({}),u=function(e){return function(t){var n=f(t.components);return r.createElement(e,i({},t,{components:n}))}},f=function(e){var t=r.useContext(l),n=t;return e&&(n="function"==typeof e?e(t):c(c({},t),e)),n},p=function(e){var t=f(e.components);return r.createElement(l.Provider,{value:t},e.children)},d="mdxType",m={inlineCode:"code",wrapper:function(e){var t=e.children;return r.createElement(r.Fragment,{},t)}},g=r.forwardRef((function(e,t){var n=e.components,a=e.mdxType,i=e.originalType,o=e.parentName,l=s(e,["components","mdxType","originalType","parentName"]),u=f(n),p=a,d=u["".concat(o,".").concat(p)]||u[p]||m[p]||i;return n?r.createElement(d,c(c({ref:t},l),{},{components:n})):r.createElement(d,c({ref:t},l))}));function h(e,t){var n=arguments,a=t&&t.mdxType;if("string"==typeof e||a){var i=n.length,o=new Array(i);o[0]=g;var c={};for(var s in t)hasOwnProperty.call(t,s)&&(c[s]=t[s]);c.originalType=e,c[d]="string"==typeof e?e:a,o[1]=c;for(var l=2;l<i;l++)o[l]=n[l];return r.createElement.apply(null,o)}return r.createElement.apply(null,n)}g.displayName="MDXCreateElement"},39919:(e,t,n)=>{n.r(t),n.d(t,{assets:()=>l,contentTitle:()=>c,default:()=>d,frontMatter:()=>o,metadata:()=>s,toc:()=>u});var r=n(58168),a=(n(96540),n(15680)),i=n(49595);const o={id:"hierarchical_static_config",title:"A hierarchical static configuration"},c=void 0,s={unversionedId:"tutorials/structured_config/hierarchical_static_config",id:"tutorials/structured_config/hierarchical_static_config",title:"A hierarchical static configuration",description:"Dataclasses can be nested and then accessed via a common root.  The entire tree is type checked.",source:"@site/docs/tutorials/structured_config/2_hierarchical_static_config.md",sourceDirName:"tutorials/structured_config",slug:"/tutorials/structured_config/hierarchical_static_config",permalink:"/docs/tutorials/structured_config/hierarchical_static_config",draft:!1,editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/docs/tutorials/structured_config/2_hierarchical_static_config.md",tags:[],version:"current",lastUpdatedBy:"dependabot[bot]",lastUpdatedAt:1742161400,formattedLastUpdatedAt:"Mar 16, 2025",sidebarPosition:2,frontMatter:{id:"hierarchical_static_config",title:"A hierarchical static configuration"},sidebar:"docs",previous:{title:"Minimal example",permalink:"/docs/tutorials/structured_config/minimal_example"},next:{title:"Config Groups",permalink:"/docs/tutorials/structured_config/config_groups"}},l={},u=[],f={toc:u},p="wrapper";function d(e){let{components:t,...n}=e;return(0,a.mdx)(p,(0,r.A)({},f,n,{components:t,mdxType:"MDXLayout"}),(0,a.mdx)(i.C,{to:"examples/tutorials/structured_configs/2_static_complex",mdxType:"ExampleGithubLink"}),(0,a.mdx)("p",null,"Dataclasses can be nested and then accessed via a common root.  The entire tree is type checked."),(0,a.mdx)("pre",null,(0,a.mdx)("code",{parentName:"pre",className:"language-python"},'from dataclasses import dataclass\n\nimport hydra\nfrom hydra.core.config_store import ConfigStore\n\n@dataclass\nclass MySQLConfig:\n    host: str = "localhost"\n    port: int = 3306\n\n@dataclass\nclass UserInterface:\n    title: str = "My app"\n    width: int = 1024\n    height: int = 768\n\n@dataclass\nclass MyConfig:\n    db: MySQLConfig = field(default_factory=MySQLConfig)\n    ui: UserInterface = field(default_factory=UserInterface)\n\ncs = ConfigStore.instance()\ncs.store(name="config", node=MyConfig)\n\n@hydra.main(version_base=None, config_name="config")\ndef my_app(cfg: MyConfig) -> None:\n    print(f"Title={cfg.ui.title}, size={cfg.ui.width}x{cfg.ui.height} pixels")\n\nif __name__ == "__main__":\n    my_app()\n')))}d.isMDXComponent=!0},49595:(e,t,n)=>{n.d(t,{A:()=>l,C:()=>u});var r=n(58168),a=n(96540),i=n(75489),o=n(44586),c=n(48295);function s(e){const t=(0,c.ir)();return(0,o.default)().siteConfig.customFields.githubLinkVersionToBaseUrl[t?.name??"current"]+e}function l(e){return a.createElement(i.default,(0,r.A)({},e,{to:s(e.to),target:"_blank"}))}function u(e){const t=e.text??"Example (Click Here)";return a.createElement(l,e,a.createElement("span",null,"\xa0"),a.createElement("img",{src:"https://img.shields.io/badge/-"+t+"-informational",alt:"Example (Click Here)"}))}}}]);