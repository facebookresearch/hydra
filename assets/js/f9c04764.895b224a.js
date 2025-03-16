"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[4012],{15680:(e,n,a)=>{a.r(n),a.d(n,{MDXContext:()=>d,MDXProvider:()=>p,mdx:()=>y,useMDXComponents:()=>m,withMDXComponents:()=>s});var t=a(96540);function l(e,n,a){return n in e?Object.defineProperty(e,n,{value:a,enumerable:!0,configurable:!0,writable:!0}):e[n]=a,e}function r(){return r=Object.assign||function(e){for(var n=1;n<arguments.length;n++){var a=arguments[n];for(var t in a)Object.prototype.hasOwnProperty.call(a,t)&&(e[t]=a[t])}return e},r.apply(this,arguments)}function o(e,n){var a=Object.keys(e);if(Object.getOwnPropertySymbols){var t=Object.getOwnPropertySymbols(e);n&&(t=t.filter((function(n){return Object.getOwnPropertyDescriptor(e,n).enumerable}))),a.push.apply(a,t)}return a}function i(e){for(var n=1;n<arguments.length;n++){var a=null!=arguments[n]?arguments[n]:{};n%2?o(Object(a),!0).forEach((function(n){l(e,n,a[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(a)):o(Object(a)).forEach((function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(a,n))}))}return e}function c(e,n){if(null==e)return{};var a,t,l=function(e,n){if(null==e)return{};var a,t,l={},r=Object.keys(e);for(t=0;t<r.length;t++)a=r[t],n.indexOf(a)>=0||(l[a]=e[a]);return l}(e,n);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);for(t=0;t<r.length;t++)a=r[t],n.indexOf(a)>=0||Object.prototype.propertyIsEnumerable.call(e,a)&&(l[a]=e[a])}return l}var d=t.createContext({}),s=function(e){return function(n){var a=m(n.components);return t.createElement(e,r({},n,{components:a}))}},m=function(e){var n=t.useContext(d),a=n;return e&&(a="function"==typeof e?e(n):i(i({},n),e)),a},p=function(e){var n=m(e.components);return t.createElement(d.Provider,{value:n},e.children)},u="mdxType",f={inlineCode:"code",wrapper:function(e){var n=e.children;return t.createElement(t.Fragment,{},n)}},b=t.forwardRef((function(e,n){var a=e.components,l=e.mdxType,r=e.originalType,o=e.parentName,d=c(e,["components","mdxType","originalType","parentName"]),s=m(a),p=l,u=s["".concat(o,".").concat(p)]||s[p]||f[p]||r;return a?t.createElement(u,i(i({ref:n},d),{},{components:a})):t.createElement(u,i({ref:n},d))}));function y(e,n){var a=arguments,l=n&&n.mdxType;if("string"==typeof e||l){var r=a.length,o=new Array(r);o[0]=b;var i={};for(var c in n)hasOwnProperty.call(n,c)&&(i[c]=n[c]);i.originalType=e,i[u]="string"==typeof e?e:l,o[1]=i;for(var d=2;d<r;d++)o[d]=a[d];return t.createElement.apply(null,o)}return t.createElement.apply(null,a)}b.displayName="MDXCreateElement"},34051:(e,n,a)=>{a.r(n),a.d(n,{assets:()=>d,contentTitle:()=>i,default:()=>u,frontMatter:()=>o,metadata:()=>c,toc:()=>s});var t=a(58168),l=(a(96540),a(15680)),r=a(49595);const o={id:"callbacks",title:"Callbacks",sidebar_label:"Callbacks"},i=void 0,c={unversionedId:"experimental/callbacks",id:"version-1.1/experimental/callbacks",title:"Callbacks",description:"The Callback interface enables custom",source:"@site/versioned_docs/version-1.1/experimental/callbacks.md",sourceDirName:"experimental",slug:"/experimental/callbacks",permalink:"/docs/1.1/experimental/callbacks",draft:!1,editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/versioned_docs/version-1.1/experimental/callbacks.md",tags:[],version:"1.1",lastUpdatedBy:"dependabot[bot]",lastUpdatedAt:1742161400,formattedLastUpdatedAt:"Mar 16, 2025",frontMatter:{id:"callbacks",title:"Callbacks",sidebar_label:"Callbacks"},sidebar:"docs",previous:{title:"Introduction",permalink:"/docs/1.1/experimental/intro"},next:{title:"Developer Guide Overview",permalink:"/docs/1.1/development/overview"}},d={},s=[{value:"Configure Callback",id:"configure-callback",level:3},{value:"Callback ordering",id:"callback-ordering",level:3}],m={toc:s},p="wrapper";function u(e){let{components:n,...a}=e;return(0,l.mdx)(p,(0,t.A)({},m,a,{components:n,mdxType:"MDXLayout"}),(0,l.mdx)("p",null,"The ",(0,l.mdx)(r.A,{to:"hydra/experimental/callback.py",mdxType:"GithubLink"},"Callback interface")," enables custom\ncode to be triggered by various Hydra events."),(0,l.mdx)("p",null,"To use the callback API, one should import Hydra's ",(0,l.mdx)("inlineCode",{parentName:"p"},"Callback")," class:"),(0,l.mdx)("pre",null,(0,l.mdx)("code",{parentName:"pre",className:"language-python"},"from hydra.experimental.callback import Callback\n")),(0,l.mdx)("p",null,"Users can then create subclasses of this ",(0,l.mdx)("inlineCode",{parentName:"p"},"Callback")," class, overriding one or more of\nthe methods defined by ",(0,l.mdx)("inlineCode",{parentName:"p"},"Callback"),". For the methods of a subclass to be called at the\nappropriate time, the subclass must be registered with Hydra in the ",(0,l.mdx)("inlineCode",{parentName:"p"},"hydra.callbacks")," config\n(see examples below)."),(0,l.mdx)("p",null,"The full API exposed by the ",(0,l.mdx)("inlineCode",{parentName:"p"},"hydra.experimental.callback.Callback")," class is listed below:"),(0,l.mdx)("details",null,(0,l.mdx)("summary",null,"Events supported (Click to expand)"),(0,l.mdx)("pre",null,(0,l.mdx)("code",{parentName:"pre",className:"language-python"},'class Callback:\n    def on_run_start(self, config: DictConfig, **kwargs: Any) -> None:\n        """\n        Called in RUN mode before job/application code starts. `config` is composed with overrides.\n        Some `hydra.runtime` configs are not populated yet.\n        See hydra.core.utils.run_job for more info.\n        """\n        ...\n\n    def on_run_end(self, config: DictConfig, **kwargs: Any) -> None:\n        """\n        Called in RUN mode after job/application code returns.\n        """\n        ...\n\n    def on_multirun_start(self, config: DictConfig, **kwargs: Any) -> None:\n        """\n        Called in MULTIRUN mode before any job starts.\n        When using a launcher, this will be executed on local machine before any Sweeper/Launcher is initialized.\n        """\n        ...\n\n    def on_multirun_end(self, config: DictConfig, **kwargs: Any) -> None:\n        """\n        Called in MULTIRUN mode after all jobs returns.\n        When using a launcher, this will be executed on local machine.\n        """\n        ...\n\n    def on_job_start(self, config: DictConfig, **kwargs: Any) -> None:\n        """\n        Called in both RUN and MULTIRUN modes, once for each Hydra job (before running application code).\n        This is called from within `hydra.core.utils.run_job`. In the case of remote launching, this will be executed\n        on the remote server along with your application code.\n        """\n        ...\n\n    def on_job_end(\n        self, config: DictConfig, job_return: JobReturn, **kwargs: Any\n    ) -> None:\n        """\n        Called in both RUN and MULTIRUN modes, once for each Hydra job (after running\n        application code).\n        This is called from within `hydra.core.utils.run_job`. In the case of remote launching, this will be executed\n        on the remote server after your application code.\n\n        `job_return` contains info that could be useful for logging or post-processing.\n        See hydra.core.utils.JobReturn for more.\n        """\n        ...\n\n'))),(0,l.mdx)("h3",{id:"configure-callback"},"Configure Callback"),(0,l.mdx)("p",null,"Say we have ",(0,l.mdx)("inlineCode",{parentName:"p"},"MyCallback")," so after every job ends we can upload a certain file to a"," ",(0,l.mdx)("a",{parentName:"p",href:"https://internalfb.com/sevmanager/view/3"},"S3")," ","bucket.\nFor simplicity we include this Callback class within the application, in real life you should have the\nCallback in a separate file.\nRunning the application, we can see our custom method ",(0,l.mdx)("inlineCode",{parentName:"p"},"on_job_end")," was called."),(0,l.mdx)("div",{className:"row"},(0,l.mdx)("div",{className:"col col--9"},(0,l.mdx)("pre",null,(0,l.mdx)("code",{parentName:"pre",className:"language-python",metastring:'title="my_app.py"',title:'"my_app.py"'},'class MyCallback(Callback):\n   def __init__(self, bucket: str, file_path: str) -> None:\n        self.bucket = bucket\n        self.file_path = file_path\n\n   def on_job_end(self, config: DictConfig, **kwargs: Any) -> None:\n        print(f"Job ended,uploading...")\n        # uploading...\n\n@hydra.main(config_path="conf", config_name="config")\ndef my_app(cfg: DictConfig) -> None:\n    print(OmegaConf.to_yaml(cfg))\n\n\nif __name__ == "__main__":\n    my_app()\n'))),(0,l.mdx)("div",{className:"col col--3"},(0,l.mdx)("pre",null,(0,l.mdx)("code",{parentName:"pre",className:"language-commandline",metastring:'title="output"',title:'"output"'},"\n$ python  my_app.py\nfoo: bar\n\nJob ended,uploading...\n\n\n\n\n\n\n\n\n\n\n\n")))),(0,l.mdx)("p",null,"Now let's take a look at the configurations. "),(0,l.mdx)("div",{className:"row"},(0,l.mdx)("div",{className:"col col--4"},(0,l.mdx)("pre",null,(0,l.mdx)("code",{parentName:"pre",className:"language-commandline",metastring:'title="$ tree conf"',title:'"$',tree:!0,'conf"':!0},"conf\n\u251c\u2500\u2500 config.yaml\n\u2514\u2500\u2500 hydra\n    \u2514\u2500\u2500 callbacks\n        \u2514\u2500\u2500 my_callback.yaml\n\n\n"))),(0,l.mdx)("div",{className:"col  col--3"},(0,l.mdx)("pre",null,(0,l.mdx)("code",{parentName:"pre",className:"language-commandline",metastring:'title="conf/config.yaml"',title:'"conf/config.yaml"'},"defaults:\n - /hydra/callbacks:\n    - my_callback\n\nfoo: bar\n\n\n"))),(0,l.mdx)("div",{className:"col  col--5"},(0,l.mdx)("pre",null,(0,l.mdx)("code",{parentName:"pre",className:"language-commandline",metastring:'title="conf/hydra/callbacks/my_callback.yaml"',title:'"conf/hydra/callbacks/my_callback.yaml"'},"# @package _global_\nhydra:\n  callbacks:\n    my_callback:\n      _target_: my_app.MyCallback\n      bucket: my_s3_bucket\n      file_path: ./test.pt\n")))),(0,l.mdx)("h3",{id:"callback-ordering"},"Callback ordering"),(0,l.mdx)("p",null,"The ",(0,l.mdx)("inlineCode",{parentName:"p"},"on_run_start")," or ",(0,l.mdx)("inlineCode",{parentName:"p"},"on_multirun_start")," method will get called first,\nfollowed by ",(0,l.mdx)("inlineCode",{parentName:"p"},"on_job_start")," (called once for each job).\nAfter each job ",(0,l.mdx)("inlineCode",{parentName:"p"},"on_job_end")," is called, and finally either ",(0,l.mdx)("inlineCode",{parentName:"p"},"on_run_end")," or\n",(0,l.mdx)("inlineCode",{parentName:"p"},"on_multirun_end")," is called one time before the application exits."),(0,l.mdx)("p",null,"In the ",(0,l.mdx)("inlineCode",{parentName:"p"},"hydra.callbacks")," section of your config, you can use a list to register multiple callbacks. They will be called in the final composed order for ",(0,l.mdx)("inlineCode",{parentName:"p"},"start")," events and\nin reversed order for ",(0,l.mdx)("inlineCode",{parentName:"p"},"end")," events. So, for example, suppose we have the following composed config:"),(0,l.mdx)("pre",null,(0,l.mdx)("code",{parentName:"pre",className:"language-commandline",metastring:'title="python my_app.py --cfg hydra -p hydra.callbacks"',title:'"python',"my_app.py":!0,"--cfg":!0,hydra:!0,"-p":!0,'hydra.callbacks"':!0},"# @package hydra.callbacks\nmy_callback1:\n  _target_: my_app.MyCallback1\n  param1: val1\nmy_callback2:\n  _target_: my_app.MyCallback2\n  param2: val2\n")),(0,l.mdx)("p",null,"Before each job starts, ",(0,l.mdx)("inlineCode",{parentName:"p"},"MyCallback1.on_job_start")," will get called first,\nfollowed by ",(0,l.mdx)("inlineCode",{parentName:"p"},"MyCallback2.on_job_start"),".\nAfter each job ends, ",(0,l.mdx)("inlineCode",{parentName:"p"},"MyCallback2.on_job_end")," will get called first,\nfollowed by ",(0,l.mdx)("inlineCode",{parentName:"p"},"MyCallback1.on_job_end"),"."))}u.isMDXComponent=!0},49595:(e,n,a)=>{a.d(n,{A:()=>d,C:()=>s});var t=a(58168),l=a(96540),r=a(75489),o=a(44586),i=a(48295);function c(e){const n=(0,i.ir)();return(0,o.default)().siteConfig.customFields.githubLinkVersionToBaseUrl[n?.name??"current"]+e}function d(e){return l.createElement(r.default,(0,t.A)({},e,{to:c(e.to),target:"_blank"}))}function s(e){const n=e.text??"Example (Click Here)";return l.createElement(d,e,l.createElement("span",null,"\xa0"),l.createElement("img",{src:"https://img.shields.io/badge/-"+n+"-informational",alt:"Example (Click Here)"}))}}}]);