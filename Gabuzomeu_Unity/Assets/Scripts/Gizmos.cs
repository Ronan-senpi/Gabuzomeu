using UnityEngine;

public class Gizmos : MonoBehaviour {
    public float gizmoSize = 1f;
    private void OnDrawGizmos() {
        UnityEngine.Gizmos.color = Color.red;
        UnityEngine.Gizmos.DrawSphere(transform.position, gizmoSize);
    }
}
