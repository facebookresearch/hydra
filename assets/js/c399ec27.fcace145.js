"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[1046],{15680:(e,t,n)=>{n.r(t),n.d(t,{MDXContext:()=>s,MDXProvider:()=>d,mdx:()=>g,useMDXComponents:()=>m,withMDXComponents:()=>c});var r=n(96540);function a(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function o(){return o=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var r in n)Object.prototype.hasOwnProperty.call(n,r)&&(e[r]=n[r])}return e},o.apply(this,arguments)}function i(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,r)}return n}function p(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?i(Object(n),!0).forEach((function(t){a(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):i(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function l(e,t){if(null==e)return{};var n,r,a=function(e,t){if(null==e)return{};var n,r,a={},o=Object.keys(e);for(r=0;r<o.length;r++)n=o[r],t.indexOf(n)>=0||(a[n]=e[n]);return a}(e,t);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(e);for(r=0;r<o.length;r++)n=o[r],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(a[n]=e[n])}return a}var s=r.createContext({}),c=function(e){return function(t){var n=m(t.components);return r.createElement(e,o({},t,{components:n}))}},m=function(e){var t=r.useContext(s),n=t;return e&&(n="function"==typeof e?e(t):p(p({},t),e)),n},d=function(e){var t=m(e.components);return r.createElement(s.Provider,{value:t},e.children)},u="mdxType",f={inlineCode:"code",wrapper:function(e){var t=e.children;return r.createElement(r.Fragment,{},t)}},y=r.forwardRef((function(e,t){var n=e.components,a=e.mdxType,o=e.originalType,i=e.parentName,s=l(e,["components","mdxType","originalType","parentName"]),c=m(n),d=a,u=c["".concat(i,".").concat(d)]||c[d]||f[d]||o;return n?r.createElement(u,p(p({ref:t},s),{},{components:n})):r.createElement(u,p({ref:t},s))}));function g(e,t){var n=arguments,a=t&&t.mdxType;if("string"==typeof e||a){var o=n.length,i=new Array(o);i[0]=y;var p={};for(var l in t)hasOwnProperty.call(t,l)&&(p[l]=t[l]);p.originalType=e,p[u]="string"==typeof e?e:a,i[1]=p;for(var s=2;s<o;s++)i[s]=n[s];return r.createElement.apply(null,i)}return r.createElement.apply(null,n)}y.displayName="MDXCreateElement"},49595:(e,t,n)=>{n.d(t,{A:()=>s,C:()=>c});var r=n(58168),a=n(96540),o=n(75489),i=n(44586),p=n(48295);function l(e){const t=(0,p.ir)();return(0,i.default)().siteConfig.customFields.githubLinkVersionToBaseUrl[t?.name??"current"]+e}function s(e){return a.createElement(o.default,(0,r.A)({},e,{to:l(e.to),target:"_blank"}))}function c(e){const t=e.text??"Example (Click Here)";return a.createElement(s,e,a.createElement("span",null,"\xa0"),a.createElement("img",{src:"https://img.shields.io/badge/-"+t+"-informational",alt:"Example (Click Here)"}))}},67298:(e,t,n)=>{n.r(t),n.d(t,{assets:()=>s,contentTitle:()=>p,default:()=>u,frontMatter:()=>i,metadata:()=>l,toc:()=>c});var r=n(58168),a=(n(96540),n(15680)),o=n(49595);const i={id:"config_file",title:"Specifying a config file"},p=void 0,l={unversionedId:"tutorials/basic/your_first_app/config_file",id:"version-1.3/tutorials/basic/your_first_app/config_file",title:"Specifying a config file",description:"It can get tedious to type all those command line arguments.",source:"@site/versioned_docs/version-1.3/tutorials/basic/your_first_app/2_config_file.md",sourceDirName:"tutorials/basic/your_first_app",slug:"/tutorials/basic/your_first_app/config_file",permalink:"/docs/1.3/tutorials/basic/your_first_app/config_file",draft:!1,editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/versioned_docs/version-1.3/tutorials/basic/your_first_app/2_config_file.md",tags:[],version:"1.3",lastUpdatedBy:"Jasha",lastUpdatedAt:1670537910,formattedLastUpdatedAt:"Dec 8, 2022",sidebarPosition:2,frontMatter:{id:"config_file",title:"Specifying a config file"},sidebar:"docs",previous:{title:"A simple command-line application",permalink:"/docs/1.3/tutorials/basic/your_first_app/simple_cli"},next:{title:"Using the config object",permalink:"/docs/1.3/tutorials/basic/your_first_app/using_config"}},s={},c=[],m={toc:c},d="wrapper";function u(e){let{components:t,...n}=e;return(0,a.mdx)(d,(0,r.A)({},m,n,{components:t,mdxType:"MDXLayout"}),(0,a.mdx)(o.C,{to:"examples/tutorials/basic/your_first_hydra_app/2_config_file",mdxType:"ExampleGithubLink"}),(0,a.mdx)("p",null,"It can get tedious to type all those command line arguments.\nYou can solve it by creating a configuration file next to my_app.py.\nHydra configuration files are yaml files and should have the .yaml file extension."),(0,a.mdx)("pre",null,(0,a.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="config.yaml"',title:'"config.yaml"'},"db: \n  driver: mysql\n  user: omry\n  password: secret\n")),(0,a.mdx)("p",null,"Specify the config name by passing a ",(0,a.mdx)("inlineCode",{parentName:"p"},"config_name")," parameter to the ",(0,a.mdx)("strong",{parentName:"p"},"@hydra.main()")," decorator.\nNote that you should omit the ",(0,a.mdx)("strong",{parentName:"p"},".yaml")," extension.\nHydra also needs to know where to find your config. Specify the directory containing it relative to the application by passing ",(0,a.mdx)("inlineCode",{parentName:"p"},"config_path"),": "),(0,a.mdx)("pre",null,(0,a.mdx)("code",{parentName:"pre",className:"language-python",metastring:'title="my_app.py" {4}',title:'"my_app.py"',"{4}":!0},'from omegaconf import DictConfig, OmegaConf\nimport hydra\n\n@hydra.main(version_base=None, config_path=".", config_name="config")\ndef my_app(cfg):\n    print(OmegaConf.to_yaml(cfg))\n\nif __name__ == "__main__":\n    my_app()\n')),(0,a.mdx)("p",null,(0,a.mdx)("inlineCode",{parentName:"p"},"config.yaml")," is loaded automatically when you run your application."),(0,a.mdx)("pre",null,(0,a.mdx)("code",{parentName:"pre",className:"language-yaml"},"$ python my_app.py\ndb:\n  driver: mysql\n  user: omry\n  password: secret\n")),(0,a.mdx)("p",null,"You can override values in the loaded config from the command line.",(0,a.mdx)("br",{parentName:"p"}),"\n","Note the lack of the ",(0,a.mdx)("inlineCode",{parentName:"p"},"+")," prefix."),(0,a.mdx)("pre",null,(0,a.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:"{4-5}","{4-5}":!0},"$ python my_app.py db.user=root db.password=1234\ndb:\n  driver: mysql\n  user: root\n  password: 1234\n")),(0,a.mdx)("p",null,"Use ",(0,a.mdx)("inlineCode",{parentName:"p"},"++")," to override a config value if it's already in the config, or add it otherwise.\ne.g:"),(0,a.mdx)("pre",null,(0,a.mdx)("code",{parentName:"pre",className:"language-shell"},"# Override an existing item\n$ python my_app.py ++db.password=1234\n\n# Add a new item\n$ python my_app.py ++db.timeout=5\n")),(0,a.mdx)("p",null,"You can enable ",(0,a.mdx)("a",{parentName:"p",href:"/docs/1.3/tutorials/basic/running_your_app/tab_completion"},"tab completion")," for your Hydra applications."))}u.isMDXComponent=!0}}]);