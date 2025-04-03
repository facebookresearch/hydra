"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[9659],{15680:(e,r,t)=>{t.r(r),t.d(r,{MDXContext:()=>p,MDXProvider:()=>s,mdx:()=>h,useMDXComponents:()=>c,withMDXComponents:()=>l});var n=t(96540);function o(e,r,t){return r in e?Object.defineProperty(e,r,{value:t,enumerable:!0,configurable:!0,writable:!0}):e[r]=t,e}function i(){return i=Object.assign||function(e){for(var r=1;r<arguments.length;r++){var t=arguments[r];for(var n in t)Object.prototype.hasOwnProperty.call(t,n)&&(e[n]=t[n])}return e},i.apply(this,arguments)}function a(e,r){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);r&&(n=n.filter((function(r){return Object.getOwnPropertyDescriptor(e,r).enumerable}))),t.push.apply(t,n)}return t}function d(e){for(var r=1;r<arguments.length;r++){var t=null!=arguments[r]?arguments[r]:{};r%2?a(Object(t),!0).forEach((function(r){o(e,r,t[r])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):a(Object(t)).forEach((function(r){Object.defineProperty(e,r,Object.getOwnPropertyDescriptor(t,r))}))}return e}function u(e,r){if(null==e)return{};var t,n,o=function(e,r){if(null==e)return{};var t,n,o={},i=Object.keys(e);for(n=0;n<i.length;n++)t=i[n],r.indexOf(t)>=0||(o[t]=e[t]);return o}(e,r);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);for(n=0;n<i.length;n++)t=i[n],r.indexOf(t)>=0||Object.prototype.propertyIsEnumerable.call(e,t)&&(o[t]=e[t])}return o}var p=n.createContext({}),l=function(e){return function(r){var t=c(r.components);return n.createElement(e,i({},r,{components:t}))}},c=function(e){var r=n.useContext(p),t=r;return e&&(t="function"==typeof e?e(r):d(d({},r),e)),t},s=function(e){var r=c(e.components);return n.createElement(p.Provider,{value:r},e.children)},m="mdxType",y={inlineCode:"code",wrapper:function(e){var r=e.children;return n.createElement(n.Fragment,{},r)}},g=n.forwardRef((function(e,r){var t=e.components,o=e.mdxType,i=e.originalType,a=e.parentName,p=u(e,["components","mdxType","originalType","parentName"]),l=c(t),s=o,m=l["".concat(a,".").concat(s)]||l[s]||y[s]||i;return t?n.createElement(m,d(d({ref:r},p),{},{components:t})):n.createElement(m,d({ref:r},p))}));function h(e,r){var t=arguments,o=r&&r.mdxType;if("string"==typeof e||o){var i=t.length,a=new Array(i);a[0]=g;var d={};for(var u in r)hasOwnProperty.call(r,u)&&(d[u]=r[u]);d.originalType=e,d[m]="string"==typeof e?e:o,a[1]=d;for(var p=2;p<i;p++)a[p]=t[p];return n.createElement.apply(null,a)}return n.createElement.apply(null,t)}g.displayName="MDXCreateElement"},33279:(e,r,t)=>{t.r(r),t.d(r,{assets:()=>p,contentTitle:()=>d,default:()=>m,frontMatter:()=>a,metadata:()=>u,toc:()=>l});var n=t(58168),o=(t(96540),t(15680)),i=t(49595);const a={id:"working_directory",title:"Output/Working directory",sidebar_label:"Output/Working directory"},d=void 0,u={unversionedId:"tutorials/basic/running_your_app/working_directory",id:"version-1.2/tutorials/basic/running_your_app/working_directory",title:"Output/Working directory",description:"Hydra can solve the problem of your needing to specify a new output directory for each run, by",source:"@site/versioned_docs/version-1.2/tutorials/basic/running_your_app/3_working_directory.md",sourceDirName:"tutorials/basic/running_your_app",slug:"/tutorials/basic/running_your_app/working_directory",permalink:"/docs/1.2/tutorials/basic/running_your_app/working_directory",draft:!1,editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/versioned_docs/version-1.2/tutorials/basic/running_your_app/3_working_directory.md",tags:[],version:"1.2",lastUpdatedBy:"dependabot[bot]",lastUpdatedAt:1743717584,formattedLastUpdatedAt:"Apr 3, 2025",sidebarPosition:3,frontMatter:{id:"working_directory",title:"Output/Working directory",sidebar_label:"Output/Working directory"},sidebar:"docs",previous:{title:"Multi-run",permalink:"/docs/1.2/tutorials/basic/running_your_app/multi-run"},next:{title:"Logging",permalink:"/docs/1.2/tutorials/basic/running_your_app/logging"}},p={},l=[{value:"Automatically change current working dir to job&#39;s output dir",id:"automatically-change-current-working-dir-to-jobs-output-dir",level:3},{value:"Changing or disabling Hydra&#39;s output subdir",id:"changing-or-disabling-hydras-output-subdir",level:3},{value:"Accessing the original working directory in your application",id:"accessing-the-original-working-directory-in-your-application",level:3}],c={toc:l},s="wrapper";function m(e){let{components:r,...t}=e;return(0,o.mdx)(s,(0,n.A)({},c,t,{components:r,mdxType:"MDXLayout"}),(0,o.mdx)(i.C,{to:"examples/tutorials/basic/running_your_hydra_app/3_working_directory",mdxType:"ExampleGithubLink"}),(0,o.mdx)("p",null,"Hydra can solve the problem of your needing to specify a new output directory for each run, by\ncreating a directory for each run and executing your code within that output directory.\nBy default, this output directory is used to store Hydra output for the run (Configuration, Logs etc)."),(0,o.mdx)("p",null,"Every time you run the app, a new output directory is created.\nYou can retrieve the path of the output directy by\n",(0,o.mdx)("a",{parentName:"p",href:"/docs/1.2/configure_hydra/intro#accessing-the-hydra-config"},"inspecting the Hydra config")," as in the example below."),(0,o.mdx)("pre",null,(0,o.mdx)("code",{parentName:"pre",className:"language-python",metastring:'title="my_app.py"',title:'"my_app.py"'},'import os\nfrom omegaconf import DictConfig\nimport hydra\n\n@hydra.main(version_base=None)\ndef my_app(_cfg: DictConfig) -> None:\n    print(f"Working directory : {os.getcwd()}")\n    print(f"Output directory  : {hydra.core.hydra_config.HydraConfig.get().runtime.output_dir}")\n')),(0,o.mdx)("pre",null,(0,o.mdx)("code",{parentName:"pre",className:"language-text"},"$ python my_app.py\nWorking directory : /home/omry/dev/hydra\nOutput directory  : /home/omry/dev/hydra/outputs/2019-09-25/15-16-17\n\n$ python my_app.py\nWorking directory : /home/omry/dev/hydra\nOutput directory  : /home/omry/dev/hydra/outputs/2019-09-25/15-16-19\n")),(0,o.mdx)("p",null,"Let's take a look at one of the output directories:"),(0,o.mdx)("pre",null,(0,o.mdx)("code",{parentName:"pre",className:"language-text"},"$ tree outputs/2019-09-25/15-16-17\noutputs/2019-09-25/15-16-17\n\u251c\u2500\u2500 .hydra\n\u2502   \u251c\u2500\u2500 config.yaml\n\u2502   \u251c\u2500\u2500 hydra.yaml\n\u2502   \u2514\u2500\u2500 overrides.yaml\n\u2514\u2500\u2500 my_app.log\n")),(0,o.mdx)("p",null,"We have the Hydra output directory (",(0,o.mdx)("inlineCode",{parentName:"p"},".hydra")," by default), and the application log file.\nInside the Hydra output directory we have:"),(0,o.mdx)("ul",null,(0,o.mdx)("li",{parentName:"ul"},(0,o.mdx)("inlineCode",{parentName:"li"},"config.yaml"),": A dump of the user specified configuration"),(0,o.mdx)("li",{parentName:"ul"},(0,o.mdx)("inlineCode",{parentName:"li"},"hydra.yaml"),": A dump of the Hydra configuration"),(0,o.mdx)("li",{parentName:"ul"},(0,o.mdx)("inlineCode",{parentName:"li"},"overrides.yaml"),": The command line overrides used")),(0,o.mdx)("p",null,"And in the main output directory:"),(0,o.mdx)("ul",null,(0,o.mdx)("li",{parentName:"ul"},(0,o.mdx)("inlineCode",{parentName:"li"},"my_app.log"),": A log file created for this run")),(0,o.mdx)("p",null,"You can configure the name of the output directory using\nthe ",(0,o.mdx)("a",{parentName:"p",href:"/docs/1.2/configure_hydra/workdir"},"customizing the working directory")," pattern."),(0,o.mdx)("h3",{id:"automatically-change-current-working-dir-to-jobs-output-dir"},"Automatically change current working dir to job's output dir"),(0,o.mdx)("p",null,"By setting ",(0,o.mdx)("inlineCode",{parentName:"p"},"hydra.job.chdir=True"),", you can configure\nHydra's ",(0,o.mdx)("inlineCode",{parentName:"p"},"@hydra.main")," decorator to change python's working directory by calling\n",(0,o.mdx)("inlineCode",{parentName:"p"},"os.chdir")," before passing control to the user's decorated main function.\nAs of Hydra v1.2, ",(0,o.mdx)("inlineCode",{parentName:"p"},"hydra.job.chdir")," defaults to ",(0,o.mdx)("inlineCode",{parentName:"p"},"False"),".\nSetting ",(0,o.mdx)("inlineCode",{parentName:"p"},"hydra.job.chdir=True")," enables convenient use of the output directory to\nstore output for the application (For example, a database dump file)."),(0,o.mdx)("pre",null,(0,o.mdx)("code",{parentName:"pre",className:"language-bash"},"# check current working dir\n$ pwd\n/home/jasha/dev/hydra\n\n# for Hydra >= 1.2, working dir remains unchanged by default\n$ python my_app.py\nWorking directory : /home/jasha/dev/hydra\nOutput directory  : /home/jasha/dev/hydra/outputs/2023-04-18/13-43-24\n\n# working dir changed to output dir\n$ python my_app.py hydra.job.chdir=True\nWorking directory : /home/jasha/dev/hydra/outputs/2023-04-18/13-43-17\nOutput directory  : /home/jasha/dev/hydra/outputs/2023-04-18/13-43-17\n\n# output dir and files are still created even if `chdir` is disabled:\n$ tree -a outputs/2023-04-18/13-43-24/\noutputs/2023-04-18/13-43-24/\n\u251c\u2500\u2500 .hydra\n\u2502\xa0\xa0 \u251c\u2500\u2500 config.yaml\n\u2502\xa0\xa0 \u251c\u2500\u2500 hydra.yaml\n\u2502\xa0\xa0 \u2514\u2500\u2500 overrides.yaml\n\u2514\u2500\u2500 my_app.log\n")),(0,o.mdx)("h3",{id:"changing-or-disabling-hydras-output-subdir"},"Changing or disabling Hydra's output subdir"),(0,o.mdx)("p",null,"You can change the ",(0,o.mdx)("inlineCode",{parentName:"p"},".hydra")," subdirectory name by overriding ",(0,o.mdx)("inlineCode",{parentName:"p"},"hydra.output_subdir"),".\nYou can disable its creation by overriding ",(0,o.mdx)("inlineCode",{parentName:"p"},"hydra.output_subdir")," to ",(0,o.mdx)("inlineCode",{parentName:"p"},"null"),"."),(0,o.mdx)("h3",{id:"accessing-the-original-working-directory-in-your-application"},"Accessing the original working directory in your application"),(0,o.mdx)("p",null,"With ",(0,o.mdx)("inlineCode",{parentName:"p"},"hydra.job.chdir=True"),", you can still access the original working directory by importing ",(0,o.mdx)("inlineCode",{parentName:"p"},"get_original_cwd()")," and ",(0,o.mdx)("inlineCode",{parentName:"p"},"to_absolute_path()")," in ",(0,o.mdx)("inlineCode",{parentName:"p"},"hydra.utils"),":"),(0,o.mdx)("pre",null,(0,o.mdx)("code",{parentName:"pre",className:"language-python"},'from hydra.utils import get_original_cwd, to_absolute_path\n\n@hydra.main(version_base=None)\ndef my_app(_cfg: DictConfig) -> None:\n    print(f"Current working directory : {os.getcwd()}")\n    print(f"Orig working directory    : {get_original_cwd()}")\n    print(f"to_absolute_path(\'foo\')   : {to_absolute_path(\'foo\')}")\n    print(f"to_absolute_path(\'/foo\')  : {to_absolute_path(\'/foo\')}")\n\nif __name__ == "__main__":\n    my_app()\n')),(0,o.mdx)("pre",null,(0,o.mdx)("code",{parentName:"pre",className:"language-text",metastring:'title="$ python examples/tutorial/8_working_directory/original_cwd.py"',title:'"$',python:!0,'examples/tutorial/8_working_directory/original_cwd.py"':!0},"Current working directory  : /Users/omry/dev/hydra/outputs/2019-10-23/10-53-03\nOriginal working directory : /Users/omry/dev/hydra\nto_absolute_path('foo')    : /Users/omry/dev/hydra/foo\nto_absolute_path('/foo')   : /foo\n")),(0,o.mdx)("p",null,"The name of the generated working directories can be ",(0,o.mdx)("a",{parentName:"p",href:"/docs/1.2/configure_hydra/workdir"},"customized"),"."))}m.isMDXComponent=!0},49595:(e,r,t)=>{t.d(r,{A:()=>p,C:()=>l});var n=t(58168),o=t(96540),i=t(75489),a=t(44586),d=t(48295);function u(e){const r=(0,d.ir)();return(0,a.default)().siteConfig.customFields.githubLinkVersionToBaseUrl[r?.name??"current"]+e}function p(e){return o.createElement(i.default,(0,n.A)({},e,{to:u(e.to),target:"_blank"}))}function l(e){const r=e.text??"Example (Click Here)";return o.createElement(p,e,o.createElement("span",null,"\xa0"),o.createElement("img",{src:"https://img.shields.io/badge/-"+r+"-informational",alt:"Example (Click Here)"}))}}}]);