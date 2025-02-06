"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[8856],{15680:(e,t,n)=>{n.r(t),n.d(t,{MDXContext:()=>s,MDXProvider:()=>m,mdx:()=>b,useMDXComponents:()=>u,withMDXComponents:()=>p});var r=n(96540);function o(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function i(){return i=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var r in n)Object.prototype.hasOwnProperty.call(n,r)&&(e[r]=n[r])}return e},i.apply(this,arguments)}function a(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,r)}return n}function l(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?a(Object(n),!0).forEach((function(t){o(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):a(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function c(e,t){if(null==e)return{};var n,r,o=function(e,t){if(null==e)return{};var n,r,o={},i=Object.keys(e);for(r=0;r<i.length;r++)n=i[r],t.indexOf(n)>=0||(o[n]=e[n]);return o}(e,t);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);for(r=0;r<i.length;r++)n=i[r],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(o[n]=e[n])}return o}var s=r.createContext({}),p=function(e){return function(t){var n=u(t.components);return r.createElement(e,i({},t,{components:n}))}},u=function(e){var t=r.useContext(s),n=t;return e&&(n="function"==typeof e?e(t):l(l({},t),e)),n},m=function(e){var t=u(e.components);return r.createElement(s.Provider,{value:t},e.children)},d={inlineCode:"code",wrapper:function(e){var t=e.children;return r.createElement(r.Fragment,{},t)}},f=r.forwardRef((function(e,t){var n=e.components,o=e.mdxType,i=e.originalType,a=e.parentName,s=c(e,["components","mdxType","originalType","parentName"]),p=u(n),m=o,f=p["".concat(a,".").concat(m)]||p[m]||d[m]||i;return n?r.createElement(f,l(l({ref:t},s),{},{components:n})):r.createElement(f,l({ref:t},s))}));function b(e,t){var n=arguments,o=t&&t.mdxType;if("string"==typeof e||o){var i=n.length,a=new Array(i);a[0]=f;var l={};for(var c in t)hasOwnProperty.call(t,c)&&(l[c]=t[c]);l.originalType=e,l.mdxType="string"==typeof e?e:o,a[1]=l;for(var s=2;s<i;s++)a[s]=n[s];return r.createElement.apply(null,a)}return r.createElement.apply(null,n)}f.displayName="MDXCreateElement"},57259:(e,t,n)=>{n.d(t,{A:()=>o});var r=n(96540);function o(e){var t=(0,r.useRef)(null),n=(0,r.useRef)("undefined"!=typeof document?document.createElement("script"):null);return(0,r.useEffect)((function(){t.current.appendChild(n.current)}),[]),(0,r.useEffect)((function(){for(var t in e)e.hasOwnProperty(t)&&(n.current[t]=e[t])})),r.createElement("div",{ref:t})}},90048:(e,t,n)=>{n.r(t),n.d(t,{contentTitle:()=>s,default:()=>d,frontMatter:()=>c,metadata:()=>p,toc:()=>u});var r=n(58168),o=n(98587),i=(n(96540),n(15680)),a=n(57259),l=["components"],c={id:"tab_completion",title:"Tab completion",sidebar_label:"Tab completion"},s=void 0,p={unversionedId:"tutorials/basic/running_your_app/tab_completion",id:"version-1.1/tutorials/basic/running_your_app/tab_completion",title:"Tab completion",description:"Tab completion can complete config groups, config nodes and values.",source:"@site/versioned_docs/version-1.1/tutorials/basic/running_your_app/6_tab_completion.md",sourceDirName:"tutorials/basic/running_your_app",slug:"/tutorials/basic/running_your_app/tab_completion",permalink:"/docs/1.1/tutorials/basic/running_your_app/tab_completion",editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/versioned_docs/version-1.1/tutorials/basic/running_your_app/6_tab_completion.md",tags:[],version:"1.1",lastUpdatedBy:"jesszzzz",lastUpdatedAt:1738870843,formattedLastUpdatedAt:"2/6/2025",sidebarPosition:6,frontMatter:{id:"tab_completion",title:"Tab completion",sidebar_label:"Tab completion"},sidebar:"version-1.1/docs",previous:{title:"Debugging",permalink:"/docs/1.1/tutorials/basic/running_your_app/debugging"},next:{title:"Introduction to Structured Configs",permalink:"/docs/1.1/tutorials/structured_config/intro"}},u=[{value:"Install tab completion",id:"install-tab-completion",children:[{value:"Zsh instructions",id:"zsh-instructions",children:[],level:4}],level:3}],m={toc:u};function d(e){var t=e.components,n=(0,o.A)(e,l);return(0,i.mdx)("wrapper",(0,r.A)({},m,n,{components:t,mdxType:"MDXLayout"}),(0,i.mdx)("p",null,"Tab completion can complete config groups, config nodes and values.\nTo complete paths, start them with ",(0,i.mdx)("inlineCode",{parentName:"p"},"/")," or ",(0,i.mdx)("inlineCode",{parentName:"p"},"./"),"."),(0,i.mdx)("p",null,"See this short video demonstration of tab completion:"),(0,i.mdx)(a.A,{id:"asciicast-272604",src:"https://asciinema.org/a/272604.js",async:!0,mdxType:"Script"}),(0,i.mdx)("h3",{id:"install-tab-completion"},"Install tab completion"),(0,i.mdx)("p",null,"Get the exact command to install the completion from ",(0,i.mdx)("inlineCode",{parentName:"p"},"--hydra-help"),".\nCurrently, Bash, zsh and Fish are supported.",(0,i.mdx)("br",{parentName:"p"}),"\n","We are relying on the community to implement tab completion plugins for additional shells."),(0,i.mdx)("p",null,"Fish support requires version >= 3.1.2.\nPrevious versions will work but add an extra space after ",(0,i.mdx)("inlineCode",{parentName:"p"},"."),"."),(0,i.mdx)("h4",{id:"zsh-instructions"},"Zsh instructions"),(0,i.mdx)("p",null,"Zsh is compatible with the existing Bash shell completion by appending"),(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre"},"autoload -Uz bashcompinit && bashcompinit\n")),(0,i.mdx)("p",null,"to the ",(0,i.mdx)("inlineCode",{parentName:"p"},".zshrc")," file after ",(0,i.mdx)("inlineCode",{parentName:"p"},"compinit"),", restarting the shell and then using the commands provided for Bash."))}d.isMDXComponent=!0}}]);