"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[1948],{15680:(e,a,r)=>{r.r(a),r.d(a,{MDXContext:()=>d,MDXProvider:()=>p,mdx:()=>y,useMDXComponents:()=>m,withMDXComponents:()=>u});var n=r(96540);function t(e,a,r){return a in e?Object.defineProperty(e,a,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[a]=r,e}function i(){return i=Object.assign||function(e){for(var a=1;a<arguments.length;a++){var r=arguments[a];for(var n in r)Object.prototype.hasOwnProperty.call(r,n)&&(e[n]=r[n])}return e},i.apply(this,arguments)}function l(e,a){var r=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);a&&(n=n.filter((function(a){return Object.getOwnPropertyDescriptor(e,a).enumerable}))),r.push.apply(r,n)}return r}function o(e){for(var a=1;a<arguments.length;a++){var r=null!=arguments[a]?arguments[a]:{};a%2?l(Object(r),!0).forEach((function(a){t(e,a,r[a])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(r)):l(Object(r)).forEach((function(a){Object.defineProperty(e,a,Object.getOwnPropertyDescriptor(r,a))}))}return e}function s(e,a){if(null==e)return{};var r,n,t=function(e,a){if(null==e)return{};var r,n,t={},i=Object.keys(e);for(n=0;n<i.length;n++)r=i[n],a.indexOf(r)>=0||(t[r]=e[r]);return t}(e,a);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);for(n=0;n<i.length;n++)r=i[n],a.indexOf(r)>=0||Object.prototype.propertyIsEnumerable.call(e,r)&&(t[r]=e[r])}return t}var d=n.createContext({}),u=function(e){return function(a){var r=m(a.components);return n.createElement(e,i({},a,{components:r}))}},m=function(e){var a=n.useContext(d),r=a;return e&&(r="function"==typeof e?e(a):o(o({},a),e)),r},p=function(e){var a=m(e.components);return n.createElement(d.Provider,{value:a},e.children)},c="mdxType",h={inlineCode:"code",wrapper:function(e){var a=e.children;return n.createElement(n.Fragment,{},a)}},f=n.forwardRef((function(e,a){var r=e.components,t=e.mdxType,i=e.originalType,l=e.parentName,d=s(e,["components","mdxType","originalType","parentName"]),u=m(r),p=t,c=u["".concat(l,".").concat(p)]||u[p]||h[p]||i;return r?n.createElement(c,o(o({ref:a},d),{},{components:r})):n.createElement(c,o({ref:a},d))}));function y(e,a){var r=arguments,t=a&&a.mdxType;if("string"==typeof e||t){var i=r.length,l=new Array(i);l[0]=f;var o={};for(var s in a)hasOwnProperty.call(a,s)&&(o[s]=a[s]);o.originalType=e,o[c]="string"==typeof e?e:t,l[1]=o;for(var d=2;d<i;d++)l[d]=r[d];return n.createElement.apply(null,l)}return n.createElement.apply(null,r)}f.displayName="MDXCreateElement"},49595:(e,a,r)=>{r.d(a,{A:()=>d,C:()=>u});var n=r(58168),t=r(96540),i=r(75489),l=r(44586),o=r(48295);function s(e){const a=(0,o.ir)();return(0,l.default)().siteConfig.customFields.githubLinkVersionToBaseUrl[a?.name??"current"]+e}function d(e){return t.createElement(i.default,(0,n.A)({},e,{to:s(e.to),target:"_blank"}))}function u(e){const a=e.text??"Example (Click Here)";return t.createElement(d,e,t.createElement("span",null,"\xa0"),t.createElement("img",{src:"https://img.shields.io/badge/-"+a+"-informational",alt:"Example (Click Here)"}))}},87950:(e,a,r)=>{r.r(a),r.d(a,{assets:()=>d,contentTitle:()=>o,default:()=>c,frontMatter:()=>l,metadata:()=>s,toc:()=>u});var n=r(58168),t=(r(96540),r(15680)),i=r(49595);const l={id:"fair-cluster",title:"Hydra on the FAIR cluster"},o=void 0,s={unversionedId:"fb/fair-cluster",id:"fb/fair-cluster",title:"Hydra on the FAIR cluster",description:"Hydra 1.0rc is available on FAIR Cluster. The recommended way for installation is via meta package hydra-fair-plugin.",source:"@site/docs/fb/fair-cluster.md",sourceDirName:"fb",slug:"/fb/fair-cluster",permalink:"/docs/fb/fair-cluster",draft:!1,editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/docs/fb/fair-cluster.md",tags:[],version:"current",lastUpdatedBy:"jesszzzz",lastUpdatedAt:1744041844,formattedLastUpdatedAt:"Apr 7, 2025",frontMatter:{id:"fair-cluster",title:"Hydra on the FAIR cluster"}},d={},u=[{value:"Hydra FAIR Plugins",id:"hydra-fair-plugins",level:2},{value:"Installation",id:"installation",level:3},{value:"Clean Install",id:"clean-install",level:3},{value:"Clean Install",id:"clean-install-1",level:3},{value:"Upgrade from stable",id:"upgrade-from-stable",level:3},{value:"Usage",id:"usage",level:3}],m={toc:u},p="wrapper";function c(e){let{components:a,...r}=e;return(0,t.mdx)(p,(0,n.A)({},m,r,{components:a,mdxType:"MDXLayout"}),(0,t.mdx)("p",null,"Hydra 1.0rc is available on FAIR Cluster. The recommended way for installation is via meta package ",(0,t.mdx)("a",{parentName:"p",href:"https://github.com/fairinternal/hydra-fair-plugins"},"hydra-fair-plugin"),"."),(0,t.mdx)("h2",{id:"hydra-fair-plugins"},"Hydra FAIR Plugins"),(0,t.mdx)("ol",null,(0,t.mdx)("li",{parentName:"ol"},"It brings the correct Hydra dependency and has been tested on the FAIR Cluster."),(0,t.mdx)("li",{parentName:"ol"},"It provides FAIR Cluster specific defaults overrides (for example, ",(0,t.mdx)("inlineCode",{parentName:"li"},"hydra.sweep.dir")," is set to be ",(0,t.mdx)("inlineCode",{parentName:"li"},"/checkpoint/${oc.env:USER}/outputs/${now:%Y-%m-%d}/${now:%H-%M-%S}"),")"),(0,t.mdx)("li",{parentName:"ol"},"It provides a ",(0,t.mdx)("a",{parentName:"li",href:"https://github.com/fairinternal/fairtask"},"fairtask")," launcher plugin."),(0,t.mdx)("li",{parentName:"ol"},"It installs ",(0,t.mdx)("a",{parentName:"li",href:"https://github.com/facebookincubator/submitit"},"Submitit")," launcher plugin by default.")),(0,t.mdx)("h3",{id:"installation"},"Installation"),(0,t.mdx)("details",null,(0,t.mdx)("summary",null,"0.3.1 (stable), compatible with Hydra 0.11"),(0,t.mdx)("h3",{id:"clean-install"},"Clean Install"),(0,t.mdx)("pre",null,(0,t.mdx)("code",{parentName:"pre",className:"language-commandline"},"pip install hydra-fair-plugins\n")),(0,t.mdx)("p",null,"The dependency installed looks like"),(0,t.mdx)("pre",null,(0,t.mdx)("code",{parentName:"pre",className:"language-commandline"},"$ pip freeze | grep hydra\nhydra-core==0.11.3\nhydra-fair-cluster==0.1.4\nhydra-fair-plugins==0.3.1\nhydra-fairtask==0.1.8\nhydra-submitit==0.2.0\n"))),(0,t.mdx)("details",null,(0,t.mdx)("summary",null,"1.0 (Release candidate), compatible with Hydra 1.0rc"),(0,t.mdx)("p",null,"With ",(0,t.mdx)("a",{parentName:"p",href:"https://github.com/facebookincubator/submitit"},(0,t.mdx)("inlineCode",{parentName:"a"},"Submitit"))," open sourced, the corresponding plugin has been moved "),(0,t.mdx)(i.A,{to:"plugins/hydra_submitit_launcher",mdxType:"GithubLink"},"here"),". Read this [doc](/docs/plugins/submitit_launcher) on installation/usage info.",(0,t.mdx)("h3",{id:"clean-install-1"},"Clean Install"),(0,t.mdx)("pre",null,(0,t.mdx)("code",{parentName:"pre",className:"language-commandline"},"pip install hydra-fair-plugins  --pre --upgrade --upgrade-strategy=eager\n")),(0,t.mdx)("h3",{id:"upgrade-from-stable"},"Upgrade from stable"),(0,t.mdx)("pre",null,(0,t.mdx)("code",{parentName:"pre",className:"language-commandline"},"# Remove legacy fair internal submitit launcher plugin\npip uninstall hydra-submitit -y\npip install hydra-fair-plugins  --pre --upgrade --upgrade-strategy=eager\n")),(0,t.mdx)("p",null,"Check out ",(0,t.mdx)("a",{parentName:"p",href:"/docs/plugins/submitit_launcher"},"Hydra documentation")," for  more info on ",(0,t.mdx)("inlineCode",{parentName:"p"},"Submitit")," launcher plugin."),(0,t.mdx)("p",null,"The depedency looks like "),(0,t.mdx)("pre",null,(0,t.mdx)("code",{parentName:"pre",className:"language-commandline"},"$ pip freeze | grep hydra\nhydra-core==1.0.0rc1\nhydra-fair-cluster==1.0.0rc1\nhydra-fair-plugins==1.0.0rc1\nhydra-fairtask==1.0.0rc1\nhydra-submitit-launcher==1.0.0rc3\n")),(0,t.mdx)("p",null,"Please refer to ",(0,t.mdx)("a",{parentName:"p",href:"/docs/upgrades/0.11_to_1.0/config_path_changes"},"Hydra upgrades")," on what changes are needed for your app for upgrading to Hydra 1.0")),(0,t.mdx)("details",null,(0,t.mdx)("summary",null,"Downgrade From 1.0rc to stable"),(0,t.mdx)("p",null,"Downgrade to stable in case you run into issues and need to be unblocked immediately."),(0,t.mdx)("pre",null,(0,t.mdx)("code",{parentName:"pre",className:"language-commandline"},"pip freeze | grep hydra | xargs pip uninstall -y\npip install hydra-fair-plugins\n"))),(0,t.mdx)("h3",{id:"usage"},"Usage"),(0,t.mdx)("details",null,(0,t.mdx)("summary",null,"0.3.1 (stable)"),"Once the plugins are installed, you can launch to the FAIR cluster by appending hydra/launcher=fairtask or hydra/launcher=submitit for example:",(0,t.mdx)("pre",null,(0,t.mdx)("code",{parentName:"pre"}," python my_app.py -m hydra/launcher=submitit db=mysql,postgresql\n# or\n python my_app.py -m hydra/launcher=fairtask db=mysql,postgresql\n")),(0,t.mdx)("p",null,"Both hydra-submitit and hydra-fairtask are providing sensible defaults for their configuration (",(0,t.mdx)("a",{parentName:"p",href:"https://github.com/fairinternal/hydra-fair-plugins/blob/master/plugins/hydra-submitit/hydra_plugins/submitit/conf/hydra/launcher/submitit.yaml"},"Submitit"),", ",(0,t.mdx)("a",{parentName:"p",href:"https://github.com/fairinternal/hydra-fair-plugins/blob/master/plugins/hydra-fairtask/hydra_plugins/fairtask/conf/hydra/launcher/fairtask.yaml"},"fairtask"),")"),(0,t.mdx)("p",null,"You can customize fairtask/submitit behavior much like you can customize anything else, from the command line or by overriding in your config file or composing in alternative launcher configuration.\nYou can view the Hydra config (which includes the config for submitit or fairtask) with this command:"),(0,t.mdx)("pre",null,(0,t.mdx)("code",{parentName:"pre"},"python my_app.py hydra/launcher=submitit --cfg=hydra\n"))),(0,t.mdx)("details",null,(0,t.mdx)("summary",null,"1.0 (Release Candidate)"),(0,t.mdx)("p",null,"For 1.0, ",(0,t.mdx)("inlineCode",{parentName:"p"},"fairtask")," usage remains the same. To use ",(0,t.mdx)("inlineCode",{parentName:"p"},"Submitit"),", the command changes to:"),(0,t.mdx)("pre",null,(0,t.mdx)("code",{parentName:"pre",className:"language-commandline"},"python my_app.py -m hydra/launcher=submitit_slurm db=mysql,postgresql\n")),(0,t.mdx)("p",null,"More info on ",(0,t.mdx)("inlineCode",{parentName:"p"},"Submitit")," launcher can be found ",(0,t.mdx)("a",{parentName:"p",href:"https://hydra.cc/docs/plugins/submitit_launcher"},"here"))))}c.isMDXComponent=!0}}]);