"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[3478],{3905:function(e,t,n){n.r(t),n.d(t,{MDXContext:function(){return l},MDXProvider:function(){return p},mdx:function(){return g},useMDXComponents:function(){return u},withMDXComponents:function(){return d}});var r=n(67294);function a(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function i(){return i=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var r in n)Object.prototype.hasOwnProperty.call(n,r)&&(e[r]=n[r])}return e},i.apply(this,arguments)}function o(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,r)}return n}function c(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?o(Object(n),!0).forEach((function(t){a(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):o(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function s(e,t){if(null==e)return{};var n,r,a=function(e,t){if(null==e)return{};var n,r,a={},i=Object.keys(e);for(r=0;r<i.length;r++)n=i[r],t.indexOf(n)>=0||(a[n]=e[n]);return a}(e,t);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);for(r=0;r<i.length;r++)n=i[r],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(a[n]=e[n])}return a}var l=r.createContext({}),d=function(e){return function(t){var n=u(t.components);return r.createElement(e,i({},t,{components:n}))}},u=function(e){var t=r.useContext(l),n=t;return e&&(n="function"==typeof e?e(t):c(c({},t),e)),n},p=function(e){var t=u(e.components);return r.createElement(l.Provider,{value:t},e.children)},m={inlineCode:"code",wrapper:function(e){var t=e.children;return r.createElement(r.Fragment,{},t)}},f=r.forwardRef((function(e,t){var n=e.components,a=e.mdxType,i=e.originalType,o=e.parentName,l=s(e,["components","mdxType","originalType","parentName"]),d=u(n),p=a,f=d["".concat(o,".").concat(p)]||d[p]||m[p]||i;return n?r.createElement(f,c(c({ref:t},l),{},{components:n})):r.createElement(f,c({ref:t},l))}));function g(e,t){var n=arguments,a=t&&t.mdxType;if("string"==typeof e||a){var i=n.length,o=new Array(i);o[0]=f;var c={};for(var s in t)hasOwnProperty.call(t,s)&&(c[s]=t[s]);c.originalType=e,c.mdxType="string"==typeof e?e:a,o[1]=c;for(var l=2;l<i;l++)o[l]=n[l];return r.createElement.apply(null,o)}return r.createElement.apply(null,n)}f.displayName="MDXCreateElement"},30166:function(e,t,n){n.r(t),n.d(t,{frontMatter:function(){return c},contentTitle:function(){return s},metadata:function(){return l},toc:function(){return d},default:function(){return p}});var r=n(87462),a=n(63366),i=(n(67294),n(3905)),o=["components"],c={id:"object_instantiation_changes",title:"Object instantiation changes",hide_title:!0},s=void 0,l={unversionedId:"upgrades/0.11_to_1.0/object_instantiation_changes",id:"version-1.2/upgrades/0.11_to_1.0/object_instantiation_changes",title:"Object instantiation changes",description:"Object instantiation changes",source:"@site/versioned_docs/version-1.2/upgrades/0.11_to_1.0/object_instantiation_changes.md",sourceDirName:"upgrades/0.11_to_1.0",slug:"/upgrades/0.11_to_1.0/object_instantiation_changes",permalink:"/docs/1.2/upgrades/0.11_to_1.0/object_instantiation_changes",editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/versioned_docs/version-1.2/upgrades/0.11_to_1.0/object_instantiation_changes.md",tags:[],version:"1.2",lastUpdatedBy:"B\xe1lint Mucs\xe1nyi",lastUpdatedAt:1668876151,formattedLastUpdatedAt:"11/19/2022",frontMatter:{id:"object_instantiation_changes",title:"Object instantiation changes",hide_title:!0},sidebar:"docs",previous:{title:"strict flag mode deprecation",permalink:"/docs/1.2/upgrades/0.11_to_1.0/strict_mode_flag_deprecated"}},d=[{value:"Object instantiation changes",id:"object-instantiation-changes",children:[],level:2},{value:"Hydra configuration",id:"hydra-configuration",children:[],level:2}],u={toc:d};function p(e){var t=e.components,n=(0,a.Z)(e,o);return(0,i.mdx)("wrapper",(0,r.Z)({},u,n,{components:t,mdxType:"MDXLayout"}),(0,i.mdx)("h2",{id:"object-instantiation-changes"},"Object instantiation changes"),(0,i.mdx)("p",null,"Hydra 1.0.0 is deprecating ObjectConf and the corresponding config structure to a simpler one without the params node.\nThis removes a level of nesting from command line and configs overrides."),(0,i.mdx)("div",{className:"row"},(0,i.mdx)("div",{className:"col col--6"},(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="Hydra 0.11"',title:'"Hydra','0.11"':!0},"class: my_app.MySQLConnection\nparams:\n  host: localhost\n  user: root\n  password: 1234\n"))),(0,i.mdx)("div",{className:"col  col--6"},(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="Hydra 1.0"',title:'"Hydra','1.0"':!0},"_target_: my_app.MySQLConnection\nhost: localhost\nuser: root\npassword: 1234\n\n")))),(0,i.mdx)("h2",{id:"hydra-configuration"},"Hydra configuration"),(0,i.mdx)("p",null,"Hydra plugins are configured using the same mechanism.\nThis means that this change will effect how all plugins are configured and overridden.\nThis is a breaking change for code overriding configs in such plugins, but luckily it's easy to fix."),(0,i.mdx)("p",null,"As an example, a Sweeper plugin override will change as follows:"),(0,i.mdx)("div",{className:"row"},(0,i.mdx)("div",{className:"col col--6"},(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre",className:"language-shell",metastring:'script title="Hydra 0.11"',script:!0,title:'"Hydra','0.11"':!0},"hydra.sweeper.params.max_batch_size=10\n"))),(0,i.mdx)("div",{className:"col  col--6"},(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre",className:"language-shell",metastring:'script title="Hydra 1.0"',script:!0,title:'"Hydra','1.0"':!0},"hydra.sweeper.max_batch_size=10\n")))))}p.isMDXComponent=!0}}]);