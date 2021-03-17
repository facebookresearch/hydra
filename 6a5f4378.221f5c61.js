(window.webpackJsonp=window.webpackJsonp||[]).push([[85],{156:function(e,t,n){"use strict";n.r(t),n.d(t,"frontMatter",(function(){return c})),n.d(t,"metadata",(function(){return s})),n.d(t,"toc",(function(){return u})),n.d(t,"default",(function(){return d}));var a=n(3),i=n(8),r=(n(0),n(268)),o=n(277),c={id:"specializing_config",title:"Specializing configuration"},s={unversionedId:"patterns/specializing_config",id:"patterns/specializing_config",isDocsHomePage:!1,title:"Specializing configuration",description:"In some cases the desired configuration should depend on other configuration choices.",source:"@site/docs/patterns/specializing_config.md",slug:"/patterns/specializing_config",permalink:"/docs/next/patterns/specializing_config",editUrl:"https://github.com/facebookresearch/hydra/edit/master/website/docs/patterns/specializing_config.md",version:"current",lastUpdatedBy:"Omry Yadan",lastUpdatedAt:1615952047,sidebar:"docs",previous:{title:"Selecting multiple configs from a Config Group",permalink:"/docs/next/patterns/select_multiple_configs_from_config_group"},next:{title:"Read-only config",permalink:"/docs/next/patterns/write_protect_config_node"}},u=[{value:"initial config.yaml",id:"initial-configyaml",children:[]},{value:"modified config.yaml",id:"modified-configyaml",children:[]},{value:"dataset_model/cifar10_alexnet.yaml",id:"dataset_modelcifar10_alexnetyaml",children:[]}],l={toc:u};function d(e){var t=e.components,n=Object(i.a)(e,["components"]);return Object(r.b)("wrapper",Object(a.a)({},l,n,{components:t,mdxType:"MDXLayout"}),Object(r.b)(o.a,{text:"Example application",to:"examples/patterns/specializing_config-select",mdxType:"ExampleGithubLink"}),Object(r.b)("p",null,"In some cases the desired configuration should depend on other configuration choices.\nFor example, You may want to use only 5 layers in your Alexnet model if the dataset of choice is cifar10, and the dafault 7 otherwise."),Object(r.b)("p",null,"We can start with a config that looks like this:"),Object(r.b)("h3",{id:"initial-configyaml"},"initial config.yaml"),Object(r.b)("pre",null,Object(r.b)("code",Object(a.a)({parentName:"pre"},{className:"language-yaml"}),"defaults:\n  - dataset: imagenet\n  - model: alexnet\n")),Object(r.b)("p",null,"We want to specialize the config based on the choice of the selected dataset and model:\nFurthermore, we only want to do it for cifar10 and alexnet and not for 3 other combinations."),Object(r.b)("p",null,"OmegaConf supports value interpolation, we can construct a value that would - at runtime - be a function of other values.\nThe idea is that we can add another element to the defaults list that would load a file name that depends on those two values:"),Object(r.b)("h3",{id:"modified-configyaml"},"modified config.yaml"),Object(r.b)("pre",null,Object(r.b)("code",Object(a.a)({parentName:"pre"},{className:"language-yaml"}),"defaults:\n  - dataset: imagenet\n  - model: alexnet\n  - optional dataset_model: ${dataset}_${model}\n")),Object(r.b)("p",null,"Let's break this down:"),Object(r.b)("h4",{id:"dataset_model"},"dataset_model"),Object(r.b)("p",null,"The key ",Object(r.b)("inlineCode",{parentName:"p"},"dataset_model")," is an arbitrary directory, it can be anything unique that makes sense, including nested directory like ",Object(r.b)("inlineCode",{parentName:"p"},"dataset/model"),"."),Object(r.b)("h4",{id:"dataset_model-1"},"${dataset}_${model}"),Object(r.b)("p",null,"the value ",Object(r.b)("inlineCode",{parentName:"p"},"${dataset}_${model}")," is using OmegaConf's ",Object(r.b)("a",Object(a.a)({parentName:"p"},{href:"https://omegaconf.readthedocs.io/en/latest/usage.html#variable-interpolation"}),"variable interpolation")," syntax.\nAt runtime, that value would resolve to ",Object(r.b)("em",{parentName:"p"},"imagenet_alexnet"),", or ",Object(r.b)("em",{parentName:"p"},"cifar_resnet")," - depending on the values of defaults.dataset and defaults.model."),Object(r.b)("div",{className:"admonition admonition-info alert alert--info"},Object(r.b)("div",Object(a.a)({parentName:"div"},{className:"admonition-heading"}),Object(r.b)("h5",{parentName:"div"},Object(r.b)("span",Object(a.a)({parentName:"h5"},{className:"admonition-icon"}),Object(r.b)("svg",Object(a.a)({parentName:"span"},{xmlns:"http://www.w3.org/2000/svg",width:"14",height:"16",viewBox:"0 0 14 16"}),Object(r.b)("path",Object(a.a)({parentName:"svg"},{fillRule:"evenodd",d:"M7 2.3c3.14 0 5.7 2.56 5.7 5.7s-2.56 5.7-5.7 5.7A5.71 5.71 0 0 1 1.3 8c0-3.14 2.56-5.7 5.7-5.7zM7 1C3.14 1 0 4.14 0 8s3.14 7 7 7 7-3.14 7-7-3.14-7-7-7zm1 3H6v5h2V4zm0 6H6v2h2v-2z"})))),"info")),Object(r.b)("div",Object(a.a)({parentName:"div"},{className:"admonition-content"}),Object(r.b)("p",{parentName:"div"},"This is non-standard interpolation and there are some subtle differences and limitations."))),Object(r.b)("h4",{id:"optional"},"optional"),Object(r.b)("p",null,"By default, Hydra fails with an error if a config specified in the defaults does not exist.\nIn this case we only want to specialize cifar10 + alexnet, not all 4 combinations.\nthe keyword ",Object(r.b)("inlineCode",{parentName:"p"},"optional")," tells Hydra to just continue if it can't find this file."),Object(r.b)("p",null,"When specializing config, you usually want to only specify what's different, and not the whole thing.\nWe want the model for alexnet, when trained on cifar - to have 5 layers."),Object(r.b)("h3",{id:"dataset_modelcifar10_alexnetyaml"},"dataset_model/cifar10_alexnet.yaml"),Object(r.b)("pre",null,Object(r.b)("code",Object(a.a)({parentName:"pre"},{className:"language-yaml"}),"model:\n  num_layers: 5\n")),Object(r.b)("p",null,"Let's check. Running with the default uses imagenet, so we don't get the specialized version of:"),Object(r.b)("pre",null,Object(r.b)("code",Object(a.a)({parentName:"pre"},{className:"language-yaml"}),"$ python example.py \ndataset:\n  name: imagenet\n  path: /datasets/imagenet\nmodel:\n  num_layers: 7\n  type: alexnet\n")),Object(r.b)("p",null,"Running with cifar10 dataset, we do get 5 for num_layers:"),Object(r.b)("pre",null,Object(r.b)("code",Object(a.a)({parentName:"pre"},{className:"language-yaml"}),"$ python example.py dataset=cifar10\ndataset:\n  name: cifar10\n  path: /datasets/cifar10\nmodel:\n  num_layers: 5\n  type: alexnet\n")))}d.isMDXComponent=!0},268:function(e,t,n){"use strict";n.d(t,"a",(function(){return d})),n.d(t,"b",(function(){return m}));var a=n(0),i=n.n(a);function r(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function o(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);t&&(a=a.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,a)}return n}function c(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?o(Object(n),!0).forEach((function(t){r(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):o(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function s(e,t){if(null==e)return{};var n,a,i=function(e,t){if(null==e)return{};var n,a,i={},r=Object.keys(e);for(a=0;a<r.length;a++)n=r[a],t.indexOf(n)>=0||(i[n]=e[n]);return i}(e,t);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);for(a=0;a<r.length;a++)n=r[a],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(i[n]=e[n])}return i}var u=i.a.createContext({}),l=function(e){var t=i.a.useContext(u),n=t;return e&&(n="function"==typeof e?e(t):c(c({},t),e)),n},d=function(e){var t=l(e.components);return i.a.createElement(u.Provider,{value:t},e.children)},f={inlineCode:"code",wrapper:function(e){var t=e.children;return i.a.createElement(i.a.Fragment,{},t)}},p=i.a.forwardRef((function(e,t){var n=e.components,a=e.mdxType,r=e.originalType,o=e.parentName,u=s(e,["components","mdxType","originalType","parentName"]),d=l(n),p=a,m=d["".concat(o,".").concat(p)]||d[p]||f[p]||r;return n?i.a.createElement(m,c(c({ref:t},u),{},{components:n})):i.a.createElement(m,c({ref:t},u))}));function m(e,t){var n=arguments,a=t&&t.mdxType;if("string"==typeof e||a){var r=n.length,o=new Array(r);o[0]=p;var c={};for(var s in t)hasOwnProperty.call(t,s)&&(c[s]=t[s]);c.originalType=e,c.mdxType="string"==typeof e?e:a,o[1]=c;for(var u=2;u<r;u++)o[u]=n[u];return i.a.createElement.apply(null,o)}return i.a.createElement.apply(null,n)}p.displayName="MDXCreateElement"},269:function(e,t,n){"use strict";function a(e){return!0===/^(\w*:|\/\/)/.test(e)}function i(e){return void 0!==e&&!a(e)}n.d(t,"b",(function(){return a})),n.d(t,"a",(function(){return i}))},270:function(e,t,n){"use strict";n.r(t);var a=n(11);n.d(t,"MemoryRouter",(function(){return a.d})),n.d(t,"Prompt",(function(){return a.f})),n.d(t,"Redirect",(function(){return a.g})),n.d(t,"Route",(function(){return a.h})),n.d(t,"Router",(function(){return a.i})),n.d(t,"StaticRouter",(function(){return a.j})),n.d(t,"Switch",(function(){return a.k})),n.d(t,"generatePath",(function(){return a.l})),n.d(t,"matchPath",(function(){return a.m})),n.d(t,"useHistory",(function(){return a.n})),n.d(t,"useLocation",(function(){return a.o})),n.d(t,"useParams",(function(){return a.p})),n.d(t,"useRouteMatch",(function(){return a.q})),n.d(t,"withRouter",(function(){return a.r})),n.d(t,"BrowserRouter",(function(){return a.a})),n.d(t,"HashRouter",(function(){return a.b})),n.d(t,"Link",(function(){return a.c})),n.d(t,"NavLink",(function(){return a.e}))},271:function(e,t,n){"use strict";var a=n(0),i=n.n(a),r=n(11),o=n(269),c=n(7),s=Object(a.createContext)({collectLink:function(){}}),u=n(272),l=function(e,t){var n={};for(var a in e)Object.prototype.hasOwnProperty.call(e,a)&&t.indexOf(a)<0&&(n[a]=e[a]);if(null!=e&&"function"==typeof Object.getOwnPropertySymbols){var i=0;for(a=Object.getOwnPropertySymbols(e);i<a.length;i++)t.indexOf(a[i])<0&&Object.prototype.propertyIsEnumerable.call(e,a[i])&&(n[a[i]]=e[a[i]])}return n};t.a=function(e){var t,n,d,f=e.isNavLink,p=e.to,m=e.href,b=e.activeClassName,g=e.isActive,v=e["data-noBrokenLinkCheck"],h=e.autoAddBaseUrl,O=void 0===h||h,y=l(e,["isNavLink","to","href","activeClassName","isActive","data-noBrokenLinkCheck","autoAddBaseUrl"]),j=Object(u.b)().withBaseUrl,w=Object(a.useContext)(s),x=p||m,D=Object(o.a)(x),_=null==x?void 0:x.replace("pathname://",""),P=void 0!==_?(n=_,O&&function(e){return e.startsWith("/")}(n)?j(n):n):void 0,A=Object(a.useRef)(!1),N=f?r.e:r.c,k=c.a.canUseIntersectionObserver;Object(a.useEffect)((function(){return!k&&D&&window.docusaurus.prefetch(P),function(){k&&d&&d.disconnect()}}),[P,k,D]);var V=null!==(t=null==P?void 0:P.startsWith("#"))&&void 0!==t&&t,E=!P||!D||V;return P&&D&&!V&&!v&&w.collectLink(P),E?i.a.createElement("a",Object.assign({href:P},x&&!D&&{target:"_blank",rel:"noopener noreferrer"},y)):i.a.createElement(N,Object.assign({},y,{onMouseEnter:function(){A.current||(window.docusaurus.preload(P),A.current=!0)},innerRef:function(e){var t,n;k&&e&&D&&(t=e,n=function(){window.docusaurus.prefetch(P)},(d=new window.IntersectionObserver((function(e){e.forEach((function(e){t===e.target&&(e.isIntersecting||e.intersectionRatio>0)&&(d.unobserve(t),d.disconnect(),n())}))}))).observe(t))},to:P||""},f&&{isActive:g,activeClassName:b}))}},272:function(e,t,n){"use strict";n.d(t,"b",(function(){return r})),n.d(t,"a",(function(){return o}));var a=n(21),i=n(269);function r(){var e=Object(a.default)().siteConfig,t=(e=void 0===e?{}:e).baseUrl,n=void 0===t?"/":t,r=e.url;return{withBaseUrl:function(e,t){return function(e,t,n,a){var r=void 0===a?{}:a,o=r.forcePrependBaseUrl,c=void 0!==o&&o,s=r.absolute,u=void 0!==s&&s;if(!n)return n;if(n.startsWith("#"))return n;if(Object(i.b)(n))return n;if(c)return t+n;var l=n.startsWith(t)?n:t+n.replace(/^\//,"");return u?e+l:l}(r,n,e,t)}}}function o(e,t){return void 0===t&&(t={}),(0,r().withBaseUrl)(e,t)}},273:function(e,t,n){try{e.exports=n(274)}catch(a){e.exports={}}},274:function(e,t,n){"use strict";Object.defineProperty(t,"__esModule",{value:!0}),t.useDocVersionSuggestions=t.useActiveDocContext=t.useActiveVersion=t.useLatestVersion=t.useVersions=t.useActivePluginAndVersion=t.useActivePlugin=t.useDocsData=t.useAllDocsData=void 0;var a=n(270),i=n(275),r=n(276);t.useAllDocsData=function(){return i.useAllPluginInstancesData("docusaurus-plugin-content-docs")},t.useDocsData=function(e){return i.usePluginData("docusaurus-plugin-content-docs",e)},t.useActivePlugin=function(e){void 0===e&&(e={});var n=t.useAllDocsData(),i=a.useLocation().pathname;return r.getActivePlugin(n,i,e)},t.useActivePluginAndVersion=function(e){void 0===e&&(e={});var n=t.useActivePlugin(e),i=a.useLocation().pathname;if(n)return{activePlugin:n,activeVersion:r.getActiveVersion(n.pluginData,i)}},t.useVersions=function(e){return t.useDocsData(e).versions},t.useLatestVersion=function(e){var n=t.useDocsData(e);return r.getLatestVersion(n)},t.useActiveVersion=function(e){var n=t.useDocsData(e),i=a.useLocation().pathname;return r.getActiveVersion(n,i)},t.useActiveDocContext=function(e){var n=t.useDocsData(e),i=a.useLocation().pathname;return r.getActiveDocContext(n,i)},t.useDocVersionSuggestions=function(e){var n=t.useDocsData(e),i=a.useLocation().pathname;return r.getDocVersionSuggestions(n,i)}},275:function(e,t,n){"use strict";n.r(t),n.d(t,"default",(function(){return i})),n.d(t,"useAllPluginInstancesData",(function(){return r})),n.d(t,"usePluginData",(function(){return o}));var a=n(21);function i(){var e=Object(a.default)().globalData;if(!e)throw new Error("Docusaurus global data not found");return e}function r(e){var t=i()[e];if(!t)throw new Error("Docusaurus plugin global data not found for pluginName="+e);return t}function o(e,t){void 0===t&&(t="default");var n=r(e)[t];if(!n)throw new Error("Docusaurus plugin global data not found for pluginName="+e+" and pluginId="+t);return n}},276:function(e,t,n){"use strict";Object.defineProperty(t,"__esModule",{value:!0}),t.getDocVersionSuggestions=t.getActiveDocContext=t.getActiveVersion=t.getLatestVersion=t.getActivePlugin=void 0;var a=n(270);t.getActivePlugin=function(e,t,n){void 0===n&&(n={});var i=Object.entries(e).find((function(e){e[0];var n=e[1];return!!a.matchPath(t,{path:n.path,exact:!1,strict:!1})})),r=i?{pluginId:i[0],pluginData:i[1]}:void 0;if(!r&&n.failfast)throw new Error("Can't find active docs plugin for pathname="+t+", while it was expected to be found. Maybe you tried to use a docs feature that can only be used on a docs-related page? Existing docs plugin paths are: "+Object.values(e).map((function(e){return e.path})).join(", "));return r},t.getLatestVersion=function(e){return e.versions.find((function(e){return e.isLast}))},t.getActiveVersion=function(e,n){var i=t.getLatestVersion(e);return[].concat(e.versions.filter((function(e){return e!==i})),[i]).find((function(e){return!!a.matchPath(n,{path:e.path,exact:!1,strict:!1})}))},t.getActiveDocContext=function(e,n){var i,r,o=t.getActiveVersion(e,n),c=null==o?void 0:o.docs.find((function(e){return!!a.matchPath(n,{path:e.path,exact:!0,strict:!1})}));return{activeVersion:o,activeDoc:c,alternateDocVersions:c?(i=c.id,r={},e.versions.forEach((function(e){e.docs.forEach((function(t){t.id===i&&(r[e.name]=t)}))})),r):{}}},t.getDocVersionSuggestions=function(e,n){var a=t.getLatestVersion(e),i=t.getActiveDocContext(e,n),r=i.activeVersion!==a;return{latestDocSuggestion:r?null==i?void 0:i.alternateDocVersions[a.name]:void 0,latestVersionSuggestion:r?a:void 0}}},277:function(e,t,n){"use strict";n.d(t,"b",(function(){return u})),n.d(t,"a",(function(){return l}));var a=n(3),i=n(0),r=n.n(i),o=n(271),c=n(21),s=n(273);function u(e){return r.a.createElement(o.a,Object(a.a)({},e,{to:(t=e.to,i=Object(s.useActiveVersion)(),Object(c.default)().siteConfig.customFields.githubLinkVersionToBaseUrl[null!==(n=null==i?void 0:i.name)&&void 0!==n?n:"current"]+t),target:"_blank"}));var t,n,i}function l(e){var t,n=null!==(t=e.text)&&void 0!==t?t:"Example";return r.a.createElement(u,e,r.a.createElement("span",null,"\xa0"),r.a.createElement("img",{src:"https://img.shields.io/badge/-"+n+"-informational",alt:"Example"}))}}}]);