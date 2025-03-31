"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[308],{10264:(e,t,n)=>{n.r(t),n.d(t,{assets:()=>p,contentTitle:()=>s,default:()=>u,frontMatter:()=>o,metadata:()=>c,toc:()=>l});var i=n(58168),r=(n(96540),n(15680)),a=n(49595);const o={id:"unit_testing",title:"Hydra in Unit Tests"},s=void 0,c={unversionedId:"advanced/unit_testing",id:"version-1.3/advanced/unit_testing",title:"Hydra in Unit Tests",description:"Use initialize(), initializeconfigmodule() or initializeconfigdir() in conjunction with compose()",source:"@site/versioned_docs/version-1.3/advanced/unit_testing.md",sourceDirName:"advanced",slug:"/advanced/unit_testing",permalink:"/docs/1.3/advanced/unit_testing",draft:!1,editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/versioned_docs/version-1.3/advanced/unit_testing.md",tags:[],version:"1.3",lastUpdatedBy:"jesszzzz",lastUpdatedAt:1743461536,formattedLastUpdatedAt:"Mar 31, 2025",frontMatter:{id:"unit_testing",title:"Hydra in Unit Tests"},sidebar:"docs",previous:{title:"Hydra in Jupyter Notebooks",permalink:"/docs/1.3/advanced/jupyter_notebooks"},next:{title:"Introduction",permalink:"/docs/1.3/experimental/intro"}},p={},l=[],d={toc:l},m="wrapper";function u(e){let{components:t,...n}=e;return(0,r.mdx)(m,(0,i.A)({},d,n,{components:t,mdxType:"MDXLayout"}),(0,r.mdx)("p",null,"Use ",(0,r.mdx)("inlineCode",{parentName:"p"},"initialize()"),", ",(0,r.mdx)("inlineCode",{parentName:"p"},"initialize_config_module()")," or ",(0,r.mdx)("inlineCode",{parentName:"p"},"initialize_config_dir()")," in conjunction with ",(0,r.mdx)("inlineCode",{parentName:"p"},"compose()"),"\nto compose configs inside your unit tests.",(0,r.mdx)("br",{parentName:"p"}),"\n","Be sure to read the ",(0,r.mdx)("a",{parentName:"p",href:"/docs/1.3/advanced/compose_api"},"Compose API documentation"),"."),(0,r.mdx)("p",null,"The Hydra example application contains an ",(0,r.mdx)(a.A,{to:"examples/advanced/hydra_app_example/tests/test_example.py",mdxType:"GithubLink"},"example test"),"."),(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-python",metastring:'title="Testing example with initialize()"',title:'"Testing',example:!0,with:!0,'initialize()"':!0},'from hydra import initialize, compose\n# 1. initialize will add config_path the config search path within the context\n# 2. The module with your configs should be importable. \n#    it needs to have a __init__.py (can be empty).\n# 3. THe config path is relative to the file calling initialize (this file)\ndef test_with_initialize() -> None:\n    with initialize(version_base=None, config_path="../hydra_app/conf"):\n        # config is relative to a module\n        cfg = compose(config_name="config", overrides=["app.user=test_user"])\n        assert cfg == {\n            "app": {"user": "test_user", "num1": 10, "num2": 20},\n            "db": {"host": "localhost", "port": 3306},\n        }\n')),(0,r.mdx)("p",null,"For an idea about how to modify Hydra's search path when using ",(0,r.mdx)("inlineCode",{parentName:"p"},"compose")," in\nunit tests, see the page on\n",(0,r.mdx)("a",{parentName:"p",href:"/docs/1.3/advanced/search_path#overriding-hydrasearchpath-config"},"overriding the ",(0,r.mdx)("inlineCode",{parentName:"a"},"hydra.searchpath")," config"),"."))}u.isMDXComponent=!0},15680:(e,t,n)=>{n.r(t),n.d(t,{MDXContext:()=>p,MDXProvider:()=>m,mdx:()=>g,useMDXComponents:()=>d,withMDXComponents:()=>l});var i=n(96540);function r(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function a(){return a=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var i in n)Object.prototype.hasOwnProperty.call(n,i)&&(e[i]=n[i])}return e},a.apply(this,arguments)}function o(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);t&&(i=i.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,i)}return n}function s(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?o(Object(n),!0).forEach((function(t){r(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):o(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function c(e,t){if(null==e)return{};var n,i,r=function(e,t){if(null==e)return{};var n,i,r={},a=Object.keys(e);for(i=0;i<a.length;i++)n=a[i],t.indexOf(n)>=0||(r[n]=e[n]);return r}(e,t);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);for(i=0;i<a.length;i++)n=a[i],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(r[n]=e[n])}return r}var p=i.createContext({}),l=function(e){return function(t){var n=d(t.components);return i.createElement(e,a({},t,{components:n}))}},d=function(e){var t=i.useContext(p),n=t;return e&&(n="function"==typeof e?e(t):s(s({},t),e)),n},m=function(e){var t=d(e.components);return i.createElement(p.Provider,{value:t},e.children)},u="mdxType",f={inlineCode:"code",wrapper:function(e){var t=e.children;return i.createElement(i.Fragment,{},t)}},h=i.forwardRef((function(e,t){var n=e.components,r=e.mdxType,a=e.originalType,o=e.parentName,p=c(e,["components","mdxType","originalType","parentName"]),l=d(n),m=r,u=l["".concat(o,".").concat(m)]||l[m]||f[m]||a;return n?i.createElement(u,s(s({ref:t},p),{},{components:n})):i.createElement(u,s({ref:t},p))}));function g(e,t){var n=arguments,r=t&&t.mdxType;if("string"==typeof e||r){var a=n.length,o=new Array(a);o[0]=h;var s={};for(var c in t)hasOwnProperty.call(t,c)&&(s[c]=t[c]);s.originalType=e,s[u]="string"==typeof e?e:r,o[1]=s;for(var p=2;p<a;p++)o[p]=n[p];return i.createElement.apply(null,o)}return i.createElement.apply(null,n)}h.displayName="MDXCreateElement"},49595:(e,t,n)=>{n.d(t,{A:()=>p,C:()=>l});var i=n(58168),r=n(96540),a=n(75489),o=n(44586),s=n(48295);function c(e){const t=(0,s.ir)();return(0,o.default)().siteConfig.customFields.githubLinkVersionToBaseUrl[t?.name??"current"]+e}function p(e){return r.createElement(a.default,(0,i.A)({},e,{to:c(e.to),target:"_blank"}))}function l(e){const t=e.text??"Example (Click Here)";return r.createElement(p,e,r.createElement("span",null,"\xa0"),r.createElement("img",{src:"https://img.shields.io/badge/-"+t+"-informational",alt:"Example (Click Here)"}))}}}]);