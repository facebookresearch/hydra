"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[8912],{15680:(e,n,t)=>{t.r(n),t.d(n,{MDXContext:()=>p,MDXProvider:()=>m,mdx:()=>y,useMDXComponents:()=>d,withMDXComponents:()=>c});var o=t(96540);function r(e,n,t){return n in e?Object.defineProperty(e,n,{value:t,enumerable:!0,configurable:!0,writable:!0}):e[n]=t,e}function a(){return a=Object.assign||function(e){for(var n=1;n<arguments.length;n++){var t=arguments[n];for(var o in t)Object.prototype.hasOwnProperty.call(t,o)&&(e[o]=t[o])}return e},a.apply(this,arguments)}function i(e,n){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(e);n&&(o=o.filter((function(n){return Object.getOwnPropertyDescriptor(e,n).enumerable}))),t.push.apply(t,o)}return t}function s(e){for(var n=1;n<arguments.length;n++){var t=null!=arguments[n]?arguments[n]:{};n%2?i(Object(t),!0).forEach((function(n){r(e,n,t[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):i(Object(t)).forEach((function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(t,n))}))}return e}function l(e,n){if(null==e)return{};var t,o,r=function(e,n){if(null==e)return{};var t,o,r={},a=Object.keys(e);for(o=0;o<a.length;o++)t=a[o],n.indexOf(t)>=0||(r[t]=e[t]);return r}(e,n);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);for(o=0;o<a.length;o++)t=a[o],n.indexOf(t)>=0||Object.prototype.propertyIsEnumerable.call(e,t)&&(r[t]=e[t])}return r}var p=o.createContext({}),c=function(e){return function(n){var t=d(n.components);return o.createElement(e,a({},n,{components:t}))}},d=function(e){var n=o.useContext(p),t=n;return e&&(t="function"==typeof e?e(n):s(s({},n),e)),t},m=function(e){var n=d(e.components);return o.createElement(p.Provider,{value:n},e.children)},u="mdxType",g={inlineCode:"code",wrapper:function(e){var n=e.children;return o.createElement(o.Fragment,{},n)}},f=o.forwardRef((function(e,n){var t=e.components,r=e.mdxType,a=e.originalType,i=e.parentName,p=l(e,["components","mdxType","originalType","parentName"]),c=d(t),m=r,u=c["".concat(i,".").concat(m)]||c[m]||g[m]||a;return t?o.createElement(u,s(s({ref:n},p),{},{components:t})):o.createElement(u,s({ref:n},p))}));function y(e,n){var t=arguments,r=n&&n.mdxType;if("string"==typeof e||r){var a=t.length,i=new Array(a);i[0]=f;var s={};for(var l in n)hasOwnProperty.call(n,l)&&(s[l]=n[l]);s.originalType=e,s[u]="string"==typeof e?e:r,i[1]=s;for(var p=2;p<a;p++)i[p]=t[p];return o.createElement.apply(null,i)}return o.createElement.apply(null,t)}f.displayName="MDXCreateElement"},92546:(e,n,t)=>{t.r(n),t.d(n,{assets:()=>l,contentTitle:()=>i,default:()=>m,frontMatter:()=>a,metadata:()=>s,toc:()=>p});var o=t(58168),r=(t(96540),t(15680));const a={id:"config_store",title:"Config Store API"},i=void 0,s={unversionedId:"tutorials/structured_config/config_store",id:"version-1.2/tutorials/structured_config/config_store",title:"Config Store API",description:"Throughout the rest of tutorials, we will be using ConfigStore to register dataclasses as input configs in Hydra.",source:"@site/versioned_docs/version-1.2/tutorials/structured_config/10_config_store.md",sourceDirName:"tutorials/structured_config",slug:"/tutorials/structured_config/config_store",permalink:"/docs/1.2/tutorials/structured_config/config_store",draft:!1,editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/versioned_docs/version-1.2/tutorials/structured_config/10_config_store.md",tags:[],version:"1.2",lastUpdatedBy:"P\xe1draig Brady",lastUpdatedAt:1652825677,formattedLastUpdatedAt:"May 17, 2022",sidebarPosition:10,frontMatter:{id:"config_store",title:"Config Store API"},sidebar:"docs",previous:{title:"Introduction to Structured Configs",permalink:"/docs/1.2/tutorials/structured_config/intro"},next:{title:"Minimal example",permalink:"/docs/1.2/tutorials/structured_config/minimal_example"}},l={},p=[{value:"API",id:"api",level:3},{value:"ConfigStore and YAML input configs",id:"configstore-and-yaml-input-configs",level:3},{value:"Example node values",id:"example-node-values",level:3}],c={toc:p},d="wrapper";function m(e){let{components:n,...t}=e;return(0,r.mdx)(d,(0,o.A)({},c,t,{components:n,mdxType:"MDXLayout"}),(0,r.mdx)("p",null,"Throughout the rest of tutorials, we will be using ",(0,r.mdx)("inlineCode",{parentName:"p"},"ConfigStore")," to register dataclasses as input configs in Hydra.\n",(0,r.mdx)("inlineCode",{parentName:"p"},"ConfigStore")," is a singleton storing configs in memory.\nThe primary API for interacting with the ",(0,r.mdx)("inlineCode",{parentName:"p"},"ConfigStore")," is the store method described below."),(0,r.mdx)("h3",{id:"api"},"API"),(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-python"},'class ConfigStore(metaclass=Singleton):\n    def store(\n        self,\n        name: str,\n        node: Any,\n        group: Optional[str] = None,\n        package: Optional[str] = "_group_",\n        provider: Optional[str] = None,\n    ) -> None:\n        """\n        Stores a config node into the repository\n        :param name: config name\n        :param node: config node, can be DictConfig, ListConfig,\n            Structured configs and even dict and list\n        :param group: config group, subgroup separator is \'/\',\n            for example hydra/launcher\n        :param package: Config node parent hierarchy.\n            Child separator is \'.\', for example foo.bar.baz\n        :param provider: the name of the module/app providing this config.\n            Helps debugging.\n        """\n    ...\n')),(0,r.mdx)("h3",{id:"configstore-and-yaml-input-configs"},"ConfigStore and YAML input configs"),(0,r.mdx)("p",null,(0,r.mdx)("inlineCode",{parentName:"p"},"ConfigStore")," has feature parity with YAML input configs. On top of that, it also provides typing validation.\n",(0,r.mdx)("inlineCode",{parentName:"p"},"ConfigStore")," can be used alone or together with YAML. We will see more examples later in this series of tutorials.\nFor now, let's see how the ",(0,r.mdx)("inlineCode",{parentName:"p"},"ConfigStore")," API translates into the YAML input configs, which we've become more familiar\nwith after the basic tutorials."),(0,r.mdx)("p",null,"Say we have a simple application and a ",(0,r.mdx)("inlineCode",{parentName:"p"},"db")," config group with a ",(0,r.mdx)("inlineCode",{parentName:"p"},"mysql")," option:"),(0,r.mdx)("div",{className:"row"},(0,r.mdx)("div",{className:"col col--5"},(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-python",metastring:'title="my_app.py"',title:'"my_app.py"'},'@hydra.main(version_base=None, config_path="conf")\ndef my_app(cfg: DictConfig) -> None:\n    print(OmegaConf.to_yaml(cfg))\n\n\nif __name__ == "__main__":\n    my_app()\n'))),(0,r.mdx)("div",{className:"col  col--4"},(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-text",metastring:'title="Directory layout"',title:'"Directory','layout"':!0},"\u251c\u2500 conf\n\u2502  \u2514\u2500 db\n\u2502      \u2514\u2500 mysql.yaml\n\u2514\u2500\u2500 my_app.py\n\n\n\n"))),(0,r.mdx)("div",{className:"col col--3"},(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="db/mysql.yaml"',title:'"db/mysql.yaml"'},"driver: mysql\nuser: omry\npassword: secret\n\n\n\n\n")))),(0,r.mdx)("p",null,"What if we want to add an ",(0,r.mdx)("inlineCode",{parentName:"p"},"postgresql")," option now? Yes, we can easily add a ",(0,r.mdx)("inlineCode",{parentName:"p"},"db/postgresql.yaml")," config group option. But\nthat is not the only way! We can also use ",(0,r.mdx)("inlineCode",{parentName:"p"},"ConfigStore")," to make another config group option for ",(0,r.mdx)("inlineCode",{parentName:"p"},"db")," available to Hydra."),(0,r.mdx)("p",null,"To achieve this, we add a few lines (highlighted) in the above ",(0,r.mdx)("inlineCode",{parentName:"p"},"my_app.py")," file:"),(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-python",metastring:'title="my_app.py" {1-9}',title:'"my_app.py"',"{1-9}":!0},'@dataclass\nclass PostgresSQLConfig:\n    driver: str = "postgresql"\n    user: str = "jieru"\n    password: str = "secret"\n\ncs = ConfigStore.instance()\n# Registering the Config class with the name `postgresql` with the config group `db`\ncs.store(name="postgresql", group="db", node=PostgresSQLConfig)\n\n@hydra.main(version_base=None, config_path="conf")\ndef my_app(cfg: DictConfig) -> None:\n    print(OmegaConf.to_yaml(cfg))\n\n\nif __name__ == "__main__":\n    my_app()\n')),(0,r.mdx)("p",null,"Now that our application has access to both ",(0,r.mdx)("inlineCode",{parentName:"p"},"db")," config group options, let's run the application to verify:"),(0,r.mdx)("div",{className:"row"},(0,r.mdx)("div",{className:"col col--6"},(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-commandline",metastring:'title="python my_app.py +db=mysql"',title:'"python',"my_app.py":!0,"+db":'mysql"'},"db:\n  driver: mysql\n  user: omry\n  password: secret\n\n"))),(0,r.mdx)("div",{className:"col  col--6"},(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-commandline",metastring:'title="python my_app.py +db=postgresql"',title:'"python',"my_app.py":!0,"+db":'postgresql"'},"db:\n  driver: postgresql\n  user: jieru\n  password: secret\n\n")))),(0,r.mdx)("h3",{id:"example-node-values"},"Example node values"),(0,r.mdx)("p",null,"A few examples of supported node values parameters:"),(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-python"},'from dataclasses import dataclass\n\nfrom hydra.core.config_store import ConfigStore\n\n@dataclass\nclass MySQLConfig:\n    host: str = "localhost"\n    port: int = 3306\n\ncs = ConfigStore.instance()\n\n# Using the type\ncs.store(name="config1", node=MySQLConfig)\n# Using an instance, overriding some default values\ncs.store(name="config2", node=MySQLConfig(host="test.db", port=3307))\n# Using a dictionary, forfeiting runtime type safety\ncs.store(name="config3", node={"host": "localhost", "port": 3308})\n')))}m.isMDXComponent=!0}}]);