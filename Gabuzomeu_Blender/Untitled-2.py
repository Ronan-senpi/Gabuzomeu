import bpy
import bmesh
from mathutils import Vector
from random import randint, uniform
def makeRig(obj, coord) : 
    bpy.ops.object.posemode_toggle()
    print('OBJ')
    print(obj)
    # Commandes de base à utiliser
    # Faire des extrude sur l'armature pour avoir des bones
    bpy.ops.armature.extrude_move(TRANSFORM_OT_translate={"value":coord})
    # Faire des Ik : Inverse Kinematics (Cinématique Inverse)
 
    # Passer ici en Pose Mode
    bpy.ops.pose.constraint_add(type='IK')

    # Après avoir sélectionner le perso + l'armature, faire le Skin (CTRL P)4
    bpy.ops.object.parent_set(type='ARMATURE_AUTO')

    bpy.ops.object.posemode_toggle()

# Quelques raccourcis
context = bpy.context
scene = context.scene

# Création de l'armature


# On crée un Objet de type Mesh
me = bpy.data.meshes.new("Thing")
ob = bpy.data.objects.new("Thing", me)
#select obj
ob.select_set(True)

# On crée un Bmesh
bm = bmesh.new()
root = bm.verts.new()

newvert1 = bm.verts.new((2, 2, 2))
newedge = bm.edges.new([root, newvert1])
newvert2 = bm.verts.new((5, 2, 2))
newedge = bm.edges.new([newvert1, newvert2])

for i in range(4): # tree branches
    v = root
    for l in range(randint(1, 4)):
        ret = bmesh.ops.extrude_vert_indiv(bm, verts=[v])
        for v in ret['verts']:
            v.co += Vector([uniform(1, 1) for axis in "xyz"])
            makeRig(bpy.data.objects['Thing'], v.co)
        bm.to_mesh(me)

# placement de l'objet
ob.location = (0, 0, 0)
# Modifier Skin
skin = ob.modifiers.new(name="Skin", type='SKIN')
sub = ob.modifiers.new(name="Sub", type='SUBSURF')
sub.levels = 2
# Ajout de l'objet dans la scène
scene.collection.objects.link(ob)

#Selection de l'objet
bpy.data.objects['Thing'].select_get()

