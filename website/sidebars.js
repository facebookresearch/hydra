module.exports = {
    Docs: {
        About: [
            'intro',
            'getting_started',
        ],
        'Basic usage': [
            'examples/minimal/example',
            'examples/config_file/example',
            'examples/config_file_merging/example',
            'examples/config_groups/example',
            'examples/sweep/example',
            {
                type: 'category',
                label: 'Misc',
                items: [
                    'examples/misc/working_directory/example',
                    'examples/misc/logging/example',
                    'examples/misc/objects/example',
                ],
            },
            {
                type: 'category',
                label: 'Advanced',
                items: [
                    'advanced/specializing_config/example',
                    'advanced/customize_logging/example',
                    'advanced/customize_working_directory/example',
                ],
            },
        ],
    }
}