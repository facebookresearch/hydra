"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[7978],{15680:(e,t,n)=>{n.r(t),n.d(t,{MDXContext:()=>c,MDXProvider:()=>p,mdx:()=>h,useMDXComponents:()=>u,withMDXComponents:()=>m});var r=n(96540);function a(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function o(){return o=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var r in n)Object.prototype.hasOwnProperty.call(n,r)&&(e[r]=n[r])}return e},o.apply(this,arguments)}function i(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,r)}return n}function s(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?i(Object(n),!0).forEach((function(t){a(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):i(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function l(e,t){if(null==e)return{};var n,r,a=function(e,t){if(null==e)return{};var n,r,a={},o=Object.keys(e);for(r=0;r<o.length;r++)n=o[r],t.indexOf(n)>=0||(a[n]=e[n]);return a}(e,t);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(e);for(r=0;r<o.length;r++)n=o[r],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(a[n]=e[n])}return a}var c=r.createContext({}),m=function(e){return function(t){var n=u(t.components);return r.createElement(e,o({},t,{components:n}))}},u=function(e){var t=r.useContext(c),n=t;return e&&(n="function"==typeof e?e(t):s(s({},t),e)),n},p=function(e){var t=u(e.components);return r.createElement(c.Provider,{value:t},e.children)},d="mdxType",f={inlineCode:"code",wrapper:function(e){var t=e.children;return r.createElement(r.Fragment,{},t)}},y=r.forwardRef((function(e,t){var n=e.components,a=e.mdxType,o=e.originalType,i=e.parentName,c=l(e,["components","mdxType","originalType","parentName"]),m=u(n),p=a,d=m["".concat(i,".").concat(p)]||m[p]||f[p]||o;return n?r.createElement(d,s(s({ref:t},c),{},{components:n})):r.createElement(d,s({ref:t},c))}));function h(e,t){var n=arguments,a=t&&t.mdxType;if("string"==typeof e||a){var o=n.length,i=new Array(o);i[0]=y;var s={};for(var l in t)hasOwnProperty.call(t,l)&&(s[l]=t[l]);s.originalType=e,s[d]="string"==typeof e?e:a,i[1]=s;for(var c=2;c<o;c++)i[c]=n[c];return r.createElement.apply(null,i)}return r.createElement.apply(null,n)}y.displayName="MDXCreateElement"},19465:(e,t,n)=>{n.r(t),n.d(t,{assets:()=>c,contentTitle:()=>s,default:()=>d,frontMatter:()=>i,metadata:()=>l,toc:()=>m});var r=n(58168),a=(n(96540),n(15680)),o=n(49595);const i={id:"composition",title:"Putting it all together"},s=void 0,l={unversionedId:"tutorials/basic/your_first_app/composition",id:"version-1.3/tutorials/basic/your_first_app/composition",title:"Putting it all together",description:"As software gets more complex, we resort to modularity and composition to keep it manageable.",source:"@site/versioned_docs/version-1.3/tutorials/basic/your_first_app/6_composition.md",sourceDirName:"tutorials/basic/your_first_app",slug:"/tutorials/basic/your_first_app/composition",permalink:"/docs/1.3/tutorials/basic/your_first_app/composition",draft:!1,editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/versioned_docs/version-1.3/tutorials/basic/your_first_app/6_composition.md",tags:[],version:"1.3",lastUpdatedBy:"jesszzzz",lastUpdatedAt:1741814683,formattedLastUpdatedAt:"Mar 12, 2025",sidebarPosition:6,frontMatter:{id:"composition",title:"Putting it all together"},sidebar:"docs",previous:{title:"Selecting default configs",permalink:"/docs/1.3/tutorials/basic/your_first_app/defaults"},next:{title:"Multi-run",permalink:"/docs/1.3/tutorials/basic/running_your_app/multi-run"}},c={},m=[{value:"Summary",id:"summary",level:3}],u={toc:m},p="wrapper";function d(e){let{components:t,...n}=e;return(0,a.mdx)(p,(0,r.A)({},u,n,{components:t,mdxType:"MDXLayout"}),(0,a.mdx)(o.C,{to:"examples/tutorials/basic/your_first_hydra_app/6_composition",mdxType:"ExampleGithubLink"}),(0,a.mdx)("p",null,"As software gets more complex, we resort to modularity and composition to keep it manageable.\nWe can do the same with configs. Suppose we want our working example to support multiple databases, with\nmultiple schemas per database, and different UIs. We wouldn't write a separate class\nfor each permutation of db, schema and UI, so we shouldn't write separate configs either. We use\nthe same solution in configuration as in writing the underlying software: composition. "),(0,a.mdx)("p",null,"To do this in Hydra, we first add a ",(0,a.mdx)("inlineCode",{parentName:"p"},"schema")," and a ",(0,a.mdx)("inlineCode",{parentName:"p"},"ui")," config group:"),(0,a.mdx)("pre",null,(0,a.mdx)("code",{parentName:"pre",className:"language-text",metastring:'title="Directory layout"',title:'"Directory','layout"':!0},"\u251c\u2500\u2500 conf\n\u2502   \u251c\u2500\u2500 config.yaml\n\u2502   \u251c\u2500\u2500 db\n\u2502   \u2502   \u251c\u2500\u2500 mysql.yaml\n\u2502   \u2502   \u2514\u2500\u2500 postgresql.yaml\n\u2502   \u251c\u2500\u2500 schema\n\u2502   \u2502   \u251c\u2500\u2500 school.yaml\n\u2502   \u2502   \u251c\u2500\u2500 support.yaml\n\u2502   \u2502   \u2514\u2500\u2500 warehouse.yaml\n\u2502   \u2514\u2500\u2500 ui\n\u2502       \u251c\u2500\u2500 full.yaml\n\u2502       \u2514\u2500\u2500 view.yaml\n\u2514\u2500\u2500 my_app.py\n")),(0,a.mdx)("p",null,"With these configs, we already have 12 possible combinations. Without composition, we would need 12 separate configs.\nA single change, such as renaming ",(0,a.mdx)("inlineCode",{parentName:"p"},"db.user")," to ",(0,a.mdx)("inlineCode",{parentName:"p"},"db.username"),", requires editing all 12 of them.\nThis is a maintenance nightmare."),(0,a.mdx)("p",null,"Composition can come to the rescue.\nInstead of creating 12 different config files, that fully specify each\nconfig, create a single config that specifies the different configuration dimensions, and the default for each."),(0,a.mdx)("pre",null,(0,a.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="config.yaml"',title:'"config.yaml"'},"defaults:\n  - db: mysql\n  - ui: full\n  - schema: school\n")),(0,a.mdx)("p",null,"The resulting configuration is a composition of the ",(0,a.mdx)("em",{parentName:"p"},"mysql")," database, the ",(0,a.mdx)("em",{parentName:"p"},"full")," ui, and the ",(0,a.mdx)("em",{parentName:"p"},"school")," schema\n(which we are seeing for the first time here):"),(0,a.mdx)("pre",null,(0,a.mdx)("code",{parentName:"pre",className:"language-yaml"},"$ python my_app.py\ndb:\n  driver: mysql\n  user: omry\n  pass: secret\nui:\n  windows:\n    create_db: true\n    view: true\nschema:\n  database: school\n  tables:\n  - name: students\n    fields:\n    - name: string\n    - class: int\n  - name: exams\n    fields:\n    - profession: string\n    - time: data\n    - class: int\n")),(0,a.mdx)("p",null,"Stay tuned to see how to run all of the combinations automatically (",(0,a.mdx)("a",{parentName:"p",href:"/docs/1.3/tutorials/basic/running_your_app/multi-run"},"Multi-run"),")."),(0,a.mdx)("h3",{id:"summary"},"Summary"),(0,a.mdx)("ul",null,(0,a.mdx)("li",{parentName:"ul"},"The addition of each new db, schema, or ui only requires a single file."),(0,a.mdx)("li",{parentName:"ul"},"Each config group can have a default specified in the Defaults List."),(0,a.mdx)("li",{parentName:"ul"},"Any combination can be composed by selecting the desired option from each config group in the\nDefaults List or the command line.")))}d.isMDXComponent=!0},49595:(e,t,n)=>{n.d(t,{A:()=>c,C:()=>m});var r=n(58168),a=n(96540),o=n(75489),i=n(44586),s=n(48295);function l(e){const t=(0,s.ir)();return(0,i.default)().siteConfig.customFields.githubLinkVersionToBaseUrl[t?.name??"current"]+e}function c(e){return a.createElement(o.default,(0,r.A)({},e,{to:l(e.to),target:"_blank"}))}function m(e){const t=e.text??"Example (Click Here)";return a.createElement(c,e,a.createElement("span",null,"\xa0"),a.createElement("img",{src:"https://img.shields.io/badge/-"+t+"-informational",alt:"Example (Click Here)"}))}}}]);