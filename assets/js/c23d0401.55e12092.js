"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[168],{15680:(e,t,n)=>{n.r(t),n.d(t,{MDXContext:()=>m,MDXProvider:()=>c,mdx:()=>y,useMDXComponents:()=>p,withMDXComponents:()=>d});var a=n(96540);function i(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function o(){return o=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var a in n)Object.prototype.hasOwnProperty.call(n,a)&&(e[a]=n[a])}return e},o.apply(this,arguments)}function r(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);t&&(a=a.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,a)}return n}function l(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?r(Object(n),!0).forEach((function(t){i(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):r(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function s(e,t){if(null==e)return{};var n,a,i=function(e,t){if(null==e)return{};var n,a,i={},o=Object.keys(e);for(a=0;a<o.length;a++)n=o[a],t.indexOf(n)>=0||(i[n]=e[n]);return i}(e,t);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(e);for(a=0;a<o.length;a++)n=o[a],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(i[n]=e[n])}return i}var m=a.createContext({}),d=function(e){return function(t){var n=p(t.components);return a.createElement(e,o({},t,{components:n}))}},p=function(e){var t=a.useContext(m),n=t;return e&&(n="function"==typeof e?e(t):l(l({},t),e)),n},c=function(e){var t=p(e.components);return a.createElement(m.Provider,{value:t},e.children)},u="mdxType",h={inlineCode:"code",wrapper:function(e){var t=e.children;return a.createElement(a.Fragment,{},t)}},f=a.forwardRef((function(e,t){var n=e.components,i=e.mdxType,o=e.originalType,r=e.parentName,m=s(e,["components","mdxType","originalType","parentName"]),d=p(n),c=i,u=d["".concat(r,".").concat(c)]||d[c]||h[c]||o;return n?a.createElement(u,l(l({ref:t},m),{},{components:n})):a.createElement(u,l({ref:t},m))}));function y(e,t){var n=arguments,i=t&&t.mdxType;if("string"==typeof e||i){var o=n.length,r=new Array(o);r[0]=f;var l={};for(var s in t)hasOwnProperty.call(t,s)&&(l[s]=t[s]);l.originalType=e,l[u]="string"==typeof e?e:i,r[1]=l;for(var m=2;m<o;m++)r[m]=n[m];return a.createElement.apply(null,r)}return a.createElement.apply(null,n)}f.displayName="MDXCreateElement"},44518:(e,t,n)=>{n.r(t),n.d(t,{assets:()=>m,contentTitle:()=>l,default:()=>u,frontMatter:()=>r,metadata:()=>s,toc:()=>d});var a=n(58168),i=(n(96540),n(15680)),o=n(49595);const r={id:"compose_api",title:"Compose API",sidebar_label:"Compose API"},l=void 0,s={unversionedId:"advanced/compose_api",id:"advanced/compose_api",title:"Compose API",description:"The compose API can compose a config similarly to @hydra.main() anywhere in the code.",source:"@site/docs/advanced/compose_api.md",sourceDirName:"advanced",slug:"/advanced/compose_api",permalink:"/docs/advanced/compose_api",draft:!1,editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/docs/advanced/compose_api.md",tags:[],version:"current",lastUpdatedBy:"jesszzzz",lastUpdatedAt:1741383139,formattedLastUpdatedAt:"Mar 7, 2025",frontMatter:{id:"compose_api",title:"Compose API",sidebar_label:"Compose API"},sidebar:"docs",previous:{title:"Structured Configs example",permalink:"/docs/advanced/instantiate_objects/structured_config"},next:{title:"Config Search Path",permalink:"/docs/advanced/search_path"}},m={},d=[{value:"When to use the Compose API",id:"when-to-use-the-compose-api",level:3},{value:"Initialization methods",id:"initialization-methods",level:3},{value:"Code example",id:"code-example",level:3},{value:"API Documentation",id:"api-documentation",level:3}],p={toc:d},c="wrapper";function u(e){let{components:t,...n}=e;return(0,i.mdx)(c,(0,a.A)({},p,n,{components:t,mdxType:"MDXLayout"}),(0,i.mdx)("p",null,"The compose API can compose a config similarly to ",(0,i.mdx)("inlineCode",{parentName:"p"},"@hydra.main()")," anywhere in the code.",(0,i.mdx)("br",{parentName:"p"}),"\n","Prior to calling compose(), you have to initialize Hydra: This can be done by using the standard ",(0,i.mdx)("inlineCode",{parentName:"p"},"@hydra.main()"),"\nor by calling one of the initialization methods listed below."),(0,i.mdx)("h3",{id:"when-to-use-the-compose-api"},"When to use the Compose API"),(0,i.mdx)("p",null,"The Compose API is useful when ",(0,i.mdx)("inlineCode",{parentName:"p"},"@hydra.main()")," is not applicable.\nFor example:"),(0,i.mdx)("ul",null,(0,i.mdx)("li",{parentName:"ul"},"Inside a Jupyter notebook (",(0,i.mdx)("a",{parentName:"li",href:"/docs/advanced/jupyter_notebooks"},"Example"),")"),(0,i.mdx)("li",{parentName:"ul"},"Inside a unit test (",(0,i.mdx)("a",{parentName:"li",href:"/docs/advanced/unit_testing"},"Example"),")"),(0,i.mdx)("li",{parentName:"ul"},"In parts of your application that does not have access to the command line (",(0,i.mdx)(o.A,{to:"examples/advanced/ad_hoc_composition",mdxType:"GithubLink"},"Example"),")."),(0,i.mdx)("li",{parentName:"ul"},"To compose multiple configuration objects (",(0,i.mdx)(o.A,{to:"examples/advanced/ray_example/ray_compose_example.py",mdxType:"GithubLink"},"Example with Ray"),").")),(0,i.mdx)("div",{class:"alert alert--info",role:"alert"},"Please avoid using the Compose API in cases where ",(0,i.mdx)("b",null,"@hydra.main()")," can be used. Doing so forfeits many of the benefits of Hydra (e.g., Tab completion, Multirun, Working directory management, Logging management and more)"),(0,i.mdx)("h3",{id:"initialization-methods"},"Initialization methods"),(0,i.mdx)("p",null,"There are 3 initialization methods:"),(0,i.mdx)("ul",null,(0,i.mdx)("li",{parentName:"ul"},(0,i.mdx)(o.A,{to:"hydra/initialize.py#L37",mdxType:"GithubLink"},"initialize()"),": Initialize with a config path relative to the caller"),(0,i.mdx)("li",{parentName:"ul"},(0,i.mdx)(o.A,{to:"hydra/initialize.py#L108",mdxType:"GithubLink"},"initialize_config_module()"),": Initialize with config_module (absolute)"),(0,i.mdx)("li",{parentName:"ul"},(0,i.mdx)(o.A,{to:"hydra/initialize.py#L143",mdxType:"GithubLink"},"initialize_config_dir()"),": Initialize with a config_dir on the file system (absolute)")),(0,i.mdx)("p",null,"All 3 can be used as methods or contexts.\nWhen used as methods, they are initializing Hydra globally and should only be called once.\nWhen used as contexts, they are initializing Hydra within the context and can be used multiple times.\nLike ",(0,i.mdx)("b",null,"@hydra.main()")," all three support the ",(0,i.mdx)("a",{parentName:"p",href:"/docs/upgrades/version_base"},"version_base")," parameter\nto define the compatibility level to use."),(0,i.mdx)("h3",{id:"code-example"},"Code example"),(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre",className:"language-python"},'from hydra import compose, initialize\nfrom omegaconf import OmegaConf\n\nif __name__ == "__main__":\n    # context initialization\n    with initialize(version_base=None, config_path="conf", job_name="test_app"):\n        cfg = compose(config_name="config", overrides=["db=mysql", "db.user=me"])\n        print(OmegaConf.to_yaml(cfg))\n\n    # global initialization\n    initialize(version_base=None, config_path="conf", job_name="test_app")\n    cfg = compose(config_name="config", overrides=["db=mysql", "db.user=me"])\n    print(OmegaConf.to_yaml(cfg))\n')),(0,i.mdx)("h3",{id:"api-documentation"},"API Documentation"),(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre",className:"language-python",metastring:'title="Compose API"',title:'"Compose','API"':!0},'def compose(\n    config_name: Optional[str] = None,\n    overrides: List[str] = [],\n    return_hydra_config: bool = False,\n) -> DictConfig:\n    """\n    :param config_name: the name of the config\n           (usually the file name without the .yaml extension)\n    :param overrides: list of overrides for config file\n    :param return_hydra_config: True to return the hydra config node in the result\n    :return: the composed config\n    """\n')),(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre",className:"language-python",metastring:'title="Relative initialization"',title:'"Relative','initialization"':!0},'def initialize(\n    version_base: Optional[str],\n    config_path: Optional[str] = None,\n    job_name: Optional[str] = "app",\n    caller_stack_depth: int = 1,\n) -> None:\n    """\n    Initializes Hydra and add the config_path to the config search path.\n    config_path is relative to the parent of the caller.\n    Hydra detects the caller type automatically at runtime.\n\n    Supported callers:\n    - Python scripts\n    - Python modules\n    - Unit tests\n    - Jupyter notebooks.\n    :param version_base: compatibility level to use.\n    :param config_path: path relative to the parent of the caller\n    :param job_name: the value for hydra.job.name (By default it is automatically detected based on the caller)\n    :param caller_stack_depth: stack depth of the caller, defaults to 1 (direct caller).\n    """\n')),(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre",className:"language-python",metastring:'title="Initialzing with config module"',title:'"Initialzing',with:!0,config:!0,'module"':!0},'def initialize_config_module(\n    config_module: str,\n    version_base: Optional[str],\n    job_name: str = "app"\n) -> None:\n    """\n    Initializes Hydra and add the config_module to the config search path.\n    The config module must be importable (an __init__.py must exist at its top level)\n    :param config_module: absolute module name, for example "foo.bar.conf".\n    :param version_base: compatibility level to use.\n    :param job_name: the value for hydra.job.name (default is \'app\')\n    """\n')),(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre",className:"language-python",metastring:'title="Initialzing with config directory"',title:'"Initialzing',with:!0,config:!0,'directory"':!0},'def initialize_config_dir(\n    config_dir: str,\n    version_base: Optional[str],\n    job_name: str = "app"\n) -> None:\n    """\n    Initializes Hydra and add an absolute config dir to the to the config search path.\n    The config_dir is always a path on the file system and is must be an absolute path.\n    Relative paths will result in an error.\n    :param config_dir: absolute file system path\n    :param version_base: compatibility level to use.\n    :param job_name: the value for hydra.job.name (default is \'app\')\n    """\n')))}u.isMDXComponent=!0},49595:(e,t,n)=>{n.d(t,{A:()=>m,C:()=>d});var a=n(58168),i=n(96540),o=n(75489),r=n(44586),l=n(48295);function s(e){const t=(0,l.ir)();return(0,r.default)().siteConfig.customFields.githubLinkVersionToBaseUrl[t?.name??"current"]+e}function m(e){return i.createElement(o.default,(0,a.A)({},e,{to:s(e.to),target:"_blank"}))}function d(e){const t=e.text??"Example (Click Here)";return i.createElement(m,e,i.createElement("span",null,"\xa0"),i.createElement("img",{src:"https://img.shields.io/badge/-"+t+"-informational",alt:"Example (Click Here)"}))}}}]);