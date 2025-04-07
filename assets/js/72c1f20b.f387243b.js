"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[9910],{15680:(e,t,n)=>{n.r(t),n.d(t,{MDXContext:()=>c,MDXProvider:()=>p,mdx:()=>h,useMDXComponents:()=>m,withMDXComponents:()=>d});var r=n(96540);function a(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function o(){return o=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var r in n)Object.prototype.hasOwnProperty.call(n,r)&&(e[r]=n[r])}return e},o.apply(this,arguments)}function i(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,r)}return n}function s(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?i(Object(n),!0).forEach((function(t){a(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):i(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function l(e,t){if(null==e)return{};var n,r,a=function(e,t){if(null==e)return{};var n,r,a={},o=Object.keys(e);for(r=0;r<o.length;r++)n=o[r],t.indexOf(n)>=0||(a[n]=e[n]);return a}(e,t);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(e);for(r=0;r<o.length;r++)n=o[r],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(a[n]=e[n])}return a}var c=r.createContext({}),d=function(e){return function(t){var n=m(t.components);return r.createElement(e,o({},t,{components:n}))}},m=function(e){var t=r.useContext(c),n=t;return e&&(n="function"==typeof e?e(t):s(s({},t),e)),n},p=function(e){var t=m(e.components);return r.createElement(c.Provider,{value:t},e.children)},u="mdxType",f={inlineCode:"code",wrapper:function(e){var t=e.children;return r.createElement(r.Fragment,{},t)}},g=r.forwardRef((function(e,t){var n=e.components,a=e.mdxType,o=e.originalType,i=e.parentName,c=l(e,["components","mdxType","originalType","parentName"]),d=m(n),p=a,u=d["".concat(i,".").concat(p)]||d[p]||f[p]||o;return n?r.createElement(u,s(s({ref:t},c),{},{components:n})):r.createElement(u,s({ref:t},c))}));function h(e,t){var n=arguments,a=t&&t.mdxType;if("string"==typeof e||a){var o=n.length,i=new Array(o);i[0]=g;var s={};for(var l in t)hasOwnProperty.call(t,l)&&(s[l]=t[l]);s.originalType=e,s[u]="string"==typeof e?e:a,i[1]=s;for(var c=2;c<o;c++)i[c]=n[c];return r.createElement.apply(null,i)}return r.createElement.apply(null,n)}g.displayName="MDXCreateElement"},29015:(e,t,n)=>{n.r(t),n.d(t,{assets:()=>c,contentTitle:()=>s,default:()=>u,frontMatter:()=>i,metadata:()=>l,toc:()=>d});var r=n(58168),a=(n(96540),n(15680)),o=n(49595);const i={id:"schema",title:"Structured config schema"},s=void 0,l={unversionedId:"tutorials/structured_config/schema",id:"version-1.0/tutorials/structured_config/schema",title:"Structured config schema",description:"We have seen how to use Structured Configs as configuration, but they can also be used as a schema (i.e. validating configuration files).",source:"@site/versioned_docs/version-1.0/tutorials/structured_config/5_schema.md",sourceDirName:"tutorials/structured_config",slug:"/tutorials/structured_config/schema",permalink:"/docs/1.0/tutorials/structured_config/schema",draft:!1,editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/versioned_docs/version-1.0/tutorials/structured_config/5_schema.md",tags:[],version:"1.0",lastUpdatedBy:"jesszzzz",lastUpdatedAt:1744041844,formattedLastUpdatedAt:"Apr 7, 2025",sidebarPosition:5,frontMatter:{id:"schema",title:"Structured config schema"},sidebar:"docs",previous:{title:"Defaults List",permalink:"/docs/1.0/tutorials/structured_config/defaults"},next:{title:"Static schema with many configs",permalink:"/docs/1.0/tutorials/structured_config/static_schema"}},c={},d=[],m={toc:d},p="wrapper";function u(e){let{components:t,...n}=e;return(0,a.mdx)(p,(0,r.A)({},m,n,{components:t,mdxType:"MDXLayout"}),(0,a.mdx)(o.C,{to:"examples/tutorials/structured_configs/5_structured_config_schema",mdxType:"ExampleGithubLink"}),(0,a.mdx)("p",null,"We have seen how to use Structured Configs as configuration, but they can also be used as a schema (i.e. validating configuration files)."),(0,a.mdx)("p",null,"When Hydra loads a config file, it looks in the ",(0,a.mdx)("inlineCode",{parentName:"p"},"ConfigStore")," for a Structured Config with a matching name and group.\nIf found, it is used as the schema for the newly loaded config."),(0,a.mdx)("p",null,"This page shows how to validate ",(0,a.mdx)("inlineCode",{parentName:"p"},"db/mysql.yaml")," and ",(0,a.mdx)("inlineCode",{parentName:"p"},"db/postgresql.yaml")," files against a pre-defined schema."),(0,a.mdx)("p",null,"Given the config directory structure:"),(0,a.mdx)("pre",null,(0,a.mdx)("code",{parentName:"pre",className:"language-text"},"conf/\n\u251c\u2500\u2500 config.yaml\n\u2514\u2500\u2500 db\n    \u251c\u2500\u2500 mysql.yaml\n    \u2514\u2500\u2500 postgresql.yaml\n")),(0,a.mdx)("p",null,"We can add Structured Configs for ",(0,a.mdx)("inlineCode",{parentName:"p"},"mysql.yaml")," and ",(0,a.mdx)("inlineCode",{parentName:"p"},"postgresql.yaml"),", providing a schema for validating them."),(0,a.mdx)("p",null,"The Structured Configs below are stored as ",(0,a.mdx)("inlineCode",{parentName:"p"},"db/mysql")," and ",(0,a.mdx)("inlineCode",{parentName:"p"},"db/postgresql"),". They will be used as schema\nwhen we load their corresponding config files."),(0,a.mdx)("pre",null,(0,a.mdx)("code",{parentName:"pre",className:"language-python",metastring:'title="my_app.py"',title:'"my_app.py"'},'@dataclass\nclass DBConfig:\n    driver: str = MISSING\n    host: str = "localhost"\n    port: int = MISSING\n\n\n@dataclass\nclass MySQLConfig(DBConfig):\n    driver: str = "mysql"\n    port: int = 3306\n    user: str = MISSING\n    password: str = MISSING\n\n@dataclass\nclass PostGreSQLConfig(DBConfig):\n    driver: str = "postgresql"\n    user: str = MISSING\n    port: int = 5432\n    password: str = MISSING\n    timeout: int = 10\n\n@dataclass\nclass Config:\n    # Note the lack of defaults list here.\n    # In this example it comes from config.yaml\n    db: DBConfig = MISSING\n\ncs = ConfigStore.instance()\ncs.store(name="config", node=Config)\ncs.store(group="db", name="mysql", node=MySQLConfig)\ncs.store(group="db", name="postgresql", node=PostGreSQLConfig)\n\n# The config name matches both \'config.yaml\' under the conf directory\n# and \'config\' stored in the ConfigStore.\n# config.yaml will compose in db: mysql by default (per the defaults list),\n# and it will be validated against the schema from the Config class\n@hydra.main(config_path="conf", config_name="config")\ndef my_app(cfg: Config) -> None:\n    print(OmegaConf.to_yaml(cfg))\n')),(0,a.mdx)("p",null,"When ",(0,a.mdx)("inlineCode",{parentName:"p"},"db/mysql.yaml")," and ",(0,a.mdx)("inlineCode",{parentName:"p"},"db/postgresql.yaml")," are loaded, the corresponding configs from the ",(0,a.mdx)("inlineCode",{parentName:"p"},"ConfigStore")," are used automatically.\nThis can be used to validate that both the configuration files (",(0,a.mdx)("inlineCode",{parentName:"p"},"mysql.yaml")," and ",(0,a.mdx)("inlineCode",{parentName:"p"},"postgresql.yaml"),") and the command line overrides are conforming to the schema. "),(0,a.mdx)("pre",null,(0,a.mdx)("code",{parentName:"pre"},"$ python my_app.py db.port=fail\nError merging override db.port=fail\nValue 'fail' could not be converted to Integer\n        full_key: db.port\n        reference_type=Optional[MySQLConfig]\n        object_type=MySQLConfig\n")),(0,a.mdx)("p",null,"Unlike the example in the previous page, the Defaults List here is ",(0,a.mdx)("inlineCode",{parentName:"p"},"config.yaml")," and ",(0,a.mdx)("strong",{parentName:"p"},"not")," in the ",(0,a.mdx)("inlineCode",{parentName:"p"},"Config")," class."),(0,a.mdx)("pre",null,(0,a.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="config.yaml"',title:'"config.yaml"'},"defaults:\n  - db: mysql\n")))}u.isMDXComponent=!0},49595:(e,t,n)=>{n.d(t,{A:()=>c,C:()=>d});var r=n(58168),a=n(96540),o=n(75489),i=n(44586),s=n(48295);function l(e){const t=(0,s.ir)();return(0,i.default)().siteConfig.customFields.githubLinkVersionToBaseUrl[t?.name??"current"]+e}function c(e){return a.createElement(o.default,(0,r.A)({},e,{to:l(e.to),target:"_blank"}))}function d(e){const t=e.text??"Example (Click Here)";return a.createElement(c,e,a.createElement("span",null,"\xa0"),a.createElement("img",{src:"https://img.shields.io/badge/-"+t+"-informational",alt:"Example (Click Here)"}))}}}]);