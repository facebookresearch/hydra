(window.webpackJsonp=window.webpackJsonp||[]).push([[90],{161:function(e,n,t){"use strict";t.r(n),t.d(n,"frontMatter",(function(){return i})),t.d(n,"metadata",(function(){return c})),t.d(n,"toc",(function(){return f})),t.d(n,"default",(function(){return s}));var a=t(3),r=t(8),o=(t(0),t(268)),i={id:"fbcode-configerator-config-source",title:"Configerator Config Source Plugin"},c={unversionedId:"fb/fbcode-configerator-config-source",id:"fb/fbcode-configerator-config-source",isDocsHomePage:!1,title:"Configerator Config Source Plugin",description:"The ConfigeratorConfigSource plugin makes it possible for Hydra applications to consume a domain of configs from configerator.",source:"@site/docs/fb/configerator-config-source.md",slug:"/fb/fbcode-configerator-config-source",permalink:"/docs/next/fb/fbcode-configerator-config-source",editUrl:"https://github.com/facebookresearch/hydra/edit/master/website/docs/fb/configerator-config-source.md",version:"current",lastUpdatedBy:"Omry Yadan",lastUpdatedAt:1616693367},f=[{value:"Dependency",id:"dependency",children:[]},{value:"Usage",id:"usage",children:[]},{value:"Example:",id:"example",children:[]}],l={toc:f};function s(e){var n=e.components,t=Object(r.a)(e,["components"]);return Object(o.b)("wrapper",Object(a.a)({},l,t,{components:n,mdxType:"MDXLayout"}),Object(o.b)("p",null,"The ConfigeratorConfigSource plugin makes it possible for Hydra applications to consume a domain of configs from configerator."),Object(o.b)("h3",{id:"dependency"},"Dependency"),Object(o.b)("p",null,"Add the following to your ",Object(o.b)("inlineCode",{parentName:"p"},"TARGET")," file"),Object(o.b)("pre",null,Object(o.b)("code",Object(a.a)({parentName:"pre"},{className:"language-commandline"}),"//fair_infra/fbcode_hydra_plugins/configerator_config_source:configerator_config_source\n")),Object(o.b)("h3",{id:"usage"},"Usage"),Object(o.b)("ol",null,Object(o.b)("li",{parentName:"ol"},"The Configerator Config Source plugin requires that you place the configs under a ",Object(o.b)("a",Object(a.a)({parentName:"li"},{href:"https://fburl.com/wiki/n5cgchxe"}),"domain"),".\nYou can find an example domain ",Object(o.b)("a",Object(a.a)({parentName:"li"},{href:"https://fburl.com/diffusion/ms50g5hu"}),"here"))),Object(o.b)("div",{className:"admonition admonition-important alert alert--info"},Object(o.b)("div",Object(a.a)({parentName:"div"},{className:"admonition-heading"}),Object(o.b)("h5",{parentName:"div"},Object(o.b)("span",Object(a.a)({parentName:"h5"},{className:"admonition-icon"}),Object(o.b)("svg",Object(a.a)({parentName:"span"},{xmlns:"http://www.w3.org/2000/svg",width:"14",height:"16",viewBox:"0 0 14 16"}),Object(o.b)("path",Object(a.a)({parentName:"svg"},{fillRule:"evenodd",d:"M7 2.3c3.14 0 5.7 2.56 5.7 5.7s-2.56 5.7-5.7 5.7A5.71 5.71 0 0 1 1.3 8c0-3.14 2.56-5.7 5.7-5.7zM7 1C3.14 1 0 4.14 0 8s3.14 7 7 7 7-3.14 7-7-3.14-7-7-7zm1 3H6v5h2V4zm0 6H6v2h2v-2z"})))),"important")),Object(o.b)("div",Object(a.a)({parentName:"div"},{className:"admonition-content"}),Object(o.b)("p",{parentName:"div"},"Due to the limitations of Configerator APIs, matching the name of your domain and directory of configs is necessary for the plugin to extract information on the full config names.\nFor example, the config paths returned by Configerator API could look like ",Object(o.b)("inlineCode",{parentName:"p"},"fair_infra/hydra_plugins/configerator_config_source/example/db/mysql"),". The plugin needs to know where the directory of configs begins (",Object(o.b)("a",Object(a.a)({parentName:"p"},{href:"https://fburl.com/diffusion/7c0c5tig"}),Object(o.b)("inlineCode",{parentName:"a"},"example")),"), in order to determine the full config name (",Object(o.b)("inlineCode",{parentName:"p"},"db/mysql"),"). So in this case the domain should be named ",Object(o.b)("a",Object(a.a)({parentName:"p"},{href:"https://fburl.com/diffusion/pyymoo1t"}),Object(o.b)("inlineCode",{parentName:"a"},"example.cconf"))))),Object(o.b)("ol",{start:2},Object(o.b)("li",{parentName:"ol"},"Create a ",Object(o.b)("a",Object(a.a)({parentName:"li"},{href:"https://hydra.cc/docs/next/advanced/search_path"}),"SearchPathPlugin")," to add the Configerator path to the list of search paths.\nThe path you add in your SearchPathPlugin should be the name of your domain of configs, such as in this ",Object(o.b)("a",Object(a.a)({parentName:"li"},{href:"https://fburl.com/diffusion/ljggtux5"}),"example SearchPathPlugin"))),Object(o.b)("div",{className:"admonition admonition-info alert alert--info"},Object(o.b)("div",Object(a.a)({parentName:"div"},{className:"admonition-heading"}),Object(o.b)("h5",{parentName:"div"},Object(o.b)("span",Object(a.a)({parentName:"h5"},{className:"admonition-icon"}),Object(o.b)("svg",Object(a.a)({parentName:"span"},{xmlns:"http://www.w3.org/2000/svg",width:"14",height:"16",viewBox:"0 0 14 16"}),Object(o.b)("path",Object(a.a)({parentName:"svg"},{fillRule:"evenodd",d:"M7 2.3c3.14 0 5.7 2.56 5.7 5.7s-2.56 5.7-5.7 5.7A5.71 5.71 0 0 1 1.3 8c0-3.14 2.56-5.7 5.7-5.7zM7 1C3.14 1 0 4.14 0 8s3.14 7 7 7 7-3.14 7-7-3.14-7-7-7zm1 3H6v5h2V4zm0 6H6v2h2v-2z"})))),"info")),Object(o.b)("div",Object(a.a)({parentName:"div"},{className:"admonition-content"}),Object(o.b)("p",{parentName:"div"},"Adding a new search path will become much easier once ",Object(o.b)("a",Object(a.a)({parentName:"p"},{href:"https://github.com/facebookresearch/hydra/issues/274"}),"#274")," is resolved, which is planned for Hydra 1.1."))),Object(o.b)("h3",{id:"example"},"Example:"),Object(o.b)("h4",{id:"example-searchpathplugin"},"Example SearchPathPlugin"),Object(o.b)("p",null,Object(o.b)("a",Object(a.a)({parentName:"p"},{href:"https://fburl.com/diffusion/vwa82fbg"}),Object(o.b)("inlineCode",{parentName:"a"},"ConfigeratorExampleSearchPathPlugin"))," adds the example configerator domain to the search path of the example applications."),Object(o.b)("h4",{id:"reading-primary-config-from-configerator"},"Reading primary config from configerator"),Object(o.b)("p",null,"This example reads its primary config from configerator ",Object(o.b)("a",Object(a.a)({parentName:"p"},{href:"https://fburl.com/diffusion/twk3smkj"}),"here")," which has a default list defined."),Object(o.b)("pre",null,Object(o.b)("code",Object(a.a)({parentName:"pre"},{className:"language-commandline"}),"$ buck run //fair_infra/fbcode_hydra_plugins/configerator_config_source/example/primary_config:my_app \n...\nParsing buck files: finished in 1.1 sec\n...\n{'driver': 'mysql', 'user': 'alau'}\n")),Object(o.b)("h4",{id:"compose-config-with-configerator"},"Compose config with configerator"),Object(o.b)("p",null,"This example reads its primary config from local yaml file ",Object(o.b)("inlineCode",{parentName:"p"},"primary_config.yaml")," but reads config groups info from configerator."),Object(o.b)("pre",null,Object(o.b)("code",Object(a.a)({parentName:"pre"},{className:"language-commandline"}),"$ buck run //fair_infra/fbcode_hydra_plugins/configerator_config_source/example/config_group:my_app -- +db=mysql\n...\nParsing buck files: finished in 1.1 sec\n...\n{'foo': 'bar', 'driver': 'mysql', 'user': 'alau'}\n")))}s.isMDXComponent=!0},268:function(e,n,t){"use strict";t.d(n,"a",(function(){return p})),t.d(n,"b",(function(){return d}));var a=t(0),r=t.n(a);function o(e,n,t){return n in e?Object.defineProperty(e,n,{value:t,enumerable:!0,configurable:!0,writable:!0}):e[n]=t,e}function i(e,n){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);n&&(a=a.filter((function(n){return Object.getOwnPropertyDescriptor(e,n).enumerable}))),t.push.apply(t,a)}return t}function c(e){for(var n=1;n<arguments.length;n++){var t=null!=arguments[n]?arguments[n]:{};n%2?i(Object(t),!0).forEach((function(n){o(e,n,t[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):i(Object(t)).forEach((function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(t,n))}))}return e}function f(e,n){if(null==e)return{};var t,a,r=function(e,n){if(null==e)return{};var t,a,r={},o=Object.keys(e);for(a=0;a<o.length;a++)t=o[a],n.indexOf(t)>=0||(r[t]=e[t]);return r}(e,n);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(e);for(a=0;a<o.length;a++)t=o[a],n.indexOf(t)>=0||Object.prototype.propertyIsEnumerable.call(e,t)&&(r[t]=e[t])}return r}var l=r.a.createContext({}),s=function(e){var n=r.a.useContext(l),t=n;return e&&(t="function"==typeof e?e(n):c(c({},n),e)),t},p=function(e){var n=s(e.components);return r.a.createElement(l.Provider,{value:n},e.children)},b={inlineCode:"code",wrapper:function(e){var n=e.children;return r.a.createElement(r.a.Fragment,{},n)}},m=r.a.forwardRef((function(e,n){var t=e.components,a=e.mdxType,o=e.originalType,i=e.parentName,l=f(e,["components","mdxType","originalType","parentName"]),p=s(t),m=a,d=p["".concat(i,".").concat(m)]||p[m]||b[m]||o;return t?r.a.createElement(d,c(c({ref:n},l),{},{components:t})):r.a.createElement(d,c({ref:n},l))}));function d(e,n){var t=arguments,a=n&&n.mdxType;if("string"==typeof e||a){var o=t.length,i=new Array(o);i[0]=m;var c={};for(var f in n)hasOwnProperty.call(n,f)&&(c[f]=n[f]);c.originalType=e,c.mdxType="string"==typeof e?e:a,i[1]=c;for(var l=2;l<o;l++)i[l]=t[l];return r.a.createElement.apply(null,i)}return r.a.createElement.apply(null,t)}m.displayName="MDXCreateElement"}}]);