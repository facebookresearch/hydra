"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[1250],{15680:(e,t,n)=>{n.r(t),n.d(t,{MDXContext:()=>s,MDXProvider:()=>u,mdx:()=>g,useMDXComponents:()=>d,withMDXComponents:()=>p});var r=n(96540);function o(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function i(){return i=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var r in n)Object.prototype.hasOwnProperty.call(n,r)&&(e[r]=n[r])}return e},i.apply(this,arguments)}function a(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,r)}return n}function c(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?a(Object(n),!0).forEach((function(t){o(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):a(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function l(e,t){if(null==e)return{};var n,r,o=function(e,t){if(null==e)return{};var n,r,o={},i=Object.keys(e);for(r=0;r<i.length;r++)n=i[r],t.indexOf(n)>=0||(o[n]=e[n]);return o}(e,t);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);for(r=0;r<i.length;r++)n=i[r],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(o[n]=e[n])}return o}var s=r.createContext({}),p=function(e){return function(t){var n=d(t.components);return r.createElement(e,i({},t,{components:n}))}},d=function(e){var t=r.useContext(s),n=t;return e&&(n="function"==typeof e?e(t):c(c({},t),e)),n},u=function(e){var t=d(e.components);return r.createElement(s.Provider,{value:t},e.children)},m={inlineCode:"code",wrapper:function(e){var t=e.children;return r.createElement(r.Fragment,{},t)}},f=r.forwardRef((function(e,t){var n=e.components,o=e.mdxType,i=e.originalType,a=e.parentName,s=l(e,["components","mdxType","originalType","parentName"]),p=d(n),u=o,f=p["".concat(a,".").concat(u)]||p[u]||m[u]||i;return n?r.createElement(f,c(c({ref:t},s),{},{components:n})):r.createElement(f,c({ref:t},s))}));function g(e,t){var n=arguments,o=t&&t.mdxType;if("string"==typeof e||o){var i=n.length,a=new Array(i);a[0]=f;var c={};for(var l in t)hasOwnProperty.call(t,l)&&(c[l]=t[l]);c.originalType=e,c.mdxType="string"==typeof e?e:o,a[1]=c;for(var s=2;s<i;s++)a[s]=n[s];return r.createElement.apply(null,a)}return r.createElement.apply(null,n)}f.displayName="MDXCreateElement"},49595:(e,t,n)=>{n.d(t,{A:()=>l,C:()=>s});var r=n(58168),o=n(96540),i=n(75489),a=n(44586),c=n(74098);function l(e){return o.createElement(i.default,(0,r.A)({},e,{to:(t=e.to,l=(0,c.useActiveVersion)(),(0,a.default)().siteConfig.customFields.githubLinkVersionToBaseUrl[null!=(n=null==l?void 0:l.name)?n:"current"]+t),target:"_blank"}));var t,n,l}function s(e){var t,n=null!=(t=e.text)?t:"Example (Click Here)";return o.createElement(l,e,o.createElement("span",null,"\xa0"),o.createElement("img",{src:"https://img.shields.io/badge/-"+n+"-informational",alt:"Example (Click Here)"}))}},31575:(e,t,n)=>{n.r(t),n.d(t,{contentTitle:()=>s,default:()=>m,frontMatter:()=>l,metadata:()=>p,toc:()=>d});var r=n(58168),o=n(98587),i=(n(96540),n(15680)),a=n(49595),c=["components"],l={id:"write_protect_config_node",title:"Read-only config"},s=void 0,p={unversionedId:"patterns/write_protect_config_node",id:"version-1.3/patterns/write_protect_config_node",title:"Read-only config",description:"Problem",source:"@site/versioned_docs/version-1.3/patterns/write_protect_config_node.md",sourceDirName:"patterns",slug:"/patterns/write_protect_config_node",permalink:"/docs/1.3/patterns/write_protect_config_node",editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/versioned_docs/version-1.3/patterns/write_protect_config_node.md",tags:[],version:"1.3",lastUpdatedBy:"jesszzzz",lastUpdatedAt:1738870843,formattedLastUpdatedAt:"2/6/2025",frontMatter:{id:"write_protect_config_node",title:"Read-only config"},sidebar:"docs",previous:{title:"Specializing configuration",permalink:"/docs/1.3/patterns/specializing_config"},next:{title:"Introduction",permalink:"/docs/1.3/configure_hydra/intro"}},d=[{value:"Problem",id:"problem",children:[],level:3},{value:"Solution",id:"solution",children:[],level:3}],u={toc:d};function m(e){var t=e.components,n=(0,o.A)(e,c);return(0,i.mdx)("wrapper",(0,r.A)({},u,n,{components:t,mdxType:"MDXLayout"}),(0,i.mdx)(a.C,{text:"Example application",to:"examples/patterns/write_protect_config_node",mdxType:"ExampleGithubLink"}),(0,i.mdx)("h3",{id:"problem"},"Problem"),(0,i.mdx)("p",null,"Sometimes you want to prevent a config node from being changed accidentally."),(0,i.mdx)("h3",{id:"solution"},"Solution"),(0,i.mdx)("p",null,"Structured Configs can enable it by passing ",(0,i.mdx)("a",{parentName:"p",href:"https://omegaconf.readthedocs.io/en/latest/structured_config.html#frozen"},"frozen=True")," in the dataclass definition.\nUsing Structured Configs, you can annotate a dataclass as frozen. This is recursive and applies to all child nodes."),(0,i.mdx)("p",null,"This will prevent modifications via code, command line overrides and config composition."),(0,i.mdx)("div",{className:"row"},(0,i.mdx)("div",{className:"col col--6"},(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre",className:"language-python",metastring:'title="frozen.py" {1}',title:'"frozen.py"',"{1}":!0},'@dataclass(frozen=True)\nclass SerialPort:\n    baud_rate: int = 19200\n    data_bits: int = 8\n    stop_bits: int = 1\n\n\ncs = ConfigStore.instance()\ncs.store(name="config", node=SerialPort)\n\n\n@hydra.main(version_base=None, config_name="config")\ndef my_app(cfg: SerialPort) -> None:\n    print(cfg)\n\n\nif __name__ == "__main__":\n    my_app()\n'))),(0,i.mdx)("div",{className:"col  col--6"},(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre",className:"language-shell",metastring:'script title="Output"',script:!0,title:'"Output"'},"$ python frozen.py data_bits=10\nError merging override data_bits=10\nCannot change read-only config container\n    full_key: data_bits\n    object_type=SerialPort\n")))),(0,i.mdx)("div",{class:"alert alert--warning",role:"alert"},(0,i.mdx)("strong",null,"NOTE"),": A crafty user can find many ways around this. This is just making it harder to change things accidentally."))}m.isMDXComponent=!0}}]);