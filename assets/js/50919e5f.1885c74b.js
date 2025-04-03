"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[9009],{15680:(e,n,r)=>{r.r(n),r.d(n,{MDXContext:()=>s,MDXProvider:()=>u,mdx:()=>y,useMDXComponents:()=>m,withMDXComponents:()=>c});var t=r(96540);function o(e,n,r){return n in e?Object.defineProperty(e,n,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[n]=r,e}function a(){return a=Object.assign||function(e){for(var n=1;n<arguments.length;n++){var r=arguments[n];for(var t in r)Object.prototype.hasOwnProperty.call(r,t)&&(e[t]=r[t])}return e},a.apply(this,arguments)}function i(e,n){var r=Object.keys(e);if(Object.getOwnPropertySymbols){var t=Object.getOwnPropertySymbols(e);n&&(t=t.filter((function(n){return Object.getOwnPropertyDescriptor(e,n).enumerable}))),r.push.apply(r,t)}return r}function d(e){for(var n=1;n<arguments.length;n++){var r=null!=arguments[n]?arguments[n]:{};n%2?i(Object(r),!0).forEach((function(n){o(e,n,r[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(r)):i(Object(r)).forEach((function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(r,n))}))}return e}function l(e,n){if(null==e)return{};var r,t,o=function(e,n){if(null==e)return{};var r,t,o={},a=Object.keys(e);for(t=0;t<a.length;t++)r=a[t],n.indexOf(r)>=0||(o[r]=e[r]);return o}(e,n);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);for(t=0;t<a.length;t++)r=a[t],n.indexOf(r)>=0||Object.prototype.propertyIsEnumerable.call(e,r)&&(o[r]=e[r])}return o}var s=t.createContext({}),c=function(e){return function(n){var r=m(n.components);return t.createElement(e,a({},n,{components:r}))}},m=function(e){var n=t.useContext(s),r=n;return e&&(r="function"==typeof e?e(n):d(d({},n),e)),r},u=function(e){var n=m(e.components);return t.createElement(s.Provider,{value:n},e.children)},h="mdxType",p={inlineCode:"code",wrapper:function(e){var n=e.children;return t.createElement(t.Fragment,{},n)}},b=t.forwardRef((function(e,n){var r=e.components,o=e.mdxType,a=e.originalType,i=e.parentName,s=l(e,["components","mdxType","originalType","parentName"]),c=m(r),u=o,h=c["".concat(i,".").concat(u)]||c[u]||p[u]||a;return r?t.createElement(h,d(d({ref:n},s),{},{components:r})):t.createElement(h,d({ref:n},s))}));function y(e,n){var r=arguments,o=n&&n.mdxType;if("string"==typeof e||o){var a=r.length,i=new Array(a);i[0]=b;var d={};for(var l in n)hasOwnProperty.call(n,l)&&(d[l]=n[l]);d.originalType=e,d[h]="string"==typeof e?e:o,i[1]=d;for(var s=2;s<a;s++)i[s]=r[s];return t.createElement.apply(null,i)}return t.createElement.apply(null,r)}b.displayName="MDXCreateElement"},49595:(e,n,r)=>{r.d(n,{A:()=>s,C:()=>c});var t=r(58168),o=r(96540),a=r(75489),i=r(44586),d=r(48295);function l(e){const n=(0,d.ir)();return(0,i.default)().siteConfig.customFields.githubLinkVersionToBaseUrl[n?.name??"current"]+e}function s(e){return o.createElement(a.default,(0,t.A)({},e,{to:l(e.to),target:"_blank"}))}function c(e){const n=e.text??"Example (Click Here)";return o.createElement(s,e,o.createElement("span",null,"\xa0"),o.createElement("img",{src:"https://img.shields.io/badge/-"+n+"-informational",alt:"Example (Click Here)"}))}},99686:(e,n,r)=>{r.r(n),r.d(n,{assets:()=>s,contentTitle:()=>d,default:()=>h,frontMatter:()=>i,metadata:()=>l,toc:()=>c});var t=r(58168),o=(r(96540),r(15680)),a=r(49595);const i={id:"job",title:"Job Configuration"},d=void 0,l={unversionedId:"configure_hydra/job",id:"version-1.2/configure_hydra/job",title:"Job Configuration",description:"The job configuration resides in hydra.job.",source:"@site/versioned_docs/version-1.2/configure_hydra/job.md",sourceDirName:"configure_hydra",slug:"/configure_hydra/job",permalink:"/docs/1.2/configure_hydra/job",draft:!1,editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/versioned_docs/version-1.2/configure_hydra/job.md",tags:[],version:"1.2",lastUpdatedBy:"dependabot[bot]",lastUpdatedAt:1743717584,formattedLastUpdatedAt:"Apr 3, 2025",frontMatter:{id:"job",title:"Job Configuration"},sidebar:"docs",previous:{title:"Introduction",permalink:"/docs/1.2/configure_hydra/intro"},next:{title:"Customizing logging",permalink:"/docs/1.2/configure_hydra/logging"}},s={},c=[{value:"hydra.job.name",id:"hydrajobname",level:3},{value:"hydra.job.chdir",id:"hydrajobchdir",level:3},{value:"hydra.job.override_dirname",id:"hydrajoboverride_dirname",level:3},{value:"hydra.job.id",id:"hydrajobid",level:3},{value:"hydra.job.num",id:"hydrajobnum",level:3},{value:"hydra.job.config_name",id:"hydrajobconfig_name",level:3},{value:"hydra.job.env_set",id:"hydrajobenv_set",level:3},{value:"hydra.job.env_copy",id:"hydrajobenv_copy",level:3}],m={toc:c},u="wrapper";function h(e){let{components:n,...r}=e;return(0,o.mdx)(u,(0,t.A)({},m,r,{components:n,mdxType:"MDXLayout"}),(0,o.mdx)("p",null,"The job configuration resides in ",(0,o.mdx)("inlineCode",{parentName:"p"},"hydra.job"),".\nThe Structured Config is below, the latest definition is ",(0,o.mdx)(a.A,{to:"hydra/conf/__init__.py",mdxType:"GithubLink"},"here"),"."),(0,o.mdx)("details",null,(0,o.mdx)("summary",null,"Expand definition"),(0,o.mdx)("pre",null,(0,o.mdx)("code",{parentName:"pre",className:"language-python"},'# job runtime information will be populated here\n@dataclass\nclass JobConf:\n    # Job name, populated automatically unless specified by the user (in config or cli)\n    name: str = MISSING\n\n    # Change current working dir to the output dir.\n    chdir: bool = True\n\n    # Concatenation of job overrides that can be used as a part\n    # of the directory name.\n    # This can be configured in hydra.job.config.override_dirname\n    override_dirname: str = MISSING\n\n    # Job ID in underlying scheduling system\n    id: str = MISSING\n\n    # Job number if job is a part of a sweep\n    num: int = MISSING\n\n    # The config name used by the job\n    config_name: Optional[str] = MISSING\n\n    # Environment variables to set remotely\n    env_set: Dict[str, str] = field(default_factory=dict)\n    # Environment variables to copy from the launching machine\n    env_copy: List[str] = field(default_factory=list)\n\n    # Job config\n    @dataclass\n    class JobConfig:\n        @dataclass\n        # configuration for the ${hydra.job.override_dirname} runtime variable\n        class OverrideDirname:\n            kv_sep: str = "="\n            item_sep: str = ","\n            exclude_keys: List[str] = field(default_factory=list)\n\n        override_dirname: OverrideDirname = field(default_factory=OverrideDirname)\n\n    config: JobConfig = field(default_factory=JobConfig)\n'))),(0,o.mdx)("h3",{id:"hydrajobname"},"hydra.job.name"),(0,o.mdx)(a.C,{text:"Example application",to:"examples/configure_hydra/job_name",mdxType:"ExampleGithubLink"}),(0,o.mdx)("p",null,"The job name is used by different things in Hydra, such as the log file name (",(0,o.mdx)("inlineCode",{parentName:"p"},"${hydra.job.name}.log"),").\nIt is normally derived from the Python file name (The job name of the file ",(0,o.mdx)("inlineCode",{parentName:"p"},"train.py")," is ",(0,o.mdx)("inlineCode",{parentName:"p"},"train"),").\nYou can override it via the command line, or your config file. "),(0,o.mdx)("h3",{id:"hydrajobchdir"},"hydra.job.chdir"),(0,o.mdx)("p",null,"Decides whether Hydra changes the current working directory to the output directory for each job.\nLearn more at the ",(0,o.mdx)("a",{parentName:"p",href:"/docs/1.2/tutorials/basic/running_your_app/working_directory#disable-changing-current-working-dir-to-jobs-output-dir"},"Output/Working directory")," page."),(0,o.mdx)("h3",{id:"hydrajoboverride_dirname"},"hydra.job.override_dirname"),(0,o.mdx)("p",null,"Enables the creation of an output directory which is based on command line overrides.\nLearn more at the ",(0,o.mdx)("a",{parentName:"p",href:"/docs/1.2/configure_hydra/workdir"},"Customizing Working Directory")," page."),(0,o.mdx)("h3",{id:"hydrajobid"},"hydra.job.id"),(0,o.mdx)("p",null,"The job ID is populated by the active Hydra launcher. For the basic launcher, the job ID is just a serial job number.\nOther launchers will set it to an ID that makes sense like SLURM job ID. "),(0,o.mdx)("h3",{id:"hydrajobnum"},"hydra.job.num"),(0,o.mdx)("p",null,"Serial job number within this current sweep run. (0 to n-1)."),(0,o.mdx)("h3",{id:"hydrajobconfig_name"},"hydra.job.config_name"),(0,o.mdx)("p",null,"The config name used by the job, this is populated automatically to match the config name in ",(0,o.mdx)("inlineCode",{parentName:"p"},"@hydra.main()"),"."),(0,o.mdx)("h3",{id:"hydrajobenv_set"},"hydra.job.env_set"),(0,o.mdx)("p",null,"A ",(0,o.mdx)("inlineCode",{parentName:"p"},"Dict[str, str]")," that is used to set the environment variables of the running job.\nSome common use cases are to automatically set environment variables that are affecting underlying libraries.\nFor example, the following will disables multithreading in Intel IPP and MKL:"),(0,o.mdx)("pre",null,(0,o.mdx)("code",{parentName:"pre",className:"language-yaml"},"hydra:\n  job:\n    env_set:\n      OMP_NUM_THREADS: 1\n")),(0,o.mdx)("p",null,"Another example, is to use interpolation to automatically set the rank\nfor ",(0,o.mdx)("a",{parentName:"p",href:"https://pytorch.org/tutorials/intermediate/dist_tuto.html"},"Torch Distributed")," run to match the job number\nin the sweep. "),(0,o.mdx)("pre",null,(0,o.mdx)("code",{parentName:"pre",className:"language-yaml"},"hydra:\n  job:\n    env_set:\n      RANK: ${hydra:job.num}\n")),(0,o.mdx)("h3",{id:"hydrajobenv_copy"},"hydra.job.env_copy"),(0,o.mdx)("p",null,"In some cases you want to automatically copy local environment variables to the running job environment variables.\nThis is particularly useful for remote runs."),(0,o.mdx)("pre",null,(0,o.mdx)("code",{parentName:"pre",className:"language-yaml"},"hydra:\n  job:\n    env_copy:\n      - AWS_KEY\n")))}h.isMDXComponent=!0}}]);