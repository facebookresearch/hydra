(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[3249],{7131:(e,t,a)=>{"use strict";a.d(t,{e:()=>i,i:()=>o});var n=a(96540),l=a(89532);const r=n.createContext(null);function o(e){let{children:t,content:a,isBlogPostPage:l=!1}=e;const o=function(e){let{content:t,isBlogPostPage:a}=e;return(0,n.useMemo)((()=>({metadata:t.metadata,frontMatter:t.frontMatter,assets:t.assets,toc:t.toc,isBlogPostPage:a})),[t,a])}({content:a,isBlogPostPage:l});return n.createElement(r.Provider,{value:o},t)}function i(){const e=(0,n.useContext)(r);if(null===e)throw new l.dV("BlogPostProvider");return e}},16669:(e,t,a)=>{"use strict";a.d(t,{A:()=>p});var n=a(96540),l=a(20053),r=a(27433),o=a(24581),i=a(75489),s=a(21312);const c={sidebar:"sidebar_re4s",sidebarItemTitle:"sidebarItemTitle_pO2u",sidebarItemList:"sidebarItemList_Yudw",sidebarItem:"sidebarItem__DBe",sidebarItemLink:"sidebarItemLink_mo7H",sidebarItemLinkActive:"sidebarItemLinkActive_I1ZP"};function m(e){let{sidebar:t}=e;return n.createElement("aside",{className:"col col--3"},n.createElement("nav",{className:(0,l.default)(c.sidebar,"thin-scrollbar"),"aria-label":(0,s.translate)({id:"theme.blog.sidebar.navAriaLabel",message:"Blog recent posts navigation",description:"The ARIA label for recent posts in the blog sidebar"})},n.createElement("div",{className:(0,l.default)(c.sidebarItemTitle,"margin-bottom--md")},t.title),n.createElement("ul",{className:(0,l.default)(c.sidebarItemList,"clean-list")},t.items.map((e=>n.createElement("li",{key:e.permalink,className:c.sidebarItem},n.createElement(i.default,{isNavLink:!0,to:e.permalink,className:c.sidebarItemLink,activeClassName:c.sidebarItemLinkActive},e.title)))))))}var u=a(75600);function d(e){let{sidebar:t}=e;return n.createElement("ul",{className:"menu__list"},t.items.map((e=>n.createElement("li",{key:e.permalink,className:"menu__list-item"},n.createElement(i.default,{isNavLink:!0,to:e.permalink,className:"menu__link",activeClassName:"menu__link--active"},e.title)))))}function g(e){return n.createElement(u.GX,{component:d,props:e})}function f(e){let{sidebar:t}=e;const a=(0,o.l)();return t?.items.length?"mobile"===a?n.createElement(g,{sidebar:t}):n.createElement(m,{sidebar:t}):null}function p(e){const{sidebar:t,toc:a,children:o,...i}=e,s=t&&t.items.length>0;return n.createElement(r.A,i,n.createElement("div",{className:"container margin-vert--lg"},n.createElement("div",{className:"row"},n.createElement(f,{sidebar:t}),n.createElement("main",{className:(0,l.default)("col",{"col--7":s,"col--9 col--offset-1":!s}),itemScope:!0,itemType:"http://schema.org/Blog"},o),a&&n.createElement("div",{className:"col col--2"},a))))}},48258:(e,t,a)=>{"use strict";a.d(t,{A:()=>M});var n=a(96540),l=a(20053),r=a(7131),o=a(86025);function i(e){let{children:t,className:a}=e;const{frontMatter:l,assets:i,metadata:{description:s}}=(0,r.e)(),{withBaseUrl:c}=(0,o.useBaseUrlUtils)(),m=i.image??l.image,u=l.keywords??[];return n.createElement("article",{className:a,itemProp:"blogPost",itemScope:!0,itemType:"http://schema.org/BlogPosting"},s&&n.createElement("meta",{itemProp:"description",content:s}),m&&n.createElement("link",{itemProp:"image",href:c(m,{absolute:!0})}),u.length>0&&n.createElement("meta",{itemProp:"keywords",content:u.join(",")}),t)}var s=a(75489);const c={title:"title_f1Hy"};function m(e){let{className:t}=e;const{metadata:a,isBlogPostPage:o}=(0,r.e)(),{permalink:i,title:m}=a,u=o?"h1":"h2";return n.createElement(u,{className:(0,l.default)(c.title,t),itemProp:"headline"},o?m:n.createElement(s.default,{itemProp:"url",to:i},m))}var u=a(21312),d=a(53465);const g={container:"container_mt6G"};function f(e){let{readingTime:t}=e;const a=function(){const{selectMessage:e}=(0,d.W)();return t=>{const a=Math.ceil(t);return e(a,(0,u.translate)({id:"theme.blog.post.readingTime.plurals",description:'Pluralized label for "{readingTime} min read". Use as much plural forms (separated by "|") as your language support (see https://www.unicode.org/cldr/cldr-aux/charts/34/supplemental/language_plural_rules.html)',message:"One min read|{readingTime} min read"},{readingTime:a}))}}();return n.createElement(n.Fragment,null,a(t))}function p(e){let{date:t,formattedDate:a}=e;return n.createElement("time",{dateTime:t,itemProp:"datePublished"},a)}function v(){return n.createElement(n.Fragment,null," \xb7 ")}function h(e){let{className:t}=e;const{metadata:a}=(0,r.e)(),{date:o,formattedDate:i,readingTime:s}=a;return n.createElement("div",{className:(0,l.default)(g.container,"margin-vert--md",t)},n.createElement(p,{date:o,formattedDate:i}),void 0!==s&&n.createElement(n.Fragment,null,n.createElement(v,null),n.createElement(f,{readingTime:s})))}function b(e){return e.href?n.createElement(s.default,e):n.createElement(n.Fragment,null,e.children)}function E(e){let{author:t,className:a}=e;const{name:r,title:o,url:i,imageURL:s,email:c}=t,m=i||c&&`mailto:${c}`||void 0;return n.createElement("div",{className:(0,l.default)("avatar margin-bottom--sm",a)},s&&n.createElement(b,{href:m,className:"avatar__photo-link"},n.createElement("img",{className:"avatar__photo",src:s,alt:r,itemProp:"image"})),r&&n.createElement("div",{className:"avatar__intro",itemProp:"author",itemScope:!0,itemType:"https://schema.org/Person"},n.createElement("div",{className:"avatar__name"},n.createElement(b,{href:m,itemProp:"url"},n.createElement("span",{itemProp:"name"},r))),o&&n.createElement("small",{className:"avatar__subtitle",itemProp:"description"},o)))}const N={authorCol:"authorCol_Hf19",imageOnlyAuthorRow:"imageOnlyAuthorRow_pa_O",imageOnlyAuthorCol:"imageOnlyAuthorCol_G86a"};function _(e){let{className:t}=e;const{metadata:{authors:a},assets:o}=(0,r.e)();if(0===a.length)return null;const i=a.every((e=>{let{name:t}=e;return!t}));return n.createElement("div",{className:(0,l.default)("margin-top--md margin-bottom--sm",i?N.imageOnlyAuthorRow:"row",t)},a.map(((e,t)=>n.createElement("div",{className:(0,l.default)(!i&&"col col--6",i?N.imageOnlyAuthorCol:N.authorCol),key:t},n.createElement(E,{author:{...e,imageURL:o.authorsImageUrls[t]??e.imageURL}})))))}function P(){return n.createElement("header",null,n.createElement(m,null),n.createElement(h,null),n.createElement(_,null))}var L=a(70440),k=a(61823),A=a.n(k);function C(e){let{children:t,className:a}=e;const{isBlogPostPage:o}=(0,r.e)();return n.createElement("div",{id:o?L.blogPostContainerID:void 0,className:(0,l.default)("markdown",a),itemProp:"articleBody"},n.createElement(A(),null,t))}var y=a(12216),I=a.n(y),x=a(62053),H=a(58168);function w(){return n.createElement("b",null,n.createElement(u.default,{id:"theme.blog.post.readMore",description:"The label used in blog post item excerpts to link to full blog posts"},"Read More"))}function T(e){const{blogPostTitle:t,...a}=e;return n.createElement(s.default,(0,H.A)({"aria-label":(0,u.translate)({message:"Read more about {title}",id:"theme.blog.post.readMoreLabel",description:"The ARIA label for the link to full blog posts from excerpts"},{title:t})},a),n.createElement(w,null))}const B={blogPostFooterDetailsFull:"blogPostFooterDetailsFull_mRVl"};function O(){const{metadata:e,isBlogPostPage:t}=(0,r.e)(),{tags:a,title:o,editUrl:i,hasTruncateMarker:s}=e,c=!t&&s,m=a.length>0;return m||c||i?n.createElement("footer",{className:(0,l.default)("row docusaurus-mt-lg",t&&B.blogPostFooterDetailsFull)},m&&n.createElement("div",{className:(0,l.default)("col",{"col--9":c})},n.createElement(x.A,{tags:a})),t&&i&&n.createElement("div",{className:"col margin-top--sm"},n.createElement(I(),{editUrl:i})),c&&n.createElement("div",{className:(0,l.default)("col text--right",{"col--3":m})},n.createElement(T,{blogPostTitle:o,to:e.permalink}))):null}function M(e){let{children:t,className:a}=e;const o=function(){const{isBlogPostPage:e}=(0,r.e)();return e?void 0:"margin-bottom--xl"}();return n.createElement(i,{className:(0,l.default)(o,a)},n.createElement(P,null),n.createElement(C,null,t),n.createElement(O,null))}},65195:(e,t,a)=>{"use strict";a.d(t,{A:()=>f});var n=a(58168),l=a(96540),r=a(6342);function o(e){const t=e.map((e=>({...e,parentIndex:-1,children:[]}))),a=Array(7).fill(-1);t.forEach(((e,t)=>{const n=a.slice(2,e.level);e.parentIndex=Math.max(...n),a[e.level]=t}));const n=[];return t.forEach((e=>{const{parentIndex:a,...l}=e;a>=0?t[a].children.push(l):n.push(l)})),n}function i(e){let{toc:t,minHeadingLevel:a,maxHeadingLevel:n}=e;return t.flatMap((e=>{const t=i({toc:e.children,minHeadingLevel:a,maxHeadingLevel:n});return function(e){return e.level>=a&&e.level<=n}(e)?[{...e,children:t}]:t}))}function s(e){const t=e.getBoundingClientRect();return t.top===t.bottom?s(e.parentNode):t}function c(e,t){let{anchorTopOffset:a}=t;const n=e.find((e=>s(e).top>=a));if(n){return function(e){return e.top>0&&e.bottom<window.innerHeight/2}(s(n))?n:e[e.indexOf(n)-1]??null}return e[e.length-1]??null}function m(){const e=(0,l.useRef)(0),{navbar:{hideOnScroll:t}}=(0,r.p)();return(0,l.useEffect)((()=>{e.current=t?0:document.querySelector(".navbar").clientHeight}),[t]),e}function u(e){const t=(0,l.useRef)(void 0),a=m();(0,l.useEffect)((()=>{if(!e)return()=>{};const{linkClassName:n,linkActiveClassName:l,minHeadingLevel:r,maxHeadingLevel:o}=e;function i(){const e=function(e){return Array.from(document.getElementsByClassName(e))}(n),i=function(e){let{minHeadingLevel:t,maxHeadingLevel:a}=e;const n=[];for(let l=t;l<=a;l+=1)n.push(`h${l}.anchor`);return Array.from(document.querySelectorAll(n.join()))}({minHeadingLevel:r,maxHeadingLevel:o}),s=c(i,{anchorTopOffset:a.current}),m=e.find((e=>s&&s.id===function(e){return decodeURIComponent(e.href.substring(e.href.indexOf("#")+1))}(e)));e.forEach((e=>{!function(e,a){a?(t.current&&t.current!==e&&t.current.classList.remove(l),e.classList.add(l),t.current=e):e.classList.remove(l)}(e,e===m)}))}return document.addEventListener("scroll",i),document.addEventListener("resize",i),i(),()=>{document.removeEventListener("scroll",i),document.removeEventListener("resize",i)}}),[e,a])}function d(e){let{toc:t,className:a,linkClassName:n,isChild:r}=e;return t.length?l.createElement("ul",{className:r?void 0:a},t.map((e=>l.createElement("li",{key:e.id},l.createElement("a",{href:`#${e.id}`,className:n??void 0,dangerouslySetInnerHTML:{__html:e.value}}),l.createElement(d,{isChild:!0,toc:e.children,className:a,linkClassName:n}))))):null}const g=l.memo(d);function f(e){let{toc:t,className:a="table-of-contents table-of-contents__left-border",linkClassName:s="table-of-contents__link",linkActiveClassName:c,minHeadingLevel:m,maxHeadingLevel:d,...f}=e;const p=(0,r.p)(),v=m??p.tableOfContents.minHeadingLevel,h=d??p.tableOfContents.maxHeadingLevel,b=function(e){let{toc:t,minHeadingLevel:a,maxHeadingLevel:n}=e;return(0,l.useMemo)((()=>i({toc:o(t),minHeadingLevel:a,maxHeadingLevel:n})),[t,a,n])}({toc:t,minHeadingLevel:v,maxHeadingLevel:h});return u((0,l.useMemo)((()=>{if(s&&c)return{linkClassName:s,linkActiveClassName:c,minHeadingLevel:v,maxHeadingLevel:h}}),[s,c,v,h])),l.createElement(g,(0,n.A)({toc:b,className:a,linkClassName:s},f))}},66590:()=>{},67763:(e,t,a)=>{"use strict";a.d(t,{A:()=>m});var n=a(58168),l=a(96540),r=a(20053),o=a(65195);const i={tableOfContents:"tableOfContents_bqdL",docItemContainer:"docItemContainer_F8PC"},s="table-of-contents__link toc-highlight",c="table-of-contents__link--active";function m(e){let{className:t,...a}=e;return l.createElement("div",{className:(0,r.default)(i.tableOfContents,"thin-scrollbar",t)},l.createElement(o.A,(0,n.A)({},a,{linkClassName:s,linkActiveClassName:c})))}},84029:(e,t,a)=>{"use strict";a.r(t),a.d(t,{default:()=>h});var n=a(96540),l=a(20053),r=a(69024),o=a(17559),i=a(7131),s=a(16669),c=a(48258),m=a(58168),u=a(21312),d=a(39022);function g(e){const{nextItem:t,prevItem:a}=e;return n.createElement("nav",{className:"pagination-nav docusaurus-mt-lg","aria-label":(0,u.translate)({id:"theme.blog.post.paginator.navAriaLabel",message:"Blog post page navigation",description:"The ARIA label for the blog posts pagination"})},a&&n.createElement(d.A,(0,m.A)({},a,{subLabel:n.createElement(u.default,{id:"theme.blog.post.paginator.newerPost",description:"The blog post button label to navigate to the newer/previous post"},"Newer Post")})),t&&n.createElement(d.A,(0,m.A)({},t,{subLabel:n.createElement(u.default,{id:"theme.blog.post.paginator.olderPost",description:"The blog post button label to navigate to the older/next post"},"Older Post"),isNext:!0})))}function f(){const{assets:e,metadata:t}=(0,i.e)(),{title:a,description:l,date:o,tags:s,authors:c,frontMatter:m}=t,{keywords:u}=m,d=e.image??m.image;return n.createElement(r.be,{title:a,description:l,keywords:u,image:d},n.createElement("meta",{property:"og:type",content:"article"}),n.createElement("meta",{property:"article:published_time",content:o}),c.some((e=>e.url))&&n.createElement("meta",{property:"article:author",content:c.map((e=>e.url)).filter(Boolean).join(",")}),s.length>0&&n.createElement("meta",{property:"article:tag",content:s.map((e=>e.label)).join(",")}))}var p=a(67763);function v(e){let{sidebar:t,children:a}=e;const{metadata:l,toc:r}=(0,i.e)(),{nextItem:o,prevItem:m,frontMatter:u}=l,{hide_table_of_contents:d,toc_min_heading_level:f,toc_max_heading_level:v}=u;return n.createElement(s.A,{sidebar:t,toc:!d&&r.length>0?n.createElement(p.A,{toc:r,minHeadingLevel:f,maxHeadingLevel:v}):void 0},n.createElement(c.A,null,a),(o||m)&&n.createElement(g,{nextItem:o,prevItem:m}))}function h(e){const t=e.content;return n.createElement(i.i,{content:e.content,isBlogPostPage:!0},n.createElement(r.e3,{className:(0,l.default)(o.G.wrapper.blogPages,o.G.page.blogPostPage)},n.createElement(f,null),n.createElement(v,{sidebar:e.sidebar},n.createElement(t,null))))}}}]);