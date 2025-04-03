"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[7541],{15680:(e,t,n)=>{n.r(t),n.d(t,{MDXContext:()=>p,MDXProvider:()=>u,mdx:()=>g,useMDXComponents:()=>s,withMDXComponents:()=>m});var r=n(96540);function a(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function i(){return i=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var r in n)Object.prototype.hasOwnProperty.call(n,r)&&(e[r]=n[r])}return e},i.apply(this,arguments)}function o(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,r)}return n}function l(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?o(Object(n),!0).forEach((function(t){a(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):o(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function c(e,t){if(null==e)return{};var n,r,a=function(e,t){if(null==e)return{};var n,r,a={},i=Object.keys(e);for(r=0;r<i.length;r++)n=i[r],t.indexOf(n)>=0||(a[n]=e[n]);return a}(e,t);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);for(r=0;r<i.length;r++)n=i[r],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(a[n]=e[n])}return a}var p=r.createContext({}),m=function(e){return function(t){var n=s(t.components);return r.createElement(e,i({},t,{components:n}))}},s=function(e){var t=r.useContext(p),n=t;return e&&(n="function"==typeof e?e(t):l(l({},t),e)),n},u=function(e){var t=s(e.components);return r.createElement(p.Provider,{value:t},e.children)},d="mdxType",y={inlineCode:"code",wrapper:function(e){var t=e.children;return r.createElement(r.Fragment,{},t)}},f=r.forwardRef((function(e,t){var n=e.components,a=e.mdxType,i=e.originalType,o=e.parentName,p=c(e,["components","mdxType","originalType","parentName"]),m=s(n),u=a,d=m["".concat(o,".").concat(u)]||m[u]||y[u]||i;return n?r.createElement(d,l(l({ref:t},p),{},{components:n})):r.createElement(d,l({ref:t},p))}));function g(e,t){var n=arguments,a=t&&t.mdxType;if("string"==typeof e||a){var i=n.length,o=new Array(i);o[0]=f;var l={};for(var c in t)hasOwnProperty.call(t,c)&&(l[c]=t[c]);l.originalType=e,l[d]="string"==typeof e?e:a,o[1]=l;for(var p=2;p<i;p++)o[p]=n[p];return r.createElement.apply(null,o)}return r.createElement.apply(null,n)}f.displayName="MDXCreateElement"},46821:(e,t,n)=>{n.r(t),n.d(t,{assets:()=>p,contentTitle:()=>l,default:()=>d,frontMatter:()=>o,metadata:()=>c,toc:()=>m});var r=n(58168),a=(n(96540),n(15680)),i=n(49595);const o={id:"minimal_example",title:"Minimal example"},l=void 0,c={unversionedId:"tutorials/structured_config/minimal_example",id:"tutorials/structured_config/minimal_example",title:"Minimal example",description:"There are four key elements in this example:",source:"@site/docs/tutorials/structured_config/1_minimal_example.md",sourceDirName:"tutorials/structured_config",slug:"/tutorials/structured_config/minimal_example",permalink:"/docs/tutorials/structured_config/minimal_example",draft:!1,editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/docs/tutorials/structured_config/1_minimal_example.md",tags:[],version:"current",lastUpdatedBy:"dependabot[bot]",lastUpdatedAt:1743717584,formattedLastUpdatedAt:"Apr 3, 2025",sidebarPosition:1,frontMatter:{id:"minimal_example",title:"Minimal example"},sidebar:"docs",previous:{title:"Config Store API",permalink:"/docs/tutorials/structured_config/config_store"},next:{title:"A hierarchical static configuration",permalink:"/docs/tutorials/structured_config/hierarchical_static_config"}},p={},m=[{value:"Duck-typing enables static type checking",id:"duck-typing-enables-static-type-checking",level:3},{value:"Structured Configs enable Hydra to catch type errors at runtime",id:"structured-configs-enable-hydra-to-catch-type-errors-at-runtime",level:3},{value:"Duck typing",id:"duck-typing",level:2}],s={toc:m},u="wrapper";function d(e){let{components:t,...n}=e;return(0,a.mdx)(u,(0,r.A)({},s,n,{components:t,mdxType:"MDXLayout"}),(0,a.mdx)(i.C,{to:"examples/tutorials/structured_configs/1_minimal",mdxType:"ExampleGithubLink"}),(0,a.mdx)("p",null,"There are four key elements in this example:"),(0,a.mdx)("ul",null,(0,a.mdx)("li",{parentName:"ul"},"A ",(0,a.mdx)("inlineCode",{parentName:"li"},"@dataclass")," describes the application's configuration"),(0,a.mdx)("li",{parentName:"ul"},(0,a.mdx)("inlineCode",{parentName:"li"},"ConfigStore")," manages the Structured Config"),(0,a.mdx)("li",{parentName:"ul"},(0,a.mdx)("inlineCode",{parentName:"li"},"cfg")," is ",(0,a.mdx)("inlineCode",{parentName:"li"},"duck typed")," as a ",(0,a.mdx)("inlineCode",{parentName:"li"},"MySQLConfig")," instead of a ",(0,a.mdx)("inlineCode",{parentName:"li"},"DictConfig")),(0,a.mdx)("li",{parentName:"ul"},"There is a subtle typo in the code below, can you spot it?")),(0,a.mdx)("p",null,"In this example, the config node stored in the ",(0,a.mdx)("inlineCode",{parentName:"p"},"ConfigStore")," replaces the traditional ",(0,a.mdx)("inlineCode",{parentName:"p"},"config.yaml")," file."),(0,a.mdx)("pre",null,(0,a.mdx)("code",{parentName:"pre",className:"language-python",metastring:'title="my_app_type_error.py" {18}',title:'"my_app_type_error.py"',"{18}":!0},'from dataclasses import dataclass\n\nimport hydra\nfrom hydra.core.config_store import ConfigStore\n\n@dataclass\nclass MySQLConfig:\n    host: str = "localhost"\n    port: int = 3306\n\ncs = ConfigStore.instance()\n# Registering the Config class with the name \'config\'.\ncs.store(name="config", node=MySQLConfig)\n\n@hydra.main(version_base=None, config_name="config")\ndef my_app(cfg: MySQLConfig) -> None:\n    # pork should be port!\n    if cfg.pork == 80:\n        print("Is this a webserver?!")\n\nif __name__ == "__main__":\n    my_app()\n')),(0,a.mdx)("h3",{id:"duck-typing-enables-static-type-checking"},"Duck-typing enables static type checking"),(0,a.mdx)("p",null,"Duck-typing the config object as ",(0,a.mdx)("inlineCode",{parentName:"p"},"MySQLConfig")," enables static type checkers like ",(0,a.mdx)("inlineCode",{parentName:"p"},"mypy")," to catch\ntype errors before you run your code:"),(0,a.mdx)("pre",null,(0,a.mdx)("code",{parentName:"pre",className:"language-text",metastring:'title="$ mypy my_app_type_error.py"',title:'"$',mypy:!0,'my_app_type_error.py"':!0},'my_app_type_error.py:22: error: "MySQLConfig" has no attribute "pork"\nFound 1 error in 1 file (checked 1 source file)\n')),(0,a.mdx)("h3",{id:"structured-configs-enable-hydra-to-catch-type-errors-at-runtime"},"Structured Configs enable Hydra to catch type errors at runtime"),(0,a.mdx)("p",null,"If you forget to run ",(0,a.mdx)("inlineCode",{parentName:"p"},"mypy"),", Hydra will report the error at runtime:"),(0,a.mdx)("pre",null,(0,a.mdx)("code",{parentName:"pre",className:"language-text",metastring:'title="$ python my_app_type_error.py"',title:'"$',python:!0,'my_app_type_error.py"':!0},"Traceback (most recent call last):\n  File \"my_app_type_error.py\", line 22, in my_app\n    if cfg.pork == 80:\nomegaconf.errors.ConfigAttributeError: Key 'pork' not in 'MySQLConfig'\n        full_key: pork\n        object_type=MySQLConfig\n\nSet the environment variable HYDRA_FULL_ERROR=1 for a complete stack trace.\n")),(0,a.mdx)("p",null,"Hydra will also catch typos, or type errors in the command line:"),(0,a.mdx)("pre",null,(0,a.mdx)("code",{parentName:"pre"},"$ python my_app_type_error.py port=fail\nError merging override port=fail\nValue 'fail' could not be converted to Integer\n        full_key: port\n        object_type=MySQLConfig\n")),(0,a.mdx)("p",null,"We will see additional types of runtime errors that Hydra can catch later in this tutorial. Such as:"),(0,a.mdx)("ul",null,(0,a.mdx)("li",{parentName:"ul"},"Trying to read or write a non existent field in your config object"),(0,a.mdx)("li",{parentName:"ul"},"Assigning a value that is incompatible with the declared type"),(0,a.mdx)("li",{parentName:"ul"},"Attempting to modify a ",(0,a.mdx)("a",{parentName:"li",href:"https://omegaconf.readthedocs.io/en/latest/structured_config.html#frozen"},"frozen config"))),(0,a.mdx)("h2",{id:"duck-typing"},"Duck typing"),(0,a.mdx)("p",null,"In the example above ",(0,a.mdx)("inlineCode",{parentName:"p"},"cfg")," is duck typed as ",(0,a.mdx)("inlineCode",{parentName:"p"},"MySQLConfig"),".\nIt is actually an instance of ",(0,a.mdx)("inlineCode",{parentName:"p"},"DictConfig"),". The duck typing enables static type checking by tools like Mypy or PyCharm.\nThis reduces development time by catching coding errors before you run your application."),(0,a.mdx)("p",null,"The name ",(0,a.mdx)("a",{parentName:"p",href:"https://en.wikipedia.org/wiki/Duck_typing"},"Duck typing"),' comes from the phrase "If it walks like a duck, swims like a duck, and quacks like a duck, then it probably is a duck".\nIt can be useful when you care about the methods or attributes of an object, not the actual type of the object.'))}d.isMDXComponent=!0},49595:(e,t,n)=>{n.d(t,{A:()=>p,C:()=>m});var r=n(58168),a=n(96540),i=n(75489),o=n(44586),l=n(48295);function c(e){const t=(0,l.ir)();return(0,o.default)().siteConfig.customFields.githubLinkVersionToBaseUrl[t?.name??"current"]+e}function p(e){return a.createElement(i.default,(0,r.A)({},e,{to:c(e.to),target:"_blank"}))}function m(e){const t=e.text??"Example (Click Here)";return a.createElement(p,e,a.createElement("span",null,"\xa0"),a.createElement("img",{src:"https://img.shields.io/badge/-"+t+"-informational",alt:"Example (Click Here)"}))}}}]);