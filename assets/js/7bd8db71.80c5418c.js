"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[1606],{15680:(e,t,n)=>{n.r(t),n.d(t,{MDXContext:()=>d,MDXProvider:()=>u,mdx:()=>g,useMDXComponents:()=>p,withMDXComponents:()=>s});var a=n(96540);function r(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function l(){return l=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var a in n)Object.prototype.hasOwnProperty.call(n,a)&&(e[a]=n[a])}return e},l.apply(this,arguments)}function o(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);t&&(a=a.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,a)}return n}function i(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?o(Object(n),!0).forEach((function(t){r(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):o(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function m(e,t){if(null==e)return{};var n,a,r=function(e,t){if(null==e)return{};var n,a,r={},l=Object.keys(e);for(a=0;a<l.length;a++)n=l[a],t.indexOf(n)>=0||(r[n]=e[n]);return r}(e,t);if(Object.getOwnPropertySymbols){var l=Object.getOwnPropertySymbols(e);for(a=0;a<l.length;a++)n=l[a],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(r[n]=e[n])}return r}var d=a.createContext({}),s=function(e){return function(t){var n=p(t.components);return a.createElement(e,l({},t,{components:n}))}},p=function(e){var t=a.useContext(d),n=t;return e&&(n="function"==typeof e?e(t):i(i({},t),e)),n},u=function(e){var t=p(e.components);return a.createElement(d.Provider,{value:t},e.children)},c={inlineCode:"code",wrapper:function(e){var t=e.children;return a.createElement(a.Fragment,{},t)}},h=a.forwardRef((function(e,t){var n=e.components,r=e.mdxType,l=e.originalType,o=e.parentName,d=m(e,["components","mdxType","originalType","parentName"]),s=p(n),u=r,h=s["".concat(o,".").concat(u)]||s[u]||c[u]||l;return n?a.createElement(h,i(i({ref:t},d),{},{components:n})):a.createElement(h,i({ref:t},d))}));function g(e,t){var n=arguments,r=t&&t.mdxType;if("string"==typeof e||r){var l=n.length,o=new Array(l);o[0]=h;var i={};for(var m in t)hasOwnProperty.call(t,m)&&(i[m]=t[m]);i.originalType=e,i.mdxType="string"==typeof e?e:r,o[1]=i;for(var d=2;d<l;d++)o[d]=n[d];return a.createElement.apply(null,o)}return a.createElement.apply(null,n)}h.displayName="MDXCreateElement"},3821:(e,t,n)=>{n.r(t),n.d(t,{contentTitle:()=>m,default:()=>u,frontMatter:()=>i,metadata:()=>d,toc:()=>s});var a=n(58168),r=n(98587),l=(n(96540),n(15680)),o=(n(86025),n(75489),["components"]),i={id:"intro",title:"Getting started",sidebar_label:"Getting started"},m=void 0,d={unversionedId:"intro",id:"version-1.0/intro",title:"Getting started",description:"Introduction",source:"@site/versioned_docs/version-1.0/intro.md",sourceDirName:".",slug:"/intro",permalink:"/docs/1.0/intro",editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/versioned_docs/version-1.0/intro.md",tags:[],version:"1.0",lastUpdatedBy:"jesszzzz",lastUpdatedAt:1738870843,formattedLastUpdatedAt:"2/6/2025",frontMatter:{id:"intro",title:"Getting started",sidebar_label:"Getting started"},sidebar:"version-1.0/docs",next:{title:"Terminology",permalink:"/docs/1.0/terminology"}},s=[{value:"Introduction",id:"introduction",children:[{value:"Key features:",id:"key-features",children:[],level:3}],level:2},{value:"Versions",id:"versions",children:[],level:2},{value:"Quick start guide",id:"quick-start-guide",children:[{value:"Installation",id:"installation",children:[],level:3},{value:"Basic example",id:"basic-example",children:[],level:3},{value:"Composition example",id:"composition-example",children:[],level:3},{value:"Multirun",id:"multirun",children:[],level:3}],level:2},{value:"Other stuff",id:"other-stuff",children:[{value:"Community",id:"community",children:[],level:3},{value:"Citing Hydra",id:"citing-hydra",children:[],level:3}],level:2}],p={toc:s};function u(e){var t=e.components,n=(0,r.A)(e,o);return(0,l.mdx)("wrapper",(0,a.A)({},p,n,{components:t,mdxType:"MDXLayout"}),(0,l.mdx)("h2",{id:"introduction"},"Introduction"),(0,l.mdx)("p",null,"Hydra is an open-source Python framework that simplifies the development of research and other complex applications.\nThe key feature is the ability to dynamically create a hierarchical configuration by composition and override it through config files and the command line.\nThe name Hydra comes from its ability to run multiple similar jobs - much like a Hydra with multiple heads."),(0,l.mdx)("h3",{id:"key-features"},"Key features:"),(0,l.mdx)("ul",null,(0,l.mdx)("li",{parentName:"ul"},"Hierarchical configuration composable from multiple sources"),(0,l.mdx)("li",{parentName:"ul"},"Configuration can be specified or overridden from the command line"),(0,l.mdx)("li",{parentName:"ul"},"Dynamic command line tab completion"),(0,l.mdx)("li",{parentName:"ul"},"Run your application locally or launch it to run remotely"),(0,l.mdx)("li",{parentName:"ul"},"Run multiple jobs with different arguments with a single command")),(0,l.mdx)("h2",{id:"versions"},"Versions"),(0,l.mdx)("p",null,"Hydra supports Linux, Mac and Windows.",(0,l.mdx)("br",{parentName:"p"}),"\n","Use the version switcher in the top bar to switch between documentation versions."),(0,l.mdx)("table",null,(0,l.mdx)("thead",{parentName:"table"},(0,l.mdx)("tr",{parentName:"thead"},(0,l.mdx)("th",{parentName:"tr",align:null}),(0,l.mdx)("th",{parentName:"tr",align:null},"Version"),(0,l.mdx)("th",{parentName:"tr",align:null},"Release notes"),(0,l.mdx)("th",{parentName:"tr",align:null},"Python Versions"))),(0,l.mdx)("tbody",{parentName:"table"},(0,l.mdx)("tr",{parentName:"tbody"},(0,l.mdx)("td",{parentName:"tr",align:null}),(0,l.mdx)("td",{parentName:"tr",align:null},"1.3 (Stable)"),(0,l.mdx)("td",{parentName:"tr",align:null},(0,l.mdx)("a",{parentName:"td",href:"https://github.com/facebookresearch/hydra/releases/tag/v1.3.0"},"Release notes")),(0,l.mdx)("td",{parentName:"tr",align:null},(0,l.mdx)("strong",{parentName:"td"},"3.6 - 3.11"))),(0,l.mdx)("tr",{parentName:"tbody"},(0,l.mdx)("td",{parentName:"tr",align:null}),(0,l.mdx)("td",{parentName:"tr",align:null},"1.2"),(0,l.mdx)("td",{parentName:"tr",align:null},(0,l.mdx)("a",{parentName:"td",href:"https://github.com/facebookresearch/hydra/releases/tag/v1.2.0"},"Release notes")),(0,l.mdx)("td",{parentName:"tr",align:null},(0,l.mdx)("strong",{parentName:"td"},"3.6 - 3.10"))),(0,l.mdx)("tr",{parentName:"tbody"},(0,l.mdx)("td",{parentName:"tr",align:null}),(0,l.mdx)("td",{parentName:"tr",align:null},"1.1"),(0,l.mdx)("td",{parentName:"tr",align:null},(0,l.mdx)("a",{parentName:"td",href:"https://github.com/facebookresearch/hydra/releases/tag/v1.1.1"},"Release notes")),(0,l.mdx)("td",{parentName:"tr",align:null},(0,l.mdx)("strong",{parentName:"td"},"3.6 - 3.9"))),(0,l.mdx)("tr",{parentName:"tbody"},(0,l.mdx)("td",{parentName:"tr",align:null},"\u25ba"),(0,l.mdx)("td",{parentName:"tr",align:null},"1.0"),(0,l.mdx)("td",{parentName:"tr",align:null},(0,l.mdx)("a",{parentName:"td",href:"https://github.com/facebookresearch/hydra/releases/tag/v1.0.7"},"Release notes")),(0,l.mdx)("td",{parentName:"tr",align:null},(0,l.mdx)("strong",{parentName:"td"},"3.6 - 3.8"))),(0,l.mdx)("tr",{parentName:"tbody"},(0,l.mdx)("td",{parentName:"tr",align:null}),(0,l.mdx)("td",{parentName:"tr",align:null},"0.11"),(0,l.mdx)("td",{parentName:"tr",align:null},(0,l.mdx)("a",{parentName:"td",href:"https://github.com/facebookresearch/hydra/releases/tag/v0.11.3"},"Release notes")),(0,l.mdx)("td",{parentName:"tr",align:null},(0,l.mdx)("strong",{parentName:"td"},"2.7, 3.5 - 3.8"))))),(0,l.mdx)("h2",{id:"quick-start-guide"},"Quick start guide"),(0,l.mdx)("p",null,"This guide will show you some of the most important features of Hydra.\nRead the ",(0,l.mdx)("a",{parentName:"p",href:"/docs/1.0/tutorials/basic/your_first_app/simple_cli"},"tutorial")," to gain a deeper understanding."),(0,l.mdx)("h3",{id:"installation"},"Installation"),(0,l.mdx)("pre",null,(0,l.mdx)("code",{parentName:"pre",className:"language-commandline"},"pip install hydra-core --upgrade\n")),(0,l.mdx)("h3",{id:"basic-example"},"Basic example"),(0,l.mdx)("p",null,"Config:"),(0,l.mdx)("pre",null,(0,l.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="config.yaml"',title:'"config.yaml"'},"db:\n  driver: mysql\n  user: omry\n  pass: secret\n")),(0,l.mdx)("p",null,"Application:"),(0,l.mdx)("pre",null,(0,l.mdx)("code",{parentName:"pre",className:"language-python",metastring:'{4-6} title="my_app.py"',"{4-6}":!0,title:'"my_app.py"'},'import hydra\nfrom omegaconf import DictConfig, OmegaConf\n\n@hydra.main(config_name="config")\ndef my_app(cfg : DictConfig) -> None:\n    print(OmegaConf.to_yaml(cfg))\n\nif __name__ == "__main__":\n    my_app()\n')),(0,l.mdx)("p",null,"You can learn more about OmegaConf ",(0,l.mdx)("a",{parentName:"p",href:"https://omegaconf.readthedocs.io/en/latest/usage.html#access-and-manipulation"},"here")," later."),(0,l.mdx)("p",null,(0,l.mdx)("inlineCode",{parentName:"p"},"config.yaml")," is loaded automatically when you run your application"),(0,l.mdx)("pre",null,(0,l.mdx)("code",{parentName:"pre",className:"language-yaml"},"$ python my_app.py\ndb:\n  driver: mysql\n  pass: secret\n  user: omry\n")),(0,l.mdx)("p",null,"You can override values in the loaded config from the command line:"),(0,l.mdx)("pre",null,(0,l.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:"{4-5}","{4-5}":!0},"$ python my_app.py db.user=root db.pass=1234\ndb:\n  driver: mysql\n  user: root\n  pass: 1234\n")),(0,l.mdx)("h3",{id:"composition-example"},"Composition example"),(0,l.mdx)("p",null,"You may want to alternate between two different databases. To support this create a ",(0,l.mdx)("inlineCode",{parentName:"p"},"config group")," named db,\nand place one config file for each alternative inside:\nThe directory structure of our application now looks like:"),(0,l.mdx)("pre",null,(0,l.mdx)("code",{parentName:"pre",className:"language-text"},"\u251c\u2500\u2500 db\n\u2502   \u251c\u2500\u2500 mysql.yaml\n\u2502   \u2514\u2500\u2500 postgresql.yaml\n\u251c\u2500\u2500 config.yaml\n\u2514\u2500\u2500 my_app.py\n")),(0,l.mdx)("p",null,"Here is the new config:"),(0,l.mdx)("pre",null,(0,l.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="config.yaml"',title:'"config.yaml"'},"defaults:\n  - db: mysql\n")),(0,l.mdx)("p",null,(0,l.mdx)("inlineCode",{parentName:"p"},"defaults")," is a special directive telling Hydra to use db/mysql.yaml when composing the configuration object.\nThe resulting cfg object is a composition of configs from defaults with configs specified in your ",(0,l.mdx)("inlineCode",{parentName:"p"},"config.yaml"),"."),(0,l.mdx)("p",null,"You can now choose which database configuration to use from the and override values from the command line: "),(0,l.mdx)("pre",null,(0,l.mdx)("code",{parentName:"pre",className:"language-yaml"},"$ python my_app.py db=postgresql db.timeout=20\ndb:\n  driver: postgresql\n  pass: drowssap\n  timeout: 20\n  user: postgres_user\nwebsite:\n  domain: example.com\n")),(0,l.mdx)("p",null,"You can have as many config groups as you need."),(0,l.mdx)("h3",{id:"multirun"},"Multirun"),(0,l.mdx)("p",null,"You can run your function multiple times with different configuration easily with the ",(0,l.mdx)("inlineCode",{parentName:"p"},"--multirun|-m")," flag."),(0,l.mdx)("pre",null,(0,l.mdx)("code",{parentName:"pre"},"$ python my_app.py --multirun db=mysql,postgresql\n[HYDRA] Sweep output dir : multirun/2020-01-09/01-16-29\n[HYDRA] Launching 2 jobs locally\n[HYDRA]        #0 : db=mysql\ndb:\n  driver: mysql\n  pass: secret\n  user: omry\nwebsite:\n    domain: example.com\n\n[HYDRA]        #1 : db=postgresql\ndb:\n  driver: postgresql\n  pass: drowssap\n  timeout: 10\n  user: postgres_user\nwebsite:\n    domain: example.com\n")),(0,l.mdx)("p",null,"There is a whole lot more to Hydra. Read the ",(0,l.mdx)("a",{parentName:"p",href:"/docs/1.0/tutorials/basic/your_first_app/simple_cli"},"tutorial")," to learn more."),(0,l.mdx)("h2",{id:"other-stuff"},"Other stuff"),(0,l.mdx)("h3",{id:"community"},"Community"),(0,l.mdx)("p",null,"Ask questions on github or StackOverflow (Use the tag #fb-hydra):"),(0,l.mdx)("ul",null,(0,l.mdx)("li",{parentName:"ul"},(0,l.mdx)("a",{parentName:"li",href:"https://github.com/facebookresearch/hydra/discussions"},"github")),(0,l.mdx)("li",{parentName:"ul"},(0,l.mdx)("a",{parentName:"li",href:"https://stackoverflow.com/questions/tagged/fb-hydra"},"StackOverflow"))),(0,l.mdx)("p",null,"Follow Hydra on Twitter and Facebook:"),(0,l.mdx)("ul",null,(0,l.mdx)("li",{parentName:"ul"},(0,l.mdx)("a",{parentName:"li",href:"https://www.facebook.com/Hydra-Framework-109364473802509/"},"Facebook page")),(0,l.mdx)("li",{parentName:"ul"},(0,l.mdx)("a",{parentName:"li",href:"https://twitter.com/Hydra_Framework"},"Twitter"))),(0,l.mdx)("h3",{id:"citing-hydra"},"Citing Hydra"),(0,l.mdx)("p",null,"If you use Hydra in your research please use the following BibTeX entry:"),(0,l.mdx)("pre",null,(0,l.mdx)("code",{parentName:"pre",className:"language-text"},"@Misc{Yadan2019Hydra,\n  author =       {Omry Yadan},\n  title =        {Hydra - A framework for elegantly configuring complex applications},\n  howpublished = {Github},\n  year =         {2019},\n  url =          {https://github.com/facebookresearch/hydra}\n}\n")))}u.isMDXComponent=!0}}]);