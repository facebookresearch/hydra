// Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
module.exports = {
    Docs: {
        About: [
            'intro',
            'getting_started',
            'contributing'
        ],
        'Basic usage': [
            'examples/minimal',
            'examples/working_directory',
            'examples/logging',
            'examples/config_file',
            'examples/config_splitting',
            'examples/config_groups',
            'examples/sweep',
            {
                type: 'category',
                label: 'Advanced',
                items: [
                    'examples/objects',
                    'examples/specializing_config',
                ],
            },
        ],
        'Configuring Hydra': [
            'configure_hydra/intro',
            'configure_hydra/hydra_config',
            'configure_hydra/logging',
            'configure_hydra/workdir',
        ],

    }
}