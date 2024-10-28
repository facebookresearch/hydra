"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[20],{15680:(e,a,n)=>{n.r(a),n.d(a,{MDXContext:()=>m,MDXProvider:()=>p,mdx:()=>f,useMDXComponents:()=>c,withMDXComponents:()=>d});var t=n(96540);function r(e,a,n){return a in e?Object.defineProperty(e,a,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[a]=n,e}function l(){return l=Object.assign||function(e){for(var a=1;a<arguments.length;a++){var n=arguments[a];for(var t in n)Object.prototype.hasOwnProperty.call(n,t)&&(e[t]=n[t])}return e},l.apply(this,arguments)}function i(e,a){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var t=Object.getOwnPropertySymbols(e);a&&(t=t.filter((function(a){return Object.getOwnPropertyDescriptor(e,a).enumerable}))),n.push.apply(n,t)}return n}function o(e){for(var a=1;a<arguments.length;a++){var n=null!=arguments[a]?arguments[a]:{};a%2?i(Object(n),!0).forEach((function(a){r(e,a,n[a])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):i(Object(n)).forEach((function(a){Object.defineProperty(e,a,Object.getOwnPropertyDescriptor(n,a))}))}return e}function s(e,a){if(null==e)return{};var n,t,r=function(e,a){if(null==e)return{};var n,t,r={},l=Object.keys(e);for(t=0;t<l.length;t++)n=l[t],a.indexOf(n)>=0||(r[n]=e[n]);return r}(e,a);if(Object.getOwnPropertySymbols){var l=Object.getOwnPropertySymbols(e);for(t=0;t<l.length;t++)n=l[t],a.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(r[n]=e[n])}return r}var m=t.createContext({}),d=function(e){return function(a){var n=c(a.components);return t.createElement(e,l({},a,{components:n}))}},c=function(e){var a=t.useContext(m),n=a;return e&&(n="function"==typeof e?e(a):o(o({},a),e)),n},p=function(e){var a=c(e.components);return t.createElement(m.Provider,{value:a},e.children)},g={inlineCode:"code",wrapper:function(e){var a=e.children;return t.createElement(t.Fragment,{},a)}},u=t.forwardRef((function(e,a){var n=e.components,r=e.mdxType,l=e.originalType,i=e.parentName,m=s(e,["components","mdxType","originalType","parentName"]),d=c(n),p=r,u=d["".concat(i,".").concat(p)]||d[p]||g[p]||l;return n?t.createElement(u,o(o({ref:a},m),{},{components:n})):t.createElement(u,o({ref:a},m))}));function f(e,a){var n=arguments,r=a&&a.mdxType;if("string"==typeof e||r){var l=n.length,i=new Array(l);i[0]=u;var o={};for(var s in a)hasOwnProperty.call(a,s)&&(o[s]=a[s]);o.originalType=e,o.mdxType="string"==typeof e?e:r,i[1]=o;for(var m=2;m<l;m++)i[m]=n[m];return t.createElement.apply(null,i)}return t.createElement.apply(null,n)}u.displayName="MDXCreateElement"},86322:(e,a,n)=>{n.r(a),n.d(a,{contentTitle:()=>s,default:()=>p,frontMatter:()=>o,metadata:()=>m,toc:()=>d});var t=n(58168),r=n(98587),l=(n(96540),n(15680)),i=["components"],o={id:"overriding_packages",title:"Packages"},s=void 0,m={unversionedId:"advanced/overriding_packages",id:"version-1.1/advanced/overriding_packages",title:"Packages",description:"The package determines where the content of each input config is placed in the output config.",source:"@site/versioned_docs/version-1.1/advanced/overriding_packages.md",sourceDirName:"advanced",slug:"/advanced/overriding_packages",permalink:"/docs/1.1/advanced/overriding_packages",editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/versioned_docs/version-1.1/advanced/overriding_packages.md",tags:[],version:"1.1",lastUpdatedBy:"dependabot[bot]",lastUpdatedAt:1730135614,formattedLastUpdatedAt:"10/28/2024",frontMatter:{id:"overriding_packages",title:"Packages"},sidebar:"version-1.1/docs",previous:{title:"The Defaults List",permalink:"/docs/1.1/advanced/defaults_list"},next:{title:"Overview",permalink:"/docs/1.1/advanced/instantiate_objects/overview"}},d=[{value:"An example using only default packages",id:"an-example-using-only-default-packages",children:[],level:3},{value:"Overriding packages using the Defaults List",id:"overriding-packages-using-the-defaults-list",children:[{value:"Default List package keywords",id:"default-list-package-keywords",children:[{value:"Absolute keywords:",id:"absolute-keywords",children:[],level:5}],level:4}],level:3},{value:"Overriding the package via the package directive",id:"overriding-the-package-via-the-package-directive",children:[],level:3},{value:"Using a config group more than once",id:"using-a-config-group-more-than-once",children:[],level:3}],c={toc:d};function p(e){var a=e.components,n=(0,r.A)(e,i);return(0,l.mdx)("wrapper",(0,t.A)({},c,n,{components:a,mdxType:"MDXLayout"}),(0,l.mdx)("p",null,"The package determines where the content of each input config is placed in the output config.\nThe default package of an input config is derived from its Config Group. e.g. The default package of ",(0,l.mdx)("inlineCode",{parentName:"p"},"server/db/mysql.yaml")," is ",(0,l.mdx)("inlineCode",{parentName:"p"},"server.db"),"."),(0,l.mdx)("p",null,"The default package can be overridden ",(0,l.mdx)("a",{parentName:"p",href:"#overriding-packages-using-the-defaults-list"},"in the Defaults List"),"\nor via a ",(0,l.mdx)("a",{parentName:"p",href:"#overriding-the-package-via-the-package-directive"},"Package Directive")," at the top of the config file.\nChanging the package of a config can be useful when using a config from another library, or when using the same\nconfig group twice in the same app."),(0,l.mdx)("p",null,"The priority for determining the final package for a config is as follows:"),(0,l.mdx)("ol",null,(0,l.mdx)("li",{parentName:"ol"},"The package specified in the Defaults List (relative to the package of the including config)"),(0,l.mdx)("li",{parentName:"ol"},"The package specified in the Package Directive (absolute)"),(0,l.mdx)("li",{parentName:"ol"},"The default package")),(0,l.mdx)("p",null,"We will use the following configs in the examples below:"),(0,l.mdx)("div",{className:"row"},(0,l.mdx)("div",{className:"col col--4"},(0,l.mdx)("pre",null,(0,l.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="config.yaml"',title:'"config.yaml"'},"defaults:\n  - server/apache\n\ndebug: false\n\n\n\n"))),(0,l.mdx)("div",{className:"col col--4"},(0,l.mdx)("pre",null,(0,l.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="server/apache.yaml"',title:'"server/apache.yaml"'},"defaults:\n  - db: mysql\n\nname: apache\n\n\n\n"))),(0,l.mdx)("div",{className:"col col--4"},(0,l.mdx)("pre",null,(0,l.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="server/db/mysql.yaml"',title:'"server/db/mysql.yaml"'},"name: mysql\n")),(0,l.mdx)("pre",null,(0,l.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="server/db/sqlite.yaml"',title:'"server/db/sqlite.yaml"'},"name: sqlite\n")))),(0,l.mdx)("pre",null,(0,l.mdx)("code",{parentName:"pre",className:"language-text",metastring:'title="Config directory structure"',title:'"Config',directory:!0,'structure"':!0},"\u251c\u2500\u2500 server\n\u2502   \u251c\u2500\u2500 db\n\u2502   \u2502   \u251c\u2500\u2500 mysql.yaml\n\u2502   \u2502   \u2514\u2500\u2500 sqlite.yaml\n\u2502   \u2514\u2500\u2500 apache.yaml\n\u2514\u2500\u2500 config.yaml\n")),(0,l.mdx)("h3",{id:"an-example-using-only-default-packages"},"An example using only default packages"),(0,l.mdx)("p",null,"The default package of ",(0,l.mdx)("em",{parentName:"p"},"config.yaml")," is the global package, of ",(0,l.mdx)("em",{parentName:"p"},"server/apache.yaml")," is ",(0,l.mdx)("em",{parentName:"p"},"server")," and of ",(0,l.mdx)("em",{parentName:"p"},"server/db/mysql.yaml")," is ",(0,l.mdx)("em",{parentName:"p"},"server.db"),". "),(0,l.mdx)("div",{className:"row"},(0,l.mdx)("div",{className:"col col--6"},(0,l.mdx)("pre",null,(0,l.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="$ python my_app.py" {1-2}',title:'"$',python:!0,'my_app.py"':!0,"{1-2}":!0},"server:\n  db:\n    name: mysql\n  name: apache\ndebug: false\n")))),(0,l.mdx)("h3",{id:"overriding-packages-using-the-defaults-list"},"Overriding packages using the Defaults List"),(0,l.mdx)("p",null,"By default, packages specified in the Defaults List are relative to the package of containing config.\nAs a consequence, overriding a package relocates the entire subtree. "),(0,l.mdx)("div",{className:"row"},(0,l.mdx)("div",{className:"col col--4"},(0,l.mdx)("pre",null,(0,l.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="config.yaml" {2}',title:'"config.yaml"',"{2}":!0},"defaults:\n  - server/apache@admin\n\ndebug: false\n\n"))),(0,l.mdx)("div",{className:"col col--4"},(0,l.mdx)("pre",null,(0,l.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="server/apache.yaml" {2}',title:'"server/apache.yaml"',"{2}":!0},"defaults:\n - db@backup: mysql\n\nname: apache\n\n"))),(0,l.mdx)("div",{className:"col col--4"},(0,l.mdx)("pre",null,(0,l.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="Output config" {1-4}',title:'"Output','config"':!0,"{1-4}":!0},"admin:\n  backup:\n    name: mysql\n  name: apache\ndebug: false\n")))),(0,l.mdx)("p",null,"Note that content of ",(0,l.mdx)("em",{parentName:"p"},"server/apache.yaml")," is relocated to ",(0,l.mdx)("em",{parentName:"p"},"admin"),"\nand the content of ",(0,l.mdx)("em",{parentName:"p"},"server/db/mysql.yaml")," to ",(0,l.mdx)("em",{parentName:"p"},"admin.backup"),"."),(0,l.mdx)("h4",{id:"default-list-package-keywords"},"Default List package keywords"),(0,l.mdx)("p",null,"We will use this example, replacing ",(0,l.mdx)("em",{parentName:"p"},"<@PACKAGE>")," to demonstrate different cases:"),(0,l.mdx)("pre",null,(0,l.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="config_group/config.yaml"',title:'"config_group/config.yaml"'},"defaults:\n  - /server/db<@PACKAGE>: mysql\n")),(0,l.mdx)("p",null,"Without a package override, the resulting package is ",(0,l.mdx)("inlineCode",{parentName:"p"},"config_group.server.db"),".",(0,l.mdx)("br",{parentName:"p"}),"\n","With the ",(0,l.mdx)("strong",{parentName:"p"},"@","_","here","_")," keyword, The resulting package is the same as the containing config (",(0,l.mdx)("inlineCode",{parentName:"p"},"config_group"),"). "),(0,l.mdx)("h5",{id:"absolute-keywords"},"Absolute keywords:"),(0,l.mdx)("ul",null,(0,l.mdx)("li",{parentName:"ul"},(0,l.mdx)("strong",{parentName:"li"},"@","_","group","_"),": ","_","group","_"," is the absolute default package of the config (",(0,l.mdx)("inlineCode",{parentName:"li"},"server.db"),")"),(0,l.mdx)("li",{parentName:"ul"},(0,l.mdx)("strong",{parentName:"li"},"@","_","global","_"),": The global package. Anything following ","_","global","_"," is absolute.",(0,l.mdx)("br",{parentName:"li"}),"e.g. ",(0,l.mdx)("strong",{parentName:"li"},"@","_","global","_",".foo")," becomes ",(0,l.mdx)("inlineCode",{parentName:"li"},"foo"),".")),(0,l.mdx)("h3",{id:"overriding-the-package-via-the-package-directive"},"Overriding the package via the package directive"),(0,l.mdx)("p",null,"The @package directive changes the package of a config file. The package specified by a @package directive is always absolute."),(0,l.mdx)("pre",null,(0,l.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="server/db/mysql.yaml" {1}',title:'"server/db/mysql.yaml"',"{1}":!0},"# @package foo.bar\nname: mysql\n")),(0,l.mdx)("p",null,"To change the package to the global (empty) package, use the keyword ",(0,l.mdx)("inlineCode",{parentName:"p"},"_global_"),"."),(0,l.mdx)("h3",{id:"using-a-config-group-more-than-once"},"Using a config group more than once"),(0,l.mdx)("p",null,"The following example adds the ",(0,l.mdx)("inlineCode",{parentName:"p"},"server/db/mysql")," config in the packages ",(0,l.mdx)("inlineCode",{parentName:"p"},"src")," and ",(0,l.mdx)("inlineCode",{parentName:"p"},"dst"),"."),(0,l.mdx)("div",{className:"row"},(0,l.mdx)("div",{className:"col col--6"},(0,l.mdx)("pre",null,(0,l.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="config.yaml"',title:'"config.yaml"'},"defaults:\n - server/db@src: mysql\n - server/db@dst: mysql\n\n"))),(0,l.mdx)("div",{className:"col  col--6"},(0,l.mdx)("pre",null,(0,l.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="$ python my_app.py"',title:'"$',python:!0,'my_app.py"':!0},"src:\n  name: mysql\ndst:\n  name: mysql\n")))),(0,l.mdx)("p",null,"When overriding config groups with a non-default package, the package must be used:"),(0,l.mdx)("pre",null,(0,l.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="$ python my_app.py server/db@src=sqlite"',title:'"$',python:!0,"my_app.py":!0,"server/db@src":'sqlite"'},"src:\n  name: sqlite\ndst:\n  name: mysql\n")))}p.isMDXComponent=!0}}]);