"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[290],{15680:(e,n,a)=>{a.r(n),a.d(n,{MDXContext:()=>m,MDXProvider:()=>u,mdx:()=>h,useMDXComponents:()=>s,withMDXComponents:()=>d});var t=a(96540);function r(e,n,a){return n in e?Object.defineProperty(e,n,{value:a,enumerable:!0,configurable:!0,writable:!0}):e[n]=a,e}function i(){return i=Object.assign||function(e){for(var n=1;n<arguments.length;n++){var a=arguments[n];for(var t in a)Object.prototype.hasOwnProperty.call(a,t)&&(e[t]=a[t])}return e},i.apply(this,arguments)}function o(e,n){var a=Object.keys(e);if(Object.getOwnPropertySymbols){var t=Object.getOwnPropertySymbols(e);n&&(t=t.filter((function(n){return Object.getOwnPropertyDescriptor(e,n).enumerable}))),a.push.apply(a,t)}return a}function p(e){for(var n=1;n<arguments.length;n++){var a=null!=arguments[n]?arguments[n]:{};n%2?o(Object(a),!0).forEach((function(n){r(e,n,a[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(a)):o(Object(a)).forEach((function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(a,n))}))}return e}function l(e,n){if(null==e)return{};var a,t,r=function(e,n){if(null==e)return{};var a,t,r={},i=Object.keys(e);for(t=0;t<i.length;t++)a=i[t],n.indexOf(a)>=0||(r[a]=e[a]);return r}(e,n);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);for(t=0;t<i.length;t++)a=i[t],n.indexOf(a)>=0||Object.prototype.propertyIsEnumerable.call(e,a)&&(r[a]=e[a])}return r}var m=t.createContext({}),d=function(e){return function(n){var a=s(n.components);return t.createElement(e,i({},n,{components:a}))}},s=function(e){var n=t.useContext(m),a=n;return e&&(a="function"==typeof e?e(n):p(p({},n),e)),a},u=function(e){var n=s(e.components);return t.createElement(m.Provider,{value:n},e.children)},c={inlineCode:"code",wrapper:function(e){var n=e.children;return t.createElement(t.Fragment,{},n)}},x=t.forwardRef((function(e,n){var a=e.components,r=e.mdxType,i=e.originalType,o=e.parentName,m=l(e,["components","mdxType","originalType","parentName"]),d=s(a),u=r,x=d["".concat(o,".").concat(u)]||d[u]||c[u]||i;return a?t.createElement(x,p(p({ref:n},m),{},{components:a})):t.createElement(x,p({ref:n},m))}));function h(e,n){var a=arguments,r=n&&n.mdxType;if("string"==typeof e||r){var i=a.length,o=new Array(i);o[0]=x;var p={};for(var l in n)hasOwnProperty.call(n,l)&&(p[l]=n[l]);p.originalType=e,p.mdxType="string"==typeof e?e:r,o[1]=p;for(var m=2;m<i;m++)o[m]=a[m];return t.createElement.apply(null,o)}return t.createElement.apply(null,a)}x.displayName="MDXCreateElement"},49595:(e,n,a)=>{a.d(n,{A:()=>l,C:()=>m});var t=a(58168),r=a(96540),i=a(75489),o=a(44586),p=a(74098);function l(e){return r.createElement(i.default,(0,t.A)({},e,{to:(n=e.to,l=(0,p.useActiveVersion)(),(0,o.default)().siteConfig.customFields.githubLinkVersionToBaseUrl[null!=(a=null==l?void 0:l.name)?a:"current"]+n),target:"_blank"}));var n,a,l}function m(e){var n,a=null!=(n=e.text)?n:"Example (Click Here)";return r.createElement(l,e,r.createElement("span",null,"\xa0"),r.createElement("img",{src:"https://img.shields.io/badge/-"+a+"-informational",alt:"Example (Click Here)"}))}},2232:(e,n,a)=>{a.r(n),a.d(n,{contentTitle:()=>d,default:()=>h,frontMatter:()=>m,metadata:()=>s,toc:()=>u});var t,r=a(58168),i=a(98587),o=(a(96540),a(15680)),p=a(49595),l=["components"],m={id:"ax_sweeper",title:"Ax Sweeper plugin",sidebar_label:"Ax Sweeper plugin"},d=void 0,s={unversionedId:"plugins/ax_sweeper",id:"plugins/ax_sweeper",title:"Ax Sweeper plugin",description:"PyPI",source:"@site/docs/plugins/ax_sweeper.md",sourceDirName:"plugins",slug:"/plugins/ax_sweeper",permalink:"/docs/plugins/ax_sweeper",editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/docs/plugins/ax_sweeper.md",tags:[],version:"current",lastUpdatedBy:"Shicong Huang",lastUpdatedAt:1726517222,formattedLastUpdatedAt:"9/16/2024",frontMatter:{id:"ax_sweeper",title:"Ax Sweeper plugin",sidebar_label:"Ax Sweeper plugin"},sidebar:"docs",previous:{title:"Submitit Launcher plugin",permalink:"/docs/plugins/submitit_launcher"},next:{title:"Nevergrad Sweeper plugin",permalink:"/docs/plugins/nevergrad_sweeper"}},u=[{value:"Installation",id:"installation",children:[],level:3},{value:"Usage",id:"usage",children:[],level:3}],c=(t="GithubLink",function(e){return console.warn("Component "+t+" was not imported, exported, or provided by MDXProvider as global scope"),(0,o.mdx)("div",e)}),x={toc:u};function h(e){var n=e.components,a=(0,i.A)(e,l);return(0,o.mdx)("wrapper",(0,r.A)({},x,a,{components:n,mdxType:"MDXLayout"}),(0,o.mdx)("p",null,(0,o.mdx)("a",{parentName:"p",href:"https://img.shields.io/pypi/v/hydra-ax-sweeper"},(0,o.mdx)("img",{parentName:"a",src:"https://img.shields.io/pypi/v/hydra-ax-sweeper",alt:"PyPI"})),"\n",(0,o.mdx)("img",{parentName:"p",src:"https://img.shields.io/pypi/l/hydra-ax-sweeper",alt:"PyPI - License"}),"\n",(0,o.mdx)("img",{parentName:"p",src:"https://img.shields.io/pypi/pyversions/hydra-ax-sweeper",alt:"PyPI - Python Version"}),"\n",(0,o.mdx)("a",{parentName:"p",href:"https://pypistats.org/packages/hydra-ax-sweeper"},(0,o.mdx)("img",{parentName:"a",src:"https://img.shields.io/pypi/dm/hydra-ax-sweeper.svg",alt:"PyPI - Downloads"})),(0,o.mdx)(p.C,{text:"Example application",to:"plugins/hydra_ax_sweeper/example",mdxType:"ExampleGithubLink"}),(0,o.mdx)(p.C,{text:"Plugin source",to:"plugins/hydra_ax_sweeper",mdxType:"ExampleGithubLink"})),(0,o.mdx)("p",null,"This plugin provides a mechanism for Hydra applications to use the ",(0,o.mdx)("a",{parentName:"p",href:"https://ax.dev/"},"Adaptive Experimentation Platform, aka Ax"),". Ax can optimize any experiment - machine learning experiments, A/B tests, and simulations."),(0,o.mdx)("h3",{id:"installation"},"Installation"),(0,o.mdx)("pre",null,(0,o.mdx)("code",{parentName:"pre",className:"language-commandline"},"pip install hydra-ax-sweeper --upgrade\n")),(0,o.mdx)("h3",{id:"usage"},"Usage"),(0,o.mdx)("p",null,"Once installed, add ",(0,o.mdx)("inlineCode",{parentName:"p"},"hydra/sweeper=ax")," to your command line. Alternatively, override ",(0,o.mdx)("inlineCode",{parentName:"p"},"hydra/sweeper")," in your config:"),(0,o.mdx)("pre",null,(0,o.mdx)("code",{parentName:"pre",className:"language-yaml"},"defaults:\n  - override hydra/sweeper: ax\n")),(0,o.mdx)("p",null,"We include an example of how to use this plugin. The file ",(0,o.mdx)(c,{to:"plugins/hydra_ax_sweeper/example/banana.py",mdxType:"GithubLink"},"example/banana.py"),"\nimplements the ",(0,o.mdx)("a",{parentName:"p",href:"https://en.wikipedia.org/wiki/Rosenbrock_function"},"Rosenbrock function (aka Banana function)"),".\nThe return value of the function should be the value that we want to optimize."),(0,o.mdx)("p",null,"To compute the best parameters for the Banana function, clone the code and run the following command in the ",(0,o.mdx)("inlineCode",{parentName:"p"},"plugins/hydra_ax_sweeper")," directory:"),(0,o.mdx)("pre",null,(0,o.mdx)("code",{parentName:"pre"},"python example/banana.py -m 'banana.x=int(interval(-5, 5))' 'banana.y=interval(-5, 10.1)'\n")),(0,o.mdx)("p",null,"The output of a run looks like:"),(0,o.mdx)("pre",null,(0,o.mdx)("code",{parentName:"pre"},"[HYDRA] AxSweeper is optimizing the following parameters:\nbanana.x: range=[-5, 5]\nbanana.y: range=[-5.0, 10.1]\nax.modelbridge.dispatch_utils: Using Bayesian Optimization generation strategy: GenerationStrategy(name='Sobol+GPEI', steps=[Sobol for 5 trials, GPEI for subsequent trials]). Iterations after 5 will take longer to generate due to model-fitting.\n[HYDRA] AxSweeper is launching 5 jobs\n[HYDRA] Launching 5 jobs locally\n[HYDRA]        #0 : banana.x=2 banana.y=-0.988\n[__main__][INFO] - Banana_Function(x=2, y=-0.988)=2488.883\n[HYDRA]        #1 : banana.x=-1 banana.y=7.701\n[__main__][INFO] - Banana_Function(x=-1, y=7.701)=4493.987\n[HYDRA]        #2 : banana.x=-1 banana.y=-3.901\n[__main__][INFO] - Banana_Function(x=-1, y=-3.901)=2406.259\n[HYDRA]        #3 : banana.x=-1 banana.y=0.209\n[__main__][INFO] - Banana_Function(x=-1, y=0.209)=66.639\n[HYDRA]        #4 : banana.x=4 banana.y=-4.557\n[__main__][INFO] - Banana_Function(x=4, y=-4.557)=42270.006\n[HYDRA] New best value: 66.639, best parameters: {'banana.x': -1, 'banana.y': 0.209}\n")),(0,o.mdx)("p",null,"In this example, we set the range of ",(0,o.mdx)("inlineCode",{parentName:"p"},"x")," parameter as an integer in the interval ",(0,o.mdx)("inlineCode",{parentName:"p"},"[-5, 5]")," and the range of ",(0,o.mdx)("inlineCode",{parentName:"p"},"y")," parameter as a float in the interval ",(0,o.mdx)("inlineCode",{parentName:"p"},"[-5, 10.1]"),". Note that in the case of ",(0,o.mdx)("inlineCode",{parentName:"p"},"x"),", we used ",(0,o.mdx)("inlineCode",{parentName:"p"},"int(interval(...))")," and hence only integers are sampled. In the case of ",(0,o.mdx)("inlineCode",{parentName:"p"},"y"),", we used ",(0,o.mdx)("inlineCode",{parentName:"p"},"interval(...)")," which refers to a floating-point interval. Other supported formats are fixed parameters (e.g.",(0,o.mdx)("inlineCode",{parentName:"p"}," banana.x=5.0"),"), choice parameters (eg ",(0,o.mdx)("inlineCode",{parentName:"p"},"banana.x=choice(1,2,3)"),") and range (eg ",(0,o.mdx)("inlineCode",{parentName:"p"},"banana.x=range(1, 10)"),"). Note that ",(0,o.mdx)("inlineCode",{parentName:"p"},"interval"),", ",(0,o.mdx)("inlineCode",{parentName:"p"},"choice")," etc. are functions provided by Hydra, and you can read more about them ",(0,o.mdx)("a",{parentName:"p",href:"/docs/advanced/override_grammar/extended"},"here"),". An important thing to remember is, use ",(0,o.mdx)("a",{parentName:"p",href:"/docs/advanced/override_grammar/extended#interval-sweep"},(0,o.mdx)("inlineCode",{parentName:"a"},"interval"))," when we want Ax to sample values from an interval. ",(0,o.mdx)("a",{parentName:"p",href:"https://ax.dev/api/ax.html#ax.RangeParameter"},(0,o.mdx)("inlineCode",{parentName:"a"},"RangeParameter"))," in Ax is equivalent to ",(0,o.mdx)("inlineCode",{parentName:"p"},"interval")," in Hydra. Remember to use ",(0,o.mdx)("inlineCode",{parentName:"p"},"int(interval(...))")," if you want to sample only integer points from the interval. ",(0,o.mdx)("a",{parentName:"p",href:"/docs/advanced/override_grammar/extended#range-sweep"},(0,o.mdx)("inlineCode",{parentName:"a"},"range"))," can be used as an alternate way of specifying choice parameters. For example ",(0,o.mdx)("inlineCode",{parentName:"p"},"python example/banana.py -m banana.x=choice(1, 2, 3, 4)")," is equivalent to ",(0,o.mdx)("inlineCode",{parentName:"p"},"python example/banana.py -m banana.x=range(1, 5)"),"."),(0,o.mdx)("p",null,"The values of the ",(0,o.mdx)("inlineCode",{parentName:"p"},"x")," and ",(0,o.mdx)("inlineCode",{parentName:"p"},"y")," parameters can also be set using the config file ",(0,o.mdx)("inlineCode",{parentName:"p"},"plugins/hydra_ax_sweeper/example/conf/config.yaml"),". For instance, the configuration corresponding to the commandline arguments is as follows:"),(0,o.mdx)("pre",null,(0,o.mdx)("code",{parentName:"pre"},"banana.x:\n type: range\n bounds: [-5, 5]\n\nbanana.y:\n type: range\n bounds: [-5, 10.1]\n")),(0,o.mdx)("p",null,"To sample in log space, you can tag the commandline override with ",(0,o.mdx)("inlineCode",{parentName:"p"},"log"),". E.g. ",(0,o.mdx)("inlineCode",{parentName:"p"},"python example/banana.py -m banana.x=tag(log, interval(1, 1000))"),". You can set ",(0,o.mdx)("inlineCode",{parentName:"p"},"log_scale: true")," in the input config to achieve the same."),(0,o.mdx)("pre",null,(0,o.mdx)("code",{parentName:"pre"},"banana.z:\n type: range\n bounds: [1, 100]\n log_scale: true\n")),(0,o.mdx)("p",null,"In general, the plugin supports setting all the Ax supported ",(0,o.mdx)("a",{parentName:"p",href:"https://ax.dev/api/core.html?highlight=range#module-ax.core.parameter"},"Parameters")," in the config. According to the ",(0,o.mdx)("a",{parentName:"p",href:"https://ax.dev/api/service.html#ax.service.ax_client.AxClient.create_experiment"},"Ax documentation"),", the required elements in the config are:"),(0,o.mdx)("ul",null,(0,o.mdx)("li",{parentName:"ul"},(0,o.mdx)("inlineCode",{parentName:"li"},"name")," - Name of the parameter. It is of type string."),(0,o.mdx)("li",{parentName:"ul"},(0,o.mdx)("inlineCode",{parentName:"li"},"type")," - Type of the parameter. It can take the following values: ",(0,o.mdx)("inlineCode",{parentName:"li"},"range"),", ",(0,o.mdx)("inlineCode",{parentName:"li"},"fixed"),", or ",(0,o.mdx)("inlineCode",{parentName:"li"},"choice"),"."),(0,o.mdx)("li",{parentName:"ul"},(0,o.mdx)("inlineCode",{parentName:"li"},"bounds")," - Required only for the ",(0,o.mdx)("inlineCode",{parentName:"li"},"range")," parameters. It should be a list of two values, with the lower bound first."),(0,o.mdx)("li",{parentName:"ul"},(0,o.mdx)("inlineCode",{parentName:"li"},"values")," - Required only for the ",(0,o.mdx)("inlineCode",{parentName:"li"},"choice")," parameters. It should be a list of values."),(0,o.mdx)("li",{parentName:"ul"},(0,o.mdx)("inlineCode",{parentName:"li"},"value")," - Required only for the ",(0,o.mdx)("inlineCode",{parentName:"li"},"fixed")," parameters. It should be a single value.")),(0,o.mdx)("p",null,"Note that if you want to sample integers in the range ",(0,o.mdx)("inlineCode",{parentName:"p"},"-5")," to ",(0,o.mdx)("inlineCode",{parentName:"p"},"5"),", you need to specify the range as ",(0,o.mdx)("inlineCode",{parentName:"p"},"int(interval(-5, 5))")," (in the command line) or ",(0,o.mdx)("inlineCode",{parentName:"p"},"[-5, 5]")," (in config). If you want to sample floats in range ",(0,o.mdx)("inlineCode",{parentName:"p"},"-5")," to ",(0,o.mdx)("inlineCode",{parentName:"p"},"5"),", you need to specify the range as ",(0,o.mdx)("inlineCode",{parentName:"p"},"interval(-5, 5)")," (in the command line) or ",(0,o.mdx)("inlineCode",{parentName:"p"},"[-5.0, 5.0]")," (in config)."),(0,o.mdx)("p",null,"The Ax Sweeper assumes the optimized function is a noisy function with unknown measurement uncertainty.\nThis can be changed by overriding the ",(0,o.mdx)("inlineCode",{parentName:"p"},"is_noisy")," parameter to False, which specifies that each measurement is exact, i.e., each measurement has a measurement uncertainty of zero."),(0,o.mdx)("p",null,"If measurement uncertainty is known or can be estimated (e.g., via a heuristic or via the ",(0,o.mdx)("a",{parentName:"p",href:"https://en.wikipedia.org/wiki/Standard_error"},"standard error of the mean")," of repeated measurements), the measurement function can return the tuple ",(0,o.mdx)("inlineCode",{parentName:"p"},"(measurement_value, measurement_uncertainty)")," instead of a scalar value."),(0,o.mdx)("p",null,"The parameters for the optimization process can also be set in the config file. Specifying the Ax config is optional. You can discover the Ax Sweeper parameters with:"),(0,o.mdx)("pre",null,(0,o.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="$ python your_app.py hydra/sweeper=ax --cfg hydra -p hydra.sweeper"',title:'"$',python:!0,"your_app.py":!0,"hydra/sweeper":"ax","--cfg":!0,hydra:!0,"-p":!0,'hydra.sweeper"':!0},"# @package hydra.sweeper\n_target_: hydra_plugins.hydra_ax_sweeper.ax_sweeper.AxSweeper\nmax_batch_size: null\nax_config:\n  max_trials: 10\n  early_stop:\n    minimize: true\n    max_epochs_without_improvement: 10\n    epsilon: 1.0e-05\n  experiment:\n    name: null\n    objective_name: objective\n    minimize: true\n    parameter_constraints: null\n    outcome_constraints: null\n    status_quo: null\n  client:\n    verbose_logging: false\n    random_seed: null\n  is_noisy: true\n  params: {}\n")),(0,o.mdx)("p",null,"There are several standard approaches for configuring plugins. Check ",(0,o.mdx)("a",{parentName:"p",href:"/docs/patterns/configuring_plugins"},"this page")," for more information."))}h.isMDXComponent=!0}}]);