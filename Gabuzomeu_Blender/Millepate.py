import bpy
import mathutils
from math import sqrt
from math import floor
from mathutils import Euler
import random
def clearScene():
    bpy.ops.object.mode_set(mode='OBJECT')
    for obj in bpy.context.scene.objects:
        obj.select_set(True)

    bpy.ops.object.delete()

def translate(vec):
    bpy.ops.transform.translate(value=vec)
    
def rotate(rotation):
    bpy.context.active_object.rotation_euler = Euler(rotation, 'XYZ')
        
#perfectDNA = ['0110', '11100100', '01100100', '10110011', '01001110', '10011000', '11001011']

                #nbArms, vertebralLenght, shoulderLength, armLength, abdomenFactor, abdomenRadius
perfectDNA =  ['1011', '11101100', '00001101', '00001100', '01000101', '11101111']


def crossOver(DNA1, DNA2) : 
    #transofme le tableau d'adn en un string
    concatDNA1 = ''.join(DNA1)
    concatDNA2 = ''.join(DNA2)
    lenMin = 1
    lenMax = min(len(concatDNA1), len(concatDNA2))
    if lenMax > 1 :
        lenMax -= 1
    split = random.randint(lenMin, lenMax)
    newDNA1 = concatDNA1[:split]
    newDNA1 += concatDNA2[split:]
    newDNA2 = concatDNA2[:split]
    newDNA2 += concatDNA1[split:]
    return [DnaStringToDnaArray(newDNA1),DnaStringToDnaArray(newDNA2)]

#Transforme une ligne d'ADN en tableau d'ADN
def DnaStringToDnaArray(str) :
    arr = []
    arr.append(str[:4])
    for i in range(1, 6) : 
        arr.append(str[4+(i-1)*8:4+i*8])
    return arr

#Détérmine la fitness de l'adn passer en parametre par rapport a l'adn parfait
def fitness(currentDNA) :
    fitnessScore = 0
    #Concat les tableau d'adn
    concatPerfectDNA = ''.join(perfectDNA)
    concatDNA =  ''.join(currentDNA)
    #Sur chaque bit
    for i in range(len(concatPerfectDNA)) :
        #on verifie si les bit son identique
        if i < len(concatDNA) and concatPerfectDNA[i] == concatDNA[i] :
            fitnessScore+=1
            
    #Retourne le score final
  #  print("fitness of " + str(currentDNA) + " : " + str(fitnessScore))
    return fitnessScore

def generateDNA():
    nbArms = random.randint(0, 15)
    vertebraLength = random.randint(0,255)
    shoulderLength = random.randint(0,255)
    armLength = random.randint(0,255)
    abdomenFactor = random.randint(0,255)
    abdomenRadius = random.randint(0,255)
    
    geneticCode = [format(nbArms, "04b"), format(vertebraLength, "08b"),format(shoulderLength, "08b"), 
    format(armLength, "08b"), format(abdomenFactor, "08b"), format(abdomenRadius, "08b")]
    return geneticCode

def chooseRandomParents(parents):
    a = 0
    b = 0
    while a == b:
        a = random.randint(0, len(parents)-1)
        b = random.randint(0, len(parents)-1)
    return[parents[a],parents[b]]

def mutation(geneticDNA, numberOfMutation):
        
    for i in range(numberOfMutation):
        if(random.randint(0,100) < 10):
            posX = random.randint(0, len(geneticDNA) - 1)
            print("size of random")
            print(posX)
            listDNA = list(geneticDNA[posX])
            posY = random.randint(0, len(listDNA[posX]) - 1)
            if(listDNA[posY] == "1"):
                listDNA[posY] = "0"
            else:
                listDNA[posY] = "1"
            geneticDNA.remove(geneticDNA[posX])
            geneticDNA.insert(posX, "".join(listDNA))
    return geneticDNA

def generateTwoChilds(bestPopulation):
    if bestPopulation is None:
        print("best is none")
        return [generateDNA(),generateDNA()]
    else:
        
        print("===========================bestPopulation====================")
        print(bestPopulation)
        parents = chooseRandomParents(bestPopulation)
        print("===========================parents====================")
        print(parents)
        children = crossOver(parents[0],parents[1])
        print("===========================children====================")
        print(children)
        children[0] = mutation(children[0], 3)
        children[1] = mutation(children[1], 3)
        return children

def choseBestBuddys(population, parentsAmount):
    theBestsOnes = []
    tuples = []
    for DNA in population:
        tuples.append( (fitness(DNA), DNA) )
    sorted(tuples, key=lambda x: x[0])
    for i in range(parentsAmount):
        #print("You are the choosen one Anakin : " + str(tuples[i]))
        theBestsOnes.append(tuples[i][1])
    return theBestsOnes
  
def generatePopulation(size, previousPopulation):
    parents = None
    if previousPopulation is not None:
        parents = choseBestBuddys(previousPopulation,int(size/4))
    
    newSize = size
    if size % 2 != 0 :
        newSize +=1
    newSize = int(newSize/2)
    count = 0
    population = []
    for i in range(newSize):
        children = generateTwoChilds(parents)
        population.append(children[0])
        count+=1
        if count < size:
            population.append(children[1])
            count+=1
    return population


def generateCreature(DNA, creaturePosition, creatureRotation):
    
    nbArms = int(int(DNA[0], 2))
    vertebraLength = int(DNA[1], 2) / 256.0 * 5-5
    shoulderLength = int(DNA[2], 2) / 256.0 * 5
    armLength = int(DNA[3], 2) / 256.0 * 10
    abdomenFactor = int(DNA[4], 2) / 255.0 * 5 + 10
    abdomenRadius = int(DNA[5], 2) / 255.0 * 10 + 2
    print("=================VALUE=================")
    print(nbArms)
    print(vertebraLength)
    print(shoulderLength)
    print(armLength)
    print(abdomenFactor)
    print(abdomenRadius)
    #Créer un cube
    bpy.ops.mesh.primitive_cube_add(
        size=2, enter_editmode=False, align="WORLD", location=(0, 0, 0), scale=(1, 1, 1)
    )
    #passe en mode edit
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
            "value": (0, vertebraLength, -0), #Algo gen (Doit TOUJOURS ETRE EN Y)
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
            "value": (-shoulderLength, -0, -0), #Algo gen
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
            "value": (0, -0, -armLength), #Algo gen
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
            "value": (0, -0, armLength), #Algo gen (le vecteur negatif de 2G)
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
            "value": (shoulderLength, -0, 0),#Algo gen (le vecteur negatif de 1G)
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
            "value": (shoulderLength, -0, 0),#Algo gen 
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
            "value": (0, -0, -armLength),#Algo gen 
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
    bpy.context.object.modifiers["Array"].count = nbArms #algo gen
    bpy.context.object.modifiers["Array"].use_merge_vertices = True

    #Applique l'array modifier 
    bpy.ops.object.modifier_apply(modifier="Array", report=True) 
    #End : Array modifier 
 
    #Place la créature au centre de la scene 
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.transform.translate(
        value=(0, -(vertebraLength * nbArms) / 2, 1), #(0, (longeurTete * NombrePairePate)/2, 1)
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
    bpy.context.object.modifiers["Cast"].factor = abdomenFactor #Algo gen
    bpy.context.object.modifiers["Cast"].radius = abdomenRadius #Algo gen
    bpy.ops.object.modifier_apply(modifier="Cast", report=True)

    #Créer Le model 
    bpy.ops.object.modifier_add(type="SKIN")
    bpy.context.object.modifiers["Skin"].use_smooth_shade = True
    bpy.ops.object.skin_armature_create(modifier="Skin")

    # fusione armature et mesh
    bpy.data.objects[bpy.data.collections[0].all_objects[1].name].select_set(True)
    bpy.data.objects[bpy.data.collections[0].all_objects[0].name].select_set(True)
    bpy.ops.object.parent_set(type="ARMATURE_AUTO")

def randomVector3(xRange,yRange,zRange):
    return (random.random()*xRange*2-xRange,random.random()*yRange*2-yRange,random.random()*zRange*2-zRange)

#print("==================== BEGINING ====================")

#clearScene()
population = generatePopulation(8,None)
generations = 50
for i in range(generations):
    population = generatePopulation(8,population)
    
for i in range(len(population)):
    x = (i % 5)
    y = floor(i / 5)
    DNA = population[i]
   # print("("+str(x)+","+str(y)+")")
    print(DNA)
    generateCreature(DNA, (x * 50,y * 50,0), (0,0,0))


#print("==================== OBJ ====================")
i = 0
scene = bpy.context.scene
for ob in scene.objects:
    ob.select_set(False)
for ob in scene.objects:
    #make the current object active and select it
    bpy.context.view_layer.objects.active = ob
    ob.select_set(True)

    #make sure that we only export meshes
  #  if ob.type == 'MESH':
    #export the currently selected object to its own file based on its name
    bpy.ops.export_scene.obj(filepath="D:/Documents/Projets/Gabuzomeu/Gabuzomeu_Unity/Assets/Blender/result" + str(i) + ".obj", use_selection=True, use_materials=False)
    # deselect the object and move on to another if any more are left
    ob.select_set(False)
    i += 1