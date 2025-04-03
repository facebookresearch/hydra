"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[2129],{15680:(e,t,a)=>{a.r(t),a.d(t,{MDXContext:()=>d,MDXProvider:()=>p,mdx:()=>y,useMDXComponents:()=>c,withMDXComponents:()=>m});var n=a(96540);function i(e,t,a){return t in e?Object.defineProperty(e,t,{value:a,enumerable:!0,configurable:!0,writable:!0}):e[t]=a,e}function o(){return o=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var a=arguments[t];for(var n in a)Object.prototype.hasOwnProperty.call(a,n)&&(e[n]=a[n])}return e},o.apply(this,arguments)}function r(e,t){var a=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);t&&(n=n.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),a.push.apply(a,n)}return a}function s(e){for(var t=1;t<arguments.length;t++){var a=null!=arguments[t]?arguments[t]:{};t%2?r(Object(a),!0).forEach((function(t){i(e,t,a[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(a)):r(Object(a)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(a,t))}))}return e}function l(e,t){if(null==e)return{};var a,n,i=function(e,t){if(null==e)return{};var a,n,i={},o=Object.keys(e);for(n=0;n<o.length;n++)a=o[n],t.indexOf(a)>=0||(i[a]=e[a]);return i}(e,t);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(e);for(n=0;n<o.length;n++)a=o[n],t.indexOf(a)>=0||Object.prototype.propertyIsEnumerable.call(e,a)&&(i[a]=e[a])}return i}var d=n.createContext({}),m=function(e){return function(t){var a=c(t.components);return n.createElement(e,o({},t,{components:a}))}},c=function(e){var t=n.useContext(d),a=t;return e&&(a="function"==typeof e?e(t):s(s({},t),e)),a},p=function(e){var t=c(e.components);return n.createElement(d.Provider,{value:t},e.children)},u="mdxType",f={inlineCode:"code",wrapper:function(e){var t=e.children;return n.createElement(n.Fragment,{},t)}},g=n.forwardRef((function(e,t){var a=e.components,i=e.mdxType,o=e.originalType,r=e.parentName,d=l(e,["components","mdxType","originalType","parentName"]),m=c(a),p=i,u=m["".concat(r,".").concat(p)]||m[p]||f[p]||o;return a?n.createElement(u,s(s({ref:t},d),{},{components:a})):n.createElement(u,s({ref:t},d))}));function y(e,t){var a=arguments,i=t&&t.mdxType;if("string"==typeof e||i){var o=a.length,r=new Array(o);r[0]=g;var s={};for(var l in t)hasOwnProperty.call(t,l)&&(s[l]=t[l]);s.originalType=e,s[u]="string"==typeof e?e:i,r[1]=s;for(var d=2;d<o;d++)r[d]=a[d];return n.createElement.apply(null,r)}return n.createElement.apply(null,a)}g.displayName="MDXCreateElement"},65788:(e,t,a)=>{a.r(t),a.d(t,{assets:()=>l,contentTitle:()=>r,default:()=>p,frontMatter:()=>o,metadata:()=>s,toc:()=>d});var n=a(58168),i=(a(96540),a(15680));const o={id:"default_composition_order",title:"Changes to default composition order"},r=void 0,s={unversionedId:"upgrades/1.0_to_1.1/default_composition_order",id:"version-1.1/upgrades/1.0_to_1.1/default_composition_order",title:"Changes to default composition order",description:"Default composition order is changing in Hydra 1.1.",source:"@site/versioned_docs/version-1.1/upgrades/1.0_to_1.1/changes_to_default_composition_order.md",sourceDirName:"upgrades/1.0_to_1.1",slug:"/upgrades/1.0_to_1.1/default_composition_order",permalink:"/docs/1.1/upgrades/1.0_to_1.1/default_composition_order",draft:!1,editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/versioned_docs/version-1.1/upgrades/1.0_to_1.1/changes_to_default_composition_order.md",tags:[],version:"1.1",lastUpdatedBy:"dependabot[bot]",lastUpdatedAt:1743717584,formattedLastUpdatedAt:"Apr 3, 2025",frontMatter:{id:"default_composition_order",title:"Changes to default composition order"},sidebar:"docs",previous:{title:"Changes to @hydra.main() and hydra.initialize()",permalink:"/docs/1.1/upgrades/1.0_to_1.1/changes_to_hydra_main_config_path"},next:{title:"Defaults List Overrides",permalink:"/docs/1.1/upgrades/1.0_to_1.1/defaults_list_override"}},l={},d=[{value:"Migration",id:"migration",level:2},{value:"Primary config is a YAML file",id:"primary-config-is-a-yaml-file",level:3},{value:"Primary config is a Structured Config",id:"primary-config-is-a-structured-config",level:3},{value:"Primary config is a config file with a Structured Config schema",id:"primary-config-is-a-config-file-with-a-structured-config-schema",level:3},{value:"Compatibility with both Hydra 1.0 and 1.1",id:"compatibility-with-both-hydra-10-and-11",level:3}],m={toc:d},c="wrapper";function p(e){let{components:t,...a}=e;return(0,i.mdx)(c,(0,n.A)({},m,a,{components:t,mdxType:"MDXLayout"}),(0,i.mdx)("p",null,"Default composition order is changing in Hydra 1.1."),(0,i.mdx)("p",null,"For this example, let's assume the following two configs:"),(0,i.mdx)("div",{className:"row"},(0,i.mdx)("div",{className:"col col--6"},(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="config.yaml"',title:'"config.yaml"'},"defaults:\n  - foo: bar\n\nfoo:\n  x: 10\n"))),(0,i.mdx)("div",{className:"col  col--6"},(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="foo/bar.yaml"',title:'"foo/bar.yaml"'},"# @package _group_\nx: 20\n\n\n\n")))),(0,i.mdx)("div",{className:"row"},(0,i.mdx)("div",{className:"col"},(0,i.mdx)("p",null,"In ",(0,i.mdx)("strong",{parentName:"p"},"Hydra 1.0"),", configs from the Defaults List are overriding ",(0,i.mdx)("em",{parentName:"p"},"config.yaml"),", resulting in the following output:")),(0,i.mdx)("div",{className:"col  col--4"},(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:"{2}","{2}":!0},"foo:\n  x: 20\n")))),(0,i.mdx)("div",{className:"row"},(0,i.mdx)("div",{className:"col"},(0,i.mdx)("p",null,"As of ",(0,i.mdx)("strong",{parentName:"p"},"Hydra 1.1"),", ",(0,i.mdx)("em",{parentName:"p"},"config.yaml")," is overriding configs from the Defaults List, resulting in the following output:")),(0,i.mdx)("div",{className:"col  col--4"},(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:"{2}","{2}":!0},"foo:\n  x: 10\n")))),(0,i.mdx)("h2",{id:"migration"},"Migration"),(0,i.mdx)("p",null,"If your application uses ",(0,i.mdx)("inlineCode",{parentName:"p"},"hydra.main"),", the best way to verify that updating Hydra versions does not change your job configurations is to compare the output of ",(0,i.mdx)("inlineCode",{parentName:"p"},"python my_app.py --cfg job")," on both the new and old Hydra versions. If your application uses the Compose API, please make sure you have comprehensive unit tests on the composed configuration."),(0,i.mdx)("h3",{id:"primary-config-is-a-yaml-file"},"Primary config is a YAML file"),(0,i.mdx)("p",null,"To ensure this change is not missed by people migrating from Hydra 1.0, Hydra 1.1 issues a warning if the Defaults List in the primary config is missing ",(0,i.mdx)("inlineCode",{parentName:"p"},"_self_"),", and there are config values in addition to the Defaults List.",(0,i.mdx)("br",{parentName:"p"}),"\n","To address the warning, add ",(0,i.mdx)("inlineCode",{parentName:"p"},"_self_")," to the Defaults List of the primary config."),(0,i.mdx)("ul",null,(0,i.mdx)("li",{parentName:"ul"},"If the new behavior works for your application, append ",(0,i.mdx)("inlineCode",{parentName:"li"},"_self_")," to the end of the Defaults List."),(0,i.mdx)("li",{parentName:"ul"},"If your application requires the previous behavior, insert ",(0,i.mdx)("inlineCode",{parentName:"li"},"_self_")," as the first item in your Defaults List.")),(0,i.mdx)("div",{className:"row"},(0,i.mdx)("div",{className:"col col--6"},(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="config.yaml" {2}',title:'"config.yaml"',"{2}":!0},"defaults:\n  - _self_\n  - foo: bar\n\nfoo:\n  x: 10\n"))),(0,i.mdx)("div",{className:"col  col--6"},(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="Output config"',title:'"Output','config"':!0},"foo:\n  x: 20\n\n\n\n\n")))),(0,i.mdx)("p",null,"The Defaults List is described ",(0,i.mdx)("a",{parentName:"p",href:"/docs/1.1/advanced/defaults_list"},"here"),"."),(0,i.mdx)("h3",{id:"primary-config-is-a-structured-config"},"Primary config is a Structured Config"),(0,i.mdx)("p",null,"Structured Configs used as primary config may see changes as well.\nYou should add ",(0,i.mdx)("inlineCode",{parentName:"p"},"_self_")," to the defaults list to indicate the composition order. In such cases you will typically want ",(0,i.mdx)("inlineCode",{parentName:"p"},"_self_")," to be the first item in the defaults list. "),(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre",className:"language-python",metastring:"{3,14}","{3,14}":!0},'defaults = [\n    "_self_",\n    {"db": "mysql"}\n]\n\n@dataclass\nclass Config:\n    # this is unfortunately verbose due to @dataclass limitations\n    defaults: List[Any] = field(default_factory=lambda: defaults)\n\n    # Hydra will populate this field based on the defaults list\n    db: Any = MISSING\n')),(0,i.mdx)("h3",{id:"primary-config-is-a-config-file-with-a-structured-config-schema"},"Primary config is a config file with a Structured Config schema"),(0,i.mdx)("p",null,"If you use Structured Config as a schema for your primary config, be sure to add ",(0,i.mdx)("inlineCode",{parentName:"p"},"_self_")," after the schema in the Defaults List, otherwise the schema will override the config instead of the other way around."),(0,i.mdx)("div",{className:"row"},(0,i.mdx)("div",{className:"col col--4"},(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre",className:"language-python",metastring:'title="my_app.py"',title:'"my_app.py"'},'@dataclass\nclass Config:\n  host: str = "localhost"\n  port: int = 8080\n\ncs.store(name="base_config", \n         node=Config)\n'))),(0,i.mdx)("div",{className:"col  col--4"},(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'{3,5} title="config.yaml"',"{3,5}":!0,title:'"config.yaml"'},"defaults:\n - base_config  # schema\n - _self_       # after schema\n\nport: 3306\n\n\n"))),(0,i.mdx)("div",{className:"col  col--4"},(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'{2} title="Output config"',"{2}":!0,title:'"Output','config"':!0},"host: localhost # schema\nport: 3306      # config.yaml\n\n\n\n\n\n")))),(0,i.mdx)("h3",{id:"compatibility-with-both-hydra-10-and-11"},"Compatibility with both Hydra 1.0 and 1.1"),(0,i.mdx)("p",null,"If your config must be compatible with both Hydra 1.0 and 1.1, Insert ",(0,i.mdx)("inlineCode",{parentName:"p"},"_self_")," as the first item in the Defaults List.\nHydra 1.0.7 (or newer releases in Hydra 1.0) ignores ",(0,i.mdx)("inlineCode",{parentName:"p"},"_self_")," in the Defaults List and Hydra 1.1 will compose the same config as Hydra 1.0 if ",(0,i.mdx)("inlineCode",{parentName:"p"},"_self_")," is the first item."))}p.isMDXComponent=!0}}]);