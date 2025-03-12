"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[9480],{15680:(e,n,t)=>{t.r(n),t.d(n,{MDXContext:()=>d,MDXProvider:()=>u,mdx:()=>g,useMDXComponents:()=>s,withMDXComponents:()=>p});var a=t(96540);function r(e,n,t){return n in e?Object.defineProperty(e,n,{value:t,enumerable:!0,configurable:!0,writable:!0}):e[n]=t,e}function o(){return o=Object.assign||function(e){for(var n=1;n<arguments.length;n++){var t=arguments[n];for(var a in t)Object.prototype.hasOwnProperty.call(t,a)&&(e[a]=t[a])}return e},o.apply(this,arguments)}function i(e,n){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);n&&(a=a.filter((function(n){return Object.getOwnPropertyDescriptor(e,n).enumerable}))),t.push.apply(t,a)}return t}function l(e){for(var n=1;n<arguments.length;n++){var t=null!=arguments[n]?arguments[n]:{};n%2?i(Object(t),!0).forEach((function(n){r(e,n,t[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):i(Object(t)).forEach((function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(t,n))}))}return e}function m(e,n){if(null==e)return{};var t,a,r=function(e,n){if(null==e)return{};var t,a,r={},o=Object.keys(e);for(a=0;a<o.length;a++)t=o[a],n.indexOf(t)>=0||(r[t]=e[t]);return r}(e,n);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(e);for(a=0;a<o.length;a++)t=o[a],n.indexOf(t)>=0||Object.prototype.propertyIsEnumerable.call(e,t)&&(r[t]=e[t])}return r}var d=a.createContext({}),p=function(e){return function(n){var t=s(n.components);return a.createElement(e,o({},n,{components:t}))}},s=function(e){var n=a.useContext(d),t=n;return e&&(t="function"==typeof e?e(n):l(l({},n),e)),t},u=function(e){var n=s(e.components);return a.createElement(d.Provider,{value:n},e.children)},c="mdxType",h={inlineCode:"code",wrapper:function(e){var n=e.children;return a.createElement(a.Fragment,{},n)}},y=a.forwardRef((function(e,n){var t=e.components,r=e.mdxType,o=e.originalType,i=e.parentName,d=m(e,["components","mdxType","originalType","parentName"]),p=s(t),u=r,c=p["".concat(i,".").concat(u)]||p[u]||h[u]||o;return t?a.createElement(c,l(l({ref:n},d),{},{components:t})):a.createElement(c,l({ref:n},d))}));function g(e,n){var t=arguments,r=n&&n.mdxType;if("string"==typeof e||r){var o=t.length,i=new Array(o);i[0]=y;var l={};for(var m in n)hasOwnProperty.call(n,m)&&(l[m]=n[m]);l.originalType=e,l[c]="string"==typeof e?e:r,i[1]=l;for(var d=2;d<o;d++)i[d]=t[d];return a.createElement.apply(null,i)}return a.createElement.apply(null,t)}y.displayName="MDXCreateElement"},49595:(e,n,t)=>{t.d(n,{A:()=>d,C:()=>p});var a=t(58168),r=t(96540),o=t(75489),i=t(44586),l=t(48295);function m(e){const n=(0,l.ir)();return(0,i.default)().siteConfig.customFields.githubLinkVersionToBaseUrl[n?.name??"current"]+e}function d(e){return r.createElement(o.default,(0,a.A)({},e,{to:m(e.to),target:"_blank"}))}function p(e){const n=e.text??"Example (Click Here)";return r.createElement(d,e,r.createElement("span",null,"\xa0"),r.createElement("img",{src:"https://img.shields.io/badge/-"+n+"-informational",alt:"Example (Click Here)"}))}},52622:(e,n,t)=>{t.r(n),t.d(n,{assets:()=>d,contentTitle:()=>l,default:()=>c,frontMatter:()=>i,metadata:()=>m,toc:()=>p});var a=t(58168),r=(t(96540),t(15680)),o=t(49595);const i={id:"multi-run",title:"Multi-run",sidebar_label:"Multi-run"},l=void 0,m={unversionedId:"tutorials/basic/running_your_app/multi-run",id:"version-1.3/tutorials/basic/running_your_app/multi-run",title:"Multi-run",description:"Sometimes you want to run the same application with multiple different configurations.",source:"@site/versioned_docs/version-1.3/tutorials/basic/running_your_app/2_multirun.md",sourceDirName:"tutorials/basic/running_your_app",slug:"/tutorials/basic/running_your_app/multi-run",permalink:"/docs/1.3/tutorials/basic/running_your_app/multi-run",draft:!1,editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/versioned_docs/version-1.3/tutorials/basic/running_your_app/2_multirun.md",tags:[],version:"1.3",lastUpdatedBy:"jesszzzz",lastUpdatedAt:1741814683,formattedLastUpdatedAt:"Mar 12, 2025",sidebarPosition:2,frontMatter:{id:"multi-run",title:"Multi-run",sidebar_label:"Multi-run"},sidebar:"docs",previous:{title:"Putting it all together",permalink:"/docs/1.3/tutorials/basic/your_first_app/composition"},next:{title:"Output/Working directory",permalink:"/docs/1.3/tutorials/basic/running_your_app/working_directory"}},d={},p=[{value:"Configure <code>hydra.mode</code> (new in Hydra 1.2)",id:"configure-hydramode-new-in-hydra-12",level:3},{value:"<code>--multirun (-m)</code> from the command-line",id:"--multirun--m-from-the-command-line",level:3},{value:"Sweeping via <code>hydra.sweeper.params</code>",id:"sweeping-via-hydrasweeperparams",level:3},{value:"Additional sweep types",id:"additional-sweep-types",level:3},{value:"Sweeper",id:"sweeper",level:3},{value:"Launcher",id:"launcher",level:3}],s={toc:p},u="wrapper";function c(e){let{components:n,...t}=e;return(0,r.mdx)(u,(0,a.A)({},s,t,{components:n,mdxType:"MDXLayout"}),(0,r.mdx)("p",null,"Sometimes you want to run the same application with multiple different configurations.",(0,r.mdx)("br",{parentName:"p"}),"\n","E.g. running a performance test on each of the databases with each of the schemas."),(0,r.mdx)("p",null,"You can multirun a Hydra application via either commandline or configuration:"),(0,r.mdx)("h3",{id:"configure-hydramode-new-in-hydra-12"},"Configure ",(0,r.mdx)("inlineCode",{parentName:"h3"},"hydra.mode")," (new in Hydra 1.2)"),(0,r.mdx)("p",null,"You can configure ",(0,r.mdx)("inlineCode",{parentName:"p"},"hydra.mode")," in any supported way. The legal values are ",(0,r.mdx)("inlineCode",{parentName:"p"},"RUN")," and ",(0,r.mdx)("inlineCode",{parentName:"p"},"MULTIRUN"),".\nThe following shows how to override from the command-line and sweep over all combinations of the dbs and schemas.\nSetting ",(0,r.mdx)("inlineCode",{parentName:"p"},"hydra.mode=MULTIRUN")," in your input config would make your application multi-run by default."),(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-text",metastring:'title="$ python my_app.py hydra.mode=MULTIRUN db=mysql,postgresql schema=warehouse,support,school"',title:'"$',python:!0,"my_app.py":!0,"hydra.mode":"MULTIRUN",db:"mysql,postgresql",schema:'warehouse,support,school"'},"[2021-01-20 17:25:03,317][HYDRA] Launching 6 jobs locally\n[2021-01-20 17:25:03,318][HYDRA]        #0 : db=mysql schema=warehouse\n[2021-01-20 17:25:03,458][HYDRA]        #1 : db=mysql schema=support\n[2021-01-20 17:25:03,602][HYDRA]        #2 : db=mysql schema=school\n[2021-01-20 17:25:03,755][HYDRA]        #3 : db=postgresql schema=warehouse\n[2021-01-20 17:25:03,895][HYDRA]        #4 : db=postgresql schema=support\n[2021-01-20 17:25:04,040][HYDRA]        #5 : db=postgresql schema=school\n")),(0,r.mdx)("p",null,"The printed configurations have been omitted for brevity."),(0,r.mdx)("h3",{id:"--multirun--m-from-the-command-line"},(0,r.mdx)("inlineCode",{parentName:"h3"},"--multirun (-m)")," from the command-line"),(0,r.mdx)("p",null,"You can achieve the above from command-line as well:"),(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-commandline"},"python my_app.py --multirun db=mysql,postgresql schema=warehouse,support,school\n")),(0,r.mdx)("p",null,"or "),(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-commandline"},"python my_app.py -m db=mysql,postgresql schema=warehouse,support,school\n")),(0,r.mdx)("p",null,"You can access ",(0,r.mdx)("inlineCode",{parentName:"p"},"hydra.mode")," at runtime to determine whether the application is in RUN or MULTIRUN mode. Check ",(0,r.mdx)("a",{parentName:"p",href:"/docs/1.3/configure_hydra/intro"},"here"),"\non how to access Hydra config at run time."),(0,r.mdx)("p",null,"If conflicts arise (e.g., ",(0,r.mdx)("inlineCode",{parentName:"p"},"hydra.mode=RUN")," and the application was run with ",(0,r.mdx)("inlineCode",{parentName:"p"},"--multirun"),"), Hydra will determine the value of ",(0,r.mdx)("inlineCode",{parentName:"p"},"hydra.mode"),"\nat run time. The following table shows what runtime ",(0,r.mdx)("inlineCode",{parentName:"p"},"hydra.mode")," value you'd get with different input configs and commandline combinations."),(0,r.mdx)("table",null,(0,r.mdx)("thead",{parentName:"table"},(0,r.mdx)("tr",{parentName:"thead"},(0,r.mdx)("th",{parentName:"tr",align:null}),(0,r.mdx)("th",{parentName:"tr",align:null},"No multirun commandline flag"),(0,r.mdx)("th",{parentName:"tr",align:null},"--multirun ( -m)"))),(0,r.mdx)("tbody",{parentName:"table"},(0,r.mdx)("tr",{parentName:"tbody"},(0,r.mdx)("td",{parentName:"tr",align:null},"hydra.mode=RUN"),(0,r.mdx)("td",{parentName:"tr",align:null},"RunMode.RUN"),(0,r.mdx)("td",{parentName:"tr",align:null},"RunMode.MULTIRUN (with UserWarning)")),(0,r.mdx)("tr",{parentName:"tbody"},(0,r.mdx)("td",{parentName:"tr",align:null},"hydra.mode=MULTIRUN"),(0,r.mdx)("td",{parentName:"tr",align:null},"RunMode.MULTIRUN"),(0,r.mdx)("td",{parentName:"tr",align:null},"RunMode.MULTIRUN")),(0,r.mdx)("tr",{parentName:"tbody"},(0,r.mdx)("td",{parentName:"tr",align:null},"hydra.mode=None (default)"),(0,r.mdx)("td",{parentName:"tr",align:null},"RunMode.RUN"),(0,r.mdx)("td",{parentName:"tr",align:null},"RunMode.MULTIRUN")))),(0,r.mdx)("admonition",{type:"important"},(0,r.mdx)("p",{parentName:"admonition"},"Hydra composes configs lazily at job launching time. If you change code or configs after launching a job/sweep, the final\ncomposed configs might be impacted.")),(0,r.mdx)("h3",{id:"sweeping-via-hydrasweeperparams"},"Sweeping via ",(0,r.mdx)("inlineCode",{parentName:"h3"},"hydra.sweeper.params")),(0,r.mdx)(o.C,{to:"examples/tutorials/basic/running_your_hydra_app/5_basic_sweep",mdxType:"ExampleGithubLink"}),(0,r.mdx)("p",null,"You can also define sweeping in the input configs by overriding\n",(0,r.mdx)("inlineCode",{parentName:"p"},"hydra.sweeper.params"),". Using the above example, the same multirun could be achieved via the following config."),(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-yaml"},"hydra:\n  sweeper:\n    params:\n      db: mysql,postgresql\n      schema: warehouse,support,school\n")),(0,r.mdx)("p",null,"The syntax are consistent for both input configs and commandline overrides.\nIf a sweep is specified in both an input config and at the command line,\nthen the commandline sweep will take precedence over the sweep defined\nin the input config. If we run the same application with the above input config and a new commandline override:"),(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-text",metastring:'title="$ python my_app.py -m db=mysql"',title:'"$',python:!0,"my_app.py":!0,"-m":!0,db:'mysql"'},"[2021-01-20 17:25:03,317][HYDRA] Launching 3 jobs locally\n[2021-01-20 17:25:03,318][HYDRA]        #0 : db=mysql schema=warehouse\n[2021-01-20 17:25:03,458][HYDRA]        #1 : db=mysql schema=support\n[2021-01-20 17:25:03,602][HYDRA]        #2 : db=mysql schema=school\n")),(0,r.mdx)("admonition",{type:"info"},(0,r.mdx)("p",{parentName:"admonition"},"The above configuration methods only apply to Hydra's default ",(0,r.mdx)("inlineCode",{parentName:"p"},"BasicSweeper")," for now. For other sweepers, please check out the\ncorresponding documentations.")),(0,r.mdx)("h3",{id:"additional-sweep-types"},"Additional sweep types"),(0,r.mdx)("p",null,"Hydra supports other kinds of sweeps, e.g.:"),(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-python"},"x=range(1,10)                  # 1-9\nschema=glob(*)                 # warehouse,support,school\nschema=glob(*,exclude=w*)      # support,school\n")),(0,r.mdx)("p",null,"See the ",(0,r.mdx)("a",{parentName:"p",href:"/docs/1.3/advanced/override_grammar/extended"},"Extended Override syntax")," for details."),(0,r.mdx)("h3",{id:"sweeper"},"Sweeper"),(0,r.mdx)("p",null,"The default sweeping logic is built into Hydra. Additional sweepers are available as plugins.\nFor example, the ",(0,r.mdx)("a",{parentName:"p",href:"/docs/1.3/plugins/ax_sweeper"},"Ax Sweeper")," can automatically find the best parameter combination!"),(0,r.mdx)("h3",{id:"launcher"},"Launcher"),(0,r.mdx)("p",null,"By default, Hydra runs your multi-run jobs locally and serially.\nOther launchers are available as plugins for launching in parallel and on different clusters. For example, the ",(0,r.mdx)("a",{parentName:"p",href:"/docs/1.3/plugins/joblib_launcher"},"JobLib Launcher"),"\ncan execute the different parameter combinations in parallel on your local machine using multi-processing."))}c.isMDXComponent=!0}}]);