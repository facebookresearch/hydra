---
id: tab_completion
title: Tab completion
sidebar_label: Tab completion
---
You can enable shell TAB completion, for example:
```
eval "$(python my_app.py -sc install=SHELL_NAME)"
```
or for Fish shell specifically
```
python my_app.py -sc install=fish | source
```

Get the exact command to install the completion from `--hydra-help`.

Replace SHELL_NAME by your shell name, currently, only Bash and Fish are supported and we are relying on the community to implement completion plugins for additional shells.

Tab completion can complete config groups, configuration nodes and values and also paths if they start with `.` or `/`. Please note that Fish version <= 3.1.2 automatically adds an extra space after `.`. You'll need to remove the space to continue the completion.

See this short video demonstration of tab completion:

import Script from '../../../src/components/Script.jsx';

<Script id="asciicast-272604" src="https://asciinema.org/a/272604.js" async></Script>
