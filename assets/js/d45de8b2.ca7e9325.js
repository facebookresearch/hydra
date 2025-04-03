"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[2539],{15680:(e,n,a)=>{a.r(n),a.d(n,{MDXContext:()=>s,MDXProvider:()=>d,mdx:()=>y,useMDXComponents:()=>u,withMDXComponents:()=>c});var r=a(96540);function t(e,n,a){return n in e?Object.defineProperty(e,n,{value:a,enumerable:!0,configurable:!0,writable:!0}):e[n]=a,e}function l(){return l=Object.assign||function(e){for(var n=1;n<arguments.length;n++){var a=arguments[n];for(var r in a)Object.prototype.hasOwnProperty.call(a,r)&&(e[r]=a[r])}return e},l.apply(this,arguments)}function i(e,n){var a=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);n&&(r=r.filter((function(n){return Object.getOwnPropertyDescriptor(e,n).enumerable}))),a.push.apply(a,r)}return a}function o(e){for(var n=1;n<arguments.length;n++){var a=null!=arguments[n]?arguments[n]:{};n%2?i(Object(a),!0).forEach((function(n){t(e,n,a[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(a)):i(Object(a)).forEach((function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(a,n))}))}return e}function p(e,n){if(null==e)return{};var a,r,t=function(e,n){if(null==e)return{};var a,r,t={},l=Object.keys(e);for(r=0;r<l.length;r++)a=l[r],n.indexOf(a)>=0||(t[a]=e[a]);return t}(e,n);if(Object.getOwnPropertySymbols){var l=Object.getOwnPropertySymbols(e);for(r=0;r<l.length;r++)a=l[r],n.indexOf(a)>=0||Object.prototype.propertyIsEnumerable.call(e,a)&&(t[a]=e[a])}return t}var s=r.createContext({}),c=function(e){return function(n){var a=u(n.components);return r.createElement(e,l({},n,{components:a}))}},u=function(e){var n=r.useContext(s),a=n;return e&&(a="function"==typeof e?e(n):o(o({},n),e)),a},d=function(e){var n=u(e.components);return r.createElement(s.Provider,{value:n},e.children)},m="mdxType",h={inlineCode:"code",wrapper:function(e){var n=e.children;return r.createElement(r.Fragment,{},n)}},b=r.forwardRef((function(e,n){var a=e.components,t=e.mdxType,l=e.originalType,i=e.parentName,s=p(e,["components","mdxType","originalType","parentName"]),c=u(a),d=t,m=c["".concat(i,".").concat(d)]||c[d]||h[d]||l;return a?r.createElement(m,o(o({ref:n},s),{},{components:a})):r.createElement(m,o({ref:n},s))}));function y(e,n){var a=arguments,t=n&&n.mdxType;if("string"==typeof e||t){var l=a.length,i=new Array(l);i[0]=b;var o={};for(var p in n)hasOwnProperty.call(n,p)&&(o[p]=n[p]);o.originalType=e,o[m]="string"==typeof e?e:t,i[1]=o;for(var s=2;s<l;s++)i[s]=a[s];return r.createElement.apply(null,i)}return r.createElement.apply(null,a)}b.displayName="MDXCreateElement"},54823:(e,n,a)=>{a.r(n),a.d(n,{assets:()=>p,contentTitle:()=>i,default:()=>d,frontMatter:()=>l,metadata:()=>o,toc:()=>s});var r=a(58168),t=(a(96540),a(15680));const l={id:"joblib_launcher",title:"Joblib Launcher plugin",sidebar_label:"Joblib Launcher plugin"},i=void 0,o={unversionedId:"plugins/joblib_launcher",id:"version-1.0/plugins/joblib_launcher",title:"Joblib Launcher plugin",description:"PyPI",source:"@site/versioned_docs/version-1.0/plugins/joblib_launcher.md",sourceDirName:"plugins",slug:"/plugins/joblib_launcher",permalink:"/docs/1.0/plugins/joblib_launcher",draft:!1,editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/versioned_docs/version-1.0/plugins/joblib_launcher.md",tags:[],version:"1.0",lastUpdatedBy:"dependabot[bot]",lastUpdatedAt:1743717584,formattedLastUpdatedAt:"Apr 3, 2025",frontMatter:{id:"joblib_launcher",title:"Joblib Launcher plugin",sidebar_label:"Joblib Launcher plugin"},sidebar:"docs",previous:{title:"Colorlog plugin",permalink:"/docs/1.0/plugins/colorlog"},next:{title:"Ray Launcher plugin",permalink:"/docs/1.0/plugins/ray_launcher"}},p={},s=[{value:"Installation",id:"installation",level:3},{value:"Usage",id:"usage",level:3}],c={toc:s},u="wrapper";function d(e){let{components:n,...a}=e;return(0,t.mdx)(u,(0,r.A)({},c,a,{components:n,mdxType:"MDXLayout"}),(0,t.mdx)("p",null,(0,t.mdx)("a",{parentName:"p",href:"https://pypi.org/project/hydra-joblib-launcher/"},(0,t.mdx)("img",{parentName:"a",src:"https://img.shields.io/pypi/v/hydra-joblib-launcher",alt:"PyPI"})),"\n",(0,t.mdx)("img",{parentName:"p",src:"https://img.shields.io/pypi/l/hydra-joblib-launcher",alt:"PyPI - License"}),"\n",(0,t.mdx)("img",{parentName:"p",src:"https://img.shields.io/pypi/pyversions/hydra-joblib-launcher",alt:"PyPI - Python Version"}),"\n",(0,t.mdx)("a",{parentName:"p",href:"https://pypistats.org/packages/hydra-joblib-launcher"},(0,t.mdx)("img",{parentName:"a",src:"https://img.shields.io/pypi/dm/hydra-joblib-launcher.svg",alt:"PyPI - Downloads"})),"\n",(0,t.mdx)("a",{parentName:"p",href:"https://github.com/facebookresearch/hydra/tree/1.0_branch/plugins/hydra_joblib_launcher/example"},(0,t.mdx)("img",{parentName:"a",src:"https://img.shields.io/badge/-Example%20application-informational",alt:"Example application"})),"\n",(0,t.mdx)("a",{parentName:"p",href:"https://github.com/facebookresearch/hydra/tree/1.0_branch/plugins/hydra_joblib_launcher"},(0,t.mdx)("img",{parentName:"a",src:"https://img.shields.io/badge/-Plugin%20source-informational",alt:"Plugin source"}))),(0,t.mdx)("p",null,"The Joblib Launcher plugin provides a launcher for parallel tasks based on ",(0,t.mdx)("a",{parentName:"p",href:"https://joblib.readthedocs.io/en/latest/parallel.html"},(0,t.mdx)("inlineCode",{parentName:"a"},"Joblib.Parallel")),"."),(0,t.mdx)("h3",{id:"installation"},"Installation"),(0,t.mdx)("pre",null,(0,t.mdx)("code",{parentName:"pre",className:"language-commandline"},"pip install hydra-joblib-launcher --upgrade\n")),(0,t.mdx)("h3",{id:"usage"},"Usage"),(0,t.mdx)("p",null,"Once installed, add ",(0,t.mdx)("inlineCode",{parentName:"p"},"hydra/launcher=joblib")," to your command line. Alternatively, override ",(0,t.mdx)("inlineCode",{parentName:"p"},"hydra/launcher")," in your config:"),(0,t.mdx)("pre",null,(0,t.mdx)("code",{parentName:"pre",className:"language-yaml"},"defaults:\n  - hydra/launcher: joblib\n")),(0,t.mdx)("p",null,"By default, process-based parallelism using all available CPU cores is used. By overriding the default configuration, it is e.g. possible limit the number of parallel executions."),(0,t.mdx)("p",null,"The JobLibLauncherConf backing the config is defined ",(0,t.mdx)("a",{parentName:"p",href:"https://github.com/facebookresearch/hydra/blob/master/plugins/hydra_joblib_launcher/hydra_plugins/hydra_joblib_launcher/config.py"},"here"),":"),(0,t.mdx)("p",null,"You can discover the Joblib Launcher parameters with:"),(0,t.mdx)("pre",null,(0,t.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="$ python your_app.py hydra/launcher=joblib --cfg hydra -p hydra.launcher"',title:'"$',python:!0,"your_app.py":!0,"hydra/launcher":"joblib","--cfg":!0,hydra:!0,"-p":!0,'hydra.launcher"':!0},"# @package hydra.launcher\n_target_: hydra_plugins.hydra_joblib_launcher.joblib_launcher.JoblibLauncher\nn_jobs: 10\nbackend: null\nprefer: processes\nrequire: null\nverbose: 0\ntimeout: null\npre_dispatch: 2*n_jobs\nbatch_size: auto\ntemp_folder: null\nmax_nbytes: null\nmmap_mode: r\n")),(0,t.mdx)("p",null,"See ",(0,t.mdx)("a",{parentName:"p",href:"https://joblib.readthedocs.io/en/latest/parallel.html"},(0,t.mdx)("inlineCode",{parentName:"a"},"Joblib.Parallel")," documentation")," for full details about the parameters above."),(0,t.mdx)("div",{class:"alert alert--info",role:"alert"},"NOTE: The only supported JobLib backend is Loky (process-based parallelism)."),(0,t.mdx)("br",null),(0,t.mdx)("p",null,"An ",(0,t.mdx)("a",{parentName:"p",href:"https://github.com/facebookresearch/hydra/tree/1.0_branch/plugins/hydra_joblib_launcher/example"},"example application")," using this launcher is provided in the plugin repository."),(0,t.mdx)("p",null,"Starting the app with ",(0,t.mdx)("inlineCode",{parentName:"p"},"python my_app.py --multirun task=1,2,3,4,5")," will launch five parallel executions:"),(0,t.mdx)("pre",null,(0,t.mdx)("code",{parentName:"pre",className:"language-text"},"$ python my_app.py --multirun task=1,2,3,4,5\n[HYDRA] Joblib.Parallel(n_jobs=-1,verbose=0,timeout=None,pre_dispatch=2*n_jobs,batch_size=auto,temp_folder=None,max_nbytes=None,mmap_mode=r,backend=loky) is launching 5 jobs\n[HYDRA] Launching jobs, sweep output dir : multirun/2020-02-18/10-00-00\n[__main__][INFO] - Process ID 14336 executing task 2 ...\n[__main__][INFO] - Process ID 14333 executing task 1 ...\n[__main__][INFO] - Process ID 14334 executing task 3 ...\n[__main__][INFO] - Process ID 14335 executing task 4 ...\n[__main__][INFO] - Process ID 14337 executing task 5 ...\n")))}d.isMDXComponent=!0}}]);