# Hydra example config source
Use this as the template a Hydra config source plugin

Config source plugins are allowing Hydra to recognize other search path schemas in addition to the built in 
`file://` (which provides access to configs in the file system) and 
`pkg://` (which provides access to configs installed with a Python package) 

This plugin provides access to configs stored in a simple in-memory data structure.