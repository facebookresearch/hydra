(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[5263],{3905:function(e,t,n){"use strict";n.d(t,{Zo:function(){return m},kt:function(){return g}});var r=n(7294);function a(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function i(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,r)}return n}function l(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?i(Object(n),!0).forEach((function(t){a(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):i(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function o(e,t){if(null==e)return{};var n,r,a=function(e,t){if(null==e)return{};var n,r,a={},i=Object.keys(e);for(r=0;r<i.length;r++)n=i[r],t.indexOf(n)>=0||(a[n]=e[n]);return a}(e,t);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);for(r=0;r<i.length;r++)n=i[r],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(a[n]=e[n])}return a}var p=r.createContext({}),s=function(e){var t=r.useContext(p),n=t;return e&&(n="function"==typeof e?e(t):l(l({},t),e)),n},m=function(e){var t=s(e.components);return r.createElement(p.Provider,{value:t},e.children)},c={inlineCode:"code",wrapper:function(e){var t=e.children;return r.createElement(r.Fragment,{},t)}},u=r.forwardRef((function(e,t){var n=e.components,a=e.mdxType,i=e.originalType,p=e.parentName,m=o(e,["components","mdxType","originalType","parentName"]),u=s(n),g=a,d=u["".concat(p,".").concat(g)]||u[g]||c[g]||i;return n?r.createElement(d,l(l({ref:t},m),{},{components:n})):r.createElement(d,l({ref:t},m))}));function g(e,t){var n=arguments,a=t&&t.mdxType;if("string"==typeof e||a){var i=n.length,l=new Array(i);l[0]=u;var o={};for(var p in t)hasOwnProperty.call(t,p)&&(o[p]=t[p]);o.originalType=e,o.mdxType="string"==typeof e?e:a,l[1]=o;for(var s=2;s<i;s++)l[s]=n[s];return r.createElement.apply(null,l)}return r.createElement.apply(null,n)}u.displayName="MDXCreateElement"},3899:function(e,t,n){"use strict";n.d(t,{Z:function(){return p},T:function(){return s}});var r=n(2122),a=n(7294),i=n(6742),l=n(2263),o=n(907);function p(e){return a.createElement(i.Z,(0,r.Z)({},e,{to:(t=e.to,p=(0,o.zu)(),(0,l.default)().siteConfig.customFields.githubLinkVersionToBaseUrl[null!=(n=null==p?void 0:p.name)?n:"current"]+t),target:"_blank"}));var t,n,p}function s(e){var t,n=null!=(t=e.text)?t:"Example";return a.createElement(p,e,a.createElement("span",null,"\xa0"),a.createElement("img",{src:"https://img.shields.io/badge/-"+n+"-informational",alt:"Example"}))}},8624:function(e,t,n){"use strict";n.r(t),n.d(t,{frontMatter:function(){return p},contentTitle:function(){return s},metadata:function(){return m},toc:function(){return c},default:function(){return g}});var r=n(2122),a=n(9756),i=(n(7294),n(3905)),l=n(3899),o=["components"],p={id:"configuring_experiments",title:"Configuring Experiments"},s=void 0,m={unversionedId:"patterns/configuring_experiments",id:"patterns/configuring_experiments",isDocsHomePage:!1,title:"Configuring Experiments",description:"Problem",source:"@site/docs/patterns/configuring_experiments.md",sourceDirName:"patterns",slug:"/patterns/configuring_experiments",permalink:"/docs/next/patterns/configuring_experiments",editUrl:"https://github.com/facebookresearch/hydra/edit/master/website/docs/patterns/configuring_experiments.md",version:"current",lastUpdatedBy:"dependabot[bot]",lastUpdatedAt:1629316222,formattedLastUpdatedAt:"8/18/2021",frontMatter:{id:"configuring_experiments",title:"Configuring Experiments"},sidebar:"docs",previous:{title:"Extending Configs",permalink:"/docs/next/patterns/extending_configs"},next:{title:"Configuring Plugins",permalink:"/docs/next/patterns/configuring_plugins"}},c=[{value:"Problem",id:"problem",children:[]},{value:"Solution",id:"solution",children:[]},{value:"Example",id:"example",children:[]},{value:"Sweeping over experiments",id:"sweeping-over-experiments",children:[]}],u={toc:c};function g(e){var t=e.components,n=(0,a.Z)(e,o);return(0,i.kt)("wrapper",(0,r.Z)({},u,n,{components:t,mdxType:"MDXLayout"}),(0,i.kt)(l.T,{text:"Example application",to:"examples/patterns/configuring_experiments",mdxType:"ExampleGithubLink"}),(0,i.kt)("h3",{id:"problem"},"Problem"),(0,i.kt)("p",null,"A common problem is maintaining multiple configurations of an application.  This can get especially\ntedious when the configuration differences span multiple dimensions.\nThis pattern shows how to cleanly support multiple configurations, with each configuration file only specifying\nthe changes to the master (default) configuration."),(0,i.kt)("h3",{id:"solution"},"Solution"),(0,i.kt)("p",null,"Create a config file specifying the overrides to the default configuration, and then call it via the command line.\ne.g. ",(0,i.kt)("inlineCode",{parentName:"p"},"$ python my_app.py +experiment=fast_mode"),"."),(0,i.kt)("p",null,"To avoid clutter, we place the experiment config files in dedicated config group called ",(0,i.kt)("em",{parentName:"p"},"experiment"),"."),(0,i.kt)("h3",{id:"example"},"Example"),(0,i.kt)("p",null,"In this example, we will create configurations for each of the server and database pairings that we want to benchmark."),(0,i.kt)("p",null,"The default configuration is:"),(0,i.kt)("div",{className:"row"},(0,i.kt)("div",{className:"col col--4"},(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-yaml",metastring:'title="config.yaml"',title:'"config.yaml"'},"defaults:\n  - db: mysql\n  - server: apache\n\n\n\n\n\n"))),(0,i.kt)("div",{className:"col col--4"},(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-yaml",metastring:'title="db/mysql.yaml"',title:'"db/mysql.yaml"'},"name: mysql\n")),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-yaml",metastring:'title="server/apache.yaml"',title:'"server/apache.yaml"'},"name: apache\nport: 80\n"))),(0,i.kt)("div",{className:"col col--4"},(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-yaml",metastring:'title="db/sqlite.yaml"',title:'"db/sqlite.yaml"'},"name: sqlite\n")),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-yaml",metastring:'title="server/nginx.yaml"',title:'"server/nginx.yaml"'},"name: nginx\nport: 80\n")))),(0,i.kt)("div",{className:"row"},(0,i.kt)("div",{className:"col col--6"},(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-text",metastring:'title="Directory structure"',title:'"Directory','structure"':!0},"\u251c\u2500\u2500 config.yaml\n\u251c\u2500\u2500 db\n\u2502   \u251c\u2500\u2500 mysql.yaml\n\u2502   \u2514\u2500\u2500 sqlite.yaml\n\u2514\u2500\u2500 server\n    \u251c\u2500\u2500 apache.yaml\n    \u2514\u2500\u2500 nginx.yaml\n"))),(0,i.kt)("div",{className:"col col--6"},(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-yaml",metastring:'title="$ python my_app.py"',title:'"$',python:!0,'my_app.py"':!0},"db:\n  name: mysql\nserver:\n  name: apache\n  port: 80\n\n\n")))),(0,i.kt)("p",null,"The benchmark config files specify the deltas from the default configuration:"),(0,i.kt)("div",{className:"row"},(0,i.kt)("div",{className:"col col--6"},(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-yaml",metastring:'title="experiment/aplite.yaml"',title:'"experiment/aplite.yaml"'},"# @package _global_\ndefaults:\n  - override /db: sqlite\n  \n  \nserver:\n  port: 8080\n"))),(0,i.kt)("div",{className:"col col--6"},(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-yaml",metastring:'title="experiment/nglite.yaml"',title:'"experiment/nglite.yaml"'},"# @package _global_\ndefaults:\n  - override /db: sqlite\n  - override /server: nginx\n  \nserver:\n  port: 8080\n")))),(0,i.kt)("div",{className:"row"},(0,i.kt)("div",{className:"col col--6"},(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-yaml",metastring:'title="$ python my_app.py +experiment=aplite"',title:'"$',python:!0,"my_app.py":!0,"+experiment":'aplite"'},"db:\n  name: sqlite\nserver:\n  name: apache\n  port: 8080\n"))),(0,i.kt)("div",{className:"col col--6"},(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-yaml",metastring:'title="$ python my_app.py +experiment=nglite"',title:'"$',python:!0,"my_app.py":!0,"+experiment":'nglite"'},"db:\n  name: sqlite\nserver:\n  name: nginx\n  port: 8080\n")))),(0,i.kt)("p",null,"Key concepts:"),(0,i.kt)("ul",null,(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("strong",{parentName:"li"},"#"," @package ","_","global","_"),(0,i.kt)("br",{parentName:"li"}),"Changes specified in this config should be interpreted as relative to the ","_","global","_"," package.",(0,i.kt)("br",{parentName:"li"}),"We could instead place ",(0,i.kt)("em",{parentName:"li"},"nglite.yaml")," and ",(0,i.kt)("em",{parentName:"li"},"aplite.yaml")," next to ",(0,i.kt)("em",{parentName:"li"},"config.yaml")," and omit this line."),(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("strong",{parentName:"li"},"The overrides of /db and /server are absolute paths."),(0,i.kt)("br",{parentName:"li"}),"This is necessary because they are outside of the experiment directory. ")),(0,i.kt)("p",null,"Running the experiments from the command line requires prefixing the experiment choice with a ",(0,i.kt)("inlineCode",{parentName:"p"},"+"),".\nThe experiment config group is an addition, not an override."),(0,i.kt)("h3",{id:"sweeping-over-experiments"},"Sweeping over experiments"),(0,i.kt)("p",null,"This approach also enables sweeping over those experiments to easily compare their results:"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-text",metastring:'title="$ python my_app.py --multirun +experiment=aplite,nglite"',title:'"$',python:!0,"my_app.py":!0,"--multirun":!0,"+experiment":'aplite,nglite"'},"[HYDRA] Launching 2 jobs locally\n[HYDRA]        #0 : +experiment=aplite\ndb:\n  name: sqlite\nserver:\n  name: apache\n  port: 8080\n\n[HYDRA]        #1 : +experiment=nglite\ndb:\n  name: sqlite\nserver:\n  name: nginx\n  port: 8080\n")),(0,i.kt)("p",null,"To run all the experiments, use the ",(0,i.kt)("a",{parentName:"p",href:"/docs/next/advanced/override_grammar/extended#glob-choice-sweep"},"glob")," syntax:"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-text",metastring:"title=\"$ python my_app.py --multirun '+experiment=glob(*)'\"",title:'"$',python:!0,"my_app.py":!0,"--multirun":!0,"'+experiment":"glob(*)'\""},"[HYDRA]        #0 : +experiment=aplite\n...\n[HYDRA]        #1 : +experiment=nglite\n...\n")))}g.isMDXComponent=!0}}]);