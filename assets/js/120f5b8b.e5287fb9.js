"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[3951],{15680:(e,t,r)=>{r.r(t),r.d(t,{MDXContext:()=>u,MDXProvider:()=>m,mdx:()=>y,useMDXComponents:()=>c,withMDXComponents:()=>p});var n=r(96540);function o(e,t,r){return t in e?Object.defineProperty(e,t,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[t]=r,e}function a(){return a=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var r=arguments[t];for(var n in r)Object.prototype.hasOwnProperty.call(r,n)&&(e[n]=r[n])}return e},a.apply(this,arguments)}function i(e,t){var r=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);t&&(n=n.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),r.push.apply(r,n)}return r}function l(e){for(var t=1;t<arguments.length;t++){var r=null!=arguments[t]?arguments[t]:{};t%2?i(Object(r),!0).forEach((function(t){o(e,t,r[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(r)):i(Object(r)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(r,t))}))}return e}function s(e,t){if(null==e)return{};var r,n,o=function(e,t){if(null==e)return{};var r,n,o={},a=Object.keys(e);for(n=0;n<a.length;n++)r=a[n],t.indexOf(r)>=0||(o[r]=e[r]);return o}(e,t);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);for(n=0;n<a.length;n++)r=a[n],t.indexOf(r)>=0||Object.prototype.propertyIsEnumerable.call(e,r)&&(o[r]=e[r])}return o}var u=n.createContext({}),p=function(e){return function(t){var r=c(t.components);return n.createElement(e,a({},t,{components:r}))}},c=function(e){var t=n.useContext(u),r=t;return e&&(r="function"==typeof e?e(t):l(l({},t),e)),r},m=function(e){var t=c(e.components);return n.createElement(u.Provider,{value:t},e.children)},d={inlineCode:"code",wrapper:function(e){var t=e.children;return n.createElement(n.Fragment,{},t)}},f=n.forwardRef((function(e,t){var r=e.components,o=e.mdxType,a=e.originalType,i=e.parentName,u=s(e,["components","mdxType","originalType","parentName"]),p=c(r),m=o,f=p["".concat(i,".").concat(m)]||p[m]||d[m]||a;return r?n.createElement(f,l(l({ref:t},u),{},{components:r})):n.createElement(f,l({ref:t},u))}));function y(e,t){var r=arguments,o=t&&t.mdxType;if("string"==typeof e||o){var a=r.length,i=new Array(a);i[0]=f;var l={};for(var s in t)hasOwnProperty.call(t,s)&&(l[s]=t[s]);l.originalType=e,l.mdxType="string"==typeof e?e:o,i[1]=l;for(var u=2;u<a;u++)i[u]=r[u];return n.createElement.apply(null,i)}return n.createElement.apply(null,r)}f.displayName="MDXCreateElement"},56948:(e,t,r)=>{r.r(t),r.d(t,{contentTitle:()=>s,default:()=>m,frontMatter:()=>l,metadata:()=>u,toc:()=>p});var n=r(58168),o=r(98587),a=(r(96540),r(15680)),i=["components"],l={id:"multi-run",title:"Multi-run",sidebar_label:"Multi-run"},s=void 0,u={unversionedId:"tutorial/multi-run",id:"version-0.11/tutorial/multi-run",title:"Multi-run",description:"Sometimes you want to run a parameter sweep.",source:"@site/versioned_docs/version-0.11/tutorial/6_multirun.md",sourceDirName:"tutorial",slug:"/tutorial/multi-run",permalink:"/docs/0.11/tutorial/multi-run",editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/versioned_docs/version-0.11/tutorial/6_multirun.md",tags:[],version:"0.11",lastUpdatedBy:"dependabot[bot]",lastUpdatedAt:1730135614,formattedLastUpdatedAt:"10/28/2024",sidebarPosition:6,frontMatter:{id:"multi-run",title:"Multi-run",sidebar_label:"Multi-run"},sidebar:"version-0.11/docs",previous:{title:"Config composition",permalink:"/docs/0.11/tutorial/composition"},next:{title:"Tab completion",permalink:"/docs/0.11/tutorial/tab_completion"}},p=[],c={toc:p};function m(e){var t=e.components,r=(0,o.A)(e,i);return(0,a.mdx)("wrapper",(0,n.A)({},c,r,{components:t,mdxType:"MDXLayout"}),(0,a.mdx)("p",null,"Sometimes you want to run a parameter sweep.\nTo run a parameter sweep, use the ",(0,a.mdx)("inlineCode",{parentName:"p"},"--multirun")," (",(0,a.mdx)("inlineCode",{parentName:"p"},"-m"),") flag and pass a comma separated list for each\ndimension you want to sweep."),(0,a.mdx)("p",null,"Here is a sweep over the db types (mysql,postgresql) and the schemas (warehouse,support,school).\nOutput does not contain the configuration prints."),(0,a.mdx)("pre",null,(0,a.mdx)("code",{parentName:"pre",className:"language-text"}," $ python tutorial/50_composition/my_app.py schema=warehouse,support,school db=mysql,postgresql -m\n[2019-10-01 14:44:16,254] - Launching 6 jobs locally\n[2019-10-01 14:44:16,254] - Sweep output dir : multirun/2019-10-01/14-44-16\n[2019-10-01 14:44:16,254] -     #0 : schema=warehouse db=mysql\n[2019-10-01 14:44:16,321] -     #1 : schema=warehouse db=postgresql\n[2019-10-01 14:44:16,390] -     #2 : schema=support db=mysql\n[2019-10-01 14:44:16,458] -     #3 : schema=support db=postgresql\n[2019-10-01 14:44:16,527] -     #4 : schema=school db=mysql\n[2019-10-01 14:44:16,602] -     #5 : schema=school db=postgresql\n")),(0,a.mdx)("p",null,"The default launcher runs the jobs locally and serially."),(0,a.mdx)("p",null,"There are plans to add additional Launchers, such as a Launcher that launches your application code on AWS."))}m.isMDXComponent=!0}}]);