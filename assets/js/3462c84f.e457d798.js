"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[7305],{15680:(e,n,t)=>{t.r(n),t.d(n,{MDXContext:()=>l,MDXProvider:()=>d,mdx:()=>y,useMDXComponents:()=>m,withMDXComponents:()=>c});var r=t(96540);function o(e,n,t){return n in e?Object.defineProperty(e,n,{value:t,enumerable:!0,configurable:!0,writable:!0}):e[n]=t,e}function a(){return a=Object.assign||function(e){for(var n=1;n<arguments.length;n++){var t=arguments[n];for(var r in t)Object.prototype.hasOwnProperty.call(t,r)&&(e[r]=t[r])}return e},a.apply(this,arguments)}function i(e,n){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);n&&(r=r.filter((function(n){return Object.getOwnPropertyDescriptor(e,n).enumerable}))),t.push.apply(t,r)}return t}function p(e){for(var n=1;n<arguments.length;n++){var t=null!=arguments[n]?arguments[n]:{};n%2?i(Object(t),!0).forEach((function(n){o(e,n,t[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):i(Object(t)).forEach((function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(t,n))}))}return e}function s(e,n){if(null==e)return{};var t,r,o=function(e,n){if(null==e)return{};var t,r,o={},a=Object.keys(e);for(r=0;r<a.length;r++)t=a[r],n.indexOf(t)>=0||(o[t]=e[t]);return o}(e,n);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);for(r=0;r<a.length;r++)t=a[r],n.indexOf(t)>=0||Object.prototype.propertyIsEnumerable.call(e,t)&&(o[t]=e[t])}return o}var l=r.createContext({}),c=function(e){return function(n){var t=m(n.components);return r.createElement(e,a({},n,{components:t}))}},m=function(e){var n=r.useContext(l),t=n;return e&&(t="function"==typeof e?e(n):p(p({},n),e)),t},d=function(e){var n=m(e.components);return r.createElement(l.Provider,{value:n},e.children)},u="mdxType",g={inlineCode:"code",wrapper:function(e){var n=e.children;return r.createElement(r.Fragment,{},n)}},f=r.forwardRef((function(e,n){var t=e.components,o=e.mdxType,a=e.originalType,i=e.parentName,l=s(e,["components","mdxType","originalType","parentName"]),c=m(t),d=o,u=c["".concat(i,".").concat(d)]||c[d]||g[d]||a;return t?r.createElement(u,p(p({ref:n},l),{},{components:t})):r.createElement(u,p({ref:n},l))}));function y(e,n){var t=arguments,o=n&&n.mdxType;if("string"==typeof e||o){var a=t.length,i=new Array(a);i[0]=f;var p={};for(var s in n)hasOwnProperty.call(n,s)&&(p[s]=n[s]);p.originalType=e,p[u]="string"==typeof e?e:o,i[1]=p;for(var l=2;l<a;l++)i[l]=t[l];return r.createElement.apply(null,i)}return r.createElement.apply(null,t)}f.displayName="MDXCreateElement"},49595:(e,n,t)=>{t.d(n,{A:()=>l,C:()=>c});var r=t(58168),o=t(96540),a=t(75489),i=t(44586),p=t(48295);function s(e){const n=(0,p.ir)();return(0,i.default)().siteConfig.customFields.githubLinkVersionToBaseUrl[n?.name??"current"]+e}function l(e){return o.createElement(a.default,(0,r.A)({},e,{to:s(e.to),target:"_blank"}))}function c(e){const n=e.text??"Example (Click Here)";return o.createElement(l,e,o.createElement("span",null,"\xa0"),o.createElement("img",{src:"https://img.shields.io/badge/-"+n+"-informational",alt:"Example (Click Here)"}))}},85940:(e,n,t)=>{t.r(n),t.d(n,{assets:()=>l,contentTitle:()=>p,default:()=>u,frontMatter:()=>i,metadata:()=>s,toc:()=>c});var r=t(58168),o=(t(96540),t(15680)),a=t(49595);const i={id:"config_groups",title:"Grouping config files"},p=void 0,s={unversionedId:"tutorials/basic/your_first_app/config_groups",id:"version-1.1/tutorials/basic/your_first_app/config_groups",title:"Grouping config files",description:"Suppose you want to benchmark your application on each of PostgreSQL and MySQL. To do this, use config groups.",source:"@site/versioned_docs/version-1.1/tutorials/basic/your_first_app/4_config_groups.md",sourceDirName:"tutorials/basic/your_first_app",slug:"/tutorials/basic/your_first_app/config_groups",permalink:"/docs/1.1/tutorials/basic/your_first_app/config_groups",draft:!1,editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/versioned_docs/version-1.1/tutorials/basic/your_first_app/4_config_groups.md",tags:[],version:"1.1",lastUpdatedBy:"dependabot[bot]",lastUpdatedAt:1742161400,formattedLastUpdatedAt:"Mar 16, 2025",sidebarPosition:4,frontMatter:{id:"config_groups",title:"Grouping config files"},sidebar:"docs",previous:{title:"Using the config object",permalink:"/docs/1.1/tutorials/basic/your_first_app/using_config"},next:{title:"Selecting default configs",permalink:"/docs/1.1/tutorials/basic/your_first_app/defaults"}},l={},c=[{value:"Creating config groups",id:"creating-config-groups",level:3},{value:"Using config groups",id:"using-config-groups",level:3},{value:"Advanced topics",id:"advanced-topics",level:3}],m={toc:c},d="wrapper";function u(e){let{components:n,...t}=e;return(0,o.mdx)(d,(0,r.A)({},m,t,{components:n,mdxType:"MDXLayout"}),(0,o.mdx)(a.C,{to:"examples/tutorials/basic/your_first_hydra_app/4_config_groups",mdxType:"ExampleGithubLink"}),(0,o.mdx)("p",null,"Suppose you want to benchmark your application on each of PostgreSQL and MySQL. To do this, use config groups. "),(0,o.mdx)("p",null,"A ",(0,o.mdx)("em",{parentName:"p"},(0,o.mdx)("strong",{parentName:"em"},"Config Group"))," is a named group with a set of valid options.\nSelecting a non-existent config option generates an error message with the valid options."),(0,o.mdx)("h3",{id:"creating-config-groups"},"Creating config groups"),(0,o.mdx)("p",null,"To create a config group, create a directory, e.g. ",(0,o.mdx)("inlineCode",{parentName:"p"},"db"),", to hold a file for each database configuration option.\nSince we are expecting to have multiple config groups, we will proactively move all the configuration files\ninto a ",(0,o.mdx)("inlineCode",{parentName:"p"},"conf")," directory."),(0,o.mdx)("div",{className:"row"},(0,o.mdx)("div",{className:"col col--4"},(0,o.mdx)("pre",null,(0,o.mdx)("code",{parentName:"pre",className:"language-text",metastring:'title="Directory layout"',title:'"Directory','layout"':!0},"\u251c\u2500 conf\n\u2502  \u2514\u2500 db\n\u2502      \u251c\u2500 mysql.yaml\n\u2502      \u2514\u2500 postgresql.yaml\n\u2514\u2500\u2500 my_app.py\n"))),(0,o.mdx)("div",{className:"col col--4"},(0,o.mdx)("pre",null,(0,o.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="db/mysql.yaml"',title:'"db/mysql.yaml"'},"driver: mysql\nuser: omry\npassword: secret\n\n\n"))),(0,o.mdx)("div",{className:"col col--4"},(0,o.mdx)("pre",null,(0,o.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="db/postgresql.yaml"',title:'"db/postgresql.yaml"'},"driver: postgresql\nuser: postgres_user\npassword: drowssap\ntimeout: 10\n\n")))),(0,o.mdx)("h3",{id:"using-config-groups"},"Using config groups"),(0,o.mdx)("p",null,"Since we moved all the configs into the ",(0,o.mdx)("inlineCode",{parentName:"p"},"conf")," directory, we need to tell Hydra where to find them using the ",(0,o.mdx)("inlineCode",{parentName:"p"},"config_path")," parameter.\n",(0,o.mdx)("strong",{parentName:"p"},(0,o.mdx)("inlineCode",{parentName:"strong"},"config_path")," is a directory relative to ",(0,o.mdx)("inlineCode",{parentName:"strong"},"my_app.py")),"."),(0,o.mdx)("pre",null,(0,o.mdx)("code",{parentName:"pre",className:"language-python",metastring:'title="my_app.py" {4}',title:'"my_app.py"',"{4}":!0},'from omegaconf import DictConfig, OmegaConf\nimport hydra\n\n@hydra.main(config_path="conf")\ndef my_app(cfg: DictConfig) -> None:\n    print(OmegaConf.to_yaml(cfg))\n\nif __name__ == "__main__":\n    my_app()\n')),(0,o.mdx)("p",null,"Running ",(0,o.mdx)("inlineCode",{parentName:"p"},"my_app.py")," without requesting a configuration will print an empty config."),(0,o.mdx)("pre",null,(0,o.mdx)("code",{parentName:"pre",className:"language-yaml"},"$ python my_app.py\n{}\n")),(0,o.mdx)("p",null,"Select an item from a config group with ",(0,o.mdx)("inlineCode",{parentName:"p"},"+GROUP=OPTION"),", e.g: "),(0,o.mdx)("pre",null,(0,o.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:"{2}","{2}":!0},"$ python my_app.py +db=postgresql\ndb:\n  driver: postgresql\n  pass: drowssap\n  timeout: 10\n  user: postgres_user\n")),(0,o.mdx)("p",null,"By default, the config group determines where the config content is placed inside the final config object.\nIn Hydra, the path to the config content is referred to as the config ",(0,o.mdx)("inlineCode",{parentName:"p"},"package"),".\nThe package of ",(0,o.mdx)("inlineCode",{parentName:"p"},"db/postgresql.yaml")," is ",(0,o.mdx)("inlineCode",{parentName:"p"},"db"),":"),(0,o.mdx)("p",null,"Like before, you can still override individual values in the resulting config:"),(0,o.mdx)("pre",null,(0,o.mdx)("code",{parentName:"pre",className:"language-yaml"},"$ python my_app.py +db=postgresql db.timeout=20\ndb:\n  driver: postgresql\n  pass: drowssap\n  timeout: 20\n  user: postgres_user\n")),(0,o.mdx)("h3",{id:"advanced-topics"},"Advanced topics"),(0,o.mdx)("ul",null,(0,o.mdx)("li",{parentName:"ul"},"Config content can be relocated via package overrides. See ",(0,o.mdx)("a",{parentName:"li",href:"/docs/1.1/advanced/overriding_packages"},"Reference Manual/Packages"),".    "),(0,o.mdx)("li",{parentName:"ul"},"Multiple options can be selected from the same Config Group by specifying them as a list.",(0,o.mdx)("br",{parentName:"li"}),"See ",(0,o.mdx)("a",{parentName:"li",href:"/docs/1.1/patterns/select_multiple_configs_from_config_group"},"Common Patterns/Selecting multiple configs from a Config Group"))))}u.isMDXComponent=!0}}]);