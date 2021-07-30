using UnityEngine;
using System.Diagnostics;
using System;
using System.IO;
using UnityEditor;
using Debug = UnityEngine.Debug;

// ReSharper disable once InconsistentNaming
public class IB : MonoBehaviour
{
    public string blenderPath;
    public string pyFilePath;
    public Material materialForCreatures;

    private Process _process;

    public void Run()
    {
        try
        {
            var processInfo = new ProcessStartInfo();
            processInfo.FileName = "cmd.exe";
            processInfo.Arguments = "/C \"" + blenderPath + " --background --python " + pyFilePath + "\"";
            processInfo.WindowStyle = ProcessWindowStyle.Hidden;
            processInfo.CreateNoWindow = true;
            //processInfo.UseShellExecute = false;
            //processInfo.RedirectStandardOutput = true;
            //processInfo.RedirectStandardError = true;

            Directory.CreateDirectory("Assets/Blender");
            _process = new Process();
            _process.StartInfo = processInfo;
            _process.Start();
            _process.WaitForExit();
            AssetDatabase.Refresh();
            
            //var outBuffer = _process.StandardOutput;
            //var errorBuffer = _process.StandardError;

            //Debug.Log(outBuffer.ReadToEnd());
            //var errorLog = errorBuffer.ReadToEnd();
            //if (errorLog != "") Debug.LogError(errorLog);

            var files = Directory.GetFiles("Assets/Blender");
            Vector3 offset = Vector3.zero;
            foreach (var file in files)
            {
                if (Path.GetExtension(file) == ".obj")
                {
                    AssetDatabase.ImportAsset(file);
                    var obj = AssetDatabase.LoadAssetAtPath<GameObject>(file);
                    
                    var go = CreatureHandler.SpawnCreature(obj);
                    offset += Vector3.right * 20;
                    go.transform.position += offset;


                    /*var go = Instantiate(obj);
                    foreach (var meshRenderer in go.GetComponentsInChildren<MeshRenderer>())
                    {
                        var mats = meshRenderer.sharedMaterials;
                        for (var index = 0; index < mats.Length; index++)
                        {
                            mats[index] = materialForCreatures;
                        }

                        meshRenderer.sharedMaterials = mats;
                    }*/
                }
            }
        }
        catch (Exception e)
        {
            Debug.LogError(e);
        }
    }
}