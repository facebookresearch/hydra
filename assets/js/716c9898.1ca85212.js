"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[1442],{15680:(e,t,n)=>{n.r(t),n.d(t,{MDXContext:()=>d,MDXProvider:()=>p,mdx:()=>y,useMDXComponents:()=>u,withMDXComponents:()=>m});var a=n(96540);function o(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function r(){return r=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var a in n)Object.prototype.hasOwnProperty.call(n,a)&&(e[a]=n[a])}return e},r.apply(this,arguments)}function i(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);t&&(a=a.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,a)}return n}function l(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?i(Object(n),!0).forEach((function(t){o(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):i(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function s(e,t){if(null==e)return{};var n,a,o=function(e,t){if(null==e)return{};var n,a,o={},r=Object.keys(e);for(a=0;a<r.length;a++)n=r[a],t.indexOf(n)>=0||(o[n]=e[n]);return o}(e,t);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);for(a=0;a<r.length;a++)n=r[a],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(o[n]=e[n])}return o}var d=a.createContext({}),m=function(e){return function(t){var n=u(t.components);return a.createElement(e,r({},t,{components:n}))}},u=function(e){var t=a.useContext(d),n=t;return e&&(n="function"==typeof e?e(t):l(l({},t),e)),n},p=function(e){var t=u(e.components);return a.createElement(d.Provider,{value:t},e.children)},f="mdxType",c={inlineCode:"code",wrapper:function(e){var t=e.children;return a.createElement(a.Fragment,{},t)}},g=a.forwardRef((function(e,t){var n=e.components,o=e.mdxType,r=e.originalType,i=e.parentName,d=s(e,["components","mdxType","originalType","parentName"]),m=u(n),p=o,f=m["".concat(i,".").concat(p)]||m[p]||c[p]||r;return n?a.createElement(f,l(l({ref:t},d),{},{components:n})):a.createElement(f,l({ref:t},d))}));function y(e,t){var n=arguments,o=t&&t.mdxType;if("string"==typeof e||o){var r=n.length,i=new Array(r);i[0]=g;var l={};for(var s in t)hasOwnProperty.call(t,s)&&(l[s]=t[s]);l.originalType=e,l[f]="string"==typeof e?e:o,i[1]=l;for(var d=2;d<r;d++)i[d]=n[d];return a.createElement.apply(null,i)}return a.createElement.apply(null,n)}g.displayName="MDXCreateElement"},43425:(e,t,n)=>{n.r(t),n.d(t,{assets:()=>d,contentTitle:()=>l,default:()=>f,frontMatter:()=>i,metadata:()=>s,toc:()=>m});var a=n(58168),o=(n(96540),n(15680)),r=n(49595);const i={id:"defaults",title:"Selecting default configs"},l=void 0,s={unversionedId:"tutorials/basic/your_first_app/defaults",id:"version-1.2/tutorials/basic/your_first_app/defaults",title:"Selecting default configs",description:"After office politics, you decide that you want to use MySQL by default.",source:"@site/versioned_docs/version-1.2/tutorials/basic/your_first_app/5_defaults.md",sourceDirName:"tutorials/basic/your_first_app",slug:"/tutorials/basic/your_first_app/defaults",permalink:"/docs/1.2/tutorials/basic/your_first_app/defaults",draft:!1,editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/versioned_docs/version-1.2/tutorials/basic/your_first_app/5_defaults.md",tags:[],version:"1.2",lastUpdatedBy:"dependabot[bot]",lastUpdatedAt:1743717584,formattedLastUpdatedAt:"Apr 3, 2025",sidebarPosition:5,frontMatter:{id:"defaults",title:"Selecting default configs"},sidebar:"docs",previous:{title:"Grouping config files",permalink:"/docs/1.2/tutorials/basic/your_first_app/config_groups"},next:{title:"Putting it all together",permalink:"/docs/1.2/tutorials/basic/your_first_app/composition"}},d={},m=[{value:"Config group defaults",id:"config-group-defaults",level:3},{value:"Overriding a config group default",id:"overriding-a-config-group-default",level:4},{value:"Composition order of primary config",id:"composition-order-of-primary-config",level:3},{value:"Non-config group defaults",id:"non-config-group-defaults",level:3}],u={toc:m},p="wrapper";function f(e){let{components:t,...n}=e;return(0,o.mdx)(p,(0,a.A)({},u,n,{components:t,mdxType:"MDXLayout"}),(0,o.mdx)(r.C,{to:"examples/tutorials/basic/your_first_hydra_app/5_defaults",mdxType:"ExampleGithubLink"}),(0,o.mdx)("p",null,"After office politics, you decide that you want to use MySQL by default.\nYou no longer want to type ",(0,o.mdx)("inlineCode",{parentName:"p"},"+db=mysql")," every time you run your application."),(0,o.mdx)("p",null,"You can add a ",(0,o.mdx)("strong",{parentName:"p"},"Default List")," to your config file.\nA ",(0,o.mdx)("strong",{parentName:"p"},"Defaults List")," is a list telling Hydra how to compose the final config object.\nBy convention, it is the first item in the config."),(0,o.mdx)("h3",{id:"config-group-defaults"},"Config group defaults"),(0,o.mdx)("pre",null,(0,o.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="config.yaml"',title:'"config.yaml"'},"defaults:\n  - db: mysql\n")),(0,o.mdx)("p",null,"Remember to specify the ",(0,o.mdx)("inlineCode",{parentName:"p"},"config_name"),":"),(0,o.mdx)("pre",null,(0,o.mdx)("code",{parentName:"pre",className:"language-python"},'from omegaconf import DictConfig, OmegaConf\nimport hydra\n\n@hydra.main(version_base=None, config_path="conf", config_name="config")\ndef my_app(cfg: DictConfig) -> None:\n    print(OmegaConf.to_yaml(cfg))\n\nif __name__ == "__main__":\n    my_app()\n')),(0,o.mdx)("p",null,"When you run the updated application, MySQL is loaded by default."),(0,o.mdx)("pre",null,(0,o.mdx)("code",{parentName:"pre",className:"language-yaml"},"$ python my_app.py\ndb:\n  driver: mysql\n  pass: secret\n  user: omry\n")),(0,o.mdx)("p",null,"You can have multiple items in the defaults list, e.g."),(0,o.mdx)("pre",null,(0,o.mdx)("code",{parentName:"pre",className:"language-yaml"},"defaults:\n - db: mysql\n - db/mysql/engine: innodb\n")),(0,o.mdx)("p",null,"The defaults are ordered:"),(0,o.mdx)("ul",null,(0,o.mdx)("li",{parentName:"ul"},"If multiple configs define the same value, the last one wins. "),(0,o.mdx)("li",{parentName:"ul"},"If multiple configs contribute to the same dictionary, the result is the combined dictionary.")),(0,o.mdx)("h4",{id:"overriding-a-config-group-default"},"Overriding a config group default"),(0,o.mdx)("p",null,"You can still load PostgreSQL, and override individual values."),(0,o.mdx)("pre",null,(0,o.mdx)("code",{parentName:"pre",className:"language-yaml"},"$ python my_app.py db=postgresql db.timeout=20\ndb:\n  driver: postgresql\n  pass: drowssap\n  timeout: 20\n  user: postgres_user\n")),(0,o.mdx)("p",null,"You can remove a default entry from the defaults list by prefixing it with ~:"),(0,o.mdx)("pre",null,(0,o.mdx)("code",{parentName:"pre",className:"language-yaml"},"$ python my_app.py ~db\n{}\n")),(0,o.mdx)("h3",{id:"composition-order-of-primary-config"},"Composition order of primary config"),(0,o.mdx)("p",null,"Your primary config can contain both config values and a Defaults List.\nIn such cases, you should add the ",(0,o.mdx)("inlineCode",{parentName:"p"},"_self_")," keyword to your defaults list to specify the composition order of the config file relative to the items in the defaults list."),(0,o.mdx)("ul",null,(0,o.mdx)("li",{parentName:"ul"},"If you want your primary config to override the values of configs from the Defaults List, append ",(0,o.mdx)("inlineCode",{parentName:"li"},"_self_")," to the end of the Defaults List."),(0,o.mdx)("li",{parentName:"ul"},"If you want the configs from the Defaults List to override the values in your primary config, insert ",(0,o.mdx)("inlineCode",{parentName:"li"},"_self_")," as the first item in your Defaults List.")),(0,o.mdx)("div",{className:"row"},(0,o.mdx)("div",{className:"col col--6"},(0,o.mdx)("pre",null,(0,o.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="config.yaml" {3}',title:'"config.yaml"',"{3}":!0},"defaults:\n  - db: mysql\n  - _self_\n\ndb:\n  user: root\n"))),(0,o.mdx)("div",{className:"col  col--6"},(0,o.mdx)("pre",null,(0,o.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="Result config: db.user from config.yaml" {4}',title:'"Result',"config:":!0,"db.user":!0,from:!0,'config.yaml"':!0,"{4}":!0},"db:\n  driver: mysql  # db/mysql.yaml\n  pass: secret   # db/mysql.yaml \n  user: root     # config.yaml\n\n\n"))),(0,o.mdx)("div",{className:"col col--6"},(0,o.mdx)("pre",null,(0,o.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="config.yaml" {2}',title:'"config.yaml"',"{2}":!0},"defaults:\n  - _self_\n  - db: mysql\n\ndb:\n  user: root\n"))),(0,o.mdx)("div",{className:"col  col--6"},(0,o.mdx)("pre",null,(0,o.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="Result config: All values from db/mysql" {4}',title:'"Result',"config:":!0,All:!0,values:!0,from:!0,'db/mysql"':!0,"{4}":!0},"db:\n  driver: mysql # db/mysql.yaml\n  pass: secret  # db/mysql.yaml\n  user: omry    # db/mysql.yaml\n\n\n")))),(0,o.mdx)("p",null,"See ",(0,o.mdx)("a",{parentName:"p",href:"/docs/1.2/advanced/defaults_list#composition-order"},"Composition Order")," for more information."),(0,o.mdx)("admonition",{type:"info"},(0,o.mdx)("p",{parentName:"admonition"},"The default composition order changed between Hydra 1.0 and Hydra 1.1."),(0,o.mdx)("ul",{parentName:"admonition"},(0,o.mdx)("li",{parentName:"ul"},(0,o.mdx)("strong",{parentName:"li"},"Hydra 1.0"),": Configs from the defaults list are overriding the primary config"),(0,o.mdx)("li",{parentName:"ul"},(0,o.mdx)("strong",{parentName:"li"},"Hydra 1.1"),": A config is overriding the configs from the defaults list.")),(0,o.mdx)("p",{parentName:"admonition"},"To mitigate confusion, Hydra 1.1 issue a warning if the primary config contains both Default List and Config values, and ",(0,o.mdx)("inlineCode",{parentName:"p"},"_self_")," is not specified in the Defaults List.",(0,o.mdx)("br",{parentName:"p"}),"\n","The warning will disappear if you add ",(0,o.mdx)("inlineCode",{parentName:"p"},"_self_")," to the Defaults List based on the desired behavior.")),(0,o.mdx)("h3",{id:"non-config-group-defaults"},"Non-config group defaults"),(0,o.mdx)("p",null,"Sometimes a config file does not belong in any config group.\nYou can still load it by default. Here is an example for ",(0,o.mdx)("inlineCode",{parentName:"p"},"some_file.yaml"),"."),(0,o.mdx)("pre",null,(0,o.mdx)("code",{parentName:"pre",className:"language-yaml"},"defaults:\n  - some_file\n")),(0,o.mdx)("p",null,"Config files that are not part of a config group will always be loaded. They cannot be overridden.",(0,o.mdx)("br",{parentName:"p"}),"\n","Prefer using a config group."),(0,o.mdx)("admonition",{type:"info"},(0,o.mdx)("p",{parentName:"admonition"},"For more information about the Defaults List see ",(0,o.mdx)("a",{parentName:"p",href:"/docs/1.2/advanced/defaults_list"},"Reference Manual/The Defaults List"),".")))}f.isMDXComponent=!0},49595:(e,t,n)=>{n.d(t,{A:()=>d,C:()=>m});var a=n(58168),o=n(96540),r=n(75489),i=n(44586),l=n(48295);function s(e){const t=(0,l.ir)();return(0,i.default)().siteConfig.customFields.githubLinkVersionToBaseUrl[t?.name??"current"]+e}function d(e){return o.createElement(r.default,(0,a.A)({},e,{to:s(e.to),target:"_blank"}))}function m(e){const t=e.text??"Example (Click Here)";return o.createElement(d,e,o.createElement("span",null,"\xa0"),o.createElement("img",{src:"https://img.shields.io/badge/-"+t+"-informational",alt:"Example (Click Here)"}))}}}]);