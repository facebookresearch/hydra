"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[9858],{3276:(e,n,r)=>{r.r(n),r.d(n,{assets:()=>m,contentTitle:()=>d,default:()=>c,frontMatter:()=>o,metadata:()=>l,toc:()=>s});var a=r(58168),t=(r(96540),r(15680)),i=r(49595);const o={id:"intro",title:"Overview",sidebar_label:"Introduction"},d=void 0,l={unversionedId:"configure_hydra/intro",id:"version-1.3/configure_hydra/intro",title:"Overview",description:"Hydra is highly configurable. Many of its aspects and subsystems can be configured, including:",source:"@site/versioned_docs/version-1.3/configure_hydra/Intro.md",sourceDirName:"configure_hydra",slug:"/configure_hydra/intro",permalink:"/docs/1.3/configure_hydra/intro",draft:!1,editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/versioned_docs/version-1.3/configure_hydra/Intro.md",tags:[],version:"1.3",lastUpdatedBy:"Jasha Sommer-Simpson",lastUpdatedAt:1681935289,formattedLastUpdatedAt:"Apr 19, 2023",frontMatter:{id:"intro",title:"Overview",sidebar_label:"Introduction"},sidebar:"docs",previous:{title:"Read-only config",permalink:"/docs/1.3/patterns/write_protect_config_node"},next:{title:"Job Configuration",permalink:"/docs/1.3/configure_hydra/job"}},m={},s=[{value:"Accessing the Hydra config",id:"accessing-the-hydra-config",level:2},{value:"In your config, using the <code>hydra</code> resolver:",id:"in-your-config-using-the-hydra-resolver",level:4},{value:"In your code, using the HydraConfig singleton.",id:"in-your-code-using-the-hydraconfig-singleton",level:4},{value:"Top-level Hydra settings",id:"top-level-hydra-settings",level:3},{value:"hydra.job:",id:"hydrajob",level:3},{value:"hydra.run:",id:"hydrarun",level:3},{value:"hydra.sweep:",id:"hydrasweep",level:3},{value:"hydra.runtime:",id:"hydraruntime",level:3},{value:"hydra.overrides",id:"hydraoverrides",level:3},{value:"Resolvers provided by Hydra",id:"resolvers-provided-by-hydra",level:3}],u={toc:s},p="wrapper";function c(e){let{components:n,...r}=e;return(0,t.mdx)(p,(0,a.A)({},u,r,{components:n,mdxType:"MDXLayout"}),(0,t.mdx)("p",null,"Hydra is highly configurable. Many of its aspects and subsystems can be configured, including:"),(0,t.mdx)("ul",null,(0,t.mdx)("li",{parentName:"ul"},"The Launcher"),(0,t.mdx)("li",{parentName:"ul"},"The Sweeper"),(0,t.mdx)("li",{parentName:"ul"},"Logging"),(0,t.mdx)("li",{parentName:"ul"},"Output directory patterns"),(0,t.mdx)("li",{parentName:"ul"},"Application help (--help and --hydra-help)")),(0,t.mdx)("p",null,"The Hydra config can be customized using the same methods you are already familiar with from the tutorial.\nYou can include some Hydra config snippet in your own config to override it directly, or compose in different\nconfigurations provided by plugins or by your own code. You can also override everything in Hydra from the command\nline just like with your own configuration."),(0,t.mdx)("p",null,"The Hydra configuration itself is composed from multiple config files. here is a partial list:"),(0,t.mdx)("pre",null,(0,t.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="hydra/config"',title:'"hydra/config"'},"defaults:\n  - job_logging : default     # Job's logging config\n  - launcher: basic           # Launcher config\n  - sweeper: basic            # Sweeper config\n  - output: default           # Output directory\n")),(0,t.mdx)("p",null,"You can view the Hydra config structure ",(0,t.mdx)(i.A,{to:"hydra/conf/__init__.py",mdxType:"GithubLink"},"here"),"."),(0,t.mdx)("p",null,"You can view the Hydra config using ",(0,t.mdx)("inlineCode",{parentName:"p"},"--cfg hydra"),":"),(0,t.mdx)("details",null,(0,t.mdx)("summary",null," $ python my_app.py ",(0,t.mdx)("b",null,"--cfg hydra")," (Click to expand)"),(0,t.mdx)("pre",null,(0,t.mdx)("code",{parentName:"pre",className:"language-yaml"},"hydra:\n  run:\n    dir: outputs/${now:%Y-%m-%d}/${now:%H-%M-%S}\n  sweep:\n    dir: multirun/${now:%Y-%m-%d}/${now:%H-%M-%S}\n    subdir: ${hydra.job.num}\n  launcher:\n    _target_: hydra._internal.core_plugins.basic_launcher.BasicLauncher\n  sweeper:\n    _target_: hydra._internal.core_plugins.basic_sweeper.BasicSweeper\n    max_batch_size: null\n  hydra_logging:\n    version: 1\n    formatters:\n    ...\n"))),(0,t.mdx)("h2",{id:"accessing-the-hydra-config"},"Accessing the Hydra config"),(0,t.mdx)("p",null,"The Hydra config is large. To reduce clutter in your own config it's being deleted from the config object\nHydra is passing to the function annotated by ",(0,t.mdx)("inlineCode",{parentName:"p"},"@hydra.main()"),"."),(0,t.mdx)("p",null,"There are two ways to access the Hydra config:"),(0,t.mdx)("h4",{id:"in-your-config-using-the-hydra-resolver"},"In your config, using the ",(0,t.mdx)("inlineCode",{parentName:"h4"},"hydra")," resolver:"),(0,t.mdx)("pre",null,(0,t.mdx)("code",{parentName:"pre",className:"language-yaml"},"config_name: ${hydra:job.name}\n")),(0,t.mdx)("p",null,"Pay close attention to the syntax: The resolver name is ",(0,t.mdx)("inlineCode",{parentName:"p"},"hydra"),", and the ",(0,t.mdx)("inlineCode",{parentName:"p"},"key")," is passed after the colon."),(0,t.mdx)("h4",{id:"in-your-code-using-the-hydraconfig-singleton"},"In your code, using the HydraConfig singleton."),(0,t.mdx)("pre",null,(0,t.mdx)("code",{parentName:"pre",className:"language-python"},"from hydra.core.hydra_config import HydraConfig\n\n@hydra.main()\ndef my_app(cfg: DictConfig) -> None:\n    print(HydraConfig.get().job.name)\n")),(0,t.mdx)("h3",{id:"top-level-hydra-settings"},"Top-level Hydra settings"),(0,t.mdx)("p",null,"The following fields are present at the top level of the Hydra Config."),(0,t.mdx)("ul",null,(0,t.mdx)("li",{parentName:"ul"},"mode: Optional, one of ",(0,t.mdx)("inlineCode",{parentName:"li"},"RUN")," or ",(0,t.mdx)("inlineCode",{parentName:"li"},"MULTIRUN"),". See ",(0,t.mdx)("a",{parentName:"li",href:"/docs/1.3/tutorials/basic/running_your_app/multi-run"},"multirun")," for more info."),(0,t.mdx)("li",{parentName:"ul"},(0,t.mdx)("strong",{parentName:"li"},"searchpath"),": A list of paths that Hydra searches in order to find configs.\nSee ",(0,t.mdx)("a",{parentName:"li",href:"/docs/1.3/advanced/search_path#overriding-hydrasearchpath-config"},"overriding ",(0,t.mdx)("inlineCode",{parentName:"a"},"hydra.searchpath"))),(0,t.mdx)("li",{parentName:"ul"},(0,t.mdx)("strong",{parentName:"li"},"job_logging")," and ",(0,t.mdx)("strong",{parentName:"li"},"hydra_logging"),": Configure logging settings.\nSee ",(0,t.mdx)("a",{parentName:"li",href:"/docs/1.3/tutorials/basic/running_your_app/logging"},"logging")," and ",(0,t.mdx)("a",{parentName:"li",href:"/docs/1.3/configure_hydra/logging"},"customizing logging"),"."),(0,t.mdx)("li",{parentName:"ul"},(0,t.mdx)("strong",{parentName:"li"},"sweeper"),": ",(0,t.mdx)("a",{parentName:"li",href:"/docs/1.3/tutorials/basic/running_your_app/multi-run#sweeper"},"Sweeper")," plugin settings. Defaults to basic sweeper."),(0,t.mdx)("li",{parentName:"ul"},(0,t.mdx)("strong",{parentName:"li"},"launcher"),": ",(0,t.mdx)("a",{parentName:"li",href:"/docs/1.3/tutorials/basic/running_your_app/multi-run#launcher"},"Launcher")," plugin settings. Defaults to basic launcher."),(0,t.mdx)("li",{parentName:"ul"},(0,t.mdx)("strong",{parentName:"li"},"callbacks"),": ",(0,t.mdx)("a",{parentName:"li",href:"/docs/1.3/experimental/callbacks"},"Experimental callback support"),"."),(0,t.mdx)("li",{parentName:"ul"},(0,t.mdx)("strong",{parentName:"li"},"help"),": Configures your app's ",(0,t.mdx)("inlineCode",{parentName:"li"},"--help")," CLI flag. See ",(0,t.mdx)("a",{parentName:"li",href:"/docs/1.3/configure_hydra/app_help"},"customizing application's help"),"."),(0,t.mdx)("li",{parentName:"ul"},(0,t.mdx)("strong",{parentName:"li"},"hydra_help"),": Configures the ",(0,t.mdx)("inlineCode",{parentName:"li"},"--hydra-help")," CLI flag."),(0,t.mdx)("li",{parentName:"ul"},(0,t.mdx)("strong",{parentName:"li"},"output_subdir"),": Configures the ",(0,t.mdx)("inlineCode",{parentName:"li"},".hydra")," subdirectory name.\nSee ",(0,t.mdx)("a",{parentName:"li",href:"/docs/1.3/tutorials/basic/running_your_app/working_directory#changing-or-disabling-hydras-output-subdir"},"changing or disabling the output subdir"),"."),(0,t.mdx)("li",{parentName:"ul"},(0,t.mdx)("strong",{parentName:"li"},"verbose"),": Configures per-file DEBUG-level logging.\nSee ",(0,t.mdx)("a",{parentName:"li",href:"/docs/1.3/tutorials/basic/running_your_app/logging"},"logging"),".")),(0,t.mdx)("h3",{id:"hydrajob"},"hydra.job:"),(0,t.mdx)("p",null,"The ",(0,t.mdx)("strong",{parentName:"p"},"hydra.job")," node is used for configuring some aspects of your job.\nBelow is a short summary of the fields in ",(0,t.mdx)("strong",{parentName:"p"},"hydra.job"),".\nYou can find more details in the ",(0,t.mdx)("a",{parentName:"p",href:"/docs/1.3/configure_hydra/job"},"Job Configuration")," page."),(0,t.mdx)("p",null,"Fields under ",(0,t.mdx)("strong",{parentName:"p"},"hydra.job"),":"),(0,t.mdx)("ul",null,(0,t.mdx)("li",{parentName:"ul"},(0,t.mdx)("strong",{parentName:"li"},"name")," : Job name, defaults to the Python file name without the suffix. can be overridden."),(0,t.mdx)("li",{parentName:"ul"},(0,t.mdx)("strong",{parentName:"li"},"override_dirname")," : Pathname derived from the overrides for this job"),(0,t.mdx)("li",{parentName:"ul"},(0,t.mdx)("strong",{parentName:"li"},"chdir"),": If ",(0,t.mdx)("inlineCode",{parentName:"li"},"True"),", Hydra calls ",(0,t.mdx)("inlineCode",{parentName:"li"},"os.chdir(output_dir)")," before calling back to the user's main function.\nSee the ",(0,t.mdx)("a",{parentName:"li",href:"/docs/1.3/tutorials/basic/running_your_app/working_directory#automatically-change-current-working-dir-to-jobs-output-dir"},"Output/Working directory tutorial"),"."),(0,t.mdx)("li",{parentName:"ul"},(0,t.mdx)("strong",{parentName:"li"},"id")," : Job ID in the underlying jobs system (SLURM etc)"),(0,t.mdx)("li",{parentName:"ul"},(0,t.mdx)("strong",{parentName:"li"},"num")," : job serial number in sweep"),(0,t.mdx)("li",{parentName:"ul"},(0,t.mdx)("strong",{parentName:"li"},"config_name")," : The name of the config used by the job (Output only)"),(0,t.mdx)("li",{parentName:"ul"},(0,t.mdx)("strong",{parentName:"li"},"env_set"),": Environment variable to set for the launched job"),(0,t.mdx)("li",{parentName:"ul"},(0,t.mdx)("strong",{parentName:"li"},"env_copy"),": Environment variable to copy from the launching machine"),(0,t.mdx)("li",{parentName:"ul"},(0,t.mdx)("strong",{parentName:"li"},"config"),": fine-grained configuration for job")),(0,t.mdx)("h3",{id:"hydrarun"},"hydra.run:"),(0,t.mdx)("p",null,"Used in single-run mode (i.e. when the ",(0,t.mdx)("inlineCode",{parentName:"p"},"--multirun")," command-line flag is omitted).\nSee ",(0,t.mdx)("a",{parentName:"p",href:"/docs/1.3/configure_hydra/workdir#configuration-for-run"},"configuration for run"),"."),(0,t.mdx)("ul",null,(0,t.mdx)("li",{parentName:"ul"},(0,t.mdx)("strong",{parentName:"li"},"dir"),": used to specify the output directory.")),(0,t.mdx)("h3",{id:"hydrasweep"},"hydra.sweep:"),(0,t.mdx)("p",null,"Used in multi-run mode (i.e. when the ",(0,t.mdx)("inlineCode",{parentName:"p"},"--multirun")," command-line flag is given)\nSee ",(0,t.mdx)("a",{parentName:"p",href:"/docs/1.3/configure_hydra/workdir#configuration-for-multirun"},"configuration for multirun"),"."),(0,t.mdx)("ul",null,(0,t.mdx)("li",{parentName:"ul"},(0,t.mdx)("strong",{parentName:"li"},"dir"),": used to specify the output directory common to all jobs in the multirun sweep"),(0,t.mdx)("li",{parentName:"ul"},(0,t.mdx)("strong",{parentName:"li"},"subdir"),": used to specify the a pattern for creation of job-specific subdirectory")),(0,t.mdx)("h3",{id:"hydraruntime"},"hydra.runtime:"),(0,t.mdx)("p",null,"Fields under ",(0,t.mdx)("strong",{parentName:"p"},"hydra.runtime")," are populated automatically and should not be overridden."),(0,t.mdx)("ul",null,(0,t.mdx)("li",{parentName:"ul"},(0,t.mdx)("strong",{parentName:"li"},"version"),": Hydra's version"),(0,t.mdx)("li",{parentName:"ul"},(0,t.mdx)("strong",{parentName:"li"},"cwd"),": Original working directory the app was executed from"),(0,t.mdx)("li",{parentName:"ul"},(0,t.mdx)("strong",{parentName:"li"},"output_dir"),": This is the directory created by Hydra for saving logs and\nyaml config files, as configured by ",(0,t.mdx)("a",{parentName:"li",href:"/docs/1.3/configure_hydra/workdir"},"customizing the working directory pattern"),"."),(0,t.mdx)("li",{parentName:"ul"},(0,t.mdx)("strong",{parentName:"li"},"choices"),": A dictionary containing the final config group choices."),(0,t.mdx)("li",{parentName:"ul"},(0,t.mdx)("strong",{parentName:"li"},"config_sources"),": The final list of config sources used to compose the config.")),(0,t.mdx)("h3",{id:"hydraoverrides"},"hydra.overrides"),(0,t.mdx)("p",null,"Fields under ",(0,t.mdx)("strong",{parentName:"p"},"hydra.overrides")," are populated automatically and should not be overridden."),(0,t.mdx)("ul",null,(0,t.mdx)("li",{parentName:"ul"},(0,t.mdx)("strong",{parentName:"li"},"task"),": Contains a list of the command-line overrides used, except ",(0,t.mdx)("inlineCode",{parentName:"li"},"hydra")," config overrides.\nContains the same information as the ",(0,t.mdx)("inlineCode",{parentName:"li"},".hydra/overrides.yaml")," file.\nSee ",(0,t.mdx)("a",{parentName:"li",href:"/docs/1.3/tutorials/basic/running_your_app/working_directory"},"Output/Working directory"),"."),(0,t.mdx)("li",{parentName:"ul"},(0,t.mdx)("strong",{parentName:"li"},"hydra"),": Contains a list of the command-line ",(0,t.mdx)("inlineCode",{parentName:"li"},"hydra")," config overrides used.")),(0,t.mdx)("h3",{id:"resolvers-provided-by-hydra"},"Resolvers provided by Hydra"),(0,t.mdx)("p",null,"Hydra provides the following ",(0,t.mdx)("a",{parentName:"p",href:"https://omegaconf.readthedocs.io/en/latest/usage.html#resolvers"},"OmegaConf resolvers")," by default."),(0,t.mdx)("p",null,(0,t.mdx)("strong",{parentName:"p"},"hydra"),": Interpolates into the ",(0,t.mdx)("inlineCode",{parentName:"p"},"hydra")," config node. e.g. Use ",(0,t.mdx)("inlineCode",{parentName:"p"},"${hydra:job.name}")," to get the Hydra job name."),(0,t.mdx)("p",null,(0,t.mdx)("strong",{parentName:"p"},"now"),": Creates a string representing the current time using\n",(0,t.mdx)("a",{parentName:"p",href:"https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior"},"strftime"),".\ne.g. for formatting the time you can use something like",(0,t.mdx)("inlineCode",{parentName:"p"},"${now:%H-%M-%S}"),"."),(0,t.mdx)("p",null,(0,t.mdx)("strong",{parentName:"p"},"python_version"),": Return a string representing the runtime python version by calling ",(0,t.mdx)("inlineCode",{parentName:"p"},"sys.version_info"),".\nTakes an optional argument of a string with the values major, minor or macro.\ne.g:"),(0,t.mdx)("pre",null,(0,t.mdx)("code",{parentName:"pre",className:"language-yaml"},"default: ${python_version:}          # 3.8\nmajor:   ${python_version:major}     # 3\nminor:   ${python_version:minor}     # 3.8\nmicro:   ${python_version:micro}     # 3.8.2\n")),(0,t.mdx)("p",null,"You can learn more about OmegaConf ",(0,t.mdx)("a",{class:"external",href:"https://omegaconf.readthedocs.io/en/latest/usage.html#access-and-manipulation",target:"_blank"},"here"),"."))}c.isMDXComponent=!0},15680:(e,n,r)=>{r.r(n),r.d(n,{MDXContext:()=>m,MDXProvider:()=>p,mdx:()=>f,useMDXComponents:()=>u,withMDXComponents:()=>s});var a=r(96540);function t(e,n,r){return n in e?Object.defineProperty(e,n,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[n]=r,e}function i(){return i=Object.assign||function(e){for(var n=1;n<arguments.length;n++){var r=arguments[n];for(var a in r)Object.prototype.hasOwnProperty.call(r,a)&&(e[a]=r[a])}return e},i.apply(this,arguments)}function o(e,n){var r=Object.keys(e);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);n&&(a=a.filter((function(n){return Object.getOwnPropertyDescriptor(e,n).enumerable}))),r.push.apply(r,a)}return r}function d(e){for(var n=1;n<arguments.length;n++){var r=null!=arguments[n]?arguments[n]:{};n%2?o(Object(r),!0).forEach((function(n){t(e,n,r[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(r)):o(Object(r)).forEach((function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(r,n))}))}return e}function l(e,n){if(null==e)return{};var r,a,t=function(e,n){if(null==e)return{};var r,a,t={},i=Object.keys(e);for(a=0;a<i.length;a++)r=i[a],n.indexOf(r)>=0||(t[r]=e[r]);return t}(e,n);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);for(a=0;a<i.length;a++)r=i[a],n.indexOf(r)>=0||Object.prototype.propertyIsEnumerable.call(e,r)&&(t[r]=e[r])}return t}var m=a.createContext({}),s=function(e){return function(n){var r=u(n.components);return a.createElement(e,i({},n,{components:r}))}},u=function(e){var n=a.useContext(m),r=n;return e&&(r="function"==typeof e?e(n):d(d({},n),e)),r},p=function(e){var n=u(e.components);return a.createElement(m.Provider,{value:n},e.children)},c="mdxType",g={inlineCode:"code",wrapper:function(e){var n=e.children;return a.createElement(a.Fragment,{},n)}},h=a.forwardRef((function(e,n){var r=e.components,t=e.mdxType,i=e.originalType,o=e.parentName,m=l(e,["components","mdxType","originalType","parentName"]),s=u(r),p=t,c=s["".concat(o,".").concat(p)]||s[p]||g[p]||i;return r?a.createElement(c,d(d({ref:n},m),{},{components:r})):a.createElement(c,d({ref:n},m))}));function f(e,n){var r=arguments,t=n&&n.mdxType;if("string"==typeof e||t){var i=r.length,o=new Array(i);o[0]=h;var d={};for(var l in n)hasOwnProperty.call(n,l)&&(d[l]=n[l]);d.originalType=e,d[c]="string"==typeof e?e:t,o[1]=d;for(var m=2;m<i;m++)o[m]=r[m];return a.createElement.apply(null,o)}return a.createElement.apply(null,r)}h.displayName="MDXCreateElement"},49595:(e,n,r)=>{r.d(n,{A:()=>m,C:()=>s});var a=r(58168),t=r(96540),i=r(75489),o=r(44586),d=r(48295);function l(e){const n=(0,d.ir)();return(0,o.default)().siteConfig.customFields.githubLinkVersionToBaseUrl[n?.name??"current"]+e}function m(e){return t.createElement(i.default,(0,a.A)({},e,{to:l(e.to),target:"_blank"}))}function s(e){const n=e.text??"Example (Click Here)";return t.createElement(m,e,t.createElement("span",null,"\xa0"),t.createElement("img",{src:"https://img.shields.io/badge/-"+n+"-informational",alt:"Example (Click Here)"}))}}}]);