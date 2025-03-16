"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[7060],{15680:(e,r,t)=>{t.r(r),t.d(r,{MDXContext:()=>s,MDXProvider:()=>l,mdx:()=>f,useMDXComponents:()=>u,withMDXComponents:()=>p});var n=t(96540);function o(e,r,t){return r in e?Object.defineProperty(e,r,{value:t,enumerable:!0,configurable:!0,writable:!0}):e[r]=t,e}function i(){return i=Object.assign||function(e){for(var r=1;r<arguments.length;r++){var t=arguments[r];for(var n in t)Object.prototype.hasOwnProperty.call(t,n)&&(e[n]=t[n])}return e},i.apply(this,arguments)}function a(e,r){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);r&&(n=n.filter((function(r){return Object.getOwnPropertyDescriptor(e,r).enumerable}))),t.push.apply(t,n)}return t}function d(e){for(var r=1;r<arguments.length;r++){var t=null!=arguments[r]?arguments[r]:{};r%2?a(Object(t),!0).forEach((function(r){o(e,r,t[r])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):a(Object(t)).forEach((function(r){Object.defineProperty(e,r,Object.getOwnPropertyDescriptor(t,r))}))}return e}function c(e,r){if(null==e)return{};var t,n,o=function(e,r){if(null==e)return{};var t,n,o={},i=Object.keys(e);for(n=0;n<i.length;n++)t=i[n],r.indexOf(t)>=0||(o[t]=e[t]);return o}(e,r);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);for(n=0;n<i.length;n++)t=i[n],r.indexOf(t)>=0||Object.prototype.propertyIsEnumerable.call(e,t)&&(o[t]=e[t])}return o}var s=n.createContext({}),p=function(e){return function(r){var t=u(r.components);return n.createElement(e,i({},r,{components:t}))}},u=function(e){var r=n.useContext(s),t=r;return e&&(t="function"==typeof e?e(r):d(d({},r),e)),t},l=function(e){var r=u(e.components);return n.createElement(s.Provider,{value:r},e.children)},h="mdxType",g={inlineCode:"code",wrapper:function(e){var r=e.children;return n.createElement(n.Fragment,{},r)}},m=n.forwardRef((function(e,r){var t=e.components,o=e.mdxType,i=e.originalType,a=e.parentName,s=c(e,["components","mdxType","originalType","parentName"]),p=u(t),l=o,h=p["".concat(a,".").concat(l)]||p[l]||g[l]||i;return t?n.createElement(h,d(d({ref:r},s),{},{components:t})):n.createElement(h,d({ref:r},s))}));function f(e,r){var t=arguments,o=r&&r.mdxType;if("string"==typeof e||o){var i=t.length,a=new Array(i);a[0]=m;var d={};for(var c in r)hasOwnProperty.call(r,c)&&(d[c]=r[c]);d.originalType=e,d[h]="string"==typeof e?e:o,a[1]=d;for(var s=2;s<i;s++)a[s]=t[s];return n.createElement.apply(null,a)}return n.createElement.apply(null,t)}m.displayName="MDXCreateElement"},97462:(e,r,t)=>{t.r(r),t.d(r,{assets:()=>c,contentTitle:()=>a,default:()=>l,frontMatter:()=>i,metadata:()=>d,toc:()=>s});var n=t(58168),o=(t(96540),t(15680));const i={id:"changes_to_job_working_dir",title:"Changes to job's runtime working directory",hide_title:!0},a=void 0,d={unversionedId:"upgrades/1.1_to_1.2/changes_to_job_working_dir",id:"upgrades/1.1_to_1.2/changes_to_job_working_dir",title:"Changes to job's runtime working directory",description:"Hydra 1.2 introduces hydra.job.chdir. This config allows users to specify whether Hydra should change the runtime working",source:"@site/docs/upgrades/1.1_to_1.2/changes_to_job_working_dir.md",sourceDirName:"upgrades/1.1_to_1.2",slug:"/upgrades/1.1_to_1.2/changes_to_job_working_dir",permalink:"/docs/upgrades/1.1_to_1.2/changes_to_job_working_dir",draft:!1,editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/docs/upgrades/1.1_to_1.2/changes_to_job_working_dir.md",tags:[],version:"current",lastUpdatedBy:"dependabot[bot]",lastUpdatedAt:1742161400,formattedLastUpdatedAt:"Mar 16, 2025",frontMatter:{id:"changes_to_job_working_dir",title:"Changes to job's runtime working directory",hide_title:!0},sidebar:"docs",previous:{title:"Changes to @hydra.main() and hydra.initialize()",permalink:"/docs/upgrades/1.1_to_1.2/changes_to_hydra_main_config_path"},next:{title:"Changes to configuring sweeper's search space",permalink:"/docs/upgrades/1.1_to_1.2/changes_to_sweeper_config"}},c={},s=[],p={toc:s},u="wrapper";function l(e){let{components:r,...t}=e;return(0,o.mdx)(u,(0,n.A)({},p,t,{components:r,mdxType:"MDXLayout"}),(0,o.mdx)("p",null,"Hydra 1.2 introduces ",(0,o.mdx)("inlineCode",{parentName:"p"},"hydra.job.chdir"),". This config allows users to specify whether Hydra should change the runtime working\ndirectory to the job's output directory.\n",(0,o.mdx)("inlineCode",{parentName:"p"},"hydra.job.chdir")," will default to ",(0,o.mdx)("inlineCode",{parentName:"p"},"False"),' if version_base is set to >= "1.2" (or None),\nor otherwise will use the old behavior and default to ',(0,o.mdx)("inlineCode",{parentName:"p"},"True"),", with a warning being issued if ",(0,o.mdx)("inlineCode",{parentName:"p"},"hydra.job.chdir")," is not set."),(0,o.mdx)("p",null,"If you want to keep the old Hydra behavior, please set ",(0,o.mdx)("inlineCode",{parentName:"p"},"hydra.job.chdir=True")," explicitly for your application."),(0,o.mdx)("p",null,"For more information about ",(0,o.mdx)("inlineCode",{parentName:"p"},"hydra.job.chdir"),",\nsee ",(0,o.mdx)("a",{parentName:"p",href:"/docs/tutorials/basic/running_your_app/working_directory#disable-changing-current-working-dir-to-jobs-output-dir"},"Output/Working directory"),"\nand ",(0,o.mdx)("a",{parentName:"p",href:"/docs/configure_hydra/job#hydrajobchdir"},"Job Configuration - hydra.job.chdir"),"."))}l.isMDXComponent=!0}}]);