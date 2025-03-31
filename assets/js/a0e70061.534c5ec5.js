"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[8535],{15680:(e,n,r)=>{r.r(n),r.d(n,{MDXContext:()=>m,MDXProvider:()=>c,mdx:()=>y,useMDXComponents:()=>u,withMDXComponents:()=>s});var a=r(96540);function t(e,n,r){return n in e?Object.defineProperty(e,n,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[n]=r,e}function o(){return o=Object.assign||function(e){for(var n=1;n<arguments.length;n++){var r=arguments[n];for(var a in r)Object.prototype.hasOwnProperty.call(r,a)&&(e[a]=r[a])}return e},o.apply(this,arguments)}function i(e,n){var r=Object.keys(e);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);n&&(a=a.filter((function(n){return Object.getOwnPropertyDescriptor(e,n).enumerable}))),r.push.apply(r,a)}return r}function d(e){for(var n=1;n<arguments.length;n++){var r=null!=arguments[n]?arguments[n]:{};n%2?i(Object(r),!0).forEach((function(n){t(e,n,r[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(r)):i(Object(r)).forEach((function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(r,n))}))}return e}function l(e,n){if(null==e)return{};var r,a,t=function(e,n){if(null==e)return{};var r,a,t={},o=Object.keys(e);for(a=0;a<o.length;a++)r=o[a],n.indexOf(r)>=0||(t[r]=e[r]);return t}(e,n);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(e);for(a=0;a<o.length;a++)r=o[a],n.indexOf(r)>=0||Object.prototype.propertyIsEnumerable.call(e,r)&&(t[r]=e[r])}return t}var m=a.createContext({}),s=function(e){return function(n){var r=u(n.components);return a.createElement(e,o({},n,{components:r}))}},u=function(e){var n=a.useContext(m),r=n;return e&&(r="function"==typeof e?e(n):d(d({},n),e)),r},c=function(e){var n=u(e.components);return a.createElement(m.Provider,{value:n},e.children)},p="mdxType",h={inlineCode:"code",wrapper:function(e){var n=e.children;return a.createElement(a.Fragment,{},n)}},b=a.forwardRef((function(e,n){var r=e.components,t=e.mdxType,o=e.originalType,i=e.parentName,m=l(e,["components","mdxType","originalType","parentName"]),s=u(r),c=t,p=s["".concat(i,".").concat(c)]||s[c]||h[c]||o;return r?a.createElement(p,d(d({ref:n},m),{},{components:r})):a.createElement(p,d({ref:n},m))}));function y(e,n){var r=arguments,t=n&&n.mdxType;if("string"==typeof e||t){var o=r.length,i=new Array(o);i[0]=b;var d={};for(var l in n)hasOwnProperty.call(n,l)&&(d[l]=n[l]);d.originalType=e,d[p]="string"==typeof e?e:t,i[1]=d;for(var m=2;m<o;m++)i[m]=r[m];return a.createElement.apply(null,i)}return a.createElement.apply(null,r)}b.displayName="MDXCreateElement"},65492:(e,n,r)=>{r.r(n),r.d(n,{assets:()=>l,contentTitle:()=>i,default:()=>c,frontMatter:()=>o,metadata:()=>d,toc:()=>m});var a=r(58168),t=(r(96540),r(15680));const o={id:"job",sidebar_label:"Job Configuration",hide_title:!0},i=void 0,d={unversionedId:"configure_hydra/job",id:"version-1.0/configure_hydra/job",title:"job",description:"Job configuration",source:"@site/versioned_docs/version-1.0/configure_hydra/job.md",sourceDirName:"configure_hydra",slug:"/configure_hydra/job",permalink:"/docs/1.0/configure_hydra/job",draft:!1,editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/versioned_docs/version-1.0/configure_hydra/job.md",tags:[],version:"1.0",lastUpdatedBy:"jesszzzz",lastUpdatedAt:1743461536,formattedLastUpdatedAt:"Mar 31, 2025",frontMatter:{id:"job",sidebar_label:"Job Configuration",hide_title:!0},sidebar:"docs",previous:{title:"Introduction",permalink:"/docs/1.0/configure_hydra/intro"},next:{title:"Customizing logging",permalink:"/docs/1.0/configure_hydra/logging"}},l={},m=[{value:"Job configuration",id:"job-configuration",level:2},{value:"Documentation",id:"documentation",level:2},{value:"hydra.job.name",id:"hydrajobname",level:3},{value:"hydra.job.override_dirname",id:"hydrajoboverride_dirname",level:3},{value:"hydra.job.id",id:"hydrajobid",level:3},{value:"hydra.job.num",id:"hydrajobnum",level:3},{value:"hydra.job.config_name",id:"hydrajobconfig_name",level:3},{value:"hydra.job.env_set",id:"hydrajobenv_set",level:3},{value:"hydra.job.env_copy",id:"hydrajobenv_copy",level:3}],s={toc:m},u="wrapper";function c(e){let{components:n,...r}=e;return(0,t.mdx)(u,(0,a.A)({},s,r,{components:n,mdxType:"MDXLayout"}),(0,t.mdx)("h2",{id:"job-configuration"},"Job configuration"),(0,t.mdx)("p",null,"The job configuration resides in ",(0,t.mdx)("inlineCode",{parentName:"p"},"hydra.job"),".\nThe structure definition is below, the latest definition ",(0,t.mdx)("a",{parentName:"p",href:"https://github.com/facebookresearch/hydra/blob/master/hydra/conf/__init__.py"},"in the code"),"."),(0,t.mdx)("details",null,(0,t.mdx)("summary",null,"Expand definition"),(0,t.mdx)("pre",null,(0,t.mdx)("code",{parentName:"pre",className:"language-python"},'# job runtime information will be populated here\n@dataclass\nclass JobConf:\n    # Job name, populated automatically unless specified by the user (in config or cli)\n    name: str = MISSING\n\n    # Concatenation of job overrides that can be used as a part\n    # of the directory name.\n    # This can be configured in hydra.job.config.override_dirname\n    override_dirname: str = MISSING\n\n    # Job ID in underlying scheduling system\n    id: str = MISSING\n\n    # Job number if job is a part of a sweep\n    num: int = MISSING\n\n    # The config name used by the job\n    config_name: Optional[str] = MISSING\n\n    # Environment variables to set remotely\n    env_set: Dict[str, str] = field(default_factory=dict)\n    # Environment variables to copy from the launching machine\n    env_copy: List[str] = field(default_factory=list)\n\n    # Job config\n    @dataclass\n    class JobConfig:\n        @dataclass\n        # configuration for the ${hydra.job.override_dirname} runtime variable\n        class OverrideDirname:\n            kv_sep: str = "="\n            item_sep: str = ","\n            exclude_keys: List[str] = field(default_factory=list)\n\n        override_dirname: OverrideDirname = field(default_factory=OverrideDirname)\n\n    config: JobConfig = field(default_factory=JobConfig)\n'))),(0,t.mdx)("h2",{id:"documentation"},"Documentation"),(0,t.mdx)("h3",{id:"hydrajobname"},"hydra.job.name"),(0,t.mdx)("p",null,(0,t.mdx)("a",{parentName:"p",href:"https://github.com/facebookresearch/hydra/tree/1.0_branch/examples/configure_hydra/job_name"},(0,t.mdx)("img",{parentName:"a",src:"https://img.shields.io/badge/-Example%20application-informational",alt:"Example application"}))),(0,t.mdx)("p",null,"The job name is used by different things in Hydra, such as the log file name (",(0,t.mdx)("inlineCode",{parentName:"p"},"${hydra.job.name}.log"),").\nIt is normally derived from the Python file name (file: ",(0,t.mdx)("inlineCode",{parentName:"p"},"train.py")," -> name: ",(0,t.mdx)("inlineCode",{parentName:"p"},"train"),").\nYou can override it via the command line or your config file. "),(0,t.mdx)("h3",{id:"hydrajoboverride_dirname"},"hydra.job.override_dirname"),(0,t.mdx)("p",null,"This field is populated automatically using your command line arguments and is typically being used as a part of your\noutput directory pattern.\nFor example, the command line arguments:"),(0,t.mdx)("pre",null,(0,t.mdx)("code",{parentName:"pre",className:"language-bash"},"$ python foo.py a=10 b=20\n")),(0,t.mdx)("p",null,"Would result in ",(0,t.mdx)("inlineCode",{parentName:"p"},"hydra.job.override_dirname")," getting the value a=10,b=20.\nWhen used with the output directory override, it can automatically generate directories that represent the\ncommand line arguments used in your run.   "),(0,t.mdx)("pre",null,(0,t.mdx)("code",{parentName:"pre",className:"language-yaml"},"hydra:\n  run:\n    dir: output/${hydra.job.override_dirname}\n")),(0,t.mdx)("p",null,"The generation of override_dirname can be controlled by ",(0,t.mdx)("inlineCode",{parentName:"p"},"hydra.job.config.override_dirname"),".\nIn particular, the separator char ",(0,t.mdx)("inlineCode",{parentName:"p"},"=")," and the item separator char ",(0,t.mdx)("inlineCode",{parentName:"p"},",")," can be modified, and in addition some command line\noverride keys can be automatically excluded from the generated ",(0,t.mdx)("inlineCode",{parentName:"p"},"override_dirname"),".\nAn example of a case where the exclude is useful is a random seed."),(0,t.mdx)("pre",null,(0,t.mdx)("code",{parentName:"pre",className:"language-yaml"},"hydra:\n  run:\n    dir: output/${hydra.job.override_dirname}/seed=${seed}\n  job:\n    config:\n      override_dirname:\n        exclude_keys:\n          - seed\n")),(0,t.mdx)("p",null,"With this configuration, running"),(0,t.mdx)("pre",null,(0,t.mdx)("code",{parentName:"pre",className:"language-bash"},"$ python foo.py a=10 b=20 seed=999\n")),(0,t.mdx)("p",null,"Would result in a directory like:"),(0,t.mdx)("pre",null,(0,t.mdx)("code",{parentName:"pre"},"output/a=10,b=20/seed=999\n")),(0,t.mdx)("p",null,"Allowing you to more easily group identical runs with different random seeds together."),(0,t.mdx)("h3",{id:"hydrajobid"},"hydra.job.id"),(0,t.mdx)("p",null,"The job ID is populated by active Hydra launcher. For the basic launcher, the job ID is just a serial job number, but\nfor other systems this could be the SLURM job ID or the AWS Instance ID."),(0,t.mdx)("h3",{id:"hydrajobnum"},"hydra.job.num"),(0,t.mdx)("p",null,"Serial job number within this current sweep run. (0 to n-1)"),(0,t.mdx)("h3",{id:"hydrajobconfig_name"},"hydra.job.config_name"),(0,t.mdx)("p",null,"The config name used by the job, this is populated automatically to match the config name in @hydra.main()"),(0,t.mdx)("h3",{id:"hydrajobenv_set"},"hydra.job.env_set"),(0,t.mdx)("p",null,"A Dict","[str, str]"," that is used to set the environment variables of the running job.\nSome common use cases are to set environment variables that are effecting underlying libraries, for example"),(0,t.mdx)("pre",null,(0,t.mdx)("code",{parentName:"pre",className:"language-yaml"},"hydra:\n  job:\n    env_set:\n      OMP_NUM_THREADS: 1\n")),(0,t.mdx)("p",null,"Disables multithreading in Intel IPP and MKL."),(0,t.mdx)("p",null,"Another example, is to use interpolation to automatically set the rank\nfor ",(0,t.mdx)("a",{parentName:"p",href:"https://pytorch.org/tutorials/intermediate/dist_tuto.html"},"Torch Distributed")," run to match the job number\nin the sweep. "),(0,t.mdx)("pre",null,(0,t.mdx)("code",{parentName:"pre",className:"language-yaml"},"hydra:\n  job:\n    env_set:\n      RANK: ${hydra:job.num}\n")),(0,t.mdx)("h3",{id:"hydrajobenv_copy"},"hydra.job.env_copy"),(0,t.mdx)("p",null,"In some cases you want to automatically copy local environment variables to the running job environment variables.\nThis is particularly useful for remote runs."),(0,t.mdx)("pre",null,(0,t.mdx)("code",{parentName:"pre",className:"language-yaml"},"hydra:\n  job:\n    env_copy:\n      - AWS_KEY\n")))}c.isMDXComponent=!0}}]);