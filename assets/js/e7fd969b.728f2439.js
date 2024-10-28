"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[8397],{15680:(e,t,n)=>{n.r(t),n.d(t,{MDXContext:()=>p,MDXProvider:()=>d,mdx:()=>f,useMDXComponents:()=>c,withMDXComponents:()=>s});var a=n(96540);function i(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function o(){return o=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var a in n)Object.prototype.hasOwnProperty.call(n,a)&&(e[a]=n[a])}return e},o.apply(this,arguments)}function r(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);t&&(a=a.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,a)}return n}function l(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?r(Object(n),!0).forEach((function(t){i(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):r(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function m(e,t){if(null==e)return{};var n,a,i=function(e,t){if(null==e)return{};var n,a,i={},o=Object.keys(e);for(a=0;a<o.length;a++)n=o[a],t.indexOf(n)>=0||(i[n]=e[n]);return i}(e,t);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(e);for(a=0;a<o.length;a++)n=o[a],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(i[n]=e[n])}return i}var p=a.createContext({}),s=function(e){return function(t){var n=c(t.components);return a.createElement(e,o({},t,{components:n}))}},c=function(e){var t=a.useContext(p),n=t;return e&&(n="function"==typeof e?e(t):l(l({},t),e)),n},d=function(e){var t=c(e.components);return a.createElement(p.Provider,{value:t},e.children)},u={inlineCode:"code",wrapper:function(e){var t=e.children;return a.createElement(a.Fragment,{},t)}},h=a.forwardRef((function(e,t){var n=e.components,i=e.mdxType,o=e.originalType,r=e.parentName,p=m(e,["components","mdxType","originalType","parentName"]),s=c(n),d=i,h=s["".concat(r,".").concat(d)]||s[d]||u[d]||o;return n?a.createElement(h,l(l({ref:t},p),{},{components:n})):a.createElement(h,l({ref:t},p))}));function f(e,t){var n=arguments,i=t&&t.mdxType;if("string"==typeof e||i){var o=n.length,r=new Array(o);r[0]=h;var l={};for(var m in t)hasOwnProperty.call(t,m)&&(l[m]=t[m]);l.originalType=e,l.mdxType="string"==typeof e?e:i,r[1]=l;for(var p=2;p<o;p++)r[p]=n[p];return a.createElement.apply(null,r)}return a.createElement.apply(null,n)}h.displayName="MDXCreateElement"},65665:(e,t,n)=>{n.r(t),n.d(t,{contentTitle:()=>m,default:()=>d,frontMatter:()=>l,metadata:()=>p,toc:()=>s});var a=n(58168),i=n(98587),o=(n(96540),n(15680)),r=["components"],l={id:"compose_api",title:"Compose API",sidebar_label:"Compose API"},m=void 0,p={unversionedId:"experimental/compose_api",id:"version-1.0/experimental/compose_api",title:"Compose API",description:"The compose API can compose a config similarly to @hydra.main() anywhere in the code.",source:"@site/versioned_docs/version-1.0/experimental/hydra_compose.md",sourceDirName:"experimental",slug:"/experimental/compose_api",permalink:"/docs/1.0/experimental/compose_api",editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/versioned_docs/version-1.0/experimental/hydra_compose.md",tags:[],version:"1.0",lastUpdatedBy:"dependabot[bot]",lastUpdatedAt:1730135614,formattedLastUpdatedAt:"10/28/2024",frontMatter:{id:"compose_api",title:"Compose API",sidebar_label:"Compose API"},sidebar:"version-1.0/docs",previous:{title:"Introduction",permalink:"/docs/1.0/experimental/intro"},next:{title:"Overview",permalink:"/docs/1.0/development/overview"}},s=[{value:"When to use the Compose API",id:"when-to-use-the-compose-api",children:[],level:3},{value:"Initialization methods",id:"initialization-methods",children:[],level:3},{value:"Code example",id:"code-example",children:[],level:3},{value:"API Documentation",id:"api-documentation",children:[],level:3}],c={toc:s};function d(e){var t=e.components,n=(0,i.A)(e,r);return(0,o.mdx)("wrapper",(0,a.A)({},c,n,{components:t,mdxType:"MDXLayout"}),(0,o.mdx)("p",null,"The compose API can compose a config similarly to ",(0,o.mdx)("inlineCode",{parentName:"p"},"@hydra.main()")," anywhere in the code.",(0,o.mdx)("br",{parentName:"p"}),"\n","Prior to calling compose(), you have to initialize Hydra: This can be done by using the standard ",(0,o.mdx)("inlineCode",{parentName:"p"},"@hydra.main()"),"\nor by calling one of the initialization methods listed below."),(0,o.mdx)("h3",{id:"when-to-use-the-compose-api"},"When to use the Compose API"),(0,o.mdx)("p",null,"The Compose API is useful when ",(0,o.mdx)("inlineCode",{parentName:"p"},"@hydra.main()")," is not applicable.\nFor example:"),(0,o.mdx)("ul",null,(0,o.mdx)("li",{parentName:"ul"},"Inside a Jupyter notebook (",(0,o.mdx)("a",{parentName:"li",href:"/docs/1.0/advanced/jupyter_notebooks"},"Example"),")"),(0,o.mdx)("li",{parentName:"ul"},"Inside a unit test (",(0,o.mdx)("a",{parentName:"li",href:"/docs/1.0/advanced/unit_testing"},"Example"),")"),(0,o.mdx)("li",{parentName:"ul"},"In parts of your application that does not have access to the command line (",(0,o.mdx)("a",{parentName:"li",href:"https://github.com/facebookresearch/hydra/tree/1.0_branch/examples/advanced/ad_hoc_composition"},"Example"),")"),(0,o.mdx)("li",{parentName:"ul"},"If you want to compose multiple configuration objects (",(0,o.mdx)("a",{parentName:"li",href:"https://github.com/facebookresearch/hydra/blob/master/examples/advanced/ray_example/ray_compose_example.py"},"Example with Ray"),")")),(0,o.mdx)("div",{class:"alert alert--info",role:"alert"},"Please avoid using the Compose API in cases where ",(0,o.mdx)("b",null,"@hydra.main()")," can be used. Doing so forfeits many of the benefits of Hydra (e.g., Tab completion, Multirun, Working directory management, Logging management and more)"),(0,o.mdx)("h3",{id:"initialization-methods"},"Initialization methods"),(0,o.mdx)("p",null,"There are 3 initialization methods:"),(0,o.mdx)("ul",null,(0,o.mdx)("li",{parentName:"ul"},(0,o.mdx)("inlineCode",{parentName:"li"},"initialize()"),": Initialize with a config path relative to the caller"),(0,o.mdx)("li",{parentName:"ul"},(0,o.mdx)("inlineCode",{parentName:"li"},"initialize_config_module()")," : Initialize with config_module (absolute)"),(0,o.mdx)("li",{parentName:"ul"},(0,o.mdx)("inlineCode",{parentName:"li"},"initialize_config_dir()")," : Initialize with a config_dir on the file system (absolute)")),(0,o.mdx)("p",null,"All 3 can be used as methods or contexts.\nWhen used as methods, they are are initializing Hydra globally and should only be called once.\nWhen used as contexts, they are initializing Hydra within the context can be used multiple times."),(0,o.mdx)("h3",{id:"code-example"},"Code example"),(0,o.mdx)("pre",null,(0,o.mdx)("code",{parentName:"pre",className:"language-python"},'from hydra.experimental import compose, initialize\nfrom omegaconf import OmegaConf\n\nif __name__ == "__main__":\n    # context initialization\n    with initialize(config_path="conf", job_name="test_app"):\n        cfg = compose(config_name="config", overrides=["db=mysql", "db.user=me"])\n        print(OmegaConf.to_yaml(cfg))\n\n    # global initialization\n    initialize(config_path="conf", job_name="test_app")\n    cfg = compose(config_name="config", overrides=["db=mysql", "db.user=me"])\n    print(OmegaConf.to_yaml(cfg))\n')),(0,o.mdx)("h3",{id:"api-documentation"},"API Documentation"),(0,o.mdx)("pre",null,(0,o.mdx)("code",{parentName:"pre",className:"language-python",metastring:'title="Compose API"',title:'"Compose','API"':!0},'def compose(\n    config_name: Optional[str] = None,\n    overrides: List[str] = [],\n    strict: Optional[bool] = None,\n    return_hydra_config: bool = False,\n) -> DictConfig:\n    """\n    :param config_name: the name of the config\n           (usually the file name without the .yaml extension)\n    :param overrides: list of overrides for config file\n    :param strict: optionally override the default strict mode\n    :param return_hydra_config: True to return the hydra config node in the result\n    :return: the composed config\n    """\n')),(0,o.mdx)("pre",null,(0,o.mdx)("code",{parentName:"pre",className:"language-python",metastring:'title="Relative initialization"',title:'"Relative','initialization"':!0},'def initialize(\n    config_path: Optional[str] = None,\n    job_name: Optional[str] = "app",\n    strict: Optional[bool] = None,\n    caller_stack_depth: int = 1,\n) -> None:\n    """\n    Initializes Hydra and add the config_path to the config search path.\n    config_path is relative to the parent of the caller.\n    Hydra detects the caller type automatically at runtime.\n\n    Supported callers:\n    - Python scripts\n    - Python modules\n    - Unit tests\n    - Jupyter notebooks.\n    :param config_path: path relative to the parent of the caller\n    :param job_name: the value for hydra.job.name (By default it is automatically detected based on the caller)\n    :param strict: (Deprecated), will be removed in the next major version\n    :param caller_stack_depth: stack depth of the caller, defaults to 1 (direct caller).\n    """\n')),(0,o.mdx)("pre",null,(0,o.mdx)("code",{parentName:"pre",className:"language-python",metastring:'title="Initialzing with config module"',title:'"Initialzing',with:!0,config:!0,'module"':!0},'def initialize_config_module(config_module: str, job_name: str = "app") -> None:\n    """\n    Initializes Hydra and add the config_module to the config search path.\n    The config module must be importable (an __init__.py must exist at its top level)\n    :param config_module: absolute module name, for example "foo.bar.conf".\n    :param job_name: the value for hydra.job.name (default is \'app\')\n    """\n')),(0,o.mdx)("pre",null,(0,o.mdx)("code",{parentName:"pre",className:"language-python",metastring:'title="Initialzing with config directory"',title:'"Initialzing',with:!0,config:!0,'directory"':!0},'def initialize_config_dir(config_dir: str, job_name: str = "app") -> None:\n    """\n    Initializes Hydra and add an absolute config dir to the to the config search path.\n    The config_dir is always a path on the file system and is must be an absolute path.\n    Relative paths will result in an error.\n    :param config_dir: absolute file system path\n    :param job_name: the value for hydra.job.name (default is \'app\')\n    """\n')))}d.isMDXComponent=!0}}]);