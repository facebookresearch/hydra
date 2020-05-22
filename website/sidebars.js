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
                {
                    type: 'category',
                    label: 'Your first Hydra app',
                    items: [
                        'tutorials/basic/your_first_app/simple_cli',
                        'tutorials/basic/your_first_app/config_file',
                        'tutorials/basic/your_first_app/using_config',
                        'tutorials/basic/your_first_app/config_groups',
                        'tutorials/basic/your_first_app/defaults',
                        'tutorials/basic/your_first_app/composition',
                    ]
                },
                {
                    type: 'category',
                    label: 'Running your Hydra app',
                    items: [
                        'tutorials/basic/running_your_app/strict_mode',
                        'tutorials/basic/running_your_app/multi-run',
                        'tutorials/basic/running_your_app/working_directory',
                        'tutorials/basic/running_your_app/logging',
                        'tutorials/basic/running_your_app/debugging',
                        'tutorials/basic/running_your_app/tab_completion',
                    ]
                },

            ],
          },

          {
            type: 'category',
            label: 'Structured Configs Tutorial',
            items: [
                'tutorials/structured_config/intro',
                'tutorials/structured_config/minimal_example',
                'tutorials/structured_config/nesting',
                'tutorials/structured_config/config_groups',
                'tutorials/structured_config/defaults',
                'tutorials/structured_config/schema',
                'tutorials/structured_config/config_store',
            ],
          },
        ],

        'Common Patterns': [
            'patterns/objects',
            'patterns/specializing_config',
        ],

        'Configuring Hydra': [
            'configure_hydra/intro',
            'configure_hydra/job',
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
            'advanced/package_directive',
            'advanced/search_path',
            'advanced/plugins',
            'advanced/app_packaging',
        ],

        "Experimental": [
            "experimental/intro",
            'experimental/compose_api',
            'experimental/ray_example',
        ],

        'Development': [
            'development/contributing',
            'development/release',
        ],

        Upgrades: [
          {
            type: 'category',
            label: '0.11 to 1.0',
            items: [
                'upgrades/0.11_to_1.0/adding_a_package_directive',
                'upgrades/0.11_to_1.0/strict_mode_flag_deprecated',
            ],
          },
        ],
    }
}
