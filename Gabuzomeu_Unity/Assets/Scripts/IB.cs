using UnityEngine;
using System.Diagnostics;
using System;
using System.Threading;
using Debug = UnityEngine.Debug;

// ReSharper disable once InconsistentNaming
public class IB : MonoBehaviour {
    public string blenderPath;
    public string pyFilePath;

    private void Awake() {
        var thread = new Thread(Run);
        thread.Start();
    }
    
    private void Run() {
        try {
            // to add  --background
            var processInfo = new ProcessStartInfo();
            //"cmd.exe", 
            processInfo.FileName = "cmd.exe";
            processInfo.Arguments = "/C \"" + blenderPath + " --python " + pyFilePath + "\"";
            processInfo.WindowStyle = ProcessWindowStyle.Maximized;
            //processInfo.CreateNoWindow = true;
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
            if(errorLog == "") Debug.LogError(errorLog);
        }
        catch (Exception e) {
            Debug.LogError(e);
        }
    }
}