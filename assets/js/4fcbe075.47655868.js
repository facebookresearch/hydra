"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[3717],{15680:(e,n,t)=>{t.r(n),t.d(n,{MDXContext:()=>c,MDXProvider:()=>m,mdx:()=>g,useMDXComponents:()=>d,withMDXComponents:()=>p});var a=t(96540);function r(e,n,t){return n in e?Object.defineProperty(e,n,{value:t,enumerable:!0,configurable:!0,writable:!0}):e[n]=t,e}function o(){return o=Object.assign||function(e){for(var n=1;n<arguments.length;n++){var t=arguments[n];for(var a in t)Object.prototype.hasOwnProperty.call(t,a)&&(e[a]=t[a])}return e},o.apply(this,arguments)}function s(e,n){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);n&&(a=a.filter((function(n){return Object.getOwnPropertyDescriptor(e,n).enumerable}))),t.push.apply(t,a)}return t}function i(e){for(var n=1;n<arguments.length;n++){var t=null!=arguments[n]?arguments[n]:{};n%2?s(Object(t),!0).forEach((function(n){r(e,n,t[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):s(Object(t)).forEach((function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(t,n))}))}return e}function l(e,n){if(null==e)return{};var t,a,r=function(e,n){if(null==e)return{};var t,a,r={},o=Object.keys(e);for(a=0;a<o.length;a++)t=o[a],n.indexOf(t)>=0||(r[t]=e[t]);return r}(e,n);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(e);for(a=0;a<o.length;a++)t=o[a],n.indexOf(t)>=0||Object.prototype.propertyIsEnumerable.call(e,t)&&(r[t]=e[t])}return r}var c=a.createContext({}),p=function(e){return function(n){var t=d(n.components);return a.createElement(e,o({},n,{components:t}))}},d=function(e){var n=a.useContext(c),t=n;return e&&(t="function"==typeof e?e(n):i(i({},n),e)),t},m=function(e){var n=d(e.components);return a.createElement(c.Provider,{value:n},e.children)},f="mdxType",u={inlineCode:"code",wrapper:function(e){var n=e.children;return a.createElement(a.Fragment,{},n)}},b=a.forwardRef((function(e,n){var t=e.components,r=e.mdxType,o=e.originalType,s=e.parentName,c=l(e,["components","mdxType","originalType","parentName"]),p=d(t),m=r,f=p["".concat(s,".").concat(m)]||p[m]||u[m]||o;return t?a.createElement(f,i(i({ref:n},c),{},{components:t})):a.createElement(f,i({ref:n},c))}));function g(e,n){var t=arguments,r=n&&n.mdxType;if("string"==typeof e||r){var o=t.length,s=new Array(o);s[0]=b;var i={};for(var l in n)hasOwnProperty.call(n,l)&&(i[l]=n[l]);i.originalType=e,i[f]="string"==typeof e?e:r,s[1]=i;for(var c=2;c<o;c++)s[c]=t[c];return a.createElement.apply(null,s)}return a.createElement.apply(null,t)}b.displayName="MDXCreateElement"},22416:(e,n,t)=>{t.r(n),t.d(n,{assets:()=>l,contentTitle:()=>s,default:()=>m,frontMatter:()=>o,metadata:()=>i,toc:()=>c});var a=t(58168),r=(t(96540),t(15680));const o={id:"objects",title:"Creating objects",sidebar_label:"Creating objects"},s=void 0,i={unversionedId:"patterns/objects",id:"version-0.11/patterns/objects",title:"Creating objects",description:"One of the best ways to drive different behavior in the application is to instantiate different implementations of an interface.",source:"@site/versioned_docs/version-0.11/patterns/objects.md",sourceDirName:"patterns",slug:"/patterns/objects",permalink:"/docs/0.11/patterns/objects",draft:!1,editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/versioned_docs/version-0.11/patterns/objects.md",tags:[],version:"0.11",lastUpdatedBy:"dependabot[bot]",lastUpdatedAt:1742161400,formattedLastUpdatedAt:"Mar 16, 2025",frontMatter:{id:"objects",title:"Creating objects",sidebar_label:"Creating objects"},sidebar:"docs",previous:{title:"Debugging",permalink:"/docs/0.11/tutorial/debugging"},next:{title:"Specializing configuration",permalink:"/docs/0.11/patterns/specializing_config"}},l={},c=[],p={toc:c},d="wrapper";function m(e){let{components:n,...t}=e;return(0,r.mdx)(d,(0,a.A)({},p,t,{components:n,mdxType:"MDXLayout"}),(0,r.mdx)("p",null,"One of the best ways to drive different behavior in the application is to instantiate different implementations of an interface.\nThe code using the instantiated object only knows the interface which remains constant, but the behavior\nis determined by the actual object instance."),(0,r.mdx)("p",null,"A Database connection interface may have a ",(0,r.mdx)("inlineCode",{parentName:"p"},"connect()")," method, implemented by different database drivers."),(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-python"},'class DBConnection:\n    def connect(self):\n        pass\n\nclass MySQLConnection(DBConnection):\n    def __init__(self, host, user, password):\n        self.host = host\n        self.user = user\n        self.password = password\n\n    def connect(self):\n        print(\n            "MySQL connecting to {} with user={} and password={}".format(\n                self.host, self.user, self.password\n            )\n        )\n\nclass PostgreSQLConnection(DBConnection):\n    def __init__(self, host, user, password, database):\n        self.host = host\n        self.user = user\n        self.password = password\n        self.database = database\n\n    def connect(self):\n        print(\n            "PostgreSQL connecting to {} "\n            "with user={} and password={} and database={}".format(\n                self.host, self.user, self.password, self.database\n            )\n        )\n')),(0,r.mdx)("p",null,"To support this, we can have a parallel config structure:"),(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-text"},"conf/\n\u251c\u2500\u2500 config.yaml\n\u2514\u2500\u2500 db\n    \u251c\u2500\u2500 mysql.yaml\n    \u2514\u2500\u2500 postgresql.yaml\n")),(0,r.mdx)("p",null,"Config file: ",(0,r.mdx)("inlineCode",{parentName:"p"},"config.yaml")),(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-yaml"},"defaults:\n  - db: mysql\n")),(0,r.mdx)("p",null,"Config file: ",(0,r.mdx)("inlineCode",{parentName:"p"},"db/mysql.yaml")),(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-yaml"},"db:\n  class: tutorial.objects_example.objects.MySQLConnection\n  params:\n    host: localhost\n    user: root\n    password: 1234\n")),(0,r.mdx)("p",null,"db/postgresql.yaml:"),(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-yaml"},"db:\n  class: tutorial.objects_example.objects.PostgreSQLConnection\n  params:\n    host: localhost\n    user: root\n    password: 1234\n    database: tutorial\n")),(0,r.mdx)("p",null,"With this, you can instantiate the object from the configuration with a single line of code:"),(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-python"},'@hydra.main(config_path="conf/config.yaml")\ndef my_app(cfg):\n    connection = hydra.utils.instantiate(cfg.db)\n    connection.connect()\n')),(0,r.mdx)("p",null,"MySQL is the default per the ",(0,r.mdx)("inlineCode",{parentName:"p"},"config.yaml")," file:"),(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-text"},"$ python my_app.py\nMySQL connecting to localhost with user=root and password=1234\n")),(0,r.mdx)("p",null,"Change the instantiated object class and override values from the command line:"),(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-text"},"$ python my_app.py db=postgresql db.params.password=abcde\nPostgreSQL connecting to localhost with user=root and password=abcde and database=tutorial\n")))}m.isMDXComponent=!0}}]);