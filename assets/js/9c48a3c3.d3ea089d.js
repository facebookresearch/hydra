"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[1461],{15680:(e,t,n)=>{n.r(t),n.d(t,{MDXContext:()=>d,MDXProvider:()=>p,mdx:()=>g,useMDXComponents:()=>c,withMDXComponents:()=>u});var a=n(96540);function r(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function o(){return o=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var a in n)Object.prototype.hasOwnProperty.call(n,a)&&(e[a]=n[a])}return e},o.apply(this,arguments)}function i(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);t&&(a=a.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,a)}return n}function l(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?i(Object(n),!0).forEach((function(t){r(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):i(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function s(e,t){if(null==e)return{};var n,a,r=function(e,t){if(null==e)return{};var n,a,r={},o=Object.keys(e);for(a=0;a<o.length;a++)n=o[a],t.indexOf(n)>=0||(r[n]=e[n]);return r}(e,t);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(e);for(a=0;a<o.length;a++)n=o[a],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(r[n]=e[n])}return r}var d=a.createContext({}),u=function(e){return function(t){var n=c(t.components);return a.createElement(e,o({},t,{components:n}))}},c=function(e){var t=a.useContext(d),n=t;return e&&(n="function"==typeof e?e(t):l(l({},t),e)),n},p=function(e){var t=c(e.components);return a.createElement(d.Provider,{value:t},e.children)},m={inlineCode:"code",wrapper:function(e){var t=e.children;return a.createElement(a.Fragment,{},t)}},f=a.forwardRef((function(e,t){var n=e.components,r=e.mdxType,o=e.originalType,i=e.parentName,d=s(e,["components","mdxType","originalType","parentName"]),u=c(n),p=r,f=u["".concat(i,".").concat(p)]||u[p]||m[p]||o;return n?a.createElement(f,l(l({ref:t},d),{},{components:n})):a.createElement(f,l({ref:t},d))}));function g(e,t){var n=arguments,r=t&&t.mdxType;if("string"==typeof e||r){var o=n.length,i=new Array(o);i[0]=f;var l={};for(var s in t)hasOwnProperty.call(t,s)&&(l[s]=t[s]);l.originalType=e,l.mdxType="string"==typeof e?e:r,i[1]=l;for(var d=2;d<o;d++)i[d]=n[d];return a.createElement.apply(null,i)}return a.createElement.apply(null,n)}f.displayName="MDXCreateElement"},49595:(e,t,n)=>{n.d(t,{A:()=>s,C:()=>d});var a=n(58168),r=n(96540),o=n(75489),i=n(44586),l=n(74098);function s(e){return r.createElement(o.default,(0,a.A)({},e,{to:(t=e.to,s=(0,l.useActiveVersion)(),(0,i.default)().siteConfig.customFields.githubLinkVersionToBaseUrl[null!=(n=null==s?void 0:s.name)?n:"current"]+t),target:"_blank"}));var t,n,s}function d(e){var t,n=null!=(t=e.text)?t:"Example (Click Here)";return r.createElement(s,e,r.createElement("span",null,"\xa0"),r.createElement("img",{src:"https://img.shields.io/badge/-"+n+"-informational",alt:"Example (Click Here)"}))}},34578:(e,t,n)=>{n.r(t),n.d(t,{contentTitle:()=>d,default:()=>m,frontMatter:()=>s,metadata:()=>u,toc:()=>c});var a=n(58168),r=n(98587),o=(n(96540),n(15680)),i=n(49595),l=["components"],s={id:"defaults",title:"Defaults List"},d=void 0,u={unversionedId:"tutorials/structured_config/defaults",id:"version-1.1/tutorials/structured_config/defaults",title:"Defaults List",description:"You can define a defaults list in your primary Structured Config just like you can in your primary config.yaml file.",source:"@site/versioned_docs/version-1.1/tutorials/structured_config/4_defaults.md",sourceDirName:"tutorials/structured_config",slug:"/tutorials/structured_config/defaults",permalink:"/docs/1.1/tutorials/structured_config/defaults",editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/versioned_docs/version-1.1/tutorials/structured_config/4_defaults.md",tags:[],version:"1.1",lastUpdatedBy:"dependabot[bot]",lastUpdatedAt:1730135614,formattedLastUpdatedAt:"10/28/2024",sidebarPosition:4,frontMatter:{id:"defaults",title:"Defaults List"},sidebar:"version-1.1/docs",previous:{title:"Config Groups",permalink:"/docs/1.1/tutorials/structured_config/config_groups"},next:{title:"Structured Config schema",permalink:"/docs/1.1/tutorials/structured_config/schema"}},c=[{value:"A Note about composition order",id:"a-note-about-composition-order",children:[],level:3},{value:"Requiring users to specify a default list value",id:"requiring-users-to-specify-a-default-list-value",children:[],level:3}],p={toc:c};function m(e){var t=e.components,n=(0,r.A)(e,l);return(0,o.mdx)("wrapper",(0,a.A)({},p,n,{components:t,mdxType:"MDXLayout"}),(0,o.mdx)(i.C,{to:"examples/tutorials/structured_configs/4_defaults/my_app.py",mdxType:"ExampleGithubLink"}),(0,o.mdx)("p",null,"You can define a defaults list in your primary Structured Config just like you can in your primary ",(0,o.mdx)("inlineCode",{parentName:"p"},"config.yaml")," file.\nThe example below extends the previous example by adding a defaults list that will load ",(0,o.mdx)("inlineCode",{parentName:"p"},"db=mysql")," by default."),(0,o.mdx)("div",{class:"alert alert--info",role:"alert"},"NOTE: You can still place your defaults list in your primary (YAML) config file (Example in next page)."),(0,o.mdx)("br",null),(0,o.mdx)("pre",null,(0,o.mdx)("code",{parentName:"pre",className:"language-python",metastring:"{11-14,19,25}","{11-14,19,25}":!0},'from dataclasses import dataclass\n\nimport hydra\nfrom hydra.core.config_store import ConfigStore\nfrom omegaconf import MISSING, OmegaConf\n\n@dataclass\nclass MySQLConfig:\n    ...\n\n@dataclass\nclass PostGreSQLConfig:\n    ...\n\ndefaults = [\n    # Load the config "mysql" from the config group "db"\n    {"db": "mysql"}\n]\n\n@dataclass\nclass Config:\n    # this is unfortunately verbose due to @dataclass limitations\n    defaults: List[Any] = field(default_factory=lambda: defaults)\n\n    # Hydra will populate this field based on the defaults list\n    db: Any = MISSING\n\ncs = ConfigStore.instance()\ncs.store(group="db", name="mysql", node=MySQLConfig)\ncs.store(group="db", name="postgresql", node=PostGreSQLConfig)\ncs.store(name="config", node=Config)\n\n\n@hydra.main(config_path=None, config_name="config")\ndef my_app(cfg: Config) -> None:\n    print(OmegaConf.to_yaml(cfg))\n\n\nif __name__ == "__main__":\n    my_app()\n')),(0,o.mdx)("p",null,"Running ",(0,o.mdx)("inlineCode",{parentName:"p"},"my_app.py")," loads the mysql config option by default:"),(0,o.mdx)("pre",null,(0,o.mdx)("code",{parentName:"pre",className:"language-yaml"},"$ python my_app.py\ndb:\n  driver: mysql\n  ...\n")),(0,o.mdx)("p",null,"You can override the default option via the command line:"),(0,o.mdx)("pre",null,(0,o.mdx)("code",{parentName:"pre",className:"language-yaml"},"$ python my_app.py db=postgresql\ndb:\n  driver: postgresql\n  ...\n")),(0,o.mdx)("h3",{id:"a-note-about-composition-order"},"A Note about composition order"),(0,o.mdx)("p",null,"The default composition order in Hydra is that values defined in a config are merged into values introduced from configs in the Defaults List - or in other words - overriding them.\nThis behavior can be unintuitive when your primary config is a Structured Config, like in the example above.\nFor example, if the primary config is:"),(0,o.mdx)("pre",null,(0,o.mdx)("code",{parentName:"pre",className:"language-python",metastring:"{6}","{6}":!0},'@dataclass\nclass Config:\n    defaults: List[Any] = field(default_factory=lambda:  [\n        "debug/activate",\n        # If you do not specify _self_, it will be appended to the end of the defaults list by default.\n        "_self_"\n    ])\n\n    debug: bool = False\n')),(0,o.mdx)("p",null,"And ",(0,o.mdx)("inlineCode",{parentName:"p"},"debug/activate.yaml")," is overriding the ",(0,o.mdx)("inlineCode",{parentName:"p"},"debug")," flag to ",(0,o.mdx)("inlineCode",{parentName:"p"},"True"),", the composition order would be such that debug ends up being ",(0,o.mdx)("inlineCode",{parentName:"p"},"False"),".",(0,o.mdx)("br",{parentName:"p"}),"\n","To get ",(0,o.mdx)("inlineCode",{parentName:"p"},"debug/activate.yaml")," to override this config, explicitly specify ",(0,o.mdx)("inlineCode",{parentName:"p"},"_self_")," before ",(0,o.mdx)("inlineCode",{parentName:"p"},"debug/activate.yaml"),":"),(0,o.mdx)("pre",null,(0,o.mdx)("code",{parentName:"pre",className:"language-python",metastring:"{4}","{4}":!0},'@dataclass\nclass Config:\n    defaults: List[Any] = field(default_factory=lambda:  [\n        "_self_",\n        "debug/activate",\n    ])\n\n    debug: bool = False\n')),(0,o.mdx)("p",null,"See ",(0,o.mdx)("a",{parentName:"p",href:"/docs/1.1/advanced/defaults_list#composition-order"},"Compositon Order")," for more information."),(0,o.mdx)("h3",{id:"requiring-users-to-specify-a-default-list-value"},"Requiring users to specify a default list value"),(0,o.mdx)("p",null,"Set ",(0,o.mdx)("inlineCode",{parentName:"p"},"db")," as ",(0,o.mdx)("inlineCode",{parentName:"p"},"MISSING")," to require the user to specify a value on the command line."),(0,o.mdx)("div",{className:"row"},(0,o.mdx)("div",{className:"col col--6"},(0,o.mdx)("pre",null,(0,o.mdx)("code",{parentName:"pre",className:"language-python",metastring:'title="Defaults list with a missing db"',title:'"Defaults',list:!0,with:!0,a:!0,missing:!0,'db"':!0},'defaults = [\n    {"db": MISSING}\n]\n\n\n'))),(0,o.mdx)("div",{className:"col  col--6"},(0,o.mdx)("pre",null,(0,o.mdx)("code",{parentName:"pre",className:"language-text",metastring:'title="Output"',title:'"Output"'},"$ python my_app.py\nYou must specify 'db', e.g, db=<OPTION>\nAvailable options:\n        mysql\n        postgresql\n")))))}m.isMDXComponent=!0}}]);