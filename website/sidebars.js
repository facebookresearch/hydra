// Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

function FBInternalOnly(elements) {
   return process.env.FB_INTERNAL ? elements : [];
}

module.exports = {
    docs: {
        About: [
            'intro',
            'terminology',
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
                'tutorials/structured_config/hierarchical_static_config',
                'tutorials/structured_config/config_groups',
                'tutorials/structured_config/defaults',
                'tutorials/structured_config/schema',
                'tutorials/structured_config/static_schema',
                'tutorials/structured_config/dynamic_schema',
                'tutorials/structured_config/config_store',
            ],
          },
        ],

        'Common Patterns': [
            {
                type: 'category',
                label: 'Instantiating Objects',
                items: [
                    'patterns/instantiate_objects/overview',
                    'patterns/instantiate_objects/config_files',
                    'patterns/instantiate_objects/structured_config',
                 ]
             },
            'patterns/specializing_config',
            'patterns/write_protect_config_node',
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
            'plugins/optuna_sweeper',
            'plugins/ray_launcher',
            'plugins/rq_launcher',
            'plugins/submitit_launcher',
        ],

        'Reference manual': [
            'advanced/hydra-command-line-flags',
            {
                type: 'category',
                label: 'Override grammar',
                items: [
                    'advanced/override_grammar/basic',
                    'advanced/override_grammar/extended',
                ]
            },
            'advanced/defaults_list',
            'advanced/overriding_packages',
            'advanced/search_path',
            'advanced/plugins',
            'advanced/app_packaging',
            'advanced/jupyter_notebooks',
            'advanced/unit_testing',
        ],

        "Experimental": [
            "experimental/intro",
            'experimental/compose_api',
        ],

        'Development': [
            'development/overview',
            'development/testing',
            'development/style_guide',
            'development/documentation',
            'development/release',
        ],

        Upgrades: [
          {
            type: 'category',
            label: '1.0 to 1.1',
            items: [
                'upgrades/1.0_to_1.1/defaults_list_interpolation',
            ],
          },
          {
            type: 'category',
            label: '0.11 to 1.0',
            items: [
                'upgrades/0.11_to_1.0/config_path_changes',
                'upgrades/0.11_to_1.0/adding_a_package_directive',
                'upgrades/0.11_to_1.0/strict_mode_flag_deprecated',
                'upgrades/0.11_to_1.0/object_instantiation_changes',
            ],
          },
        ],

        'FB Only': FBInternalOnly([
            'fb/intro',
            'fb/fbcode',
            'fb/internal-fb-cluster',
            'fb/fair-cluster',
        ]),
    }
}
