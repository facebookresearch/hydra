"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[819],{15680:(e,t,r)=>{r.r(t),r.d(t,{MDXContext:()=>s,MDXProvider:()=>d,mdx:()=>y,useMDXComponents:()=>m,withMDXComponents:()=>c});var n=r(96540);function a(e,t,r){return t in e?Object.defineProperty(e,t,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[t]=r,e}function i(){return i=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var r=arguments[t];for(var n in r)Object.prototype.hasOwnProperty.call(r,n)&&(e[n]=r[n])}return e},i.apply(this,arguments)}function o(e,t){var r=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);t&&(n=n.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),r.push.apply(r,n)}return r}function l(e){for(var t=1;t<arguments.length;t++){var r=null!=arguments[t]?arguments[t]:{};t%2?o(Object(r),!0).forEach((function(t){a(e,t,r[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(r)):o(Object(r)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(r,t))}))}return e}function p(e,t){if(null==e)return{};var r,n,a=function(e,t){if(null==e)return{};var r,n,a={},i=Object.keys(e);for(n=0;n<i.length;n++)r=i[n],t.indexOf(r)>=0||(a[r]=e[r]);return a}(e,t);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);for(n=0;n<i.length;n++)r=i[n],t.indexOf(r)>=0||Object.prototype.propertyIsEnumerable.call(e,r)&&(a[r]=e[r])}return a}var s=n.createContext({}),c=function(e){return function(t){var r=m(t.components);return n.createElement(e,i({},t,{components:r}))}},m=function(e){var t=n.useContext(s),r=t;return e&&(r="function"==typeof e?e(t):l(l({},t),e)),r},d=function(e){var t=m(e.components);return n.createElement(s.Provider,{value:t},e.children)},u={inlineCode:"code",wrapper:function(e){var t=e.children;return n.createElement(n.Fragment,{},t)}},f=n.forwardRef((function(e,t){var r=e.components,a=e.mdxType,i=e.originalType,o=e.parentName,s=p(e,["components","mdxType","originalType","parentName"]),c=m(r),d=a,f=c["".concat(o,".").concat(d)]||c[d]||u[d]||i;return r?n.createElement(f,l(l({ref:t},s),{},{components:r})):n.createElement(f,l({ref:t},s))}));function y(e,t){var r=arguments,a=t&&t.mdxType;if("string"==typeof e||a){var i=r.length,o=new Array(i);o[0]=f;var l={};for(var p in t)hasOwnProperty.call(t,p)&&(l[p]=t[p]);l.originalType=e,l.mdxType="string"==typeof e?e:a,o[1]=l;for(var s=2;s<i;s++)o[s]=r[s];return n.createElement.apply(null,o)}return n.createElement.apply(null,r)}f.displayName="MDXCreateElement"},49595:(e,t,r)=>{r.d(t,{A:()=>p,C:()=>s});var n=r(58168),a=r(96540),i=r(75489),o=r(44586),l=r(74098);function p(e){return a.createElement(i.default,(0,n.A)({},e,{to:(t=e.to,p=(0,l.useActiveVersion)(),(0,o.default)().siteConfig.customFields.githubLinkVersionToBaseUrl[null!=(r=null==p?void 0:p.name)?r:"current"]+t),target:"_blank"}));var t,r,p}function s(e){var t,r=null!=(t=e.text)?t:"Example (Click Here)";return a.createElement(p,e,a.createElement("span",null,"\xa0"),a.createElement("img",{src:"https://img.shields.io/badge/-"+r+"-informational",alt:"Example (Click Here)"}))}},26218:(e,t,r)=>{r.r(t),r.d(t,{contentTitle:()=>s,default:()=>u,frontMatter:()=>p,metadata:()=>c,toc:()=>m});var n=r(58168),a=r(98587),i=(r(96540),r(15680)),o=r(49595),l=["components"],p={id:"simple_cli",title:"A simple command-line application"},s=void 0,c={unversionedId:"tutorials/basic/your_first_app/simple_cli",id:"version-1.0/tutorials/basic/your_first_app/simple_cli",title:"A simple command-line application",description:"This is a simple Hydra application that prints your configuration.",source:"@site/versioned_docs/version-1.0/tutorials/basic/your_first_app/1_simple_cli.md",sourceDirName:"tutorials/basic/your_first_app",slug:"/tutorials/basic/your_first_app/simple_cli",permalink:"/docs/1.0/tutorials/basic/your_first_app/simple_cli",editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/versioned_docs/version-1.0/tutorials/basic/your_first_app/1_simple_cli.md",tags:[],version:"1.0",lastUpdatedBy:"dependabot[bot]",lastUpdatedAt:1734709105,formattedLastUpdatedAt:"12/20/2024",sidebarPosition:1,frontMatter:{id:"simple_cli",title:"A simple command-line application"},sidebar:"version-1.0/docs",previous:{title:"Tutorials intro",permalink:"/docs/1.0/tutorials/intro"},next:{title:"Specifying a config file",permalink:"/docs/1.0/tutorials/basic/your_first_app/config_file"}},m=[],d={toc:m};function u(e){var t=e.components,r=(0,a.A)(e,l);return(0,i.mdx)("wrapper",(0,n.A)({},d,r,{components:t,mdxType:"MDXLayout"}),(0,i.mdx)(o.C,{to:"examples/tutorials/basic/your_first_hydra_app/1_simple_cli/my_app.py",mdxType:"ExampleGithubLink"}),(0,i.mdx)("p",null,"This is a simple Hydra application that prints your configuration.\nThe ",(0,i.mdx)("inlineCode",{parentName:"p"},"my_app")," function is a placeholder for your code.\nWe will slowly evolve this example to showcase more Hydra features."),(0,i.mdx)("p",null,"The examples in this tutorial are available ",(0,i.mdx)(o.A,{to:"examples/tutorials/basic",mdxType:"GithubLink"},"here"),"."),(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre",className:"language-python",metastring:'title="my_app.py"',title:'"my_app.py"'},'from omegaconf import DictConfig, OmegaConf\nimport hydra\n\n@hydra.main()\ndef my_app(cfg: DictConfig) -> None:\n    print(OmegaConf.to_yaml(cfg))\n\nif __name__ == "__main__":\n    my_app()\n')),(0,i.mdx)("p",null,"In this example, Hydra creates an empty ",(0,i.mdx)("inlineCode",{parentName:"p"},"cfg")," object and passes it to the function annotated with ",(0,i.mdx)("inlineCode",{parentName:"p"},"@hydra.main"),"."),(0,i.mdx)("p",null,"You can add config values via the command line. The ",(0,i.mdx)("inlineCode",{parentName:"p"},"+")," indicates that the field is new."),(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre",className:"language-yaml"},"$ python my_app.py +db.driver=mysql +db.user=omry +db.password=secret\ndb:\n  driver: mysql\n  user: omry\n  password: secret\n")),(0,i.mdx)("p",null,"See ",(0,i.mdx)("a",{parentName:"p",href:"/docs/1.0/advanced/hydra-command-line-flags"},"Hydra's command line flags")," and\n",(0,i.mdx)("a",{parentName:"p",href:"/docs/1.0/advanced/override_grammar/basic"},"Basic Override Syntax")," for more information about the command line."))}u.isMDXComponent=!0}}]);