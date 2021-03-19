using System.IO;
using UnityEditor;
using UnityEngine;

// ReSharper disable once CheckNamespace
// ReSharper disable once InconsistentNaming
[CustomEditor(typeof(IB))]
public class IBEditor : Editor {
    private SerializedProperty _blenderPathProperty;
    private SerializedProperty _pyFilePathProperty;
    private SerializedProperty _creaturesMaterialProperty;

    private void OnEnable() {
        _blenderPathProperty = serializedObject.FindProperty("blenderPath");
        _pyFilePathProperty = serializedObject.FindProperty("pyFilePath");
        _creaturesMaterialProperty = serializedObject.FindProperty("materialForCreatures");
    }
    
    public override void OnInspectorGUI() {
        serializedObject.Update();
        GUILayout.BeginHorizontal();
        EditorGUILayout.PropertyField(_blenderPathProperty);
        if (GUILayout.Button("Browse")) {
            string value = _blenderPathProperty.stringValue;
            _blenderPathProperty.stringValue =
                "\"" + EditorUtility.OpenFilePanel("Select blender app", Path.GetDirectoryName(value.Trim('"')), "exe") + "\"";
        }
        GUILayout.EndHorizontal();
        GUILayout.BeginHorizontal();
        EditorGUILayout.PropertyField(_pyFilePathProperty);
        if (GUILayout.Button("Browse")) {
            var value = _pyFilePathProperty.stringValue;
            _pyFilePathProperty.stringValue =
                "\"" + EditorUtility.OpenFilePanel("Select python file", Path.GetDirectoryName(value.Trim('"')), "py") + "\"";
        }
        GUILayout.EndHorizontal();
        EditorGUILayout.PropertyField(_creaturesMaterialProperty);
        if (GUILayout.Button("Run")) {
            ((IB) target).Run();
        }
        serializedObject.ApplyModifiedProperties();
    }
}
