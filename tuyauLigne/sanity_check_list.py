sanity_check_list = [
    {
        'function_name': 'check_workspace',
        'report_called': 'report_workspace',
        'description': "The workspace is not configured correctly, or the currently open scene file is outside your"
                       " workspace.",
        'label': 'check workspace',
        'category': 'global',
    },
    {
        'function_name': 'check_master_grp',
        'report_called': 'report_master_grp',
        'description': "The main group has an error. Either there is no main group in your scene, or the main "
                       "group is incorrectly named (it should match the file name without the version increment), or"
                       " it is not at the root level of the scene.",
        'label': 'main group',
        'category': 'global',
    },
    {
        'function_name': 'check_unique_name',
        'report_called': 'report_unique_name',
        'description': "Multiple elements in your scene have identical names. Ensure each element has a unique name.",
        'label': 'non-unique names',
        'category': 'global',
    },
    {
        'function_name': 'check_empty_group',
        'report_called': 'report_empty_group',
        'description': "One or more empty groups detected.",
        'label': 'empty group',
        'category': 'hierarchy',
    },
    {
        'function_name': 'check_prp_in_master',
        'report_called': 'report_prp_in_master',
        'description': "'prp_' groups must be direct children of the main group.",
        'label': '"prp" group in main group',
        'category': 'hierarchy',
    },
    {
        'function_name': 'check_purpose_grp_hierarchy',
        'report_called': 'report_purpose_grp_hierarchy',
        'description': "'proxy_' and 'render_' groups should be direct children of 'prp_' groups.",
        'label': '"proxy/render" groups in "prp"',
        'category': 'hierarchy',
    },
    {
        'function_name': 'check_mesh_in_grp',
        'report_called': 'report_mesh_in_grp',
        'description': "Meshes should not be direct children of the main group.",
        'label': 'Meshes in main group',
        'category': 'hierarchy',
    },
    {
        'function_name': 'check_prefix_prp',
        'report_called': 'report_prefix_prp',
        'description': "Child groups under the main group should have the prefix 'prp_'.",
        'label': 'Prefix "prp_"',
        'category': 'naming',
    },
    {
        'function_name': 'check_existing_prp',
        'report_called': 'report_existing_prp',
        'description': "These props have already been published. Rename the prop you want to publish or delete the "
                       "folder of the already published props if not required.",
        'label': 'Existing prop',
        'category': 'naming',
    },
    {
        'function_name': 'check_existing_set',
        'report_called': 'report_existing_set',
        'description': "This set has already been published. Delete the folder of the already published set if it is "
                       "not needed.",
        'label': 'Existing set',
        'category': 'naming',
    },
    {
        'function_name': 'check_prp_hierarchy_naming',
        'report_called': 'report_prp_hierarchy_naming',
        'description': 'Main "prp" groups should follow the naming convention, such as prp_nameA, proxy_nameA.',
        'label': '"prp" hierarchy naming',
        'category': 'naming',
    },
    {
        'function_name': 'check_grp_name',
        'report_called': 'report_grp_name',
        'description': 'Groups that are not "prp_" or "proxy_" should have the prefix "grp_".',
        'label': 'Group names',
        'category': 'naming',
    },
    {
        'function_name': 'check_history',
        'report_called': 'report_history',
        'description': 'The following meshes contain history data.',
        'label': 'History',
        'category': 'modeling',
    },
    {
        'function_name': 'check_group_id',
        'report_called': 'report_group_id',
        'description': 'Group IDs found in the scene. Please remove them.',
        'label': 'Group ID',
        'category': 'modeling',
    },
    {
        'function_name': 'check_ghost_mesh',
        'report_called': 'report_ghost_mesh',
        'description': 'Mesh nodes without connections detected.',
        'label': 'Ghost mesh',
        'category': 'modeling',
    },
    {
        'function_name': 'check_transforms',
        'report_called': 'report_transforms',
        'description': 'The main group and "proxy" groups should have default transform values for translation,'
                       ' rotation, and scale. The pivot point of "prp_" group transforms, when set to default'
                       ' translate/rotation values (0,0,0), must be at the world center. All scale transforms should '
                       'be set to (1,1,1).',
        'label': 'Transforms',
        'category': 'modeling',
    },
    {
        'function_name': 'check_usd_preview',
        'report_called': 'report_usd_preview',
        'description': 'All meshes in the proxy group must have a usdPreviewSurface shader assigned to them.',
        'label': 'USD Preview',
        'category': 'shading',
    },
    {
        'function_name': 'check_tmp_mat',
        'report_called': 'report_tmp_mat',
        'description': 'All meshes in the render group must have a usdPreviewSurface shader assigned to them.',
        'label': 'Temporary Material',
        'category': 'shading',
    },
    {
        'function_name': 'check_shader_naming',
        'report_called': 'report_shader_naming',
        'description': 'All proxy meshes should have shaders named usdPrev_shortNameA, while all render meshes should '
                       'have shaders named matTmp_shortNameA. For instance, for a prop named prp_bowlA, the proxy '
                       'shader should be named usdPrev_bowlA.',
        'label': 'Shader Naming',
        'category': 'shading',
    },
]

sanity_cat_list = [
    {
        'category': 'global',
        'label': "Global"
    },
    {
        'category': 'hierarchy',
        'label': "Hierarchy"
    },
    {
        'category': 'naming',
        'label': "Naming Convention"
    },
    {
        'category': 'modeling',
        'label': "Modeling"
    },
    {
        'category': 'shading',
        'label': "Shading"
    },
]
