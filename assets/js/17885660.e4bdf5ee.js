"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[6432],{15680:(e,t,n)=>{n.r(t),n.d(t,{MDXContext:()=>s,MDXProvider:()=>p,mdx:()=>f,useMDXComponents:()=>c,withMDXComponents:()=>d});var a=n(96540);function o(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function i(){return i=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var a in n)Object.prototype.hasOwnProperty.call(n,a)&&(e[a]=n[a])}return e},i.apply(this,arguments)}function l(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);t&&(a=a.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,a)}return n}function r(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?l(Object(n),!0).forEach((function(t){o(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):l(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function m(e,t){if(null==e)return{};var n,a,o=function(e,t){if(null==e)return{};var n,a,o={},i=Object.keys(e);for(a=0;a<i.length;a++)n=i[a],t.indexOf(n)>=0||(o[n]=e[n]);return o}(e,t);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);for(a=0;a<i.length;a++)n=i[a],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(o[n]=e[n])}return o}var s=a.createContext({}),d=function(e){return function(t){var n=c(t.components);return a.createElement(e,i({},t,{components:n}))}},c=function(e){var t=a.useContext(s),n=t;return e&&(n="function"==typeof e?e(t):r(r({},t),e)),n},p=function(e){var t=c(e.components);return a.createElement(s.Provider,{value:t},e.children)},u="mdxType",h={inlineCode:"code",wrapper:function(e){var t=e.children;return a.createElement(a.Fragment,{},t)}},g=a.forwardRef((function(e,t){var n=e.components,o=e.mdxType,i=e.originalType,l=e.parentName,s=m(e,["components","mdxType","originalType","parentName"]),d=c(n),p=o,u=d["".concat(l,".").concat(p)]||d[p]||h[p]||i;return n?a.createElement(u,r(r({ref:t},s),{},{components:n})):a.createElement(u,r({ref:t},s))}));function f(e,t){var n=arguments,o=t&&t.mdxType;if("string"==typeof e||o){var i=n.length,l=new Array(i);l[0]=g;var r={};for(var m in t)hasOwnProperty.call(t,m)&&(r[m]=t[m]);r.originalType=e,r[u]="string"==typeof e?e:o,l[1]=r;for(var s=2;s<i;s++)l[s]=n[s];return a.createElement.apply(null,l)}return a.createElement.apply(null,n)}g.displayName="MDXCreateElement"},15750:(e,t,n)=>{n.r(t),n.d(t,{assets:()=>m,contentTitle:()=>l,default:()=>p,frontMatter:()=>i,metadata:()=>r,toc:()=>s});var a=n(58168),o=(n(96540),n(15680));const i={id:"automatic_schema_matching",title:"Automatic schema-matching",hide_title:!0},l=void 0,r={unversionedId:"upgrades/1.0_to_1.1/automatic_schema_matching",id:"upgrades/1.0_to_1.1/automatic_schema_matching",title:"Automatic schema-matching",description:"In Hydra 1.0, when a config file is loaded, if a config with a matching name and group is present in the ConfigStore,",source:"@site/docs/upgrades/1.0_to_1.1/automatic_schema_matching.md",sourceDirName:"upgrades/1.0_to_1.1",slug:"/upgrades/1.0_to_1.1/automatic_schema_matching",permalink:"/docs/upgrades/1.0_to_1.1/automatic_schema_matching",draft:!1,editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/docs/upgrades/1.0_to_1.1/automatic_schema_matching.md",tags:[],version:"current",lastUpdatedBy:"jesszzzz",lastUpdatedAt:1743461536,formattedLastUpdatedAt:"Mar 31, 2025",frontMatter:{id:"automatic_schema_matching",title:"Automatic schema-matching",hide_title:!0},sidebar:"docs",previous:{title:"Changes to Package Header",permalink:"/docs/upgrades/1.0_to_1.1/changes_to_package_header"},next:{title:"Config path changes",permalink:"/docs/upgrades/0.11_to_1.0/config_path_changes"}},m={},s=[{value:"Migration",id:"migration",level:2},{value:"Option 1: rename the Structured Config",id:"option-1-rename-the-structured-config",level:3},{value:"Hydra 1.0",id:"hydra-10",level:4},{value:"Hydra 1.1",id:"hydra-11",level:4},{value:"Option 2: rename the config file",id:"option-2-rename-the-config-file",level:3},{value:"Hydra 1.0",id:"hydra-10-1",level:4},{value:"Hydra 1.1",id:"hydra-11-1",level:4}],d={toc:s},c="wrapper";function p(e){let{components:t,...n}=e;return(0,o.mdx)(c,(0,a.A)({},d,n,{components:t,mdxType:"MDXLayout"}),(0,o.mdx)("p",null,"In Hydra 1.0, when a config file is loaded, if a config with a matching name and group is present in the ",(0,o.mdx)("inlineCode",{parentName:"p"},"ConfigStore"),",\nit is used as the schema for the newly loaded config."),(0,o.mdx)("p",null,"There are several problems with this approach:"),(0,o.mdx)("ul",null,(0,o.mdx)("li",{parentName:"ul"},(0,o.mdx)("strong",{parentName:"li"},"Inflexible"),": This approach can only be used when a schema should validate a single config file.\nIt does not work if you want to use the same schema to validate multiple config files."),(0,o.mdx)("li",{parentName:"ul"},(0,o.mdx)("strong",{parentName:"li"},"Unexpected"),": This behavior can be unexpected. There is no way to tell this is going to happen when looking at a given\nconfig file.")),(0,o.mdx)("p",null,"Hydra 1.1 deprecates this behavior in favor of an explicit config extension via the Defaults List.",(0,o.mdx)("br",{parentName:"p"}),"\n","This upgrade page aims to provide a summary of the required changes. It is highly recommended that you read the following pages:"),(0,o.mdx)("ul",null,(0,o.mdx)("li",{parentName:"ul"},(0,o.mdx)("a",{parentName:"li",href:"/docs/advanced/defaults_list"},"Background: The Defaults List")),(0,o.mdx)("li",{parentName:"ul"},(0,o.mdx)("a",{parentName:"li",href:"/docs/patterns/extending_configs"},"Background: Extending configs")),(0,o.mdx)("li",{parentName:"ul"},(0,o.mdx)("a",{parentName:"li",href:"/docs/tutorials/structured_config/schema"},"Tutorial: Structured config schema"))),(0,o.mdx)("h2",{id:"migration"},"Migration"),(0,o.mdx)("p",null,"Before the upgrade, you have two different configs with the same name (a config file, and a Structured Config in the ",(0,o.mdx)("inlineCode",{parentName:"p"},"ConfigStore"),").\nYou need to rename one of them. Depending on the circumstances and your preference you may rename one or the other."),(0,o.mdx)("ul",null,(0,o.mdx)("li",{parentName:"ul"},"If you control both configs, you can rename either of them."),(0,o.mdx)("li",{parentName:"ul"},"If you only control the config file, rename it.")),(0,o.mdx)("h3",{id:"option-1-rename-the-structured-config"},"Option 1: rename the Structured Config"),(0,o.mdx)("p",null,"This option is less disruptive. Use it if you control the Structured Config.  "),(0,o.mdx)("ol",null,(0,o.mdx)("li",{parentName:"ol"},"Use a different name when storing the schema into the Config Store. Common choices:",(0,o.mdx)("ul",{parentName:"li"},(0,o.mdx)("li",{parentName:"ul"},(0,o.mdx)("inlineCode",{parentName:"li"},"base_")," prefix, e.g. ",(0,o.mdx)("inlineCode",{parentName:"li"},"base_mysql"),"."),(0,o.mdx)("li",{parentName:"ul"},(0,o.mdx)("inlineCode",{parentName:"li"},"_schema")," suffix, e.g. ",(0,o.mdx)("inlineCode",{parentName:"li"},"mysql_schema"),"."))),(0,o.mdx)("li",{parentName:"ol"},"Add the schema to the Defaults List of the extending config file.")),(0,o.mdx)("details",null,(0,o.mdx)("summary",null,"Click to show an example"),(0,o.mdx)("h4",{id:"hydra-10"},"Hydra 1.0"),(0,o.mdx)("div",{className:"row"},(0,o.mdx)("div",{className:"col col--6"},(0,o.mdx)("pre",null,(0,o.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="db/mysql.yaml"',title:'"db/mysql.yaml"'},"# @package _group_\nhost: localhost\nport: 3306\n\n\n\n\n\n\n"))),(0,o.mdx)("div",{className:"col col--6"},(0,o.mdx)("pre",null,(0,o.mdx)("code",{parentName:"pre",className:"language-python",metastring:'title="db/mysql schema in the ConfigStore"',title:'"db/mysql',schema:!0,in:!0,the:!0,'ConfigStore"':!0},'@dataclass\nclass MySQLConfig:\n    host: str\n    port: int\n\ncs = ConfigStore.instance()\ncs.store(group="db",\n         name="mysql", \n         node=MySQLConfig)\n')))),(0,o.mdx)("h4",{id:"hydra-11"},"Hydra 1.1"),(0,o.mdx)("div",{className:"row"},(0,o.mdx)("div",{className:"col col--6"},(0,o.mdx)("pre",null,(0,o.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="db/mysql.yaml" {1,2}',title:'"db/mysql.yaml"',"{1,2}":!0},"defaults:\n  - base_mysql\n\nhost: localhost\nport: 3306\n\n\n\n\n"))),(0,o.mdx)("div",{className:"col col--6"},(0,o.mdx)("pre",null,(0,o.mdx)("code",{parentName:"pre",className:"language-python",metastring:'title="db/mysql schema in the ConfigStore" {8}',title:'"db/mysql',schema:!0,in:!0,the:!0,'ConfigStore"':!0,"{8}":!0},'@dataclass\nclass MySQLConfig:\n    host: str\n    port: int\n\ncs = ConfigStore.instance()\ncs.store(group="db",\n         name="base_mysql", \n         node=MySQLConfig)\n'))))),(0,o.mdx)("h3",{id:"option-2-rename-the-config-file"},"Option 2: rename the config file"),(0,o.mdx)("p",null,"This option is a bit more disruptive. Use it if you only control the config file."),(0,o.mdx)("ol",null,(0,o.mdx)("li",{parentName:"ol"},"Rename the config file. Common choices are ",(0,o.mdx)("inlineCode",{parentName:"li"},"custom_")," or ",(0,o.mdx)("inlineCode",{parentName:"li"},"my_")," prefix, e.g. ",(0,o.mdx)("inlineCode",{parentName:"li"},"custom_mysql.yaml"),". You can also use a domain specific name like ",(0,o.mdx)("inlineCode",{parentName:"li"},"prod_mysql.yaml"),"."),(0,o.mdx)("li",{parentName:"ol"},"Add the schema to the Defaults List of the extending config file."),(0,o.mdx)("li",{parentName:"ol"},"Update references to the config name accordingly, e.g. on the command-line ",(0,o.mdx)("inlineCode",{parentName:"li"},"db=mysql")," would become ",(0,o.mdx)("inlineCode",{parentName:"li"},"db=custom_mysql"),", and in a defaults list ",(0,o.mdx)("inlineCode",{parentName:"li"},"db: mysql")," would become ",(0,o.mdx)("inlineCode",{parentName:"li"},"db: custom_mysql"),".")),(0,o.mdx)("details",null,(0,o.mdx)("summary",null,"Click to show an example"),(0,o.mdx)("h4",{id:"hydra-10-1"},"Hydra 1.0"),(0,o.mdx)("div",{className:"row"},(0,o.mdx)("div",{className:"col col--6"},(0,o.mdx)("pre",null,(0,o.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="db/mysql.yaml"',title:'"db/mysql.yaml"'},"# @package _group_\nhost: localhost\nport: 3306\n")),(0,o.mdx)("pre",null,(0,o.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="config.yaml"',title:'"config.yaml"'},"defaults:\n  - db: mysql\n"))),(0,o.mdx)("div",{className:"col col--6"},(0,o.mdx)("pre",null,(0,o.mdx)("code",{parentName:"pre",className:"language-python",metastring:'title="db/mysql schema in the ConfigStore"',title:'"db/mysql',schema:!0,in:!0,the:!0,'ConfigStore"':!0},'@dataclass\nclass MySQLConfig:\n    host: str\n    port: int\n\ncs = ConfigStore.instance()\ncs.store(group="db",\n         name="mysql", \n         node=MySQLConfig)\n\n')))),(0,o.mdx)("h4",{id:"hydra-11-1"},"Hydra 1.1"),(0,o.mdx)("p",null,"Rename ",(0,o.mdx)("inlineCode",{parentName:"p"},"db/mysql.yaml")," to ",(0,o.mdx)("inlineCode",{parentName:"p"},"db/custom_mysql.yaml")," and explicitly add the schema to the Defaults List."),(0,o.mdx)("div",{className:"row"},(0,o.mdx)("div",{className:"col col--6"},(0,o.mdx)("pre",null,(0,o.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="db/custom_mysql.yaml" {1,2}',title:'"db/custom_mysql.yaml"',"{1,2}":!0},"defaults:\n  - mysql\n\nhost: localhost\nport: 3306\n")),(0,o.mdx)("pre",null,(0,o.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="config.yaml" {2}',title:'"config.yaml"',"{2}":!0},"defaults:\n  - db: custom_mysql\n"))),(0,o.mdx)("div",{className:"col col--6"},(0,o.mdx)("pre",null,(0,o.mdx)("code",{parentName:"pre",className:"language-python",metastring:'title="db/mysql schema in the ConfigStore"',title:'"db/mysql',schema:!0,in:!0,the:!0,'ConfigStore"':!0},"\n\n\n\n\n                   NO CHANGES\n\n\n\n\n\n\n")))),(0,o.mdx)("p",null,"Don't forget to also update your command line overrides from ",(0,o.mdx)("inlineCode",{parentName:"p"},"db=mysql")," to ",(0,o.mdx)("inlineCode",{parentName:"p"},"db=custom_mysql"),".")))}p.isMDXComponent=!0}}]);