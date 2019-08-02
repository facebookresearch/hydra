module.exports = {
    Docs: {
        About: [
            'intro',
            'getting_started',
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
            'configure_hydra/customize_logging/example',
            'configure_hydra/customize_working_directory/example',
        ],

    }
}