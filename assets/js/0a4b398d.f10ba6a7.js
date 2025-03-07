"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[5908],{15680:(e,n,t)=>{t.r(n),t.d(n,{MDXContext:()=>s,MDXProvider:()=>u,mdx:()=>h,useMDXComponents:()=>c,withMDXComponents:()=>m});var r=t(96540);function a(e,n,t){return n in e?Object.defineProperty(e,n,{value:t,enumerable:!0,configurable:!0,writable:!0}):e[n]=t,e}function i(){return i=Object.assign||function(e){for(var n=1;n<arguments.length;n++){var t=arguments[n];for(var r in t)Object.prototype.hasOwnProperty.call(t,r)&&(e[r]=t[r])}return e},i.apply(this,arguments)}function o(e,n){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);n&&(r=r.filter((function(n){return Object.getOwnPropertyDescriptor(e,n).enumerable}))),t.push.apply(t,r)}return t}function l(e){for(var n=1;n<arguments.length;n++){var t=null!=arguments[n]?arguments[n]:{};n%2?o(Object(t),!0).forEach((function(n){a(e,n,t[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):o(Object(t)).forEach((function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(t,n))}))}return e}function p(e,n){if(null==e)return{};var t,r,a=function(e,n){if(null==e)return{};var t,r,a={},i=Object.keys(e);for(r=0;r<i.length;r++)t=i[r],n.indexOf(t)>=0||(a[t]=e[t]);return a}(e,n);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);for(r=0;r<i.length;r++)t=i[r],n.indexOf(t)>=0||Object.prototype.propertyIsEnumerable.call(e,t)&&(a[t]=e[t])}return a}var s=r.createContext({}),m=function(e){return function(n){var t=c(n.components);return r.createElement(e,i({},n,{components:t}))}},c=function(e){var n=r.useContext(s),t=n;return e&&(t="function"==typeof e?e(n):l(l({},n),e)),t},u=function(e){var n=c(e.components);return r.createElement(s.Provider,{value:n},e.children)},d="mdxType",f={inlineCode:"code",wrapper:function(e){var n=e.children;return r.createElement(r.Fragment,{},n)}},g=r.forwardRef((function(e,n){var t=e.components,a=e.mdxType,i=e.originalType,o=e.parentName,s=p(e,["components","mdxType","originalType","parentName"]),m=c(t),u=a,d=m["".concat(o,".").concat(u)]||m[u]||f[u]||i;return t?r.createElement(d,l(l({ref:n},s),{},{components:t})):r.createElement(d,l({ref:n},s))}));function h(e,n){var t=arguments,a=n&&n.mdxType;if("string"==typeof e||a){var i=t.length,o=new Array(i);o[0]=g;var l={};for(var p in n)hasOwnProperty.call(n,p)&&(l[p]=n[p]);l.originalType=e,l[d]="string"==typeof e?e:a,o[1]=l;for(var s=2;s<i;s++)o[s]=t[s];return r.createElement.apply(null,o)}return r.createElement.apply(null,t)}g.displayName="MDXCreateElement"},49595:(e,n,t)=>{t.d(n,{A:()=>s,C:()=>m});var r=t(58168),a=t(96540),i=t(75489),o=t(44586),l=t(48295);function p(e){const n=(0,l.ir)();return(0,o.default)().siteConfig.customFields.githubLinkVersionToBaseUrl[n?.name??"current"]+e}function s(e){return a.createElement(i.default,(0,r.A)({},e,{to:p(e.to),target:"_blank"}))}function m(e){const n=e.text??"Example (Click Here)";return a.createElement(s,e,a.createElement("span",null,"\xa0"),a.createElement("img",{src:"https://img.shields.io/badge/-"+n+"-informational",alt:"Example (Click Here)"}))}},52699:(e,n,t)=>{t.r(n),t.d(n,{assets:()=>s,contentTitle:()=>l,default:()=>d,frontMatter:()=>o,metadata:()=>p,toc:()=>m});var r=t(58168),a=(t(96540),t(15680)),i=t(49595);const o={id:"rerun",title:"Re-run a job from previous config",sidebar_label:"Re-run"},l=void 0,p={unversionedId:"experimental/rerun",id:"experimental/rerun",title:"Re-run a job from previous config",description:"This is an experimental feature. Please read through this page to understand what is supported.",source:"@site/docs/experimental/rerun.md",sourceDirName:"experimental",slug:"/experimental/rerun",permalink:"/docs/experimental/rerun",draft:!1,editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/docs/experimental/rerun.md",tags:[],version:"current",lastUpdatedBy:"Jasha Sommer-Simpson",lastUpdatedAt:1671904059,formattedLastUpdatedAt:"Dec 24, 2022",frontMatter:{id:"rerun",title:"Re-run a job from previous config",sidebar_label:"Re-run"},sidebar:"docs",previous:{title:"Callbacks",permalink:"/docs/experimental/callbacks"},next:{title:"Developer Guide Overview",permalink:"/docs/development/overview"}},s={},m=[{value:"Important Notes",id:"important-notes",level:3}],c={toc:m},u="wrapper";function d(e){let{components:n,...t}=e;return(0,a.mdx)(u,(0,r.A)({},c,t,{components:n,mdxType:"MDXLayout"}),(0,a.mdx)(i.C,{text:"Example application",to:"examples/experimental/rerun",mdxType:"ExampleGithubLink"}),(0,a.mdx)("admonition",{type:"caution"},(0,a.mdx)("p",{parentName:"admonition"},"This is an experimental feature. Please read through this page to understand what is supported.")),(0,a.mdx)("p",null,"We use the example app linked above for demonstration. To save the configs for re-run, first use the experimental\nHydra Callback for saving the job info:"),(0,a.mdx)("pre",null,(0,a.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="config.yaml"',title:'"config.yaml"'},"hydra:\n  callbacks:\n    save_job_info:\n      _target_: hydra.experimental.callbacks.PickleJobInfoCallback\n")),(0,a.mdx)("pre",null,(0,a.mdx)("code",{parentName:"pre",className:"language-python",metastring:'title="Example function"',title:'"Example','function"':!0},'@hydra.main(version_base=None, config_path=".", config_name="config")\ndef my_app(cfg: DictConfig) -> None:\n    log.info(f"output_dir={HydraConfig.get().runtime.output_dir}")\n    log.info(f"cfg.foo={cfg.foo}")\n')),(0,a.mdx)("p",null,"Run the example app:"),(0,a.mdx)("pre",null,(0,a.mdx)("code",{parentName:"pre",className:"language-commandline"},"$ python my_app.py\n[2022-03-16 14:51:30,905][hydra.experimental.pickle_job_info_callback][INFO] - Saving job configs in /Users/jieru/workspace/hydra/examples/experimental/outputs/2022-03-16/14-51-30/.hydra/config.pickle\n[2022-03-16 14:51:30,906][__main__][INFO] - Output_dir=/Users/jieru/workspace/hydra/examples/experimental/outputs/2022-03-16/14-51-30\n[2022-03-16 14:51:30,906][__main__][INFO] - cfg.foo=bar\n[2022-03-16 14:51:30,906][hydra.experimental.pickle_job_info_callback][INFO] - Saving job_return in /Users/jieru/workspace/hydra/examples/experimental/outputs/2022-03-16/14-51-30/.hydra/job_return.pickle\n")),(0,a.mdx)("p",null,"The Callback saves ",(0,a.mdx)("inlineCode",{parentName:"p"},"config.pickle")," in ",(0,a.mdx)("inlineCode",{parentName:"p"},".hydra")," sub dir, this is what we will use for rerun."),(0,a.mdx)("p",null,"Now rerun the app"),(0,a.mdx)("pre",null,(0,a.mdx)("code",{parentName:"pre",className:"language-commandline"},"$ OUTPUT_DIR=/Users/jieru/workspace/hydra/examples/experimental/outputs/2022-03-16/14-51-30/.hydra/\n$ python my_app.py --experimental-rerun $OUTPUT_DIR/config.pickle\n/Users/jieru/workspace/hydra/hydra/main.py:23: UserWarning: Experimental rerun CLI option.\n  warnings.warn(msg, UserWarning)\n[2022-03-16 14:59:21,666][__main__][INFO] - Output_dir=/Users/jieru/workspace/hydra/examples/experimental/outputs/2022-03-16/14-51-30\n[2022-03-16 14:59:21,666][__main__][INFO] - cfg.foo=bar\n")),(0,a.mdx)("p",null,"You will notice ",(0,a.mdx)("inlineCode",{parentName:"p"},"my_app.log")," is updated with the logging from the second run, but Callbacks are not called this time. Read on to learn more."),(0,a.mdx)("h3",{id:"important-notes"},"Important Notes"),(0,a.mdx)("p",null,"This is an experimental feature. Please reach out if you have any question. "),(0,a.mdx)("ul",null,(0,a.mdx)("li",{parentName:"ul"},"Only single run is supported."),(0,a.mdx)("li",{parentName:"ul"},(0,a.mdx)("inlineCode",{parentName:"li"},"--experimental-rerun")," cannot be used with other command-line options or overrides. They will simply be ignored."),(0,a.mdx)("li",{parentName:"ul"},"Rerun passes in a cfg_passthrough directly to your application, this means except for logging, no other ",(0,a.mdx)("inlineCode",{parentName:"li"},"hydra.main"),"\nfunctions are called (such as change working dir, or calling callbacks.) "),(0,a.mdx)("li",{parentName:"ul"},"The configs are preserved and reconstructed to the best efforts. Meaning we can only guarantee that the ",(0,a.mdx)("inlineCode",{parentName:"li"},"cfg")," object\nitself passed in by ",(0,a.mdx)("inlineCode",{parentName:"li"},"hydra.main")," stays the same across runs. However, configs are resolved lazily. Meaning we cannot\nguarantee your application will behave the same if your application resolves configs during run time. In the following example,\n",(0,a.mdx)("inlineCode",{parentName:"li"},"cfg.time_now")," will resolve to different value every run.")),(0,a.mdx)("div",{className:"row"},(0,a.mdx)("div",{className:"col  col--5"},(0,a.mdx)("pre",null,(0,a.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="config.yaml"',title:'"config.yaml"'},"time_now: ${now:%H-%M-%S}\n\n\n\n"))),(0,a.mdx)("div",{className:"col col--7"},(0,a.mdx)("pre",null,(0,a.mdx)("code",{parentName:"pre",className:"language-python",metastring:'title="Example function"',title:'"Example','function"':!0},'@hydra.main(version_base=None, config_path=".", config_name="config")\ndef my_app(cfg: DictConfig) -> None:\n    val = cfg.time_now\n    # the rest of the application\n')))))}d.isMDXComponent=!0}}]);