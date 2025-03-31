"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[3610],{15680:(e,n,a)=>{a.r(n),a.d(n,{MDXContext:()=>m,MDXProvider:()=>s,mdx:()=>g,useMDXComponents:()=>c,withMDXComponents:()=>p});var t=a(96540);function i(e,n,a){return n in e?Object.defineProperty(e,n,{value:a,enumerable:!0,configurable:!0,writable:!0}):e[n]=a,e}function r(){return r=Object.assign||function(e){for(var n=1;n<arguments.length;n++){var a=arguments[n];for(var t in a)Object.prototype.hasOwnProperty.call(a,t)&&(e[t]=a[t])}return e},r.apply(this,arguments)}function o(e,n){var a=Object.keys(e);if(Object.getOwnPropertySymbols){var t=Object.getOwnPropertySymbols(e);n&&(t=t.filter((function(n){return Object.getOwnPropertyDescriptor(e,n).enumerable}))),a.push.apply(a,t)}return a}function d(e){for(var n=1;n<arguments.length;n++){var a=null!=arguments[n]?arguments[n]:{};n%2?o(Object(a),!0).forEach((function(n){i(e,n,a[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(a)):o(Object(a)).forEach((function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(a,n))}))}return e}function l(e,n){if(null==e)return{};var a,t,i=function(e,n){if(null==e)return{};var a,t,i={},r=Object.keys(e);for(t=0;t<r.length;t++)a=r[t],n.indexOf(a)>=0||(i[a]=e[a]);return i}(e,n);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);for(t=0;t<r.length;t++)a=r[t],n.indexOf(a)>=0||Object.prototype.propertyIsEnumerable.call(e,a)&&(i[a]=e[a])}return i}var m=t.createContext({}),p=function(e){return function(n){var a=c(n.components);return t.createElement(e,r({},n,{components:a}))}},c=function(e){var n=t.useContext(m),a=n;return e&&(a="function"==typeof e?e(n):d(d({},n),e)),a},s=function(e){var n=c(e.components);return t.createElement(m.Provider,{value:n},e.children)},h="mdxType",f={inlineCode:"code",wrapper:function(e){var n=e.children;return t.createElement(t.Fragment,{},n)}},u=t.forwardRef((function(e,n){var a=e.components,i=e.mdxType,r=e.originalType,o=e.parentName,m=l(e,["components","mdxType","originalType","parentName"]),p=c(a),s=i,h=p["".concat(o,".").concat(s)]||p[s]||f[s]||r;return a?t.createElement(h,d(d({ref:n},m),{},{components:a})):t.createElement(h,d({ref:n},m))}));function g(e,n){var a=arguments,i=n&&n.mdxType;if("string"==typeof e||i){var r=a.length,o=new Array(r);o[0]=u;var d={};for(var l in n)hasOwnProperty.call(n,l)&&(d[l]=n[l]);d.originalType=e,d[h]="string"==typeof e?e:i,o[1]=d;for(var m=2;m<r;m++)o[m]=a[m];return t.createElement.apply(null,o)}return t.createElement.apply(null,a)}u.displayName="MDXCreateElement"},17765:(e,n,a)=>{a.r(n),a.d(n,{assets:()=>m,contentTitle:()=>d,default:()=>h,frontMatter:()=>o,metadata:()=>l,toc:()=>p});var t=a(58168),i=(a(96540),a(15680)),r=a(49595);const o={id:"search_path",title:"Config Search Path"},d=void 0,l={unversionedId:"advanced/search_path",id:"version-1.1/advanced/search_path",title:"Config Search Path",description:"The Config Search Path is a list of paths that Hydra searches in order to find non-primary configs. It is",source:"@site/versioned_docs/version-1.1/advanced/search_path.md",sourceDirName:"advanced",slug:"/advanced/search_path",permalink:"/docs/1.1/advanced/search_path",draft:!1,editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/versioned_docs/version-1.1/advanced/search_path.md",tags:[],version:"1.1",lastUpdatedBy:"jesszzzz",lastUpdatedAt:1743461536,formattedLastUpdatedAt:"Mar 31, 2025",frontMatter:{id:"search_path",title:"Config Search Path"},sidebar:"docs",previous:{title:"Compose API",permalink:"/docs/1.1/advanced/compose_api"},next:{title:"Plugins Overview",permalink:"/docs/1.1/advanced/plugins/overview"}},m={},p=[{value:"Using <code>@hydra.main()</code>",id:"using-hydramain",level:4},{value:"Overriding <code>hydra.searchpath</code> config",id:"overriding-hydrasearchpath-config",level:4},{value:"Overriding <code>--config-dir</code> from the command line",id:"overriding---config-dir-from-the-command-line",level:4},{value:"Creating a <code>SearchPathPlugin</code>",id:"creating-a-searchpathplugin",level:4}],c={toc:p},s="wrapper";function h(e){let{components:n,...a}=e;return(0,i.mdx)(s,(0,t.A)({},c,a,{components:n,mdxType:"MDXLayout"}),(0,i.mdx)("p",null,"The Config Search Path is a list of paths that Hydra searches in order to find ",(0,i.mdx)("strong",{parentName:"p"},"non-primary")," configs. It is\nsimilar to the Python ",(0,i.mdx)("inlineCode",{parentName:"p"},"PYTHONPATH"),"."),(0,i.mdx)("ul",null,(0,i.mdx)("li",{parentName:"ul"},"When a config is requested, The first matching config in the search path is used."),(0,i.mdx)("li",{parentName:"ul"},"Each search path element has a schema prefix such as ",(0,i.mdx)("inlineCode",{parentName:"li"},"file://")," or ",(0,i.mdx)("inlineCode",{parentName:"li"},"pkg://")," that corresponds to a ",(0,i.mdx)("inlineCode",{parentName:"li"},"ConfigSourcePlugin"),".",(0,i.mdx)("ul",{parentName:"li"},(0,i.mdx)("li",{parentName:"ul"},(0,i.mdx)("inlineCode",{parentName:"li"},"file://")," points to a file system path. It can either be an absolute path or a relative path.\nRelative path will be resolved to absolute based on the current working dir. Path separator is ",(0,i.mdx)("inlineCode",{parentName:"li"},"/")," on all Operating\nSystems."),(0,i.mdx)("li",{parentName:"ul"},(0,i.mdx)("inlineCode",{parentName:"li"},"pkg://")," points to an importable Python module, with ",(0,i.mdx)("inlineCode",{parentName:"li"},".")," being the separator. ",(0,i.mdx)("inlineCode",{parentName:"li"},"__init__.py")," files are needed in\ndirectories for Python to treat them as packages.")))),(0,i.mdx)("p",null,"You can inspect the search path and the configurations loaded by Hydra via the ",(0,i.mdx)("inlineCode",{parentName:"p"},"--info")," flag:"),(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre",className:"language-bash"},"$ python my_app.py --info searchpath\n")),(0,i.mdx)("p",null,"There are a few ways to modify the config search path, enabling Hydra to access configuration in\ndifferent locations.\nUse a combination of the methods described below:"),(0,i.mdx)("h4",{id:"using-hydramain"},"Using ",(0,i.mdx)("inlineCode",{parentName:"h4"},"@hydra.main()")),(0,i.mdx)("p",null,"Using the  ",(0,i.mdx)("inlineCode",{parentName:"p"},"config_path")," parameter ",(0,i.mdx)("inlineCode",{parentName:"p"},"@hydra.main()"),".  The ",(0,i.mdx)("inlineCode",{parentName:"p"},"config_path")," is relative to location of the Python script."),(0,i.mdx)("h4",{id:"overriding-hydrasearchpath-config"},"Overriding ",(0,i.mdx)("inlineCode",{parentName:"h4"},"hydra.searchpath")," config"),(0,i.mdx)(r.C,{text:"Example application",to:"examples/advanced/config_search_path",mdxType:"ExampleGithubLink"}),(0,i.mdx)("p",null,"In some cases you may want to add multiple locations to the search path.\nFor example, an app may want to read the configs from an additional Python module or\nan additional directory on the file system. Another example is in unit testing,\nwhere the defaults list in a config loaded from the ",(0,i.mdx)("inlineCode",{parentName:"p"},"tests/configs")," folder may\nmake reference to another config from the ",(0,i.mdx)("inlineCode",{parentName:"p"},"app/configs")," folder. If the\n",(0,i.mdx)("inlineCode",{parentName:"p"},"config_path")," or ",(0,i.mdx)("inlineCode",{parentName:"p"},"config_dir")," argument passed to ",(0,i.mdx)("inlineCode",{parentName:"p"},"@hydra.main")," or to one of the\n",(0,i.mdx)("a",{parentName:"p",href:"/docs/1.1/advanced/compose_api#initialization-methods"},"initialization methods")," points to\n",(0,i.mdx)("inlineCode",{parentName:"p"},"tests/configs"),", the configs located in ",(0,i.mdx)("inlineCode",{parentName:"p"},"app/configs")," will not be discoverable\nunless Hydra's search path is modified."),(0,i.mdx)("p",null,"You can configure ",(0,i.mdx)("inlineCode",{parentName:"p"},"hydra.searchpath")," in your primary config or from the command line."),(0,i.mdx)("admonition",{type:"info"},(0,i.mdx)("p",{parentName:"admonition"},"hydra.searchpath can ",(0,i.mdx)("strong",{parentName:"p"},"only")," be configured in the primary config. Attempting  to configure it in other\nconfigs will result in an error.")),(0,i.mdx)("p",null,"In this example, we add a second config directory - ",(0,i.mdx)("inlineCode",{parentName:"p"},"additional_conf"),", next to the first config directory:"),(0,i.mdx)("div",{className:"row"},(0,i.mdx)("div",{className:"col col--4"},(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre",className:"language-bash"},"\u251c\u2500\u2500 __init__.py\n\u251c\u2500\u2500 conf\n\u2502\xa0\xa0 \u251c\u2500\u2500 config.yaml\n\u2502\xa0\xa0 \u2514\u2500\u2500 dataset\n\u2502\xa0\xa0     \u2514\u2500\u2500 cifar10.yaml\n\u251c\u2500\u2500 additional_conf\n\u2502\xa0\xa0 \u251c\u2500\u2500 __init__.py\n\u2502\xa0\xa0 \u2514\u2500\u2500 dataset\n\u2502\xa0\xa0     \u2514\u2500\u2500 imagenet.yaml\n\u2514\u2500\u2500 my_app.py\n"))),(0,i.mdx)("div",{className:"col  col--8"},(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre",className:"language-python",metastring:'title="my_app.py"',title:'"my_app.py"'},'\n@hydra.main(config_path="conf", config_name="config")\ndef my_app(cfg: DictConfig) -> None:\n    print(OmegaConf.to_yaml(cfg))\n\n\nif __name__ == "__main__":\n    my_app()\n')))),(0,i.mdx)("p",null,(0,i.mdx)("inlineCode",{parentName:"p"},"conf/config.yaml")," is the primary config for ",(0,i.mdx)("inlineCode",{parentName:"p"},"my_app.py"),", config groups ",(0,i.mdx)("inlineCode",{parentName:"p"},"cifar10")," and ",(0,i.mdx)("inlineCode",{parentName:"p"},"imagenet")," are\nunder different folders.\nWe can add ",(0,i.mdx)("inlineCode",{parentName:"p"},"additional_conf")," to  ",(0,i.mdx)("inlineCode",{parentName:"p"},"hydra.searchpath")," for Hydra to discover ",(0,i.mdx)("inlineCode",{parentName:"p"},"dataset/imagenet"),"."),(0,i.mdx)("div",{className:"row"},(0,i.mdx)("div",{className:"col col--7"},(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="config.yaml"',title:'"config.yaml"'},"defaults:\n  - dataset: cifar10\n\nhydra:\n  searchpath:\n    - pkg://additional_conf\n    # You can also use file based schema:\n    # - file:///etc/my_app\n    # - file://${oc.env:HOME}/.my_app\n"))),(0,i.mdx)("div",{className:"col  col--5"},(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre",className:"language-python",metastring:'title="my_app.py output"',title:'"my_app.py','output"':!0},"dataset:\n  name: cifar10\n  path: /datasets/cifar10\n\n\n\n\n\n\n")))),(0,i.mdx)("p",null,"Overriding ",(0,i.mdx)("inlineCode",{parentName:"p"},"dataset=imagenet")," from the commandline:"),(0,i.mdx)("div",{className:"row"},(0,i.mdx)("div",{className:"col col--6"},(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre",className:"language-bash",metastring:'title="command line override"',title:'"command',line:!0,'override"':!0},"python my_app.py dataset=imagenet\n\n\n"))),(0,i.mdx)("div",{className:"col  col--6"},(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre",className:"language-python",metastring:'title="my_app.py output"',title:'"my_app.py','output"':!0},"dataset:\n  name: imagenet\n  path: /datasets/imagenet\n")))),(0,i.mdx)("p",null,(0,i.mdx)("inlineCode",{parentName:"p"},"hydra.searchpath")," can be defined or overridden via the command line as well:"),(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre",className:"language-bash",metastring:'title="command line override"',title:'"command',line:!0,'override"':!0},"python my_app.py 'hydra.searchpath=[pkg://additional_conf]'\n")),(0,i.mdx)("h4",{id:"overriding---config-dir-from-the-command-line"},"Overriding ",(0,i.mdx)("inlineCode",{parentName:"h4"},"--config-dir")," from the command line"),(0,i.mdx)("p",null,"This is a less flexible alternative to ",(0,i.mdx)("inlineCode",{parentName:"p"},"hydra.searchpath"),".\nSee this ",(0,i.mdx)("a",{parentName:"p",href:"/docs/1.1/advanced/hydra-command-line-flags"},"page")," for more info."),(0,i.mdx)("h4",{id:"creating-a-searchpathplugin"},"Creating a ",(0,i.mdx)("inlineCode",{parentName:"h4"},"SearchPathPlugin")),(0,i.mdx)(r.C,{text:"ExampleSearchPathPlugin",to:"examples/plugins/example_searchpath_plugin/",mdxType:"ExampleGithubLink"}),(0,i.mdx)("p",null,"Framework authors may want to add their configs to the search path automatically once their package is installed,\neliminating the need for any actions from the users.\nThis can be achieved using a ",(0,i.mdx)("inlineCode",{parentName:"p"},"SearchPathPlugin"),". Check the example plugin linked above for more details."))}h.isMDXComponent=!0},49595:(e,n,a)=>{a.d(n,{A:()=>m,C:()=>p});var t=a(58168),i=a(96540),r=a(75489),o=a(44586),d=a(48295);function l(e){const n=(0,d.ir)();return(0,o.default)().siteConfig.customFields.githubLinkVersionToBaseUrl[n?.name??"current"]+e}function m(e){return i.createElement(r.default,(0,t.A)({},e,{to:l(e.to),target:"_blank"}))}function p(e){const n=e.text??"Example (Click Here)";return i.createElement(m,e,i.createElement("span",null,"\xa0"),i.createElement("img",{src:"https://img.shields.io/badge/-"+n+"-informational",alt:"Example (Click Here)"}))}}}]);