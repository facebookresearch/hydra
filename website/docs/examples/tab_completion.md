---
id: tab_completion
title: Tab completion
sidebar_label: Tab completion
---
By installing shell completion you can TAB complete your configuration in the command line.


```
eval "$(python your_python_script.py -sc install=SHELL_NAME)"
```

If you have created a package for your app (see [deploymnet](../deployment/app_packaging)), you can also install the completion with
```
eval "$(your_app -sc install=SHELL_NAME)"
```
For example
```
eval "$(your_app -sc install=bash)"
```
Currently, only Bash is supported and we are relying on the community to implement completion plugins for additional shells.

See this short video demonstration of tab completion:

import Script from '../../src/components/Script.jsx';

<Script id="asciicast-269183" src="https://asciinema.org/a/269183.js" async></Script> 