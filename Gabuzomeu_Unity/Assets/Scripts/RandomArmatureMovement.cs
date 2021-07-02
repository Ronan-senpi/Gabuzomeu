using System.Collections.Generic;
using UnityEngine;

public class RandomArmatureMovement : MonoBehaviour {
    public Transform rootTransform;
    
    public List<Transform> legs;
    public List<Quaternion> firstLegsRotation;
    public List<Transform> spineParts;
    public List<Quaternion> firstSpinePartsRotation;

    public PhysicMaterial physicMaterial;

    public float maxAngleLeg = 5;
    public float maxAngleBack = 90f;

    public float speed = 5;
    private void Awake() {
        Transform root = rootTransform;
        while (root.childCount > 0) {
            int childCount = 0;
            Transform newRoot = root.GetChild(0);
            foreach (Transform child in root) {
                if (child.childCount == 1) {
                    legs.Add(child);
                    firstLegsRotation.Add(child.localRotation);
                    var underChild = child.GetChild(0);
                    if (underChild.childCount > 0) underChild = underChild.GetChild(0);
                    var col = underChild.gameObject.AddComponent<BoxCollider>();
                    col.material = physicMaterial;
                    col.size /= 100;
                    col.size /= 2;

                }
                if (child.childCount > childCount) {
                    childCount = child.childCount;
                    newRoot = child;
                }
            }

            spineParts.Add(newRoot);
            firstSpinePartsRotation.Add(newRoot.localRotation);
            root = newRoot;
        }
    }

    private void Update() {
        /*for (var index = 0; index < spineParts.Count; index++) {
            var spinePart = spineParts[index];
            spinePart.localRotation = firstSpinePartsRotation[index] * Quaternion.Euler(0f, 0, Mathf.Sin((Time.time + index) * 5) * maxAngleBack);
        }*/

        for (var index = 0; index < legs.Count; index++) {
            var leg = legs[index];
            if (index % 2 == 0)
                leg.localRotation = firstLegsRotation[index] * Quaternion.Euler(
                    Mathf.Cos((Time.time + index) * speed) * maxAngleLeg, Mathf.Sin((Time.time + index) * speed) * maxAngleLeg,
                    0);
            else leg.localRotation = firstLegsRotation[index] * Quaternion.Euler(
                -Mathf.Cos((Time.time + index) * speed) * maxAngleLeg, Mathf.Sin((Time.time + index) * speed) * maxAngleLeg,
                0);
        }

    }
}
