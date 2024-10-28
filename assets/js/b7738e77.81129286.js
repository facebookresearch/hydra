"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[6895],{15680:(e,n,r)=>{r.r(n),r.d(n,{MDXContext:()=>p,MDXProvider:()=>c,mdx:()=>f,useMDXComponents:()=>u,withMDXComponents:()=>d});var a=r(96540);function t(e,n,r){return n in e?Object.defineProperty(e,n,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[n]=r,e}function i(){return i=Object.assign||function(e){for(var n=1;n<arguments.length;n++){var r=arguments[n];for(var a in r)Object.prototype.hasOwnProperty.call(r,a)&&(e[a]=r[a])}return e},i.apply(this,arguments)}function o(e,n){var r=Object.keys(e);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);n&&(a=a.filter((function(n){return Object.getOwnPropertyDescriptor(e,n).enumerable}))),r.push.apply(r,a)}return r}function l(e){for(var n=1;n<arguments.length;n++){var r=null!=arguments[n]?arguments[n]:{};n%2?o(Object(r),!0).forEach((function(n){t(e,n,r[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(r)):o(Object(r)).forEach((function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(r,n))}))}return e}function s(e,n){if(null==e)return{};var r,a,t=function(e,n){if(null==e)return{};var r,a,t={},i=Object.keys(e);for(a=0;a<i.length;a++)r=i[a],n.indexOf(r)>=0||(t[r]=e[r]);return t}(e,n);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);for(a=0;a<i.length;a++)r=i[a],n.indexOf(r)>=0||Object.prototype.propertyIsEnumerable.call(e,r)&&(t[r]=e[r])}return t}var p=a.createContext({}),d=function(e){return function(n){var r=u(n.components);return a.createElement(e,i({},n,{components:r}))}},u=function(e){var n=a.useContext(p),r=n;return e&&(r="function"==typeof e?e(n):l(l({},n),e)),r},c=function(e){var n=u(e.components);return a.createElement(p.Provider,{value:n},e.children)},m={inlineCode:"code",wrapper:function(e){var n=e.children;return a.createElement(a.Fragment,{},n)}},h=a.forwardRef((function(e,n){var r=e.components,t=e.mdxType,i=e.originalType,o=e.parentName,p=s(e,["components","mdxType","originalType","parentName"]),d=u(r),c=t,h=d["".concat(o,".").concat(c)]||d[c]||m[c]||i;return r?a.createElement(h,l(l({ref:n},p),{},{components:r})):a.createElement(h,l({ref:n},p))}));function f(e,n){var r=arguments,t=n&&n.mdxType;if("string"==typeof e||t){var i=r.length,o=new Array(i);o[0]=h;var l={};for(var s in n)hasOwnProperty.call(n,s)&&(l[s]=n[s]);l.originalType=e,l.mdxType="string"==typeof e?e:t,o[1]=l;for(var p=2;p<i;p++)o[p]=r[p];return a.createElement.apply(null,o)}return a.createElement.apply(null,r)}h.displayName="MDXCreateElement"},65806:(e,n,r)=>{r.r(n),r.d(n,{contentTitle:()=>s,default:()=>c,frontMatter:()=>l,metadata:()=>p,toc:()=>d});var a=r(58168),t=r(98587),i=(r(96540),r(15680)),o=["components"],l={id:"rq_launcher",title:"RQ Launcher plugin",sidebar_label:"RQ Launcher plugin"},s=void 0,p={unversionedId:"plugins/rq_launcher",id:"version-1.0/plugins/rq_launcher",title:"RQ Launcher plugin",description:"PyPI",source:"@site/versioned_docs/version-1.0/plugins/rq_launcher.md",sourceDirName:"plugins",slug:"/plugins/rq_launcher",permalink:"/docs/1.0/plugins/rq_launcher",editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/versioned_docs/version-1.0/plugins/rq_launcher.md",tags:[],version:"1.0",lastUpdatedBy:"dependabot[bot]",lastUpdatedAt:1730135614,formattedLastUpdatedAt:"10/28/2024",frontMatter:{id:"rq_launcher",title:"RQ Launcher plugin",sidebar_label:"RQ Launcher plugin"},sidebar:"version-1.0/docs",previous:{title:"Ray Launcher plugin",permalink:"/docs/1.0/plugins/ray_launcher"},next:{title:"Submitit Launcher plugin",permalink:"/docs/1.0/plugins/submitit_launcher"}},d=[{value:"Installation",id:"installation",children:[],level:3},{value:"Usage",id:"usage",children:[],level:3}],u={toc:d};function c(e){var n=e.components,r=(0,t.A)(e,o);return(0,i.mdx)("wrapper",(0,a.A)({},u,r,{components:n,mdxType:"MDXLayout"}),(0,i.mdx)("p",null,(0,i.mdx)("a",{parentName:"p",href:"https://pypi.org/project/hydra-rq-launcher/"},(0,i.mdx)("img",{parentName:"a",src:"https://img.shields.io/pypi/v/hydra-rq-launcher",alt:"PyPI"})),"\n",(0,i.mdx)("img",{parentName:"p",src:"https://img.shields.io/pypi/l/hydra-rq-launcher",alt:"PyPI - License"}),"\n",(0,i.mdx)("img",{parentName:"p",src:"https://img.shields.io/pypi/pyversions/hydra-rq-launcher",alt:"PyPI - Python Version"}),"\n",(0,i.mdx)("a",{parentName:"p",href:"https://pypistats.org/packages/hydra-rq-launcher"},(0,i.mdx)("img",{parentName:"a",src:"https://img.shields.io/pypi/dm/hydra-rq-launcher.svg",alt:"PyPI - Downloads"})),"\n",(0,i.mdx)("a",{parentName:"p",href:"https://github.com/facebookresearch/hydra/tree/1.0_branch/plugins/hydra_rq_launcher/example"},(0,i.mdx)("img",{parentName:"a",src:"https://img.shields.io/badge/-Example%20application-informational",alt:"Example application"})),"\n",(0,i.mdx)("a",{parentName:"p",href:"https://github.com/facebookresearch/hydra/tree/1.0_branch/plugins/hydra_rq_launcher"},(0,i.mdx)("img",{parentName:"a",src:"https://img.shields.io/badge/-Plugin%20source-informational",alt:"Plugin source"}))),(0,i.mdx)("p",null,"The RQ Launcher plugin provides a launcher for distributed execution and job queuing based on ",(0,i.mdx)("a",{parentName:"p",href:"https://python-rq.org"},"Redis Queue (RQ)"),"."),(0,i.mdx)("p",null,"RQ launcher allows parallelizing across multiple nodes and scheduling jobs in queues. Usage of this plugin requires a ",(0,i.mdx)("a",{parentName:"p",href:"https://redis.io/topics/quickstart"},"Redis server"),". When parallelisation on a single node is intended, the Joblib launcher may be preferable, since it works without a database."),(0,i.mdx)("h3",{id:"installation"},"Installation"),(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre",className:"language-commandline"},"pip install hydra-rq-launcher --upgrade\n")),(0,i.mdx)("p",null,"Usage of this plugin requires a ",(0,i.mdx)("a",{parentName:"p",href:"https://redis.io/topics/quickstart"},"Redis server"),"."),(0,i.mdx)("p",null,"Note that RQ does ",(0,i.mdx)("a",{parentName:"p",href:"https://python-rq.org/docs/#limitations"},"not support Windows"),"."),(0,i.mdx)("h3",{id:"usage"},"Usage"),(0,i.mdx)("p",null,"Once installed, add ",(0,i.mdx)("inlineCode",{parentName:"p"},"hydra/launcher=rq")," to your command line. Alternatively, override ",(0,i.mdx)("inlineCode",{parentName:"p"},"hydra/launcher")," in your config:"),(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre",className:"language-yaml"},"defaults:\n  - hydra/launcher: rq\n")),(0,i.mdx)("p",null,"The configuration packaged with the plugin is defined ",(0,i.mdx)("a",{parentName:"p",href:"https://github.com/facebookresearch/hydra/blob/master/plugins/hydra_rq_launcher/hydra_plugins/hydra_rq_launcher/config.py"},"here"),". The default configuration is as follows:"),(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="$ python your_app.py hydra/launcher=rq --cfg hydra -p hydra.launcher"',title:'"$',python:!0,"your_app.py":!0,"hydra/launcher":"rq","--cfg":!0,hydra:!0,"-p":!0,'hydra.launcher"':!0},'# @package hydra.launcher\n_target_: hydra_plugins.hydra_rq_launcher.rq_launcher.RQLauncher\nenqueue:\n  job_timeout: null                  # maximum runtime of the job before it\'s killed (e.g. "1d" for 1 day, units: d/h/m/s), default: no limit\n  ttl: null                          # maximum queued time before the job before is discarded (e.g. "1d" for 1 day, units: d/h/m/s), default: no limit\n  result_ttl: null                   # how long successful jobs and their results are kept (e.g. "1d" for 1 day, units: d/h/m/s), default: no limit\n  failure_ttl: null                  # specifies how long failed jobs are kept (e.g. "1d" for 1 day, units: d/h/m/s), default: no limit\n  at_front: false                    # place job at the front of the queue, instead of the back\n  job_id: null                       # job id, will be overidden automatically by a uuid unless specified explicitly\n  description: null                  # description, will be overidden automatically unless specified explicitly\nqueue: default                       # queue name\nredis:\n  host: ${env:REDIS_HOST,localhost}  # host address via REDIS_HOST environment variable, default: localhost\n  port: ${env:REDIS_PORT,6379}       # port via REDIS_PORT environment variable, default: 6379\n  db: ${env:REDIS_DB,0}              # database via REDIS_DB environment variable, default: 0\n  password: ${env:REDIS_PASSWORD,}   # password via REDIS_PASSWORD environment variable, default: no password\n  mock: ${env:REDIS_MOCK,False}      # switch to run without redis server in single thread, for testing purposes only\nstop_after_enqueue: false            # stop after enqueueing by raising custom exception\nwait_polling: 1.0                    # wait time in seconds when polling results\n')),(0,i.mdx)("p",null,"The plugin is using environment variables to store Redis connection information. The environment variables ",(0,i.mdx)("inlineCode",{parentName:"p"},"REDIS_HOST"),", ",(0,i.mdx)("inlineCode",{parentName:"p"},"REDIS_PORT"),", ",(0,i.mdx)("inlineCode",{parentName:"p"},"REDIS_DB"),", and ",(0,i.mdx)("inlineCode",{parentName:"p"},"REDIS_PASSWORD"),", are used for the host address, port, database, and password of the server, respectively."),(0,i.mdx)("p",null,"For example, they might be set as follows when using ",(0,i.mdx)("inlineCode",{parentName:"p"},"bash")," or ",(0,i.mdx)("inlineCode",{parentName:"p"},"zsh")," as a shell:"),(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre",className:"language-commandline"},'export REDIS_HOST="localhost"\nexport REDIS_PORT="6379"\nexport REDIS_DB="0"\nexport REDIS_PASSWORD=""\n')),(0,i.mdx)("p",null,"Assuming configured environment variables, workers connecting to the Redis server can be launched using:"),(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre",className:"language-commandline"},"rq worker --url redis://:$REDIS_PASSWORD@$REDIS_HOST:$REDIS_PORT/$REDIS_DB\n")),(0,i.mdx)("p",null,"An ",(0,i.mdx)("a",{parentName:"p",href:"https://github.com/facebookresearch/hydra/tree/1.0_branch/plugins/hydra_rq_launcher/example"},"example application")," using this launcher is provided in the plugin repository."),(0,i.mdx)("p",null,"Starting the app with ",(0,i.mdx)("inlineCode",{parentName:"p"},"python my_app.py --multirun task=1,2,3,4,5")," will enqueue five jobs to be processed by worker instances:"),(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre",className:"language-text"},"$ python my_app.py --multirun task=1,2,3,4,5\n\n[HYDRA] RQ Launcher is enqueuing 5 job(s) in queue : default\n[HYDRA] Sweep output dir : multirun/2020-06-15/18-00-00\n[HYDRA] Enqueued 13b3da4e-03f7-4d16-9ca8-cfb3c48afeae\n[HYDRA]     #1 : task=1\n[HYDRA] Enqueued 00c6a32d-e5a4-432c-a0f3-b9d4ef0dd585\n[HYDRA]     #2 : task=2\n[HYDRA] Enqueued 63b90f27-0711-4c95-8f63-70164fd850df\n[HYDRA]     #3 : task=3\n[HYDRA] Enqueued b1d49825-8b28-4516-90ca-8106477e1eb1\n[HYDRA]     #4 : task=4\n[HYDRA] Enqueued ed96bdaa-087d-4c7f-9ecb-56daf948d5e2\n[HYDRA]     #5 : task=5\n[HYDRA] Finished enqueuing\n[HYDRA] Polling job statuses every 1.0 sec\n")),(0,i.mdx)("p",null,"Note that any dependencies need to be installed in the Python environment used to run the RQ worker. For serialization of jobs ",(0,i.mdx)("a",{parentName:"p",href:"https://github.com/cloudpickle/cloudpickle"},(0,i.mdx)("inlineCode",{parentName:"a"},"cloudpickle"))," is used."),(0,i.mdx)("p",null,"The ",(0,i.mdx)("a",{parentName:"p",href:"https://python-rq.org/"},"RQ documentation")," holds further information on ",(0,i.mdx)("a",{parentName:"p",href:"http://python-rq.org/docs/monitoring/"},"job monitoring"),", which can be done via console or ",(0,i.mdx)("a",{parentName:"p",href:"https://github.com/nvie/rq-dashboard"},"web interfaces"),", and provides ",(0,i.mdx)("a",{parentName:"p",href:"https://python-rq.org/patterns/"},"patterns")," for worker and exception handling."))}c.isMDXComponent=!0}}]);