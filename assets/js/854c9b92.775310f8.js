"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[9550],{3905:function(e,t,n){n.r(t),n.d(t,{MDXContext:function(){return l},MDXProvider:function(){return f},mdx:function(){return g},useMDXComponents:function(){return p},withMDXComponents:function(){return u}});var r=n(67294);function o(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function i(){return i=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var r in n)Object.prototype.hasOwnProperty.call(n,r)&&(e[r]=n[r])}return e},i.apply(this,arguments)}function a(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,r)}return n}function c(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?a(Object(n),!0).forEach((function(t){o(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):a(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function s(e,t){if(null==e)return{};var n,r,o=function(e,t){if(null==e)return{};var n,r,o={},i=Object.keys(e);for(r=0;r<i.length;r++)n=i[r],t.indexOf(n)>=0||(o[n]=e[n]);return o}(e,t);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);for(r=0;r<i.length;r++)n=i[r],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(o[n]=e[n])}return o}var l=r.createContext({}),u=function(e){return function(t){var n=p(t.components);return r.createElement(e,i({},t,{components:n}))}},p=function(e){var t=r.useContext(l),n=t;return e&&(n="function"==typeof e?e(t):c(c({},t),e)),n},f=function(e){var t=p(e.components);return r.createElement(l.Provider,{value:t},e.children)},m={inlineCode:"code",wrapper:function(e){var t=e.children;return r.createElement(r.Fragment,{},t)}},d=r.forwardRef((function(e,t){var n=e.components,o=e.mdxType,i=e.originalType,a=e.parentName,l=s(e,["components","mdxType","originalType","parentName"]),u=p(n),f=o,d=u["".concat(a,".").concat(f)]||u[f]||m[f]||i;return n?r.createElement(d,c(c({ref:t},l),{},{components:n})):r.createElement(d,c({ref:t},l))}));function g(e,t){var n=arguments,o=t&&t.mdxType;if("string"==typeof e||o){var i=n.length,a=new Array(i);a[0]=d;var c={};for(var s in t)hasOwnProperty.call(t,s)&&(c[s]=t[s]);c.originalType=e,c.mdxType="string"==typeof e?e:o,a[1]=c;for(var l=2;l<i;l++)a[l]=n[l];return r.createElement.apply(null,a)}return r.createElement.apply(null,n)}d.displayName="MDXCreateElement"},93899:function(e,t,n){n.d(t,{Z:function(){return s},T:function(){return l}});var r=n(87462),o=n(67294),i=n(39960),a=n(52263),c=n(80907);function s(e){return o.createElement(i.default,(0,r.Z)({},e,{to:(t=e.to,s=(0,c.useActiveVersion)(),(0,a.default)().siteConfig.customFields.githubLinkVersionToBaseUrl[null!=(n=null==s?void 0:s.name)?n:"current"]+t),target:"_blank"}));var t,n,s}function l(e){var t,n=null!=(t=e.text)?t:"Example (Click Here)";return o.createElement(s,e,o.createElement("span",null,"\xa0"),o.createElement("img",{src:"https://img.shields.io/badge/-"+n+"-informational",alt:"Example (Click Here)"}))}},95543:function(e,t,n){n.r(t),n.d(t,{frontMatter:function(){return s},contentTitle:function(){return l},metadata:function(){return u},toc:function(){return p},default:function(){return m}});var r=n(87462),o=n(63366),i=(n(67294),n(3905)),a=n(93899),c=["components"],s={id:"using_config",title:"Using the config object"},l=void 0,u={unversionedId:"tutorials/basic/your_first_app/using_config",id:"version-1.0/tutorials/basic/your_first_app/using_config",title:"Using the config object",description:"Your configuration object is an instance of OmegaConf's DictConfig.",source:"@site/versioned_docs/version-1.0/tutorials/basic/your_first_app/3_using_config.md",sourceDirName:"tutorials/basic/your_first_app",slug:"/tutorials/basic/your_first_app/using_config",permalink:"/docs/1.0/tutorials/basic/your_first_app/using_config",editUrl:"https://github.com/facebookresearch/hydra/edit/main/website/versioned_docs/version-1.0/tutorials/basic/your_first_app/3_using_config.md",tags:[],version:"1.0",lastUpdatedBy:"Elliot Ford",lastUpdatedAt:1701366127,formattedLastUpdatedAt:"11/30/2023",sidebarPosition:3,frontMatter:{id:"using_config",title:"Using the config object"},sidebar:"version-1.0/docs",previous:{title:"Specifying a config file",permalink:"/docs/1.0/tutorials/basic/your_first_app/config_file"},next:{title:"Grouping config files",permalink:"/docs/1.0/tutorials/basic/your_first_app/config_groups"}},p=[],f={toc:p};function m(e){var t=e.components,n=(0,o.Z)(e,c);return(0,i.mdx)("wrapper",(0,r.Z)({},f,n,{components:t,mdxType:"MDXLayout"}),(0,i.mdx)(a.T,{to:"examples/tutorials/basic/your_first_hydra_app/3_using_config",mdxType:"ExampleGithubLink"}),(0,i.mdx)("p",null,"Your configuration object is an instance of OmegaConf's DictConfig.",(0,i.mdx)("br",{parentName:"p"}),"\n","Here are some of the basic features:"),(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre",className:"language-yaml",metastring:'title="config.yaml"',title:'"config.yaml"'},'node:                         # Config is hierarchical\n  loompa: 10                  # Simple value\n  zippity: ${node.loompa}     # Value interpolation\n  do: "oompa ${node.loompa}"  # String interpolation\n  waldo: ???                  # Missing value, must be populated prior to access\n')),(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre",className:"language-python",metastring:'title="my_app.py"',title:'"my_app.py"'},'@hydra.main(config_name="config")\ndef my_app(cfg: DictConfig):\n    assert cfg.node.loompa == 10          # attribute style access\n    assert cfg["node"]["loompa"] == 10    # dictionary style access\n\n    assert cfg.node.zippity == 10         # Value interpolation\n    assert isinstance(cfg.node.zippity, int)  # Value interpolation type\n    assert cfg.node.do == "oompa 10"      # string interpolation\n\n    cfg.node.waldo                        # raises an exception\n')),(0,i.mdx)("p",null,"Outputs:"),(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre"},"$ python my_app.py \nMissing mandatory value: waldo\n        full_key: waldo\n        reference_type=Optional[Dict[Any, Any]]\n        object_type=dict\n")),(0,i.mdx)("p",null,"You can learn more about OmegaConf ",(0,i.mdx)("a",{class:"external",href:"https://omegaconf.readthedocs.io/en/2.0_branch/usage.html#access-and-manipulation",target:"_blank"},"here"),"."))}m.isMDXComponent=!0}}]);