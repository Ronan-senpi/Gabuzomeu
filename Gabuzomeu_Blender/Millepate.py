import bpy
import mathutils
from math import sqrt
        #mbArms  posArmX    scaleArmX scaleArmY  scaleArmZ    offsetY   castRadius
input = ['1111','10111101','01100110','10110010','11101000','00100101','10011001']

#int(input[], 2)
nbPawPairs = int(input[0], 2)

              #    [-10,0] 
posArmX = int(input[1], 2) / 256.0 * 10 -10
positionArmOffset = (posArmX, 0, 0)

#               [0,1][0,1][0,1]
scaleArmX = int(input[2], 2) / 256.0
scaleArmY = int(input[3], 2) / 256.0
scaleArmZ = int(input[4], 2) / 256.0
scaleArmOffset = (scaleArmX, scaleArmY, scaleArmZ)

#             [0.1,2.7]
offsetY = int(input[5], 2) / 256.0 * 2.6 + 0.1
arrayOffset = (0, offsetY, 0)
mergeDetection = sqrt(arrayOffset[0]*arrayOffset[0] + arrayOffset[1]*arrayOffset[1] + arrayOffset[2]*arrayOffset[2])
mergeDetection = mergeDetection + mergeDetection*mergeDetection/10

castRadius = int(input[6], 2) / 256.0 * 30


basePaw = (0.5,0.5,0.5)
#Ajouter un cube
bpy.ops.mesh.primitive_cube_add(size=2,
                                enter_editmode=False,
                                align='WORLD',
                                location=(0, 0, 0),
                                scale=(1, 2, 1))

#select cube
obj = bpy.context.active_object

#passe en edit
bpy.ops.object.editmode_toggle()

bpy.ops.mesh.select_all(action='SELECT')

bpy.ops.transform.translate(value=(-0.5, 0, 0), orient_type='GLOBAL')

#Start : Select Faceg
bpy.ops.object.mode_set(mode = 'EDIT') 
bpy.ops.mesh.select_mode(type="FACE")
bpy.ops.mesh.select_all(action = 'DESELECT')
bpy.ops.object.mode_set(mode = 'OBJECT')
obj.data.polygons[0].select = True
bpy.ops.object.mode_set(mode = 'EDIT') 
#end : Select face

#Start : Base pate 
bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={
                                            "value":(0, 0, 0),
                                            "orient_type":'NORMAL'})
bpy.ops.transform.resize(value=basePaw,
                         orient_type='GLOBAL',
                         orient_matrix=((1, 0, 0),
                                        (0, 1, 0),
                                        (0, 0, 1)),
                         orient_matrix_type='GLOBAL',
                         mirror=True,
                         use_proportional_edit=False,
                         proportional_edit_falloff='SMOOTH',
                         proportional_size=1,
                         use_proportional_connected=False,
                         use_proportional_projected=False)
                         
#end : Base pate

#Start : creating paw
for i in range(3) :
    bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={
                                            "value":(-i, 0, 1),
                                            "orient_type":'NORMAL'})
    pos = (positionArmOffset[0],positionArmOffset[1],positionArmOffset[2]*i/2)                                                                          
    bpy.ops.transform.translate(value=pos,orient_type='GLOBAL');#resize(value=positionPaw);
    bpy.ops.transform.resize(value=scaleArmOffset,orient_type='GLOBAL');#resize(value=positionPaw);
#end : creating paw

#Start : le mirroir
bpy.ops.object.modifier_add(type='MIRROR')
bpy.context.object.modifiers["Mirror"].use_clip = True
#End : le mirroir
#Start : Array
bpy.ops.object.modifier_add(type='ARRAY')
bpy.context.object.modifiers["Array"].relative_offset_displace = arrayOffset
bpy.context.object.modifiers["Array"].use_merge_vertices = True
bpy.context.object.modifiers["Array"].use_merge_vertices_cap = True
bpy.context.object.modifiers["Array"].merge_threshold = mergeDetection

bpy.context.object.modifiers["Array"].count = nbPawPairs
#End :Array

#Start : cast
bpy.ops.object.modifier_add(type='CAST')
bpy.context.object.modifiers["Cast"].name = "CastSphere"
bpy.context.object.modifiers["CastSphere"].factor = 0
bpy.context.object.modifiers["CastSphere"].radius = 5


bpy.ops.object.modifier_add(type='CAST')
bpy.context.object.modifiers["Cast"].name = "CastCylinder"
bpy.context.object.modifiers["CastCylinder"].cast_type = 'CYLINDER'
bpy.context.object.modifiers["CastCylinder"].factor = 0.5
bpy.context.object.modifiers["CastCylinder"].radius = castRadius
#end : cast
#Start : sub division
bpy.ops.object.modifier_add(type='SUBSURF')
#End : sub division 

#Head : 
bpy.ops.object.editmode_toggle()

