module.exports = {
    Docs: {
        About: [
            'intro',
            'getting_started',
        ],
        'Basic usage': [
            'examples/minimal/example',
            'examples/misc/working_directory/example',
            'examples/misc/logging/example',
            'examples/config_file/example',
            'examples/config_file_merging/example',
            'examples/config_groups/example',
            'examples/sweep/example',
            {
                type: 'category',
                label: 'Advanced',
                items: [
                    'examples/misc/objects/example',
                    'examples/specializing_config/example',
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