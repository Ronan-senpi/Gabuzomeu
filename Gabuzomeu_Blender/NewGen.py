import bpy
import mathutils
from math import sqrt
from math import floor
from mathutils import Euler
import random


def clearScene():
    for collection in bpy.data.collections:
        # Parcourir tous les objets
        for obj in collection.all_objects:
            # Selectionner l'objet
            bpy.data.objects[obj.name].select_set(True)


#Vide la scene
clearScene()
#Créer un cube
bpy.ops.mesh.primitive_cube_add(
    size=2, enter_editmode=False, align="WORLD", location=(0, 0, 0), scale=(1, 1, 1)
)
#passe ne mode edit
bpy.ops.object.editmode_toggle()
#fusione le cube en un point, pour pouvoir extrude sur 1 point plutot qu'une face
#pour pouvoir faire les bones plus tard
mesh = bpy.context.active_object
bpy.ops.mesh.merge(type="CENTER")
bpy.ops.mesh.select_all(action="SELECT")

#Start: du corps de base
#On creer la "tête" de la créature
bpy.ops.mesh.extrude_region_move(
    MESH_OT_extrude_region={
        "use_normal_flip": False,
        "use_dissolve_ortho_edges": False,
        "mirror": False,
    },
    TRANSFORM_OT_translate={
        "value": (0, -1, -0), #Algo gen (Doit TOUJOURS ETRE EN Y)
        "orient_type": "GLOBAL",
        "orient_matrix": ((1, 0, 0), (0, 1, 0), (0, 0, 1)),
        "orient_matrix_type": "GLOBAL",
        "constraint_axis": (False, False, True),
        "mirror": False,
        "use_proportional_edit": False,
        "proportional_edit_falloff": "SMOOTH",
        "proportional_size": 1,
        "use_proportional_connected": False,
        "use_proportional_projected": False,
        "snap": False,
        "snap_target": "CLOSEST",
        "snap_point": (0, 0, 0),
        "snap_align": False,
        "snap_normal": (0, 0, 0),
        "gpencil_strokes": False,
        "cursor_transform": False,
        "texture_space": False,
        "remove_on_cancel": False,
        "release_confirm": False,
        "use_accurate": False,
        "use_automerge_and_split": False,
    },
)
#On créer l'articulation 1G (L'épaule ??)
bpy.ops.mesh.extrude_region_move(
    MESH_OT_extrude_region={
        "use_normal_flip": False,
        "use_dissolve_ortho_edges": False,
        "mirror": False,
    },
    TRANSFORM_OT_translate={
        "value": (-1, -0, -0), #Algo gen
        "orient_type": "GLOBAL",
        "orient_matrix": ((1, 0, 0), (0, 1, 0), (0, 0, 1)),
        "orient_matrix_type": "GLOBAL",
        "constraint_axis": (False, False, True),
        "mirror": False,
        "use_proportional_edit": False,
        "proportional_edit_falloff": "SMOOTH",
        "proportional_size": 1,
        "use_proportional_connected": False,
        "use_proportional_projected": False,
        "snap": False,
        "snap_target": "CLOSEST",
        "snap_point": (0, 0, 0),
        "snap_align": False,
        "snap_normal": (0, 0, 0),
        "gpencil_strokes": False,
        "cursor_transform": False,
        "texture_space": False,
        "remove_on_cancel": False,
        "release_confirm": False,
        "use_accurate": False,
        "use_automerge_and_split": False,
    },
)

#On créer l'articulation 2G (Le bras ??)
bpy.ops.mesh.extrude_region_move(
    MESH_OT_extrude_region={
        "use_normal_flip": False,
        "use_dissolve_ortho_edges": False,
        "mirror": False,
    },
    TRANSFORM_OT_translate={
        "value": (0, -0, -1), #Algo gen
        "orient_type": "GLOBAL",
        "orient_matrix": ((1, 0, 0), (0, 1, 0), (0, 0, 1)),
        "orient_matrix_type": "GLOBAL",
        "constraint_axis": (False, False, True),
        "mirror": False,
        "use_proportional_edit": False,
        "proportional_edit_falloff": "SMOOTH",
        "proportional_size": 1,
        "use_proportional_connected": False,
        "use_proportional_projected": False,
        "snap": False,
        "snap_target": "CLOSEST",
        "snap_point": (0, 0, 0),
        "snap_align": False,
        "snap_normal": (0, 0, 0),
        "gpencil_strokes": False,
        "cursor_transform": False,
        "texture_space": False,
        "remove_on_cancel": False,
        "release_confirm": False,
        "use_accurate": False,
        "use_automerge_and_split": False,
    },
)
#On remote le long l'articulation 2G (Le bras ??)
#ce point sera supp plus tard
bpy.ops.mesh.extrude_region_move(
    MESH_OT_extrude_region={
        "use_normal_flip": False,
        "use_dissolve_ortho_edges": False,
        "mirror": False,
    },
    TRANSFORM_OT_translate={
        "value": (0, -0, 1), #Algo gen (le vecteur negatif de 2G)
        "orient_type": "GLOBAL",
        "orient_matrix": ((1, 0, 0), (0, 1, 0), (0, 0, 1)),
        "orient_matrix_type": "GLOBAL",
        "constraint_axis": (False, False, True),
        "mirror": False,
        "use_proportional_edit": False,
        "proportional_edit_falloff": "SMOOTH",
        "proportional_size": 1,
        "use_proportional_connected": False,
        "use_proportional_projected": False,
        "snap": False,
        "snap_target": "CLOSEST",
        "snap_point": (0, 0, 0),
        "snap_align": False,
        "snap_normal": (0, 0, 0),
        "gpencil_strokes": False,
        "cursor_transform": False,
        "texture_space": False,
        "remove_on_cancel": False,
        "release_confirm": False,
        "use_accurate": False,
        "use_automerge_and_split": False,
    },
)
#On remote le long l'articulation 1G (L'épaule ??)
#ce point sera supp plus tard
bpy.ops.mesh.extrude_region_move(
    MESH_OT_extrude_region={
        "use_normal_flip": False,
        "use_dissolve_ortho_edges": False,
        "mirror": False,
    },
    TRANSFORM_OT_translate={
        "value": (1, -0, 0),#Algo gen (le vecteur negatif de 1G)
        "orient_type": "GLOBAL",
        "orient_matrix": ((1, 0, 0), (0, 1, 0), (0, 0, 1)),
        "orient_matrix_type": "GLOBAL",
        "constraint_axis": (False, False, True),
        "mirror": False,
        "use_proportional_edit": False,
        "proportional_edit_falloff": "SMOOTH",
        "proportional_size": 1,
        "use_proportional_connected": False,
        "use_proportional_projected": False,
        "snap": False,
        "snap_target": "CLOSEST",
        "snap_point": (0, 0, 0),
        "snap_align": False,
        "snap_normal": (0, 0, 0),
        "gpencil_strokes": False,
        "cursor_transform": False,
        "texture_space": False,
        "remove_on_cancel": False,
        "release_confirm": False,
        "use_accurate": False,
        "use_automerge_and_split": False,
    },
)

#On créer l'articulation 1D (L'épaule ??)
bpy.ops.mesh.extrude_region_move(
    MESH_OT_extrude_region={
        "use_normal_flip": False,
        "use_dissolve_ortho_edges": False,
        "mirror": False,
    },
    TRANSFORM_OT_translate={
        "value": (1, -0, 0),#Algo gen 
        "orient_type": "GLOBAL",
        "orient_matrix": ((1, 0, 0), (0, 1, 0), (0, 0, 1)),
        "orient_matrix_type": "GLOBAL",
        "constraint_axis": (False, False, True),
        "mirror": False,
        "use_proportional_edit": False,
        "proportional_edit_falloff": "SMOOTH",
        "proportional_size": 1,
        "use_proportional_connected": False,
        "use_proportional_projected": False,
        "snap": False,
        "snap_target": "CLOSEST",
        "snap_point": (0, 0, 0),
        "snap_align": False,
        "snap_normal": (0, 0, 0),
        "gpencil_strokes": False,
        "cursor_transform": False,
        "texture_space": False,
        "remove_on_cancel": False,
        "release_confirm": False,
        "use_accurate": False,
        "use_automerge_and_split": False,
    },
)
#On créer l'articulation 2D (L'épaule ??)
bpy.ops.mesh.extrude_region_move(
    MESH_OT_extrude_region={
        "use_normal_flip": False,
        "use_dissolve_ortho_edges": False,
        "mirror": False,
    },
    TRANSFORM_OT_translate={
        "value": (0, -0, -1),#Algo gen 
        "orient_type": "GLOBAL",
        "orient_matrix": ((1, 0, 0), (0, 1, 0), (0, 0, 1)),
        "orient_matrix_type": "GLOBAL",
        "constraint_axis": (False, False, True),
        "mirror": False,
        "use_proportional_edit": False,
        "proportional_edit_falloff": "SMOOTH",
        "proportional_size": 1,
        "use_proportional_connected": False,
        "use_proportional_projected": False,
        "snap": False,
        "snap_target": "CLOSEST",
        "snap_point": (0, 0, 0),
        "snap_align": False,
        "snap_normal": (0, 0, 0),
        "gpencil_strokes": False,
        "cursor_transform": False,
        "texture_space": False,
        "remove_on_cancel": False,
        "release_confirm": False,
        "use_accurate": False,
        "use_automerge_and_split": False,
    },
)
#supprimes les points -1G et -2G 
bpy.ops.mesh.select_all(action="SELECT")
bpy.ops.mesh.remove_doubles()
#Start: du corps de base

# editmode
bpy.ops.object.editmode_toggle()
# objectmode

#Start : Array modifier
#Pour le nombre de paire de pattes 
bpy.ops.object.modifier_add(type="ARRAY")
bpy.context.object.modifiers["Array"].relative_offset_displace[0] = 0
bpy.context.object.modifiers["Array"].relative_offset_displace[1] = -1 # Corespond au Y de la position de la tête
bpy.context.object.modifiers["Array"].relative_offset_displace[2] = 0
bpy.context.object.modifiers["Array"].count = 10 #algo gen
bpy.context.object.modifiers["Array"].use_merge_vertices = True

#Applique l'array modifier 
bpy.ops.object.modifier_apply(modifier="Array", report=True)
#End : Array modifier

#Place la créature au centre de la scene
bpy.ops.object.editmode_toggle()
bpy.ops.mesh.select_all(action="SELECT")
bpy.ops.transform.translate(
    value=(0, 5, 1), #(0, (longeurTete * NombrePairePate)/2, 1)
    orient_type="GLOBAL",
    orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
    orient_matrix_type="GLOBAL",
    constraint_axis=(False, True, False),
    mirror=True,
    use_proportional_edit=False,
    proportional_edit_falloff="SMOOTH",
    proportional_size=1,
    use_proportional_connected=False,
    use_proportional_projected=False,
)

bpy.ops.object.editmode_toggle()
bpy.ops.object.modifier_add(type="CAST")
bpy.context.object.modifiers["Cast"].factor = 3.25 #Algo gen
bpy.context.object.modifiers["Cast"].radius = 2.7 #Algo gen

#Créer Le model 
bpy.ops.object.modifier_add(type="SKIN")
bpy.context.object.modifiers["Skin"].use_smooth_shade = True
bpy.ops.object.skin_armature_create(modifier="Skin")

# fusione armature et mesh
bpy.data.objects[bpy.data.collections[0].all_objects[1].name].select_set(True)
bpy.data.objects[bpy.data.collections[0].all_objects[0].name].select_set(True)
bpy.ops.object.parent_set(type="ARMATURE_AUTO")

# armature = bpy.context.active_object
# bpy.ops.object.parent_set(type='ARMATURE_AUTO')
