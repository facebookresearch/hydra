"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[8196],{15680:(e,t,n)=>{n.r(t),n.d(t,{MDXContext:()=>d,MDXProvider:()=>c,mdx:()=>h,useMDXComponents:()=>p,withMDXComponents:()=>m});var a=n(96540);function i(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function r(){return r=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var a in n)Object.prototype.hasOwnProperty.call(n,a)&&(e[a]=n[a])}return e},r.apply(this,arguments)}function o(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);t&&(a=a.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,a)}return n}function s(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?o(Object(n),!0).forEach((function(t){i(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):o(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function l(e,t){if(null==e)return{};var n,a,i=function(e,t){if(null==e)return{};var n,a,i={},r=Object.keys(e);for(a=0;a<r.length;a++)n=r[a],t.indexOf(n)>=0||(i[n]=e[n]);return i}(e,t);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);for(a=0;a<r.length;a++)n=r[a],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(i[n]=e[n])}return i}var d=a.createContext({}),m=function(e){return function(t){var n=p(t.components);return a.createElement(e,r({},t,{components:n}))}},p=function(e){var t=a.useContext(d),n=t;return e&&(n="function"==typeof e?e(t):s(s({},t),e)),n},c=function(e){var t=p(e.components);return a.createElement(d.Provider,{value:t},e.children)},u="mdxType",g={inlineCode:"code",wrapper:function(e){var t=e.children;return a.createElement(a.Fragment,{},t)}},f=a.forwardRef((function(e,t){var n=e.components,i=e.mdxType,r=e.originalType,o=e.parentName,d=l(e,["components","mdxType","originalType","parentName"]),m=p(n),c=i,u=m["".concat(o,".").concat(c)]||m[c]||g[c]||r;return n?a.createElement(u,s(s({ref:t},d),{},{components:n})):a.createElement(u,s({ref:t},d))}));function h(e,t){var n=arguments,i=t&&t.mdxType;if("string"==typeof e||i){var r=n.length,o=new Array(r);o[0]=f;var s={};for(var l in t)hasOwnProperty.call(t,l)&&(s[l]=t[l]);s.originalType=e,s[u]="string"==typeof e?e:i,o[1]=s;for(var d=2;d<r;d++)o[d]=n[d];return a.createElement.apply(null,o)}return a.createElement.apply(null,n)}f.displayName="MDXCreateElement"},49595:(e,t,n)=>{n.d(t,{A:()=>d,C:()=>m});var a=n(58168),i=n(96540),r=n(75489),o=n(44586),s=n(48295);function l(e){const t=(0,s.ir)();return(0,o.default)().siteConfig.customFields.githubLinkVersionToBaseUrl[t?.name??"current"]+e}function d(e){return i.createElement(r.default,(0,a.A)({},e,{to:l(e.to),target:"_blank"}))}function m(e){const t=e.text??"Example (Click Here)";return i.createElement(d,e,i.createElement("span",null,"\xa0"),i.createElement("img",{src:"https://img.shields.io/badge/-"+t+"-informational",alt:"Example (Click Here)"}))}},60394:(e,t,n)=>{n.r(t),n.d(t,{assets:()=>d,contentTitle:()=>s,default:()=>f,frontMatter:()=>o,metadata:()=>l,toc:()=>m});var a=n(58168),i=(n(96540),n(15680)),r=n(49595);const o={id:"overview",title:"Instantiating objects with Hydra",sidebar_label:"Overview"},s=void 0,l={unversionedId:"advanced/instantiate_objects/overview",id:"advanced/instantiate_objects/overview",title:"Instantiating objects with Hydra",description:"One of the best ways to drive different behavior in an application is to instantiate different implementations of an interface.",source:"@site/docs/advanced/instantiate_objects/overview.md",sourceDirName:"advanced/instantiate_objects",slug:"/advanced/instantiate_objects/overview",permalink:"/docs/advanced/instantiate_objects/overview",draft:!1,editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/docs/advanced/instantiate_objects/overview.md",tags:[],version:"current",lastUpdatedBy:"jesszzzz",lastUpdatedAt:1741383139,formattedLastUpdatedAt:"Mar 7, 2025",frontMatter:{id:"overview",title:"Instantiating objects with Hydra",sidebar_label:"Overview"},sidebar:"docs",previous:{title:"Packages",permalink:"/docs/advanced/overriding_packages"},next:{title:"Config files example",permalink:"/docs/advanced/instantiate_objects/config_files"}},d={},m=[{value:"Simple usage",id:"simple-usage",level:3},{value:"Recursive instantiation",id:"recursive-instantiation",level:3},{value:"Disable recursive instantiation",id:"disable-recursive-instantiation",level:3},{value:"Parameter conversion strategies",id:"parameter-conversion-strategies",level:3},{value:"Partial Instantiation",id:"partial-instantiation",level:3},{value:"Instantiation of builtins",id:"instantiation-of-builtins",level:3},{value:"Dotpath lookup machinery",id:"dotpath-lookup-machinery",level:3}],p=(c="GithubLink",function(e){return console.warn("Component "+c+" was not imported, exported, or provided by MDXProvider as global scope"),(0,i.mdx)("div",e)});var c;const u={toc:m},g="wrapper";function f(e){let{components:t,...n}=e;return(0,i.mdx)(g,(0,a.A)({},u,n,{components:t,mdxType:"MDXLayout"}),(0,i.mdx)(r.C,{text:"Example applications",to:"examples/instantiate",mdxType:"ExampleGithubLink"}),(0,i.mdx)("p",null,"One of the best ways to drive different behavior in an application is to instantiate different implementations of an interface.\nThe code using the instantiated object only knows the interface which remains constant, but the behavior\nis determined by the actual object instance."),(0,i.mdx)("p",null,"Hydra provides ",(0,i.mdx)("inlineCode",{parentName:"p"},"hydra.utils.instantiate()")," (and its alias ",(0,i.mdx)("inlineCode",{parentName:"p"},"hydra.utils.call()"),") for instantiating objects and calling functions. Prefer ",(0,i.mdx)("inlineCode",{parentName:"p"},"instantiate")," for creating objects and ",(0,i.mdx)("inlineCode",{parentName:"p"},"call")," for invoking functions."),(0,i.mdx)("p",null,"Call/instantiate supports:"),(0,i.mdx)("ul",null,(0,i.mdx)("li",{parentName:"ul"},"Constructing an object by calling the ",(0,i.mdx)("inlineCode",{parentName:"li"},"__init__")," method"),(0,i.mdx)("li",{parentName:"ul"},"Calling functions, static functions, class methods and other callable global objects")),(0,i.mdx)("details",null,(0,i.mdx)("summary",null,"Instantiate API (Expand for details)"),(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre",className:"language-python"},'def instantiate(config: Any, *args: Any, **kwargs: Any) -> Any:\n    """\n    :param config: An config object describing what to call and what params to use.\n                   In addition to the parameters, the config must contain:\n                   _target_ : target class or callable name (str)\n                   And may contain:\n                   _args_: List-like of positional arguments to pass to the target\n                   _recursive_: Construct nested objects as well (bool).\n                                True by default.\n                                may be overridden via a _recursive_ key in\n                                the kwargs\n                   _convert_: Conversion strategy\n                        none    : Passed objects are DictConfig and ListConfig, default\n                        partial : Passed objects are converted to dict and list, with\n                                  the exception of Structured Configs (and their fields).\n                        object  : Passed objects are converted to dict and list.\n                                  Structured Configs are converted to instances of the\n                                  backing dataclass / attr class.\n                        all     : Passed objects are dicts, lists and primitives without\n                                  a trace of OmegaConf containers. Structured configs\n                                  are converted to dicts / lists too.\n                   _partial_: If True, return functools.partial wrapped method or object\n                              False by default. Configure per target.\n    :param args: Optional positional parameters pass-through\n    :param kwargs: Optional named parameters to override\n                   parameters in the config object. Parameters not present\n                   in the config objects are being passed as is to the target.\n                   IMPORTANT: dataclasses instances in kwargs are interpreted as config\n                              and cannot be used as passthrough\n    :return: if _target_ is a class name: the instantiated object\n             if _target_ is a callable: the return value of the call\n    """\n\n# Alias for instantiate\ncall = instantiate\n'))),(0,i.mdx)("br",null),(0,i.mdx)("p",null,"The config passed to these functions must have a key called ",(0,i.mdx)("inlineCode",{parentName:"p"},"_target_"),", with the value of a fully qualified class name, class method, static method or callable.\nFor convenience, ",(0,i.mdx)("inlineCode",{parentName:"p"},"None")," config results in a ",(0,i.mdx)("inlineCode",{parentName:"p"},"None")," object."),(0,i.mdx)("p",null,(0,i.mdx)("strong",{parentName:"p"},"Named arguments")," : Config fields (except reserved fields like ",(0,i.mdx)("inlineCode",{parentName:"p"},"_target_"),") are passed as named arguments to the target.\nNamed arguments in the config can be overridden by passing named argument with the same name in the ",(0,i.mdx)("inlineCode",{parentName:"p"},"instantiate()")," call-site."),(0,i.mdx)("p",null,(0,i.mdx)("strong",{parentName:"p"},"Positional arguments")," : The config may contain a ",(0,i.mdx)("inlineCode",{parentName:"p"},"_args_")," field representing positional arguments to pass to the target.\nThe positional arguments can be overridden together by passing positional arguments in the ",(0,i.mdx)("inlineCode",{parentName:"p"},"instantiate()")," call-site."),(0,i.mdx)("h3",{id:"simple-usage"},"Simple usage"),(0,i.mdx)("p",null,"Your application might have an Optimizer class:"),(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre",className:"language-python",metastring:'title="Example class"',title:'"Example','class"':!0},"class Optimizer:\n    algo: str\n    lr: float\n\n    def __init__(self, algo: str, lr: float) -> None:\n        self.algo = algo\n        self.lr = lr\n")),(0,i.mdx)("div",{className:"row"},(0,i.mdx)("div",{className:"col col--6"},(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="Config"',title:'"Config"'},"optimizer:\n  _target_: my_app.Optimizer\n  algo: SGD\n  lr: 0.01\n\n\n\n\n"))),(0,i.mdx)("div",{className:"col col--6"},(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre",className:"language-python",metastring:'title="Instantiation"',title:'"Instantiation"'},"opt = instantiate(cfg.optimizer)\nprint(opt)\n# Optimizer(algo=SGD,lr=0.01)\n\n# override parameters on the call-site\nopt = instantiate(cfg.optimizer, lr=0.2)\nprint(opt)\n# Optimizer(algo=SGD,lr=0.2)\n")))),(0,i.mdx)("h3",{id:"recursive-instantiation"},"Recursive instantiation"),(0,i.mdx)("p",null,"Let's add a Dataset and a Trainer class. The trainer holds a Dataset and an Optimizer instances."),(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre",className:"language-python",metastring:'title="Additional classes"',title:'"Additional','classes"':!0},"class Dataset:\n    name: str\n    path: str\n\n    def __init__(self, name: str, path: str) -> None:\n        self.name = name\n        self.path = path\n\n\nclass Trainer:\n    def __init__(self, optimizer: Optimizer, dataset: Dataset) -> None:\n        self.optimizer = optimizer\n        self.dataset = dataset\n")),(0,i.mdx)("p",null,"With the following config, you can instantiate the whole thing with a single call:"),(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="Example config"',title:'"Example','config"':!0},"trainer:\n  _target_: my_app.Trainer\n  optimizer:\n    _target_: my_app.Optimizer\n    algo: SGD\n    lr: 0.01\n  dataset:\n    _target_: my_app.Dataset\n    name: Imagenet\n    path: /datasets/imagenet\n")),(0,i.mdx)("p",null,"Hydra will instantiate nested objects recursively by default."),(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre",className:"language-python"},"trainer = instantiate(cfg.trainer)\nprint(trainer)\n# Trainer(\n#  optimizer=Optimizer(algo=SGD,lr=0.01),\n#  dataset=Dataset(name=Imagenet, path=/datasets/imagenet)\n# )\n")),(0,i.mdx)("p",null,"You can override parameters for nested objects:"),(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre",className:"language-python"},'trainer = instantiate(\n    cfg.trainer,\n    optimizer={"lr": 0.3},\n    dataset={"name": "cifar10", "path": "/datasets/cifar10"},\n)\nprint(trainer)\n# Trainer(\n#   optimizer=Optimizer(algo=SGD,lr=0.3),\n#   dataset=Dataset(name=cifar10, path=/datasets/cifar10)\n# )\n')),(0,i.mdx)("p",null,"Similarly, positional arguments of nested objects can be overridden:"),(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre",className:"language-python"},'obj = instantiate(\n    cfg.object,\n    # pass 1 and 2 as positional arguments to the target object\n    1, 2,  \n    # pass 3 and 4 as positional arguments to a nested child object\n    child={"_args_": [3, 4]},\n)\n')),(0,i.mdx)("h3",{id:"disable-recursive-instantiation"},"Disable recursive instantiation"),(0,i.mdx)("p",null,"You can disable recursive instantiation by setting ",(0,i.mdx)("inlineCode",{parentName:"p"},"_recursive_")," to ",(0,i.mdx)("inlineCode",{parentName:"p"},"False")," in the config node or in the call-site\nIn that case the Trainer object will receive an OmegaConf DictConfig for nested dataset and optimizer instead of the instantiated objects."),(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre",className:"language-python"},"optimizer = instantiate(cfg.trainer, _recursive_=False)\nprint(optimizer)\n")),(0,i.mdx)("p",null,"Output:"),(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre",className:"language-python"},"Trainer(\n  optimizer={\n    '_target_': 'my_app.Optimizer', 'algo': 'SGD', 'lr': 0.01\n  },\n  dataset={\n    '_target_': 'my_app.Dataset', 'name': 'Imagenet', 'path': '/datasets/imagenet'\n  }\n)\n")),(0,i.mdx)("h3",{id:"parameter-conversion-strategies"},"Parameter conversion strategies"),(0,i.mdx)("p",null,"By default, the parameters passed to the target are either primitives (int,\nfloat, bool etc) or OmegaConf containers (",(0,i.mdx)("inlineCode",{parentName:"p"},"DictConfig"),", ",(0,i.mdx)("inlineCode",{parentName:"p"},"ListConfig"),").\nOmegaConf containers have many advantages over primitive dicts and lists,\nincluding convenient attribute access for keys,\n",(0,i.mdx)("a",{parentName:"p",href:"https://omegaconf.readthedocs.io/en/latest/structured_config.html"},"duck-typing as instances of dataclasses or attrs classes"),", and\nsupport for ",(0,i.mdx)("a",{parentName:"p",href:"https://omegaconf.readthedocs.io/en/latest/usage.html#variable-interpolation"},"variable interpolation"),"\nand ",(0,i.mdx)("a",{parentName:"p",href:"https://omegaconf.readthedocs.io/en/latest/custom_resolvers.html"},"custom resolvers"),".\nIf the callable targeted by ",(0,i.mdx)("inlineCode",{parentName:"p"},"instantiate")," leverages OmegaConf's features, it\nwill make sense to pass ",(0,i.mdx)("inlineCode",{parentName:"p"},"DictConfig")," and ",(0,i.mdx)("inlineCode",{parentName:"p"},"ListConfig")," instances directly to\nthat callable."),(0,i.mdx)("p",null,"That being said, in many cases it's desired to pass normal Python dicts and\nlists, rather than ",(0,i.mdx)("inlineCode",{parentName:"p"},"DictConfig")," or ",(0,i.mdx)("inlineCode",{parentName:"p"},"ListConfig")," instances, as arguments to your\ncallable. You can change instantiate's argument conversion strategy using the\n",(0,i.mdx)("inlineCode",{parentName:"p"},"_convert_")," parameter. Supported values are:"),(0,i.mdx)("ul",null,(0,i.mdx)("li",{parentName:"ul"},(0,i.mdx)("inlineCode",{parentName:"li"},'"none"')," : Default behavior, Use OmegaConf containers"),(0,i.mdx)("li",{parentName:"ul"},(0,i.mdx)("inlineCode",{parentName:"li"},'"partial"')," : Convert OmegaConf containers to dict and list, except\nStructured Configs, which remain as DictConfig instances."),(0,i.mdx)("li",{parentName:"ul"},(0,i.mdx)("inlineCode",{parentName:"li"},'"object"')," : Convert OmegaConf containers to dict and list, except Structured\nConfigs, which are converted to instances of the backing dataclass / attr\nclass using ",(0,i.mdx)("inlineCode",{parentName:"li"},"OmegaConf.to_object"),"."),(0,i.mdx)("li",{parentName:"ul"},(0,i.mdx)("inlineCode",{parentName:"li"},'"all"')," : Convert everything to primitive containers")),(0,i.mdx)("p",null,"The conversion strategy applies recursively to all subconfigs of the instantiation target.\nHere is an example demonstrating the various conversion strategies:"),(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre",className:"language-python"},'from dataclasses import dataclass\nfrom omegaconf import DictConfig, OmegaConf\nfrom hydra.utils import instantiate\n\n@dataclass\nclass Foo:\n    a: int = 123\n\nclass MyTarget:\n    def __init__(self, foo, bar):\n        self.foo = foo\n        self.bar = bar\n\ncfg = OmegaConf.create(\n    {\n        "_target_": "__main__.MyTarget",\n        "foo": Foo(),\n        "bar": {"b": 456},\n    }\n)\n\nobj_none = instantiate(cfg, _convert_="none")\nassert isinstance(obj_none, MyTarget)\nassert isinstance(obj_none.foo, DictConfig)\nassert isinstance(obj_none.bar, DictConfig)\n\nobj_partial = instantiate(cfg, _convert_="partial")\nassert isinstance(obj_partial, MyTarget)\nassert isinstance(obj_partial.foo, DictConfig)\nassert isinstance(obj_partial.bar, dict)\n\nobj_object = instantiate(cfg, _convert_="object")\nassert isinstance(obj_object, MyTarget)\nassert isinstance(obj_object.foo, Foo)\nassert isinstance(obj_object.bar, dict)\n\nobj_all = instantiate(cfg, _convert_="all")\nassert isinstance(obj_all, MyTarget)\nassert isinstance(obj_all.foo, dict)\nassert isinstance(obj_all.bar, dict)\n')),(0,i.mdx)("p",null,"Passing the ",(0,i.mdx)("inlineCode",{parentName:"p"},"_convert_")," keyword argument to ",(0,i.mdx)("inlineCode",{parentName:"p"},"instantiate")," has the same effect as defining\na ",(0,i.mdx)("inlineCode",{parentName:"p"},"_convert_")," attribute on your config object. Here is an example creating\ninstances of ",(0,i.mdx)("inlineCode",{parentName:"p"},"MyTarget")," that are equivalent to the above:"),(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre",className:"language-python"},'cfg_none = OmegaConf.create({..., "_convert_": "none"})\nobj_none = instantiate(cfg_none)\n\ncfg_partial = OmegaConf.create({..., "_convert_": "partial"})\nobj_partial = instantiate(cfg_partial)\n\ncfg_object = OmegaConf.create({..., "_convert_": "object"})\nobj_object = instantiate(cfg_object)\n\ncfg_all = OmegaConf.create({..., "_convert_": "all"})\nobj_all = instantiate(cfg_all)\n')),(0,i.mdx)("h3",{id:"partial-instantiation"},"Partial Instantiation"),(0,i.mdx)("p",null,"Sometimes you may not set all parameters needed to instantiate an object from the configuration, in this case you can set\n",(0,i.mdx)("inlineCode",{parentName:"p"},"_partial_")," to be ",(0,i.mdx)("inlineCode",{parentName:"p"},"True")," to get a ",(0,i.mdx)("inlineCode",{parentName:"p"},"functools.partial")," wrapped object or method, then complete initializing the object in\nthe application code. Here is an example:"),(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre",className:"language-python",metastring:'title="Example classes"',title:'"Example','classes"':!0},'class Optimizer:\n    algo: str\n    lr: float\n\n    def __init__(self, algo: str, lr: float) -> None:\n        self.algo = algo\n        self.lr = lr\n\n    def __repr__(self) -> str:\n        return f"Optimizer(algo={self.algo},lr={self.lr})"\n\n\nclass Model:\n    def __init__(self, optim_partial: Any, lr: float):\n        super().__init__()\n        self.optim = optim_partial(lr=lr)\n        self.lr = lr\n\n    def __repr__(self) -> str:\n        return f"Model(Optimizer={self.optim},lr={self.lr})"\n')),(0,i.mdx)("div",{className:"row"},(0,i.mdx)("div",{className:"col col--5"},(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="Config"',title:'"Config"'},"model:\n  _target_: my_app.Model\n  optim_partial:\n    _partial_: true\n    _target_: my_app.Optimizer\n    algo: SGD\n  lr: 0.01\n"))),(0,i.mdx)("div",{className:"col col--7"},(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre",className:"language-python",metastring:'title="Instantiation"',title:'"Instantiation"'},'model = instantiate(cfg.model)\nprint(model)\n# "Model(Optimizer=Optimizer(algo=SGD,lr=0.01),lr=0.01)\n')))),(0,i.mdx)("p",null,"If you are repeatedly instantiating the same config,\nusing ",(0,i.mdx)("inlineCode",{parentName:"p"},"_partial_=True")," may provide a significant speedup as compared with regular (non-partial) instantiation."),(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre",className:"language-python"},"factory = instantiate(config, _partial_=True)\nobj = factory()\n")),(0,i.mdx)("p",null,"In the above example, repeatedly calling ",(0,i.mdx)("inlineCode",{parentName:"p"},"factory")," would be faster than repeatedly calling ",(0,i.mdx)("inlineCode",{parentName:"p"},"instantiate(config)"),".\nA caveat of this approach is that the same keyword arguments would be re-used in each call to ",(0,i.mdx)("inlineCode",{parentName:"p"},"factory"),"."),(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre",className:"language-python"},'class Foo:\n    ...\n\nclass Bar:\n    def __init__(self, foo):\n        self.foo = foo\n\nbar_conf = {\n    "_target_": "__main__.Bar",\n    "foo": {"_target_": "__main__.Foo"},\n}\n\nbar_factory = instantiate(bar_conf, _partial_=True)\nbar1 = bar_factory()\nbar2 = bar_factory()\n\nassert bar1 is not bar2\nassert bar1.foo is bar2.foo  # the `Foo` instance is re-used here\n')),(0,i.mdx)("p",null,"This does not apply if ",(0,i.mdx)("inlineCode",{parentName:"p"},"_partial_=False"),",\nin which case a new ",(0,i.mdx)("inlineCode",{parentName:"p"},"Foo")," instance would be created with each call to ",(0,i.mdx)("inlineCode",{parentName:"p"},"instantiate"),"."),(0,i.mdx)("h3",{id:"instantiation-of-builtins"},"Instantiation of builtins"),(0,i.mdx)("p",null,"The value of ",(0,i.mdx)("inlineCode",{parentName:"p"},"_target_")," passed to ",(0,i.mdx)("inlineCode",{parentName:"p"},"instantiate"),' should be a "dotpath" pointing\nto some callable that can be looked up via a combination of ',(0,i.mdx)("inlineCode",{parentName:"p"},"import")," and ",(0,i.mdx)("inlineCode",{parentName:"p"},"getattr"),".\nIf you want to target one of Python's ",(0,i.mdx)("a",{parentName:"p",href:"https://docs.python.org/3/library/functions.html"},"built-in functions")," (such as ",(0,i.mdx)("inlineCode",{parentName:"p"},"len")," or ",(0,i.mdx)("inlineCode",{parentName:"p"},"print")," or ",(0,i.mdx)("inlineCode",{parentName:"p"},"divmod"),"),\nyou will need to provide a dotpath looking up that function in Python's ",(0,i.mdx)("a",{parentName:"p",href:"https://docs.python.org/3/library/builtins.html"},(0,i.mdx)("inlineCode",{parentName:"a"},"builtins"))," module."),(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre",className:"language-python"},'from hydra.utils import instantiate\n# instantiate({"_target_": "len"}, [1,2,3])  # this gives an InstantiationException\ninstantiate({"_target_": "builtins.len"}, [1,2,3])  # this works, returns the number 3\n')),(0,i.mdx)("h3",{id:"dotpath-lookup-machinery"},"Dotpath lookup machinery"),(0,i.mdx)("p",null,"Hydra looks up a given ",(0,i.mdx)("inlineCode",{parentName:"p"},"_target_")," by attempting to find a module that\ncorresponds to a prefix of the given dotpath and then looking for an object in\nthat module corresponding to the dotpath's tail. For example, to look up a ",(0,i.mdx)("inlineCode",{parentName:"p"},"_target_"),"\ngiven by the dotpath ",(0,i.mdx)("inlineCode",{parentName:"p"},'"my_module.my_nested_module.my_object"'),", hydra first locates\nthe module ",(0,i.mdx)("inlineCode",{parentName:"p"},"my_module.my_nested_module"),", then find ",(0,i.mdx)("inlineCode",{parentName:"p"},"my_object")," inside that nested module."),(0,i.mdx)("p",null,"Hydra exposes an API allowing direct use of this dotpath lookup machinery.\nThe following three functions, which can be imported from the ",(0,i.mdx)(p,{to:"hydra/utils.py",mdxType:"GithubLink"},"hydra.utils")," module,\naccept a string-typed dotpath as an argument and return the located class/callable/object:"),(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre",className:"language-python"},'def get_class(path: str) -> type:\n    """\n    Look up a class based on a dotpath.\n    Fails if the path does not point to a class.\n\n    >>> import my_module\n    >>> from hydra.utils import get_class\n    >>> assert get_class("my_module.MyClass") is my_module.MyClass\n    """\n    ...\n\ndef get_method(path: str) -> Callable[..., Any]:\n    """\n    Look up a callable based on a dotpath.\n    Fails if the path does not point to a callable object.\n\n    >>> import my_module\n    >>> from hydra.utils import get_method\n    >>> assert get_method("my_module.my_function") is my_module.my_function\n    """\n    ...\n\n# Alias for get_method\nget_static_method = get_method\n\ndef get_object(path: str) -> Any:\n    """\n    Look up a callable based on a dotpath.\n\n    >>> import my_module\n    >>> from hydra.utils import get_object\n    >>> assert get_object("my_module.my_object") is my_module.my_object\n    """\n    ...\n')))}f.isMDXComponent=!0}}]);