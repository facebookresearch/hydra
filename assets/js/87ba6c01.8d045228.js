"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[6419],{15680:(e,t,n)=>{n.r(t),n.d(t,{MDXContext:()=>p,MDXProvider:()=>m,mdx:()=>h,useMDXComponents:()=>d,withMDXComponents:()=>l});var i=n(96540);function r(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function o(){return o=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var i in n)Object.prototype.hasOwnProperty.call(n,i)&&(e[i]=n[i])}return e},o.apply(this,arguments)}function a(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);t&&(i=i.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,i)}return n}function c(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?a(Object(n),!0).forEach((function(t){r(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):a(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function s(e,t){if(null==e)return{};var n,i,r=function(e,t){if(null==e)return{};var n,i,r={},o=Object.keys(e);for(i=0;i<o.length;i++)n=o[i],t.indexOf(n)>=0||(r[n]=e[n]);return r}(e,t);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(e);for(i=0;i<o.length;i++)n=o[i],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(r[n]=e[n])}return r}var p=i.createContext({}),l=function(e){return function(t){var n=d(t.components);return i.createElement(e,o({},t,{components:n}))}},d=function(e){var t=i.useContext(p),n=t;return e&&(n="function"==typeof e?e(t):c(c({},t),e)),n},m=function(e){var t=d(e.components);return i.createElement(p.Provider,{value:t},e.children)},u="mdxType",f={inlineCode:"code",wrapper:function(e){var t=e.children;return i.createElement(i.Fragment,{},t)}},y=i.forwardRef((function(e,t){var n=e.components,r=e.mdxType,o=e.originalType,a=e.parentName,p=s(e,["components","mdxType","originalType","parentName"]),l=d(n),m=r,u=l["".concat(a,".").concat(m)]||l[m]||f[m]||o;return n?i.createElement(u,c(c({ref:t},p),{},{components:n})):i.createElement(u,c({ref:t},p))}));function h(e,t){var n=arguments,r=t&&t.mdxType;if("string"==typeof e||r){var o=n.length,a=new Array(o);a[0]=y;var c={};for(var s in t)hasOwnProperty.call(t,s)&&(c[s]=t[s]);c.originalType=e,c[u]="string"==typeof e?e:r,a[1]=c;for(var p=2;p<o;p++)a[p]=n[p];return i.createElement.apply(null,a)}return i.createElement.apply(null,n)}y.displayName="MDXCreateElement"},52541:(e,t,n)=>{n.r(t),n.d(t,{assets:()=>s,contentTitle:()=>a,default:()=>m,frontMatter:()=>o,metadata:()=>c,toc:()=>p});var i=n(58168),r=(n(96540),n(15680));const o={id:"unit_testing",title:"Hydra in Unit Tests"},a=void 0,c={unversionedId:"advanced/unit_testing",id:"version-1.0/advanced/unit_testing",title:"Hydra in Unit Tests",description:"Use initialize(), initializeconfigmodule() or initializeconfigdir() in conjunction with compose()",source:"@site/versioned_docs/version-1.0/advanced/unit_testing.md",sourceDirName:"advanced",slug:"/advanced/unit_testing",permalink:"/docs/1.0/advanced/unit_testing",draft:!1,editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/versioned_docs/version-1.0/advanced/unit_testing.md",tags:[],version:"1.0",lastUpdatedBy:"jesszzzz",lastUpdatedAt:1744041844,formattedLastUpdatedAt:"Apr 7, 2025",frontMatter:{id:"unit_testing",title:"Hydra in Unit Tests"},sidebar:"docs",previous:{title:"Hydra in Jupyter Notebooks",permalink:"/docs/1.0/advanced/jupyter_notebooks"},next:{title:"Introduction",permalink:"/docs/1.0/experimental/intro"}},s={},p=[],l={toc:p},d="wrapper";function m(e){let{components:t,...n}=e;return(0,r.mdx)(d,(0,i.A)({},l,n,{components:t,mdxType:"MDXLayout"}),(0,r.mdx)("p",null,"Use ",(0,r.mdx)("inlineCode",{parentName:"p"},"initialize()"),", ",(0,r.mdx)("inlineCode",{parentName:"p"},"initialize_config_module()")," or ",(0,r.mdx)("inlineCode",{parentName:"p"},"initialize_config_dir()")," in conjunction with ",(0,r.mdx)("inlineCode",{parentName:"p"},"compose()"),"\nto compose configs inside your unit tests.",(0,r.mdx)("br",{parentName:"p"}),"\n","Be sure to read the ",(0,r.mdx)("a",{parentName:"p",href:"/docs/1.0/experimental/compose_api"},"Compose API documentation"),"."),(0,r.mdx)("p",null,"The Hydra example application contains complete ",(0,r.mdx)("a",{parentName:"p",href:"https://github.com/facebookresearch/hydra/tree/1.0_branch/examples/advanced/hydra_app_example/tests/test_example.py"},"example test"),"."),(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-python",metastring:'title="Testing example with initialize()"',title:'"Testing',example:!0,with:!0,'initialize()"':!0},'from hydra.experimental import initialize, compose\n# 1. initialize will add config_path the config search path within the context\n# 2. The module with your configs should be importable. \n#    it needs to have a __init__.py (can be empty).\n# 3. THe config path is relative to the file calling initialize (this file)\ndef test_with_initialize() -> None:\n    with initialize(config_path="../hydra_app/conf"):\n        # config is relative to a module\n        cfg = compose(config_name="config", overrides=["app.user=test_user"])\n        assert cfg == {\n            "app": {"user": "test_user", "num1": 10, "num2": 20},\n            "db": {"host": "localhost", "port": 3306},\n        }\n')))}m.isMDXComponent=!0}}]);