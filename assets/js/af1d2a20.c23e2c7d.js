"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[8292],{15680:(e,n,t)=>{t.r(n),t.d(n,{MDXContext:()=>l,MDXProvider:()=>s,mdx:()=>v,useMDXComponents:()=>m,withMDXComponents:()=>d});var r=t(96540);function o(e,n,t){return n in e?Object.defineProperty(e,n,{value:t,enumerable:!0,configurable:!0,writable:!0}):e[n]=t,e}function a(){return a=Object.assign||function(e){for(var n=1;n<arguments.length;n++){var t=arguments[n];for(var r in t)Object.prototype.hasOwnProperty.call(t,r)&&(e[r]=t[r])}return e},a.apply(this,arguments)}function i(e,n){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);n&&(r=r.filter((function(n){return Object.getOwnPropertyDescriptor(e,n).enumerable}))),t.push.apply(t,r)}return t}function c(e){for(var n=1;n<arguments.length;n++){var t=null!=arguments[n]?arguments[n]:{};n%2?i(Object(t),!0).forEach((function(n){o(e,n,t[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):i(Object(t)).forEach((function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(t,n))}))}return e}function p(e,n){if(null==e)return{};var t,r,o=function(e,n){if(null==e)return{};var t,r,o={},a=Object.keys(e);for(r=0;r<a.length;r++)t=a[r],n.indexOf(t)>=0||(o[t]=e[t]);return o}(e,n);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);for(r=0;r<a.length;r++)t=a[r],n.indexOf(t)>=0||Object.prototype.propertyIsEnumerable.call(e,t)&&(o[t]=e[t])}return o}var l=r.createContext({}),d=function(e){return function(n){var t=m(n.components);return r.createElement(e,a({},n,{components:t}))}},m=function(e){var n=r.useContext(l),t=n;return e&&(t="function"==typeof e?e(n):c(c({},n),e)),t},s=function(e){var n=m(e.components);return r.createElement(l.Provider,{value:n},e.children)},u="mdxType",f={inlineCode:"code",wrapper:function(e){var n=e.children;return r.createElement(r.Fragment,{},n)}},y=r.forwardRef((function(e,n){var t=e.components,o=e.mdxType,a=e.originalType,i=e.parentName,l=p(e,["components","mdxType","originalType","parentName"]),d=m(t),s=o,u=d["".concat(i,".").concat(s)]||d[s]||f[s]||a;return t?r.createElement(u,c(c({ref:n},l),{},{components:t})):r.createElement(u,c({ref:n},l))}));function v(e,n){var t=arguments,o=n&&n.mdxType;if("string"==typeof e||o){var a=t.length,i=new Array(a);i[0]=y;var c={};for(var p in n)hasOwnProperty.call(n,p)&&(c[p]=n[p]);c.originalType=e,c[u]="string"==typeof e?e:o,i[1]=c;for(var l=2;l<a;l++)i[l]=t[l];return r.createElement.apply(null,i)}return r.createElement.apply(null,t)}y.displayName="MDXCreateElement"},32678:(e,n,t)=>{t.r(n),t.d(n,{assets:()=>p,contentTitle:()=>i,default:()=>s,frontMatter:()=>a,metadata:()=>c,toc:()=>l});var r=t(58168),o=(t(96540),t(15680));const a={id:"compose_api",title:"Compose API",sidebar_label:"Experimental compose API"},i=void 0,c={unversionedId:"advanced/compose_api",id:"version-0.11/advanced/compose_api",title:"Compose API",description:"Hydra 0.11.0 introduces a new experimental API for composing configuration via the hydra.experimental.compose() function.",source:"@site/versioned_docs/version-0.11/advanced/hydra_compose.md",sourceDirName:"advanced",slug:"/advanced/compose_api",permalink:"/docs/0.11/advanced/compose_api",draft:!1,editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/versioned_docs/version-0.11/advanced/hydra_compose.md",tags:[],version:"0.11",lastUpdatedBy:"dependabot[bot]",lastUpdatedAt:1743717584,formattedLastUpdatedAt:"Apr 3, 2025",frontMatter:{id:"compose_api",title:"Compose API",sidebar_label:"Experimental compose API"},sidebar:"docs",previous:{title:"Hydra plugins",permalink:"/docs/0.11/advanced/plugins"},next:{title:"Ray example",permalink:"/docs/0.11/advanced/ray_example"}},p={},l=[{value:"<code>hydra.experimental.compose()</code> example",id:"hydraexperimentalcompose-example",level:3},{value:"API Documentation",id:"api-documentation",level:3}],d={toc:l},m="wrapper";function s(e){let{components:n,...t}=e;return(0,o.mdx)(m,(0,r.A)({},d,t,{components:n,mdxType:"MDXLayout"}),(0,o.mdx)("p",null,"Hydra 0.11.0 introduces a new experimental API for composing configuration via the ",(0,o.mdx)("inlineCode",{parentName:"p"},"hydra.experimental.compose()")," function.\nPrior to calling compose(), you have to initialize Hydra: This can be done by using the standard ",(0,o.mdx)("inlineCode",{parentName:"p"},"@hydra.main()")," or by calling ",(0,o.mdx)("inlineCode",{parentName:"p"},"hydra.experimental.initialize()"),"."),(0,o.mdx)("p",null,"Here is an ",(0,o.mdx)("a",{parentName:"p",href:"https://github.com/facebookresearch/hydra/tree/0.11_branch/examples/notebook"},"example Jupyter notebook utilizing this API"),"."),(0,o.mdx)("h3",{id:"hydraexperimentalcompose-example"},(0,o.mdx)("inlineCode",{parentName:"h3"},"hydra.experimental.compose()")," example"),(0,o.mdx)("pre",null,(0,o.mdx)("code",{parentName:"pre",className:"language-python"},'from hydra.experimental import compose, initialize\n\n\nif __name__ == "__main__":\n    initialize(\n        config_dir="conf", strict=True,\n    )\n\n    cfg = compose("config.yaml", overrides=["db=mysql", "db.user=me"])\n    print(OmegaConf.to_yaml(cfg))\n')),(0,o.mdx)("h3",{id:"api-documentation"},"API Documentation"),(0,o.mdx)("pre",null,(0,o.mdx)("code",{parentName:"pre",className:"language-python"},'def compose(config_file=None, overrides=[], strict=None):\n    """\n    :param config_file: optional config file to load\n    :param overrides: list of overrides for config file\n    :param strict: optionally override the default strict mode\n    :return: the composed config\n    """\n\n\ndef initialize(config_dir=None, strict=None, caller_stack_depth=1):\n    """\n    Initializes the Hydra sub system\n\n    :param config_dir: config directory relative to the calling script\n    :param strict: Default value for strict mode\n    :param caller_stack_depth:\n    :return:\n    """\n')))}s.isMDXComponent=!0}}]);