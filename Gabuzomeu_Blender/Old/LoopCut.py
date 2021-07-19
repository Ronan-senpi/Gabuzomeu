def loopCut(numberCuts, edgeIndex) : 
    old_type = bpy.context.area.type
    bpy.context.area.type = 'VIEW_3D'
    bpy.ops.object.editmode_toggle()
    def view3d_find( return_area = False ):
        # returns first 3d view, normally we get from context
        for area in bpy.context.window.screen.areas:
            if area.type == 'VIEW_3D':
                v3d = area.spaces[0]
                rv3d = v3d.region_3d
                for region in area.regions:
                    if region.type == 'WINDOW':
                        if return_area: return region, rv3d, v3d, area
                        return region, rv3d, v3d
        return None, None

    region, rv3d, v3d, area = view3d_find(True)

    override = {
        'scene'  : bpy.context.scene,
        'region' : region,
        'area'   : area,
        'space'  : v3d
    }
    bpy.ops.mesh.loopcut_slide(
        override,
        MESH_OT_loopcut = {
            "number_cuts"           : numberCuts,
            "smoothness"            : 0,     
            "falloff"               : 'INVERSE_SQUARE',  # Was 'INVERSE_SQUARE' that does not exist
            "edge_index"            : edgeIndex,
            "mesh_select_mode_init" : (True, False, False),
            "object_index" : 0
        },
        TRANSFORM_OT_edge_slide = {
            "value"           : 0,
            "mirror"          : False, 
            "snap"            : False,
            "snap_target"     : 'CLOSEST',
            "snap_point"      : (0, 0, 0),
            "snap_align"      : False,
            "snap_normal"     : (0, 0, 0),
            "correct_uv"      : False,
            "release_confirm" : False,
            "use_accurate"    : False
        }
    )
    bpy.ops.object.editmode_toggle()
    bpy.context.area.type = old_type 
    old_type = bpy.context.area.type