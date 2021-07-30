using UnityEngine;

public class CreatureHandler : MonoBehaviour
{
    public static GameObject SpawnCreature(GameObject model)
    {
        var go = Instantiate(model);
        var meshRenderers = go.GetComponentsInChildren<MeshRenderer>();
        foreach (var meshRenderer in meshRenderers)
        {
            var mats = meshRenderer.sharedMaterials;
            for (var index = 0; index < mats.Length; ++index)
            {
                
            }
        }
        return go;
    }
}
