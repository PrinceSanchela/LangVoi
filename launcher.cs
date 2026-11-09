using System;
using System.Diagnostics;
using System.IO;
using System.Reflection;
using System.Windows.Forms;

[assembly: AssemblyTitle("LangVoi Voice Studio Pro")]
[assembly: AssemblyDescription("Universal Audio Engineering, Laboratory Acoustic Biometrics & Neural Whisper Language Identification")]
[assembly: AssemblyCompany("Prince Sanchela")]
[assembly: AssemblyProduct("LangVoi Voice Studio Pro")]
[assembly: AssemblyCopyright("Copyright © 2026 Prince Sanchela. All Rights Reserved.")]
[assembly: AssemblyTrademark("LangVoi™ by Prince Sanchela")]
[assembly: AssemblyVersion("2.2.0.0")]
[assembly: AssemblyFileVersion("2.2.0.0")]

namespace LangVoi
{
    static class Program
    {
        [STAThread]
        static void Main()
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);

            string appDir = AppDomain.CurrentDomain.BaseDirectory;
            Directory.SetCurrentDirectory(appDir);

            string scriptPath = Path.Combine(appDir, "run.py");
            if (!File.Exists(scriptPath))
            {
                scriptPath = Path.Combine(appDir, "main.py");
            }

            if (!File.Exists(scriptPath))
            {
                MessageBox.Show(
                    "Error: 'run.py' was not found in directory:\n" + appDir,
                    "LangVoi Voice Studio Pro — Prince Sanchela",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Error
                );
                return;
            }

            // Find pythonw.exe (Windows GUI Python runner) or python.exe
            string pythonExe = FindPythonwExecutable();
            if (string.IsNullOrEmpty(pythonExe))
            {
                MessageBox.Show(
                    "Python was not detected on your system.\nPlease install Python 3.10+ to run LangVoi Voice Studio Pro.",
                    "LangVoi Voice Studio Pro — Missing Python",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Error
                );
                return;
            }

            // Launch Native Desktop Application Silently (No black command box)
            try
            {
                ProcessStartInfo psi = new ProcessStartInfo();
                psi.FileName = pythonExe;
                psi.Arguments = string.Format("\"{0}\"", scriptPath);
                psi.WorkingDirectory = appDir;
                psi.CreateNoWindow = true;
                psi.UseShellExecute = false;
                psi.WindowStyle = ProcessWindowStyle.Hidden;

                Process p = Process.Start(psi);
                if (p != null)
                {
                    p.WaitForExit();
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show(
                    "Error launching LangVoi Voice Studio Pro:\n" + ex.Message,
                    "LangVoi Voice Studio Pro",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Error
                );
            }
        }

        private static string FindPythonwExecutable()
        {
            string[] possiblePaths = new string[]
            {
                @"C:\Python314\pythonw.exe",
                @"C:\Python313\pythonw.exe",
                @"C:\Python312\pythonw.exe",
                @"C:\Python311\pythonw.exe",
                @"C:\Python310\pythonw.exe",
                Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData) + @"\Programs\Python\Python314\pythonw.exe",
                Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData) + @"\Programs\Python\Python313\pythonw.exe",
                Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData) + @"\Programs\Python\Python312\pythonw.exe",
                Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData) + @"\Programs\Python\Python311\pythonw.exe",
                Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData) + @"\Programs\Python\Python310\pythonw.exe",
                "pythonw.exe",
                @"C:\Python314\python.exe",
                "python.exe"
            };

            foreach (string p in possiblePaths)
            {
                try
                {
                    if (File.Exists(p)) return p;
                }
                catch { }
            }

            // Search PATH
            try
            {
                ProcessStartInfo psi = new ProcessStartInfo("where.exe", "pythonw.exe");
                psi.CreateNoWindow = true;
                psi.UseShellExecute = false;
                psi.RedirectStandardOutput = true;
                using (Process proc = Process.Start(psi))
                {
                    string output = proc.StandardOutput.ReadToEnd();
                    proc.WaitForExit();
                    if (proc.ExitCode == 0)
                    {
                        string[] lines = output.Split(new char[] { '\r', '\n' }, StringSplitOptions.RemoveEmptyEntries);
                        if (lines.Length > 0 && File.Exists(lines[0].Trim()))
                        {
                            return lines[0].Trim();
                        }
                    }
                }
            }
            catch { }

            return "pythonw.exe";
        }
    }
}
