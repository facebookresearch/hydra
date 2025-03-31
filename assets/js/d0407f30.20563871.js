"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[4417],{15680:(e,t,n)=>{n.r(t),n.d(t,{MDXContext:()=>l,MDXProvider:()=>u,mdx:()=>h,useMDXComponents:()=>d,withMDXComponents:()=>p});var o=n(96540);function r(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function i(){return i=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var o in n)Object.prototype.hasOwnProperty.call(n,o)&&(e[o]=n[o])}return e},i.apply(this,arguments)}function a(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(e);t&&(o=o.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,o)}return n}function s(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?a(Object(n),!0).forEach((function(t){r(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):a(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function c(e,t){if(null==e)return{};var n,o,r=function(e,t){if(null==e)return{};var n,o,r={},i=Object.keys(e);for(o=0;o<i.length;o++)n=i[o],t.indexOf(n)>=0||(r[n]=e[n]);return r}(e,t);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);for(o=0;o<i.length;o++)n=i[o],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(r[n]=e[n])}return r}var l=o.createContext({}),p=function(e){return function(t){var n=d(t.components);return o.createElement(e,i({},t,{components:n}))}},d=function(e){var t=o.useContext(l),n=t;return e&&(n="function"==typeof e?e(t):s(s({},t),e)),n},u=function(e){var t=d(e.components);return o.createElement(l.Provider,{value:t},e.children)},m="mdxType",f={inlineCode:"code",wrapper:function(e){var t=e.children;return o.createElement(o.Fragment,{},t)}},g=o.forwardRef((function(e,t){var n=e.components,r=e.mdxType,i=e.originalType,a=e.parentName,l=c(e,["components","mdxType","originalType","parentName"]),p=d(n),u=r,m=p["".concat(a,".").concat(u)]||p[u]||f[u]||i;return n?o.createElement(m,s(s({ref:t},l),{},{components:n})):o.createElement(m,s({ref:t},l))}));function h(e,t){var n=arguments,r=t&&t.mdxType;if("string"==typeof e||r){var i=n.length,a=new Array(i);a[0]=g;var s={};for(var c in t)hasOwnProperty.call(t,c)&&(s[c]=t[c]);s.originalType=e,s[m]="string"==typeof e?e:r,a[1]=s;for(var l=2;l<i;l++)a[l]=n[l];return o.createElement.apply(null,a)}return o.createElement.apply(null,n)}g.displayName="MDXCreateElement"},20674:(e,t,n)=>{n.r(t),n.d(t,{assets:()=>l,contentTitle:()=>s,default:()=>m,frontMatter:()=>a,metadata:()=>c,toc:()=>p});var o=n(58168),r=(n(96540),n(15680)),i=n(49595);const a={id:"config_groups",title:"Config Groups"},s=void 0,c={unversionedId:"tutorials/structured_config/config_groups",id:"version-1.3/tutorials/structured_config/config_groups",title:"Config Groups",description:"Structured Configs can be used to implement config groups. Special care needs to be taken when specifying a",source:"@site/versioned_docs/version-1.3/tutorials/structured_config/3_config_groups.md",sourceDirName:"tutorials/structured_config",slug:"/tutorials/structured_config/config_groups",permalink:"/docs/1.3/tutorials/structured_config/config_groups",draft:!1,editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/versioned_docs/version-1.3/tutorials/structured_config/3_config_groups.md",tags:[],version:"1.3",lastUpdatedBy:"jesszzzz",lastUpdatedAt:1743461536,formattedLastUpdatedAt:"Mar 31, 2025",sidebarPosition:3,frontMatter:{id:"config_groups",title:"Config Groups"},sidebar:"docs",previous:{title:"A hierarchical static configuration",permalink:"/docs/1.3/tutorials/structured_config/hierarchical_static_config"},next:{title:"Defaults List",permalink:"/docs/1.3/tutorials/structured_config/defaults"}},l={},p=[{value:"Config inheritance",id:"config-inheritance",level:3},{value:"Missing fields",id:"missing-fields",level:3}],d={toc:p},u="wrapper";function m(e){let{components:t,...n}=e;return(0,r.mdx)(u,(0,o.A)({},d,n,{components:t,mdxType:"MDXLayout"}),(0,r.mdx)(i.C,{to:"examples/tutorials/structured_configs/3_config_groups/my_app.py",mdxType:"ExampleGithubLink"}),(0,r.mdx)("p",null,"Structured Configs can be used to implement config groups. Special care needs to be taken when specifying a\ndefault value for fields populated by a config group. We will look at why below."),(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-python",metastring:'title="Defining a config group for database" {16-17,22-23}',title:'"Defining',a:!0,config:!0,group:!0,for:!0,'database"':!0,"{16-17,22-23}":!0},'from dataclasses import dataclass\n\nimport hydra\nfrom hydra.core.config_store import ConfigStore\n\n@dataclass\nclass MySQLConfig:\n    driver: str = "mysql"\n    host: str = "localhost"\n    port: int = 3306\n\n@dataclass\nclass PostGreSQLConfig:\n    driver: str = "postgresql"\n    host: str = "localhost"\n    port: int = 5432\n    timeout: int = 10\n\n@dataclass\nclass Config:\n    # We will populate db using composition.\n    db: Any\n\n# Create config group `db` with options \'mysql\' and \'postgreqsl\'\ncs = ConfigStore.instance()\ncs.store(name="config", node=Config)\ncs.store(group="db", name="mysql", node=MySQLConfig)\ncs.store(group="db", name="postgresql", node=PostGreSQLConfig)\n\n@hydra.main(version_base=None, config_name="config")\ndef my_app(cfg: Config) -> None:\n    print(OmegaConf.to_yaml(cfg))\n\nif __name__ == "__main__":\n    my_app()\n')),(0,r.mdx)("admonition",{type:"caution"},(0,r.mdx)("p",{parentName:"admonition"},"The ",(0,r.mdx)("em",{parentName:"p"},"Config")," class is ",(0,r.mdx)("strong",{parentName:"p"},"NOT")," the Defaults list. We will see the Defaults list in the next page.")),(0,r.mdx)("p",null,"You can select the database from the command line:"),(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-yaml"},"$ python my_app.py +db=postgresql\ndb:\n  driver: postgresql\n  host: localhost\n  password: drowssap\n  port: 5432\n  timeout: 10\n  user: postgres_user\n")),(0,r.mdx)("p",null,"The ",(0,r.mdx)("inlineCode",{parentName:"p"},"+")," above is required because there is no default choice for the config group ",(0,r.mdx)("inlineCode",{parentName:"p"},"db"),".\nThe next page will reintroduce the Defaults List, eliminating the need for the ",(0,r.mdx)("inlineCode",{parentName:"p"},"+"),"."),(0,r.mdx)("h3",{id:"config-inheritance"},"Config inheritance"),(0,r.mdx)(i.C,{to:"examples/tutorials/structured_configs/3_config_groups/my_app_with_inheritance.py",mdxType:"ExampleGithubLink"}),(0,r.mdx)("p",null,"Standard Python inheritance can be used to get improved type safety, and to move common fields to the parent class."),(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-python",metastring:'title="Defining a config group for database using inheritance"',title:'"Defining',a:!0,config:!0,group:!0,for:!0,database:!0,using:!0,'inheritance"':!0},'from omegaconf import MISSING\n\n@dataclass\nclass DBConfig:\n    host: str = "localhost"\n    port: int = MISSING\n    driver: str = MISSING\n\n@dataclass\nclass MySQLConfig(DBConfig):\n    driver: str = "mysql"\n    port: int = 3306\n\n@dataclass\nclass PostGreSQLConfig(DBConfig):\n    driver: str = "postgresql"\n    port: int = 5432\n    timeout: int = 10\n\n@dataclass\nclass Config:\n    # We can now annotate db as DBConfig which\n    # improves both static and dynamic type safety.\n    db: DBConfig\n')),(0,r.mdx)("h3",{id:"missing-fields"},"Missing fields"),(0,r.mdx)("p",null,"Assign ",(0,r.mdx)("em",{parentName:"p"},"MISSING")," to a field to indicates that it does not have a default value. This is equivalent to\nthe ",(0,r.mdx)("inlineCode",{parentName:"p"},"???")," literal we have seen in OmegaConf configs before."),(0,r.mdx)("p",null,"Omitting a default value is equivalent to assigning ",(0,r.mdx)("em",{parentName:"p"},"MISSING")," to it, although it is sometimes\nconvenient to be able to assign MISSING it to a field."),(0,r.mdx)("admonition",{type:"caution"},(0,r.mdx)("p",{parentName:"admonition"},"Do not confuse ",(0,r.mdx)("strong",{parentName:"p"},"omegaconf.MISSING")," with ",(0,r.mdx)("strong",{parentName:"p"},"dataclass.MISSING"),".")))}m.isMDXComponent=!0},49595:(e,t,n)=>{n.d(t,{A:()=>l,C:()=>p});var o=n(58168),r=n(96540),i=n(75489),a=n(44586),s=n(48295);function c(e){const t=(0,s.ir)();return(0,a.default)().siteConfig.customFields.githubLinkVersionToBaseUrl[t?.name??"current"]+e}function l(e){return r.createElement(i.default,(0,o.A)({},e,{to:c(e.to),target:"_blank"}))}function p(e){const t=e.text??"Example (Click Here)";return r.createElement(l,e,r.createElement("span",null,"\xa0"),r.createElement("img",{src:"https://img.shields.io/badge/-"+t+"-informational",alt:"Example (Click Here)"}))}}}]);