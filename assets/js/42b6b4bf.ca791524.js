"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[7663],{15680:(e,t,n)=>{n.r(t),n.d(t,{MDXContext:()=>u,MDXProvider:()=>c,mdx:()=>y,useMDXComponents:()=>d,withMDXComponents:()=>p});var r=n(96540);function a(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function o(){return o=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var r in n)Object.prototype.hasOwnProperty.call(n,r)&&(e[r]=n[r])}return e},o.apply(this,arguments)}function i(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,r)}return n}function l(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?i(Object(n),!0).forEach((function(t){a(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):i(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function s(e,t){if(null==e)return{};var n,r,a=function(e,t){if(null==e)return{};var n,r,a={},o=Object.keys(e);for(r=0;r<o.length;r++)n=o[r],t.indexOf(n)>=0||(a[n]=e[n]);return a}(e,t);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(e);for(r=0;r<o.length;r++)n=o[r],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(a[n]=e[n])}return a}var u=r.createContext({}),p=function(e){return function(t){var n=d(t.components);return r.createElement(e,o({},t,{components:n}))}},d=function(e){var t=r.useContext(u),n=t;return e&&(n="function"==typeof e?e(t):l(l({},t),e)),n},c=function(e){var t=d(e.components);return r.createElement(u.Provider,{value:t},e.children)},f="mdxType",m={inlineCode:"code",wrapper:function(e){var t=e.children;return r.createElement(r.Fragment,{},t)}},g=r.forwardRef((function(e,t){var n=e.components,a=e.mdxType,o=e.originalType,i=e.parentName,u=s(e,["components","mdxType","originalType","parentName"]),p=d(n),c=a,f=p["".concat(i,".").concat(c)]||p[c]||m[c]||o;return n?r.createElement(f,l(l({ref:t},u),{},{components:n})):r.createElement(f,l({ref:t},u))}));function y(e,t){var n=arguments,a=t&&t.mdxType;if("string"==typeof e||a){var o=n.length,i=new Array(o);i[0]=g;var l={};for(var s in t)hasOwnProperty.call(t,s)&&(l[s]=t[s]);l.originalType=e,l[f]="string"==typeof e?e:a,i[1]=l;for(var u=2;u<o;u++)i[u]=n[u];return r.createElement.apply(null,i)}return r.createElement.apply(null,n)}g.displayName="MDXCreateElement"},29163:(e,t,n)=>{n.r(t),n.d(t,{assets:()=>u,contentTitle:()=>l,default:()=>f,frontMatter:()=>i,metadata:()=>s,toc:()=>p});var r=n(58168),a=(n(96540),n(15680)),o=n(49595);const i={id:"defaults",title:"Selecting defaults for config groups"},l=void 0,s={unversionedId:"tutorials/basic/your_first_app/defaults",id:"version-1.0/tutorials/basic/your_first_app/defaults",title:"Selecting defaults for config groups",description:"After office politics, you decide that you want to use MySQL by default.",source:"@site/versioned_docs/version-1.0/tutorials/basic/your_first_app/5_defaults.md",sourceDirName:"tutorials/basic/your_first_app",slug:"/tutorials/basic/your_first_app/defaults",permalink:"/docs/1.0/tutorials/basic/your_first_app/defaults",draft:!1,editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/versioned_docs/version-1.0/tutorials/basic/your_first_app/5_defaults.md",tags:[],version:"1.0",lastUpdatedBy:"jesszzzz",lastUpdatedAt:1741814683,formattedLastUpdatedAt:"Mar 12, 2025",sidebarPosition:5,frontMatter:{id:"defaults",title:"Selecting defaults for config groups"},sidebar:"docs",previous:{title:"Grouping config files",permalink:"/docs/1.0/tutorials/basic/your_first_app/config_groups"},next:{title:"Putting it all together",permalink:"/docs/1.0/tutorials/basic/your_first_app/composition"}},u={},p=[{value:"Config group defaults",id:"config-group-defaults",level:2},{value:"Overriding a config group default",id:"overriding-a-config-group-default",level:3},{value:"Non-config group defaults",id:"non-config-group-defaults",level:2}],d={toc:p},c="wrapper";function f(e){let{components:t,...n}=e;return(0,a.mdx)(c,(0,r.A)({},d,n,{components:t,mdxType:"MDXLayout"}),(0,a.mdx)(o.C,{to:"examples/tutorials/basic/your_first_hydra_app/5_defaults",mdxType:"ExampleGithubLink"}),(0,a.mdx)("p",null,"After office politics, you decide that you want to use MySQL by default.\nYou no longer want to type ",(0,a.mdx)("inlineCode",{parentName:"p"},"+db=mysql")," every time you run your application."),(0,a.mdx)("p",null,"You can add a ",(0,a.mdx)("inlineCode",{parentName:"p"},"defaults")," list into your config file."),(0,a.mdx)("h2",{id:"config-group-defaults"},"Config group defaults"),(0,a.mdx)("pre",null,(0,a.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="config.yaml"',title:'"config.yaml"'},"defaults:\n  - db: mysql\n")),(0,a.mdx)("p",null,"Remember to specify the ",(0,a.mdx)("inlineCode",{parentName:"p"},"config_name"),":"),(0,a.mdx)("pre",null,(0,a.mdx)("code",{parentName:"pre",className:"language-python"},'@hydra.main(config_path="conf", config_name="config")\ndef my_app(cfg: DictConfig) -> None:\n    print(OmegaConf.to_yaml(cfg))\n')),(0,a.mdx)("p",null,"When you run the updated application, MySQL is loaded by default."),(0,a.mdx)("pre",null,(0,a.mdx)("code",{parentName:"pre",className:"language-yaml"},"$ python my_app.py\ndb:\n  driver: mysql\n  pass: secret\n  user: omry\n")),(0,a.mdx)("p",null,"You can have multiple items in the defaults list, e.g"),(0,a.mdx)("pre",null,(0,a.mdx)("code",{parentName:"pre",className:"language-yaml"},"defaults:\n - db: mysql\n - db/mysql/storage_engine: innodb\n")),(0,a.mdx)("p",null,"The defaults are ordered:"),(0,a.mdx)("ul",null,(0,a.mdx)("li",{parentName:"ul"},"If multiple configs define the same value, the last one wins. "),(0,a.mdx)("li",{parentName:"ul"},"If multiple configs contribute to the same dictionary, the result is the combined dictionary.")),(0,a.mdx)("h3",{id:"overriding-a-config-group-default"},"Overriding a config group default"),(0,a.mdx)("p",null,"You can still load PostgreSQL, and override individual values."),(0,a.mdx)("pre",null,(0,a.mdx)("code",{parentName:"pre",className:"language-yaml"},"$ python my_app.py db=postgresql db.timeout=20\ndb:\n  driver: postgresql\n  pass: drowssap\n  timeout: 20\n  user: postgres_user\n")),(0,a.mdx)("p",null,"You can remove a default entry from the defaults list by prefixing it with ~:"),(0,a.mdx)("pre",null,(0,a.mdx)("code",{parentName:"pre",className:"language-yaml"},"$ python my_app.py ~db\n{}\n")),(0,a.mdx)("h2",{id:"non-config-group-defaults"},"Non-config group defaults"),(0,a.mdx)("p",null,"Sometimes a config file does not belong in any config group.\nYou can still load it by default. Here is an example for ",(0,a.mdx)("inlineCode",{parentName:"p"},"some_file.yaml"),"."),(0,a.mdx)("pre",null,(0,a.mdx)("code",{parentName:"pre",className:"language-yaml"},"defaults:\n  - some_file\n")),(0,a.mdx)("p",null,"Config files that are not part of a config group will always be loaded. They cannot be overridden.",(0,a.mdx)("br",{parentName:"p"}),"\n","Prefer using a config group."))}f.isMDXComponent=!0},49595:(e,t,n)=>{n.d(t,{A:()=>u,C:()=>p});var r=n(58168),a=n(96540),o=n(75489),i=n(44586),l=n(48295);function s(e){const t=(0,l.ir)();return(0,i.default)().siteConfig.customFields.githubLinkVersionToBaseUrl[t?.name??"current"]+e}function u(e){return a.createElement(o.default,(0,r.A)({},e,{to:s(e.to),target:"_blank"}))}function p(e){const t=e.text??"Example (Click Here)";return a.createElement(u,e,a.createElement("span",null,"\xa0"),a.createElement("img",{src:"https://img.shields.io/badge/-"+t+"-informational",alt:"Example (Click Here)"}))}}}]);