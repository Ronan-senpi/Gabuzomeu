using UnityEngine;
using System.Diagnostics;
using System;
using System.IO;
using System.Threading;
using UnityEditor;
using Debug = UnityEngine.Debug;

// ReSharper disable once InconsistentNaming
public class IB : MonoBehaviour {
    public string blenderPath;
    public string pyFilePath;

    public void Run() {
        try {
            var processInfo = new ProcessStartInfo();
            processInfo.FileName = "cmd.exe";
            processInfo.Arguments = "/C \"" + blenderPath + " --background --python " + pyFilePath + "\"";
            processInfo.WindowStyle = ProcessWindowStyle.Hidden;
            processInfo.CreateNoWindow = true;
            processInfo.UseShellExecute = false;
            processInfo.RedirectStandardOutput = true;
            processInfo.RedirectStandardError = true;

            var process = new Process();
            process.StartInfo = processInfo;
            process.EnableRaisingEvents = true;
            process.Start();
            process.WaitForExit();
            var outBuffer = process.StandardOutput;
            var errorBuffer = process.StandardError;
            
            Debug.Log(outBuffer.ReadToEnd());
            var errorLog = errorBuffer.ReadToEnd();
            if(errorLog != "") Debug.LogError(errorLog);
            AssetDatabase.Refresh();
            var files = Directory.GetFiles("Assets/Blender");
            Vector3 position = Vector3.zero;
            foreach (var file in files) {
                if (Path.GetExtension(file) == ".obj") {
                    var obj = AssetDatabase.LoadAssetAtPath<GameObject>(file);
                    Instantiate(obj, position, Quaternion.identity);
                    position.x += 2f;
                }
            }
        }
        catch (Exception e) {
            Debug.LogError(e);
        }
    }
}