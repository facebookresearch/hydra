---
id: tab_completion
title: Tab completion
sidebar_label: Tab completion
---
You can enable shell TAB completion 
```
eval "$(python your_python_script.py -sc install=SHELL_NAME)"
# Or
eval "$(your_app -sc install=SHELL_NAME)"
```

Replace SHELL_NAME by your shell name, currently, only Bash is supported and we are relying on the community to implement completion plugins for additional shells.

Example:
```
eval "$(python your_python_script.py -sc install=bash)"
```

See this short video demonstration of tab completion:

import Script from '../../src/components/Script.jsx';

<Script id="asciicast-269503" src="https://asciinema.org/a/269503.js" async></Script>