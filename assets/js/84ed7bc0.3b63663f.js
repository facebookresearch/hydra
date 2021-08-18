(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[1005],{3905:function(e,t,r){"use strict";r.d(t,{Zo:function(){return c},kt:function(){return m}});var n=r(7294);function o(e,t,r){return t in e?Object.defineProperty(e,t,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[t]=r,e}function a(e,t){var r=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);t&&(n=n.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),r.push.apply(r,n)}return r}function i(e){for(var t=1;t<arguments.length;t++){var r=null!=arguments[t]?arguments[t]:{};t%2?a(Object(r),!0).forEach((function(t){o(e,t,r[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(r)):a(Object(r)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(r,t))}))}return e}function l(e,t){if(null==e)return{};var r,n,o=function(e,t){if(null==e)return{};var r,n,o={},a=Object.keys(e);for(n=0;n<a.length;n++)r=a[n],t.indexOf(r)>=0||(o[r]=e[r]);return o}(e,t);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);for(n=0;n<a.length;n++)r=a[n],t.indexOf(r)>=0||Object.prototype.propertyIsEnumerable.call(e,r)&&(o[r]=e[r])}return o}var p=n.createContext({}),s=function(e){var t=n.useContext(p),r=t;return e&&(r="function"==typeof e?e(t):i(i({},t),e)),r},c=function(e){var t=s(e.components);return n.createElement(p.Provider,{value:t},e.children)},u={inlineCode:"code",wrapper:function(e){var t=e.children;return n.createElement(n.Fragment,{},t)}},d=n.forwardRef((function(e,t){var r=e.components,o=e.mdxType,a=e.originalType,p=e.parentName,c=l(e,["components","mdxType","originalType","parentName"]),d=s(r),m=o,f=d["".concat(p,".").concat(m)]||d[m]||u[m]||a;return r?n.createElement(f,i(i({ref:t},c),{},{components:r})):n.createElement(f,i({ref:t},c))}));function m(e,t){var r=arguments,o=t&&t.mdxType;if("string"==typeof e||o){var a=r.length,i=new Array(a);i[0]=d;var l={};for(var p in t)hasOwnProperty.call(t,p)&&(l[p]=t[p]);l.originalType=e,l.mdxType="string"==typeof e?e:o,i[1]=l;for(var s=2;s<a;s++)i[s]=r[s];return n.createElement.apply(null,i)}return n.createElement.apply(null,r)}d.displayName="MDXCreateElement"},7928:function(e,t,r){"use strict";r.r(t),r.d(t,{frontMatter:function(){return l},contentTitle:function(){return p},metadata:function(){return s},toc:function(){return c},default:function(){return d}});var n=r(2122),o=r(9756),a=(r(7294),r(3905)),i=["components"],l={id:"release",title:"Release process",sidebar_label:"Release process"},p=void 0,s={unversionedId:"development/release",id:"version-1.0/development/release",isDocsHomePage:!1,title:"Release process",description:"The release process may be automated in the future.",source:"@site/versioned_docs/version-1.0/development/release.md",sourceDirName:"development",slug:"/development/release",permalink:"/docs/1.0/development/release",editUrl:"https://github.com/facebookresearch/hydra/edit/master/website/versioned_docs/version-1.0/development/release.md",version:"1.0",lastUpdatedBy:"dependabot[bot]",lastUpdatedAt:1629316222,formattedLastUpdatedAt:"8/18/2021",frontMatter:{id:"release",title:"Release process",sidebar_label:"Release process"},sidebar:"version-1.0/docs",previous:{title:"Documentation",permalink:"/docs/1.0/development/documentation"},next:{title:"Config path changes",permalink:"/docs/1.0/upgrades/0.11_to_1.0/config_path_changes"}},c=[],u={toc:c};function d(e){var t=e.components,r=(0,o.Z)(e,i);return(0,a.kt)("wrapper",(0,n.Z)({},u,r,{components:t,mdxType:"MDXLayout"}),(0,a.kt)("p",null,"The release process may be automated in the future."),(0,a.kt)("ul",null,(0,a.kt)("li",{parentName:"ul"},"Checkout master"),(0,a.kt)("li",{parentName:"ul"},"Update the Hydra version in ",(0,a.kt)("inlineCode",{parentName:"li"},"hydra/__init__.py")),(0,a.kt)("li",{parentName:"ul"},"Update NEWS.md with towncrier"),(0,a.kt)("li",{parentName:"ul"},"Create a pip package for hydra-core: ",(0,a.kt)("inlineCode",{parentName:"li"},"python setup.py sdist bdist_wheel")),(0,a.kt)("li",{parentName:"ul"},"Upload pip package: ",(0,a.kt)("inlineCode",{parentName:"li"},"python -m twine upload dist/*"))))}d.isMDXComponent=!0}}]);