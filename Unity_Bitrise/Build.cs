#if UNITY_EDITOR

using System.Linq;
using System;
using UnityEditor;
using UnityEditor.Android;
using UnityEngine;
using System.IO;

public static class BuildScript
{
    /// <summary>
    /// creates Xcode project from Unity outputting  to locationPathName
    /// </summary>
    [MenuItem("Build/Build iOS")]
    public static void BuildIos()
    {
        #if UNITY_EDITOR_OSX
        BitriseTools tools = new BitriseTools();
        tools.PrintInputs();

        BuildPlayerOptions buildPlayerOptions = new BuildPlayerOptions();
        buildPlayerOptions.locationPathName = tools.inputs.buildOutput;
        buildPlayerOptions.target = BuildTarget.iOS;
        buildPlayerOptions.options = BuildOptions.None;
        buildPlayerOptions.scenes = GetScenes();
        tools.log.Print("Building iOS");
        BuildPipeline.BuildPlayer(buildPlayerOptions);
        tools.log.Print("Built iOS");
        #endif
    }

    /// <summary>
    /// creates Android project from Unity outputting  to locationPathName
    /// Using androidSdkPath, androidJdkPath and androidNdkPath for the Android SDK settings
    /// </summary>
    [MenuItem("Build/Build Android")]
    public static void BuildAndroid()
    {
        #if UNITY_EDITOR_LINUX
        BitriseTools tools = new BitriseTools();
        tools.PrintInputs();        
        EditorUserBuildSettings.exportAsGoogleAndroidProject = true;

        //https://docs.unity3d.com/ScriptReference/Android.AndroidExternalToolsSettings.html
        //below elements may show as not found depending on Unity version
        AndroidExternalToolsSettings.sdkRootPath=tools.inputs.androidSdkPath;
        AndroidExternalToolsSettings.jdkRootPath=tools.inputs.androidJdkPath;
        AndroidExternalToolsSettings.ndkRootPath=tools.inputs.androidNdkPath;
        
        BuildPlayerOptions buildPlayerOptions = new BuildPlayerOptions();
        buildPlayerOptions.locationPathName = tools.inputs.buildOutput;
        buildPlayerOptions.target = BuildTarget.Android;
        buildPlayerOptions.options = BuildOptions.None;
        buildPlayerOptions.scenes = GetScenes();

        tools.log.Print("****");
        tools.log.Print("AndroidExternalToolsSettings.sdkRootPath");
        tools.log.Print(AndroidExternalToolsSettings.sdkRootPath);
        tools.log.Print("AndroidExternalToolsSettings.jdkRootPath");
        tools.log.Print(AndroidExternalToolsSettings.jdkRootPath);
        tools.log.Print("AndroidExternalToolsSettings.ndkRootPath");
        tools.log.Print(AndroidExternalToolsSettings.ndkRootPath);
        tools.log.Print("****");
        
        tools.log.Print("Building Android");
        BuildPipeline.BuildPlayer(buildPlayerOptions);
        tools.log.Print("Built Android");
        #endif
    }

    /// <summary>
    /// runs BuildIos or BuildAndroid based on buildPlatform flag in inputs (optional)
    /// </summary>
    public static void Build()
    {
        BitriseTools tools = new BitriseTools();
        tools.PrintInputs();
        if (tools.inputs.buildPlatform == BitriseTools.BuildPlatform.android) { 
            BuildAndroid();
        } else if (tools.inputs.buildPlatform == BitriseTools.BuildPlatform.ios) {
            BuildIos();
        } else {
            tools.log.Fail("Invalid buildPlatform: "+tools.inputs.buildPlatform.ToString());
        }
    }

    private static string[] GetScenes()
    {
        return (from scene in EditorBuildSettings.scenes where scene.enabled select scene.path).ToArray();
    }
}

/// <summary>
/// Class <c>BitriseTools</c>
/// reads inputs and provides logging feature
/// </summary>
public class BitriseTools {

    public Inputs inputs;
    public Logging log;

    public enum BuildPlatform {
        unknown,
        android,
        ios,
    }

    public BitriseTools() {
        inputs = new Inputs ();
        log = new Logging ();
    }
        
    //inputs
    public class Inputs {
        public string buildOutput;
        public string androidSdkPath;
        public string androidJdkPath;
        public string androidNdkPath;

        public BuildPlatform buildPlatform;

        public Inputs() {
            string[] cmdArgs = Environment.GetCommandLineArgs();
            
            for(int i=0;i<cmdArgs.Length;i++){
                if (cmdArgs[i].Equals("-buildPlatform")) buildPlatform = (BuildPlatform)Enum.Parse(typeof(BuildPlatform),cmdArgs[i + 1]); //will be switch here rather than on Bitrise side
                if (cmdArgs[i].Equals("-buildOutput")) buildOutput = cmdArgs[i + 1]; //put build in specific place
                if (cmdArgs[i].Equals("-androidSdkPath")) androidSdkPath = cmdArgs[i + 1]; //specify SDK path
                if (cmdArgs[i].Equals("-androidJdkPath")) androidJdkPath = cmdArgs[i + 1]; //specify JDK path
                if (cmdArgs[i].Equals("-androidNdkPath")) androidNdkPath = cmdArgs[i + 1]; //specify JDK path
            }
        }
    }

    //logging
    public class Logging {
        bool initialized = false;

        void _init()
        {
            if (!initialized) {
                StreamWriter sw = new StreamWriter(Console.OpenStandardOutput (), System.Text.Encoding.ASCII);
                sw.AutoFlush = true;
                Console.SetOut(sw);
                initialized = true;
            }
        }
            
        public void Fail(string message) {_init();Console.WriteLine("\x1b[31m"+message+"\x1b[0m");}
        public void Done(string message) {_init();Console.WriteLine("\x1b[32m"+message+"\x1b[0m");}
        public void Info(string message) {_init();Console.WriteLine("\x1b[34m"+message+"\x1b[0m");}
        public void Warn(string message) {_init();Console.WriteLine("\x1b[33m"+message+"\x1b[0m");}
        public void Print(string message) {_init();Console.WriteLine(message);}
    }

    public void PrintInputs() {
        log.Info("Bitrise Unity build script inputs:");
        log.Print(" -buildOutput: "+inputs.buildOutput);
        log.Print(" -buildPlatform: "+inputs.buildPlatform.ToString());
        log.Print(" -androidSdkPath: "+inputs.androidSdkPath);
        log.Print(" -androidJdkPath: "+inputs.androidJdkPath);
        log.Print("");
    }
}

#endif
