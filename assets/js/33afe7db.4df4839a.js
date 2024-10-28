"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[8678],{15680:(e,t,n)=>{n.r(t),n.d(t,{MDXContext:()=>m,MDXProvider:()=>d,mdx:()=>f,useMDXComponents:()=>p,withMDXComponents:()=>c});var a=n(96540);function o(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function r(){return r=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var a in n)Object.prototype.hasOwnProperty.call(n,a)&&(e[a]=n[a])}return e},r.apply(this,arguments)}function l(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);t&&(a=a.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,a)}return n}function i(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?l(Object(n),!0).forEach((function(t){o(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):l(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function s(e,t){if(null==e)return{};var n,a,o=function(e,t){if(null==e)return{};var n,a,o={},r=Object.keys(e);for(a=0;a<r.length;a++)n=r[a],t.indexOf(n)>=0||(o[n]=e[n]);return o}(e,t);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);for(a=0;a<r.length;a++)n=r[a],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(o[n]=e[n])}return o}var m=a.createContext({}),c=function(e){return function(t){var n=p(t.components);return a.createElement(e,r({},t,{components:n}))}},p=function(e){var t=a.useContext(m),n=t;return e&&(n="function"==typeof e?e(t):i(i({},t),e)),n},d=function(e){var t=p(e.components);return a.createElement(m.Provider,{value:t},e.children)},g={inlineCode:"code",wrapper:function(e){var t=e.children;return a.createElement(a.Fragment,{},t)}},u=a.forwardRef((function(e,t){var n=e.components,o=e.mdxType,r=e.originalType,l=e.parentName,m=s(e,["components","mdxType","originalType","parentName"]),c=p(n),d=o,u=c["".concat(l,".").concat(d)]||c[d]||g[d]||r;return n?a.createElement(u,i(i({ref:t},m),{},{components:n})):a.createElement(u,i({ref:t},m))}));function f(e,t){var n=arguments,o=t&&t.mdxType;if("string"==typeof e||o){var r=n.length,l=new Array(r);l[0]=u;var i={};for(var s in t)hasOwnProperty.call(t,s)&&(i[s]=t[s]);i.originalType=e,i.mdxType="string"==typeof e?e:o,l[1]=i;for(var m=2;m<r;m++)l[m]=n[m];return a.createElement.apply(null,l)}return a.createElement.apply(null,n)}u.displayName="MDXCreateElement"},49595:(e,t,n)=>{n.d(t,{A:()=>s,C:()=>m});var a=n(58168),o=n(96540),r=n(75489),l=n(44586),i=n(74098);function s(e){return o.createElement(r.default,(0,a.A)({},e,{to:(t=e.to,s=(0,i.useActiveVersion)(),(0,l.default)().siteConfig.customFields.githubLinkVersionToBaseUrl[null!=(n=null==s?void 0:s.name)?n:"current"]+t),target:"_blank"}));var t,n,s}function m(e){var t,n=null!=(t=e.text)?t:"Example (Click Here)";return o.createElement(s,e,o.createElement("span",null,"\xa0"),o.createElement("img",{src:"https://img.shields.io/badge/-"+n+"-informational",alt:"Example (Click Here)"}))}},88123:(e,t,n)=>{n.r(t),n.d(t,{contentTitle:()=>m,default:()=>g,frontMatter:()=>s,metadata:()=>c,toc:()=>p});var a=n(58168),o=n(98587),r=(n(96540),n(15680)),l=n(49595),i=["components"],s={id:"select_multiple_configs_from_config_group",title:"Selecting multiple configs from a Config Group"},m=void 0,c={unversionedId:"patterns/select_multiple_configs_from_config_group",id:"version-1.1/patterns/select_multiple_configs_from_config_group",title:"Selecting multiple configs from a Config Group",description:"Problem",source:"@site/versioned_docs/version-1.1/patterns/select_multiple_configs_from_config_group.md",sourceDirName:"patterns",slug:"/patterns/select_multiple_configs_from_config_group",permalink:"/docs/1.1/patterns/select_multiple_configs_from_config_group",editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/versioned_docs/version-1.1/patterns/select_multiple_configs_from_config_group.md",tags:[],version:"1.1",lastUpdatedBy:"dependabot[bot]",lastUpdatedAt:1730135614,formattedLastUpdatedAt:"10/28/2024",frontMatter:{id:"select_multiple_configs_from_config_group",title:"Selecting multiple configs from a Config Group"},sidebar:"version-1.1/docs",previous:{title:"Configuring Plugins",permalink:"/docs/1.1/patterns/configuring_plugins"},next:{title:"Specializing configuration",permalink:"/docs/1.1/patterns/specializing_config"}},p=[{value:"Problem",id:"problem",children:[],level:3},{value:"Solution",id:"solution",children:[],level:3},{value:"Example",id:"example",children:[],level:3},{value:"Overriding packages",id:"overriding-packages",children:[],level:3},{value:"Implementation considerations",id:"implementation-considerations",children:[],level:3}],d={toc:p};function g(e){var t=e.components,n=(0,o.A)(e,i);return(0,r.mdx)("wrapper",(0,a.A)({},d,n,{components:t,mdxType:"MDXLayout"}),(0,r.mdx)(l.C,{text:"Example application",to:"examples/patterns/multi-select",mdxType:"ExampleGithubLink"}),(0,r.mdx)("h3",{id:"problem"},"Problem"),(0,r.mdx)("p",null,"In some scenarios, one may need to select multiple configs from the same Config Group."),(0,r.mdx)("h3",{id:"solution"},"Solution"),(0,r.mdx)("p",null,"Use a list of config names as the value of the config group in the Defaults List or in the command line."),(0,r.mdx)("h3",{id:"example"},"Example"),(0,r.mdx)("p",null,"In this example, we configure a server. The server can host multiple websites at the same time."),(0,r.mdx)("div",{className:"row"},(0,r.mdx)("div",{className:"col col--4"},(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-text",metastring:'title="Config directory"',title:'"Config','directory"':!0},"\u251c\u2500\u2500 config.yaml\n\u2514\u2500\u2500 server\n    \u251c\u2500\u2500 apache.yaml\n    \u2514\u2500\u2500 site\n        \u251c\u2500\u2500 amazon.yaml\n        \u251c\u2500\u2500 fb.yaml\n        \u2514\u2500\u2500 google.yaml\n"))),(0,r.mdx)("div",{className:"col col--4"},(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="config.yaml"',title:'"config.yaml"'},"defaults:\n  - server/apache\n\n\n\n\n\n"))),(0,r.mdx)("div",{className:"col col--4"},(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="server/apache.yaml" {3,4}',title:'"server/apache.yaml"',"{3,4}":!0},"defaults:\n  - site:\n    - fb\n    - google\n\nhost: localhost\nport: 443\n"))),(0,r.mdx)("div",{className:"col col--4"},(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="server/site/amazon.yaml"',title:'"server/site/amazon.yaml"'},"amazon:\n  domain: amazon.com\n"))),(0,r.mdx)("div",{className:"col col--4"},(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="server/site/fb.yaml"',title:'"server/site/fb.yaml"'},"fb:\n  domain: facebook.com\n"))),(0,r.mdx)("div",{className:"col col--4"},(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="server/site/google.yaml"',title:'"server/site/google.yaml"'},"google:\n  domain: google.com\n")))),(0,r.mdx)("p",null,"Output:"),(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="$ python my_app.py" {3,5}',title:'"$',python:!0,'my_app.py"':!0,"{3,5}":!0},"server:\n  site:\n    fb:\n      domain: facebook.com\n    google:\n      domain: google.com\n  host: localhost\n  port: 443\n")),(0,r.mdx)("p",null,"Override the selected sites from the command line by passing a list. e.g:"),(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:"title=\"$ python my_app.py 'server/site=[google,amazon]'\" {3,5}",title:'"$',python:!0,"my_app.py":!0,"'server/site":"[google,amazon]'\"","{3,5}":!0},"server:\n  site:\n    google:\n      domain: google.com\n    amazon:\n      domain: amazon.com\n  host: localhost\n  port: 443\n")),(0,r.mdx)("h3",{id:"overriding-packages"},"Overriding packages"),(0,r.mdx)("p",null,"You can relocate the package of all the configs in the list. e.g:"),(0,r.mdx)("div",{className:"row"},(0,r.mdx)("div",{className:"col col--6"},(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="server/apache.yaml" {2}',title:'"server/apache.yaml"',"{2}":!0},"defaults:\n  - site@https:\n    - fb\n    - google\n\n\n"))),(0,r.mdx)("div",{className:"col col--6"},(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="$ python my_app.py" {2}',title:'"$',python:!0,'my_app.py"':!0,"{2}":!0},"server:\n  https:\n    fb:\n      domain: facebook.com\n    google:\n      domain: google.com\n")))),(0,r.mdx)("p",null,"When overriding the selected configs of config groups with overridden packages you need to use the package. e.g:"),(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="$ python my_app.py server/site@server.https=amazon"',title:'"$',python:!0,"my_app.py":!0,"server/site@server.https":'amazon"'},"server:\n  https:\n    amazon:\n      domain: amazon.com\n  host: localhost\n  port: 443\n")),(0,r.mdx)("h3",{id:"implementation-considerations"},"Implementation considerations"),(0,r.mdx)("p",null,"A nested list in the Defaults List is interpreted as a list of non-overridable configs:"),(0,r.mdx)("div",{className:"row"},(0,r.mdx)("div",{className:"col col--6"},(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="server/apache.yaml" {3,4}',title:'"server/apache.yaml"',"{3,4}":!0},"defaults:\n  - site:\n    - fb\n    - google\n"))),(0,r.mdx)("div",{className:"col col--6"},(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="Equivalent to" {2,3}',title:'"Equivalent','to"':!0,"{2,3}":!0},"defaults:\n  - site/fb\n  - site/google\n\n")))),(0,r.mdx)("p",null,"All default package for all the configs in ",(0,r.mdx)("inlineCode",{parentName:"p"},"server/site")," is ",(0,r.mdx)("inlineCode",{parentName:"p"},"server.site"),".\nThis example uses an explicit nesting level inside each of the website configs to prevent them stepping over one another:"),(0,r.mdx)("pre",null,(0,r.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="server/site/amazon.yaml" {1}',title:'"server/site/amazon.yaml"',"{1}":!0},"amazon:\n  ...\n")))}g.isMDXComponent=!0}}]);