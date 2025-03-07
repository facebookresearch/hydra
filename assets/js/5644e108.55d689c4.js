"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[5746],{15680:(e,t,n)=>{n.r(t),n.d(t,{MDXContext:()=>m,MDXProvider:()=>c,mdx:()=>g,useMDXComponents:()=>o,withMDXComponents:()=>s});var a=n(96540);function r(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function i(){return i=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var a in n)Object.prototype.hasOwnProperty.call(n,a)&&(e[a]=n[a])}return e},i.apply(this,arguments)}function l(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);t&&(a=a.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,a)}return n}function u(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?l(Object(n),!0).forEach((function(t){r(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):l(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function p(e,t){if(null==e)return{};var n,a,r=function(e,t){if(null==e)return{};var n,a,r={},i=Object.keys(e);for(a=0;a<i.length;a++)n=i[a],t.indexOf(n)>=0||(r[n]=e[n]);return r}(e,t);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);for(a=0;a<i.length;a++)n=i[a],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(r[n]=e[n])}return r}var m=a.createContext({}),s=function(e){return function(t){var n=o(t.components);return a.createElement(e,i({},t,{components:n}))}},o=function(e){var t=a.useContext(m),n=t;return e&&(n="function"==typeof e?e(t):u(u({},t),e)),n},c=function(e){var t=o(e.components);return a.createElement(m.Provider,{value:t},e.children)},d="mdxType",h={inlineCode:"code",wrapper:function(e){var t=e.children;return a.createElement(a.Fragment,{},t)}},y=a.forwardRef((function(e,t){var n=e.components,r=e.mdxType,i=e.originalType,l=e.parentName,m=p(e,["components","mdxType","originalType","parentName"]),s=o(n),c=r,d=s["".concat(l,".").concat(c)]||s[c]||h[c]||i;return n?a.createElement(d,u(u({ref:t},m),{},{components:n})):a.createElement(d,u({ref:t},m))}));function g(e,t){var n=arguments,r=t&&t.mdxType;if("string"==typeof e||r){var i=n.length,l=new Array(i);l[0]=y;var u={};for(var p in t)hasOwnProperty.call(t,p)&&(u[p]=t[p]);u.originalType=e,u[d]="string"==typeof e?e:r,l[1]=u;for(var m=2;m<i;m++)l[m]=n[m];return a.createElement.apply(null,l)}return a.createElement.apply(null,n)}y.displayName="MDXCreateElement"},41544:(e,t,n)=>{n.r(t),n.d(t,{assets:()=>m,contentTitle:()=>u,default:()=>d,frontMatter:()=>l,metadata:()=>p,toc:()=>s});var a=n(58168),r=(n(96540),n(15680)),i=n(49595);const l={id:"submitit_launcher",title:"Submitit Launcher plugin",sidebar_label:"Submitit Launcher plugin"},u=void 0,p={unversionedId:"plugins/submitit_launcher",id:"version-1.2/plugins/submitit_launcher",title:"Submitit Launcher plugin",description:"PyPI",source:"@site/versioned_docs/version-1.2/plugins/submitit_launcher.md",sourceDirName:"plugins",slug:"/plugins/submitit_launcher",permalink:"/docs/1.2/plugins/submitit_launcher",draft:!1,editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/versioned_docs/version-1.2/plugins/submitit_launcher.md",tags:[],version:"1.2",lastUpdatedBy:"P\xe1draig Brady",lastUpdatedAt:1652825677,formattedLastUpdatedAt:"May 17, 2022",frontMatter:{id:"submitit_launcher",title:"Submitit Launcher plugin",sidebar_label:"Submitit Launcher plugin"},sidebar:"docs",previous:{title:"RQ Launcher plugin",permalink:"/docs/1.2/plugins/rq_launcher"},next:{title:"Ax Sweeper plugin",permalink:"/docs/1.2/plugins/ax_sweeper"}},m={},s=[{value:"Installation",id:"installation",level:3},{value:"Usage",id:"usage",level:3},{value:"Example",id:"example",level:3}],o={toc:s},c="wrapper";function d(e){let{components:t,...n}=e;return(0,r.mdx)(c,(0,a.A)({},o,n,{components:t,mdxType:"MDXLayout"}),(0,r.mdx)("p",null,(0,r.mdx)("a",{parentName:"p",href:"https://pypi.org/project/hydra-submitit-launcher/"},(0,r.mdx)("img",{parentName:"a",src:"https://img.shields.io/pypi/v/hydra-submitit-launcher",alt:"PyPI"})),"\n",(0,r.mdx)("img",{parentName:"p",src:"https://img.shields.io/pypi/l/hydra-submitit-launcher",alt:"PyPI - License"}),"\n",(0,r.mdx)("img",{parentName:"p",src:"https://img.shields.io/pypi/pyversions/hydra-submitit-launcher",alt:"PyPI - Python Version"}),"\n",(0,r.mdx)("a",{parentName:"p",href:"https://pypistats.org/packages/hydra-submitit-launcher"},(0,r.mdx)("img",{parentName:"a",src:"https://img.shields.io/pypi/dm/hydra-submitit-launcher.svg",alt:"PyPI - Downloads"})),(0,r.mdx)(i.C,{text:"Example application",to:"plugins/hydra_submitit_launcher/examples",mdxType:"ExampleGithubLink"}),(0,r.mdx)(i.C,{text:"Plugin source",to:"plugins/hydra_submitit_launcher",mdxType:"ExampleGithubLink"})),(0,r.mdx)("p",null,"The Submitit Launcher plugin provides a ",(0,r.mdx)("a",{parentName:"p",href:"https://slurm.schedmd.com/documentation.html"},"SLURM")," Launcher based on ",(0,r.mdx)("a",{parentName:"p",href:"https://github.com/facebookincubator/submitit"},"Submitit"),"."),(0,r.mdx)("h3",{id:"installation"},"Installation"),(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-commandline"},"pip install hydra-submitit-launcher --upgrade\n")),(0,r.mdx)("h3",{id:"usage"},"Usage"),(0,r.mdx)("p",null,"Once installed, add ",(0,r.mdx)("inlineCode",{parentName:"p"},"hydra/launcher=submitit_slurm")," to your command line. Alternatively, override ",(0,r.mdx)("inlineCode",{parentName:"p"},"hydra/launcher")," in your config:"),(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-yaml"},"defaults:\n  - override hydra/launcher: submitit_slurm\n")),(0,r.mdx)("p",null,"There are several standard approaches for configuring plugins. Check ",(0,r.mdx)("a",{parentName:"p",href:"/docs/1.2/patterns/configuring_plugins"},"this page")," for more information.\nNote that this plugin expects a valid environment in the target host. Usually this means a shared file system between\nthe launching host and the target host."),(0,r.mdx)("p",null,"The Submitit Plugin implements 2 different launchers: ",(0,r.mdx)("inlineCode",{parentName:"p"},"submitit_slurm")," to run on a SLURM cluster, and ",(0,r.mdx)("inlineCode",{parentName:"p"},"submitit_local")," for basic local tests."),(0,r.mdx)("details",null,(0,r.mdx)("summary",null,"Discover the SLURM Launcher parameters ",(0,r.mdx)("b",null,"(Expand)")),(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="$ python your_app.py hydra/launcher=submitit_slurm --cfg hydra -p hydra.launcher"',title:'"$',python:!0,"your_app.py":!0,"hydra/launcher":"submitit_slurm","--cfg":!0,hydra:!0,"-p":!0,'hydra.launcher"':!0},"# @package hydra.launcher\nsubmitit_folder: ${hydra.sweep.dir}/.submitit/%j\ntimeout_min: 60\ncpus_per_task: null\ngpus_per_node: null\ntasks_per_node: 1\nmem_gb: null\nnodes: 1\nname: ${hydra.job.name}\n_target_: hydra_plugins.hydra_submitit_launcher.submitit_launcher.SlurmLauncher\npartition: null\nqos: null\ncomment: null\nconstraint: null\nexclude: null\ngres: null\ncpus_per_gpu: null\ngpus_per_task: null\nmem_per_gpu: null\nmem_per_cpu: null\naccount: null\nsignal_delay_s: 120\nmax_num_timeout: 0\nadditional_parameters: {}\narray_parallelism: 256\nsetup: null\n"))),(0,r.mdx)("details",null,(0,r.mdx)("summary",null,"Discover the Local Launcher parameters ",(0,r.mdx)("b",null,"(Expand)")),(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="$ python example/my_app.py hydra/launcher=submitit_local --cfg hydra -p hydra.launcher"',title:'"$',python:!0,"example/my_app.py":!0,"hydra/launcher":"submitit_local","--cfg":!0,hydra:!0,"-p":!0,'hydra.launcher"':!0},"# @package hydra.launcher\n_target_: hydra_plugins.hydra_submitit_launcher.submitit_launcher.LocalLauncher\nsubmitit_folder: ${hydra.sweep.dir}/.submitit/%j\ntimeout_min: 60\ncpus_per_task: 1\ngpus_per_node: 0\ntasks_per_node: 1\nmem_gb: 4\nnodes: 1\nname: ${hydra.job.name}\n"))),(0,r.mdx)("br",null),"You can set all these parameters in your configuration file and/or override them in the command-line:",(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-text"},"python foo.py --multirun hydra/launcher=submitit_slurm hydra.launcher.timeout_min=3\n")),(0,r.mdx)("p",null,"For more details, including descriptions for each parameter, check out the ",(0,r.mdx)(i.A,{to:"plugins/hydra_submitit_launcher/hydra_plugins/hydra_submitit_launcher/config.py",mdxType:"GithubLink"},"config file"),".\nYou can also check the ",(0,r.mdx)("a",{parentName:"p",href:"https://github.com/facebookincubator/submitit"},"Submitit documentation"),"."),(0,r.mdx)("p",null,(0,r.mdx)("strong",{parentName:"p"},"Caution"),": use of ",(0,r.mdx)("inlineCode",{parentName:"p"},"--multirun")," is required for the launcher to be picked up."),(0,r.mdx)("h3",{id:"example"},"Example"),(0,r.mdx)("p",null,"An ",(0,r.mdx)(i.A,{to:"plugins/hydra_submitit_launcher/example",mdxType:"GithubLink"},"example application")," using this launcher is provided in the plugin repository."),(0,r.mdx)("p",null,"Starting the app with ",(0,r.mdx)("inlineCode",{parentName:"p"},"python my_app.py task=1,2,3 --multirun")," (see ",(0,r.mdx)("a",{parentName:"p",href:"/docs/1.2/tutorials/basic/running_your_app/multi-run"},"Multi-run")," for details) will launch 3 executions (you can override the launcher to run locally for testing by adding ",(0,r.mdx)("inlineCode",{parentName:"p"},"hydra/launcher=submitit_local"),"):"),(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-text"},"$ python my_app.py task=1,2,3 --multirun\n[HYDRA] Sweep output dir : multirun/2020-05-28/15-05-22\n[HYDRA]        #0 : task=1\n[HYDRA]        #1 : task=2\n[HYDRA]        #2 : task=3\n")),(0,r.mdx)("p",null,"You will be able to see the output of the app in the output dir:"),(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-commandline"},"$ tree\n.\n\u251c\u2500\u2500 0\n\u2502\xa0\xa0 \u2514\u2500\u2500 my_app.log\n\u251c\u2500\u2500 1\n\u2502\xa0\xa0 \u2514\u2500\u2500 my_app.log\n\u251c\u2500\u2500 2\n\u2502\xa0\xa0 \u2514\u2500\u2500 my_app.log\n\u2514\u2500\u2500 multirun.yaml\n\n$ cat 0/my_app.log \n[2020-05-28 15:05:23,511][__main__][INFO] - Process ID 15887 executing task 1 ...\n[2020-05-28 15:05:24,514][submitit][INFO] - Job completed successfully\n")))}d.isMDXComponent=!0},49595:(e,t,n)=>{n.d(t,{A:()=>m,C:()=>s});var a=n(58168),r=n(96540),i=n(75489),l=n(44586),u=n(48295);function p(e){const t=(0,u.ir)();return(0,l.default)().siteConfig.customFields.githubLinkVersionToBaseUrl[t?.name??"current"]+e}function m(e){return r.createElement(i.default,(0,a.A)({},e,{to:p(e.to),target:"_blank"}))}function s(e){const t=e.text??"Example (Click Here)";return r.createElement(m,e,r.createElement("span",null,"\xa0"),r.createElement("img",{src:"https://img.shields.io/badge/-"+t+"-informational",alt:"Example (Click Here)"}))}}}]);