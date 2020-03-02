// Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
module.exports = {
    Docs: {
        About: [
            'intro',
        ],
        Tutorials: [
          'tutorials/intro',
          {
            type: 'category',
            label: 'Basic Tutorial',
            items: [
                'tutorials/basic/simple_cli',
                'tutorials/basic/config_file',
                'tutorials/basic/config_groups',
                'tutorials/basic/defaults',
                'tutorials/basic/composition',
                'tutorials/basic/multi-run',
                'tutorials/basic/tab_completion',
                'tutorials/basic/working_directory',
                'tutorials/basic/logging',
                'tutorials/basic/debugging',
            ],
          },

          {
            type: 'category',
            label: 'Structured configs tutorial',
            items: [
                'tutorials/structured_config/basic',
                'tutorials/structured_config/node_paths',
                'tutorials/structured_config/nesting',
                'tutorials/structured_config/config_groups',
                'tutorials/structured_config/defaults',
                'tutorials/structured_config/schema',
                'tutorials/structured_config/config_store',
            ],
          },
        ],

        'Common patterns': [
            'patterns/objects',
            'patterns/specializing_config',
        ],

        'Configuring Hydra': [
            'configure_hydra/intro',
            'configure_hydra/logging',
            'configure_hydra/workdir',
            'configure_hydra/app_help',
        ],

        'Plugins': [
            'plugins/ax_sweeper',
            'plugins/colorlog',
            'plugins/joblib_launcher',
            'plugins/nevergrad_sweeper',
        ],

        'Advanced': [
            'advanced/app_packaging',
            'advanced/plugins',
            'advanced/search_path',

        ],

        "Experimental": [
            "experimental/intro",
            'experimental/compose_api',
            'experimental/ray_example',
        ],

        'Development': [
            'development/contributing',
            'development/release',
        ]

    }
}
