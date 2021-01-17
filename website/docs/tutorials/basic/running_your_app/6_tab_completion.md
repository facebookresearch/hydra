---
id: tab_completion
title: Tab completion
sidebar_label: Tab completion
---

Tab completion can complete config groups, config nodes and values.
To complete paths, start them with `/` or `./`.

See this short video demonstration of tab completion:

import Script from '@site/src/components/Script.jsx';

<Script id="asciicast-272604" src="https://asciinema.org/a/272604.js" async></Script>


### Install tab completion
Get the exact command to install the completion from `--hydra-help`.
Currently, Bash, zsh and Fish are supported.   
We are relying on the community to implement tab completion plugins for additional shells.

Fish support requires version >= 3.1.2.
Previous versions will work but add an extra space after `.`.

#### Zsh instructions
Zsh is compatible with the existing Bash shell completion by appending
```
autoload -Uz bashcompinit && bashcompinit
```
to the `.zshrc` file after `compinit`, restarting the shell and then using the commands provided for Bash.