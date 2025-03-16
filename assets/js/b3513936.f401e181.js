"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[7715],{15680:(e,r,n)=>{n.r(r),n.d(r,{MDXContext:()=>m,MDXProvider:()=>p,mdx:()=>f,useMDXComponents:()=>c,withMDXComponents:()=>u});var t=n(96540);function a(e,r,n){return r in e?Object.defineProperty(e,r,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[r]=n,e}function i(){return i=Object.assign||function(e){for(var r=1;r<arguments.length;r++){var n=arguments[r];for(var t in n)Object.prototype.hasOwnProperty.call(n,t)&&(e[t]=n[t])}return e},i.apply(this,arguments)}function o(e,r){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var t=Object.getOwnPropertySymbols(e);r&&(t=t.filter((function(r){return Object.getOwnPropertyDescriptor(e,r).enumerable}))),n.push.apply(n,t)}return n}function d(e){for(var r=1;r<arguments.length;r++){var n=null!=arguments[r]?arguments[r]:{};r%2?o(Object(n),!0).forEach((function(r){a(e,r,n[r])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):o(Object(n)).forEach((function(r){Object.defineProperty(e,r,Object.getOwnPropertyDescriptor(n,r))}))}return e}function l(e,r){if(null==e)return{};var n,t,a=function(e,r){if(null==e)return{};var n,t,a={},i=Object.keys(e);for(t=0;t<i.length;t++)n=i[t],r.indexOf(n)>=0||(a[n]=e[n]);return a}(e,r);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);for(t=0;t<i.length;t++)n=i[t],r.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(a[n]=e[n])}return a}var m=t.createContext({}),u=function(e){return function(r){var n=c(r.components);return t.createElement(e,i({},r,{components:n}))}},c=function(e){var r=t.useContext(m),n=r;return e&&(n="function"==typeof e?e(r):d(d({},r),e)),n},p=function(e){var r=c(e.components);return t.createElement(m.Provider,{value:r},e.children)},s="mdxType",g={inlineCode:"code",wrapper:function(e){var r=e.children;return t.createElement(t.Fragment,{},r)}},y=t.forwardRef((function(e,r){var n=e.components,a=e.mdxType,i=e.originalType,o=e.parentName,m=l(e,["components","mdxType","originalType","parentName"]),u=c(n),p=a,s=u["".concat(o,".").concat(p)]||u[p]||g[p]||i;return n?t.createElement(s,d(d({ref:r},m),{},{components:n})):t.createElement(s,d({ref:r},m))}));function f(e,r){var n=arguments,a=r&&r.mdxType;if("string"==typeof e||a){var i=n.length,o=new Array(i);o[0]=y;var d={};for(var l in r)hasOwnProperty.call(r,l)&&(d[l]=r[l]);d.originalType=e,d[s]="string"==typeof e?e:a,o[1]=d;for(var m=2;m<i;m++)o[m]=n[m];return t.createElement.apply(null,o)}return t.createElement.apply(null,n)}y.displayName="MDXCreateElement"},31465:(e,r,n)=>{n.r(r),n.d(r,{assets:()=>m,contentTitle:()=>d,default:()=>s,frontMatter:()=>o,metadata:()=>l,toc:()=>u});var t=n(58168),a=(n(96540),n(15680)),i=n(49595);const o={id:"workdir",title:"Customizing working directory pattern",sidebar_label:"Customizing working directory pattern"},d=void 0,l={unversionedId:"configure_hydra/workdir",id:"version-1.2/configure_hydra/workdir",title:"Customizing working directory pattern",description:"Hydra automatically creates an output directory used to store log files and",source:"@site/versioned_docs/version-1.2/configure_hydra/workdir.md",sourceDirName:"configure_hydra",slug:"/configure_hydra/workdir",permalink:"/docs/1.2/configure_hydra/workdir",draft:!1,editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/versioned_docs/version-1.2/configure_hydra/workdir.md",tags:[],version:"1.2",lastUpdatedBy:"dependabot[bot]",lastUpdatedAt:1742161400,formattedLastUpdatedAt:"Mar 16, 2025",frontMatter:{id:"workdir",title:"Customizing working directory pattern",sidebar_label:"Customizing working directory pattern"},sidebar:"docs",previous:{title:"Customizing logging",permalink:"/docs/1.2/configure_hydra/logging"},next:{title:"Customizing Application's help",permalink:"/docs/1.2/configure_hydra/app_help"}},m={},u=[{value:"Configuration for run",id:"configuration-for-run",level:3},{value:"Configuration for multirun",id:"configuration-for-multirun",level:3},{value:"Using <code>hydra.job.override_dirname</code>",id:"using-hydrajoboverride_dirname",level:3}],c={toc:u},p="wrapper";function s(e){let{components:r,...n}=e;return(0,a.mdx)(p,(0,t.A)({},c,n,{components:r,mdxType:"MDXLayout"}),(0,a.mdx)(i.C,{text:"Example application",to:"examples/configure_hydra/workdir",mdxType:"ExampleGithubLink"}),(0,a.mdx)("p",null,"Hydra automatically creates an output directory used to store log files and\nsave yaml configs. This directory can be configured by setting ",(0,a.mdx)("inlineCode",{parentName:"p"},"hydra.run.dir"),"\n(for single hydra runs) or ",(0,a.mdx)("inlineCode",{parentName:"p"},"hydra.sweep.dir"),"/",(0,a.mdx)("inlineCode",{parentName:"p"},"hydra.sweep.subdir")," (for multirun\nsweeps). At runtime, the path of the output directory can be\n",(0,a.mdx)("a",{parentName:"p",href:"/docs/1.2/configure_hydra/intro#accessing-the-hydra-config"},"accessed")," via the ",(0,a.mdx)("inlineCode",{parentName:"p"},"hydra.runtime.output_dir")," variable.\nBelow are a few examples of customizing output directory patterns."),(0,a.mdx)("h3",{id:"configuration-for-run"},"Configuration for run"),(0,a.mdx)("p",null,"Run output directory grouped by date:"),(0,a.mdx)("pre",null,(0,a.mdx)("code",{parentName:"pre",className:"language-yaml"},"hydra:\n  run:\n    dir: ./outputs/${now:%Y-%m-%d}/${now:%H-%M-%S}\n")),(0,a.mdx)("p",null,"Run output directory grouped by job name:"),(0,a.mdx)("pre",null,(0,a.mdx)("code",{parentName:"pre",className:"language-yaml"},"hydra:\n  run:\n    dir: outputs/${hydra.job.name}/${now:%Y-%m-%d_%H-%M-%S}\n")),(0,a.mdx)("p",null,"Run output directory can contain user configuration variables:"),(0,a.mdx)("pre",null,(0,a.mdx)("code",{parentName:"pre",className:"language-yaml"},"hydra:\n  run:\n    dir: outputs/${now:%Y-%m-%d_%H-%M-%S}/opt:${optimizer.type}\n")),(0,a.mdx)("h3",{id:"configuration-for-multirun"},"Configuration for multirun"),(0,a.mdx)("p",null,"We will run the application with same command but different configurations:"),(0,a.mdx)("pre",null,(0,a.mdx)("code",{parentName:"pre",className:"language-bash"},"python my_app.py --multirun a=a1,a2,a3 \n")),(0,a.mdx)("p",null,"Default multirun dir configurations:"),(0,a.mdx)("div",{className:"row"},(0,a.mdx)("div",{className:"col col--8"},(0,a.mdx)("pre",null,(0,a.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="config.yaml"',title:'"config.yaml"'},"hydra:\n  sweep:\n    dir: multirun/${now:%Y-%m-%d}/${now:%H-%M-%S}\n    subdir: ${hydra.job.num}\n\n"))),(0,a.mdx)("div",{className:"col  col--4"},(0,a.mdx)("pre",null,(0,a.mdx)("code",{parentName:"pre",className:"language-bash",metastring:'title="workding dir created"',title:'"workding',dir:!0,'created"':!0},"$ tree my_app -d\nmy_app\n\u251c\u2500\u2500 0\n\u251c\u2500\u2500 1\n\u2514\u2500\u2500 2\n")))),(0,a.mdx)("p",null,"Similar configuration patterns in run can be applied to config multirun dir as well."),(0,a.mdx)("p",null,"For example, multirun output directory grouped by job name, and sub dir by job num:"),(0,a.mdx)("div",{className:"row"},(0,a.mdx)("div",{className:"col col--6"},(0,a.mdx)("pre",null,(0,a.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="config.yaml"',title:'"config.yaml"'},"hydra:\n  sweep:\n    dir: ${hydra.job.name}\n    subdir: ${hydra.job.num}\n\n"))),(0,a.mdx)("div",{className:"col  col--6"},(0,a.mdx)("pre",null,(0,a.mdx)("code",{parentName:"pre",className:"language-bash",metastring:'title="workding dir created"',title:'"workding',dir:!0,'created"':!0},"$ tree my_app -d\nmy_app\n\u251c\u2500\u2500 0\n\u251c\u2500\u2500 1\n\u2514\u2500\u2500 2\n")))),(0,a.mdx)("h3",{id:"using-hydrajoboverride_dirname"},"Using ",(0,a.mdx)("inlineCode",{parentName:"h3"},"hydra.job.override_dirname")),(0,a.mdx)(i.C,{text:"Example application",to:"examples/configure_hydra/job_override_dirname",mdxType:"ExampleGithubLink"}),(0,a.mdx)("p",null,"This field is populated automatically using your command line arguments and is typically being used as a part of your\noutput directory pattern. It is meant to be used along with the configuration for working dir, especially\nin ",(0,a.mdx)("inlineCode",{parentName:"p"},"hydra.sweep.subdir"),"."),(0,a.mdx)("p",null,"If we run the example application with the following commandline overrides and configs:"),(0,a.mdx)("pre",null,(0,a.mdx)("code",{parentName:"pre",className:"language-bash"},"python my_app.py --multirun batch_size=32 learning_rate=0.1,0.01\n")),(0,a.mdx)("div",{className:"row"},(0,a.mdx)("div",{className:"col col--6"},(0,a.mdx)("pre",null,(0,a.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="config.yaml"',title:'"config.yaml"'},"hydra:\n  sweep:\n    dir: multirun\n    subdir: ${hydra.job.override_dirname}\n"))),(0,a.mdx)("div",{className:"col  col--6"},(0,a.mdx)("pre",null,(0,a.mdx)("code",{parentName:"pre",className:"language-bash",metastring:'title="working dir created"',title:'"working',dir:!0,'created"':!0},"$ tree multirun -d\nmultirun\n\u251c\u2500\u2500 batch_size=32,learning_rate=0.01\n\u2514\u2500\u2500 batch_size=32,learning_rate=0.1\n")))),(0,a.mdx)("p",null,"You can further customized the output dir creation by configuring",(0,a.mdx)("inlineCode",{parentName:"p"},"hydra.job.override_dirname"),"."),(0,a.mdx)("p",null,"In particular, the separator char ",(0,a.mdx)("inlineCode",{parentName:"p"},"=")," and the item separator char ",(0,a.mdx)("inlineCode",{parentName:"p"},",")," can be modified by overriding\n",(0,a.mdx)("inlineCode",{parentName:"p"},"hydra.job.config.override_dirname.kv_sep")," and ",(0,a.mdx)("inlineCode",{parentName:"p"},"hydra.job.config.override_dirname.item_sep"),".\nCommand line override keys can also be automatically excluded from the generated ",(0,a.mdx)("inlineCode",{parentName:"p"},"override_dirname"),"."),(0,a.mdx)("p",null,"An example of a case where the exclude is useful is a random seed."),(0,a.mdx)("pre",null,(0,a.mdx)("code",{parentName:"pre",className:"language-yaml"},"hydra:\n  run:\n    dir: output/${hydra.job.override_dirname}/seed=${seed}\n  job:\n    config:\n      override_dirname:\n        exclude_keys:\n          - seed\n")),(0,a.mdx)("p",null,"With this configuration, running"),(0,a.mdx)("pre",null,(0,a.mdx)("code",{parentName:"pre",className:"language-bash"},"$ python my_app.py --multirun  batch_size=32 learning_rate=0.1,0.01 seed=1,2\n")),(0,a.mdx)("p",null,"Would result in a directory structure like:"),(0,a.mdx)("pre",null,(0,a.mdx)("code",{parentName:"pre"},"$ tree multirun -d\nmultirun\n\u251c\u2500\u2500 batch_size=32,learning_rate=0.01\n\u2502\xa0\xa0 \u251c\u2500\u2500 seed=1\n\u2502\xa0\xa0 \u2514\u2500\u2500 seed=2\n\u2514\u2500\u2500 batch_size=32,learning_rate=0.1\n    \u251c\u2500\u2500 seed=1\n    \u2514\u2500\u2500 seed=2\n")))}s.isMDXComponent=!0},49595:(e,r,n)=>{n.d(r,{A:()=>m,C:()=>u});var t=n(58168),a=n(96540),i=n(75489),o=n(44586),d=n(48295);function l(e){const r=(0,d.ir)();return(0,o.default)().siteConfig.customFields.githubLinkVersionToBaseUrl[r?.name??"current"]+e}function m(e){return a.createElement(i.default,(0,t.A)({},e,{to:l(e.to),target:"_blank"}))}function u(e){const r=e.text??"Example (Click Here)";return a.createElement(m,e,a.createElement("span",null,"\xa0"),a.createElement("img",{src:"https://img.shields.io/badge/-"+r+"-informational",alt:"Example (Click Here)"}))}}}]);