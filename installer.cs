using System;
using System.IO;
using System.Drawing;
using System.Reflection;
using System.Diagnostics;
using System.Windows.Forms;
using Microsoft.Win32;
using System.Runtime.InteropServices;

[assembly: AssemblyTitle("LangVoi Voice Studio Pro Setup Wizard")]
[assembly: AssemblyDescription("Universal Audio Engineering, Laboratory Acoustic Biometrics & Neural Whisper Language Identification")]
[assembly: AssemblyCompany("Prince Sanchela")]
[assembly: AssemblyProduct("LangVoi Voice Studio Pro")]
[assembly: AssemblyCopyright("Copyright © 2026 Prince Sanchela. All Rights Reserved.")]
[assembly: AssemblyTrademark("LangVoi™ by Prince Sanchela")]
[assembly: AssemblyVersion("2.2.0.0")]
[assembly: AssemblyFileVersion("2.2.0.0")]

namespace LangVoi.Installer
{
    public class SetupForm : Form
    {
        private TextBox txtInstallDir;
        private CheckBox chkDesktopShortcut;
        private CheckBox chkStartMenuShortcut;
        private CheckBox chkLaunchApp;
        private ProgressBar prgProgress;
        private Label lblStatus;
        private Button btnInstall;
        private Button btnCancel;

        private string sourceDir;

        [STAThread]
        public static void Main()
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            Application.Run(new SetupForm());
        }

        public SetupForm()
        {
            this.sourceDir = AppDomain.CurrentDomain.BaseDirectory;

            // Form Properties
            this.Text = "LangVoi Voice Studio Pro v2.2 — Setup Wizard";
            this.Size = new Size(580, 480);
            this.MinimumSize = new Size(580, 480);
            this.StartPosition = FormStartPosition.CenterScreen;
            this.FormBorderStyle = FormBorderStyle.FixedDialog;
            this.MaximizeBox = false;
            this.BackColor = Color.FromArgb(15, 23, 42); // Theme.BG_ROOT (Midnight Slate)
            this.ForeColor = Color.FromArgb(241, 245, 249);
            this.Font = new Font("Segoe UI", 9.25f, FontStyle.Regular);

            // Try to set Form Icon
            string icoPath = Path.Combine(sourceDir, "assets", "app_icon.ico");
            if (File.Exists(icoPath))
            {
                try { this.Icon = new Icon(icoPath); } catch { }
            }

            BuildUI();
        }

        private void BuildUI()
        {
            // 1. Header Banner
            Panel pnlHeader = new Panel
            {
                Dock = DockStyle.Top,
                Height = 80,
                BackColor = Color.FromArgb(11, 14, 20)
            };

            Label lblTitle = new Label
            {
                Text = "LangVoi Voice Studio Pro",
                Font = new Font("Segoe UI", 14f, FontStyle.Bold),
                ForeColor = Color.FromArgb(56, 189, 248), // Cyan
                Location = new Point(18, 12),
                AutoSize = true
            };

            Label lblSub = new Label
            {
                Text = "Universal Audio Workstation & Neural Whisper LID • Created by Prince Sanchela",
                Font = new Font("Segoe UI", 8.5f, FontStyle.Regular),
                ForeColor = Color.FromArgb(148, 163, 184),
                Location = new Point(20, 42),
                AutoSize = true
            };

            pnlHeader.Controls.Add(lblTitle);
            pnlHeader.Controls.Add(lblSub);
            this.Controls.Add(pnlHeader);

            // 2. Main Content Container
            Panel pnlBody = new Panel
            {
                Location = new Point(20, 95),
                Size = new Size(525, 290)
            };

            // Destination Folder Group
            Label lblDestPrompt = new Label
            {
                Text = "Destination Installation Folder:",
                Font = new Font("Segoe UI", 9f, FontStyle.Bold),
                ForeColor = Color.FromArgb(226, 232, 240),
                Location = new Point(0, 0),
                AutoSize = true
            };

            string defaultTarget = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData), "Programs", "LangVoi");

            txtInstallDir = new TextBox
            {
                Text = defaultTarget,
                Location = new Point(0, 24),
                Size = new Size(415, 24),
                BackColor = Color.FromArgb(8, 10, 16),
                ForeColor = Color.FromArgb(56, 189, 248),
                Font = new Font("Segoe UI", 9f)
            };

            Button btnBrowse = new Button
            {
                Text = "Browse...",
                Location = new Point(425, 22),
                Size = new Size(95, 27),
                BackColor = Color.FromArgb(30, 41, 59),
                ForeColor = Color.White,
                FlatStyle = FlatStyle.Flat
            };
            btnBrowse.Click += (s, e) =>
            {
                using (FolderBrowserDialog fbd = new FolderBrowserDialog())
                {
                    fbd.SelectedPath = txtInstallDir.Text;
                    if (fbd.ShowDialog() == DialogResult.OK)
                    {
                        txtInstallDir.Text = fbd.SelectedPath;
                    }
                }
            };

            pnlBody.Controls.Add(lblDestPrompt);
            pnlBody.Controls.Add(txtInstallDir);
            pnlBody.Controls.Add(btnBrowse);

            // Additional Tasks (Asks the user directly!)
            Label lblTasks = new Label
            {
                Text = "Select Additional Options:",
                Font = new Font("Segoe UI", 9f, FontStyle.Bold),
                ForeColor = Color.FromArgb(226, 232, 240),
                Location = new Point(0, 75),
                AutoSize = true
            };

            chkDesktopShortcut = new CheckBox
            {
                Text = "Create a Desktop shortcut icon (Recommended)",
                Checked = true,
                Location = new Point(5, 102),
                Size = new Size(450, 24),
                ForeColor = Color.FromArgb(241, 245, 249)
            };

            chkStartMenuShortcut = new CheckBox
            {
                Text = "Create a Start Menu shortcut program group",
                Checked = true,
                Location = new Point(5, 130),
                Size = new Size(450, 24),
                ForeColor = Color.FromArgb(241, 245, 249)
            };

            chkLaunchApp = new CheckBox
            {
                Text = "Launch LangVoi Voice Studio Pro after setup completes",
                Checked = true,
                Location = new Point(5, 158),
                Size = new Size(450, 24),
                ForeColor = Color.FromArgb(241, 245, 249)
            };

            pnlBody.Controls.Add(lblTasks);
            pnlBody.Controls.Add(chkDesktopShortcut);
            pnlBody.Controls.Add(chkStartMenuShortcut);
            pnlBody.Controls.Add(chkLaunchApp);

            // Progress Bar & Status
            lblStatus = new Label
            {
                Text = "Ready to install. Click 'Install Now' to begin.",
                Location = new Point(0, 215),
                Size = new Size(520, 20),
                ForeColor = Color.FromArgb(148, 163, 184)
            };

            prgProgress = new ProgressBar
            {
                Location = new Point(0, 240),
                Size = new Size(520, 18),
                Style = ProgressBarStyle.Blocks,
                Value = 0
            };

            pnlBody.Controls.Add(lblStatus);
            pnlBody.Controls.Add(prgProgress);
            this.Controls.Add(pnlBody);

            // 3. Footer Bar with Action Buttons
            Panel pnlFooter = new Panel
            {
                Dock = DockStyle.Bottom,
                Height = 55,
                BackColor = Color.FromArgb(11, 14, 20)
            };

            btnCancel = new Button
            {
                Text = "Cancel",
                Location = new Point(335, 12),
                Size = new Size(95, 30),
                BackColor = Color.FromArgb(30, 41, 59),
                ForeColor = Color.White,
                FlatStyle = FlatStyle.Flat
            };
            btnCancel.Click += (s, e) => this.Close();

            btnInstall = new Button
            {
                Text = "Install Now",
                Location = new Point(440, 12),
                Size = new Size(105, 30),
                BackColor = Color.FromArgb(2, 132, 199), // Cyan Blue
                ForeColor = Color.White,
                Font = new Font("Segoe UI", 9.25f, FontStyle.Bold),
                FlatStyle = FlatStyle.Flat
            };
            btnInstall.Click += BtnInstall_Click;

            pnlFooter.Controls.Add(btnCancel);
            pnlFooter.Controls.Add(btnInstall);
            this.Controls.Add(pnlFooter);
        }

        private void BtnInstall_Click(object sender, EventArgs e)
        {
            btnInstall.Enabled = false;
            btnCancel.Enabled = false;
            txtInstallDir.Enabled = false;
            chkDesktopShortcut.Enabled = false;
            chkStartMenuShortcut.Enabled = false;
            chkLaunchApp.Enabled = false;

            string targetDir = txtInstallDir.Text.Trim();
            if (string.IsNullOrEmpty(targetDir))
            {
                MessageBox.Show("Please specify a valid installation directory.", "Invalid Path", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                btnInstall.Enabled = true;
                btnCancel.Enabled = true;
                return;
            }

            try
            {
                lblStatus.Text = "Creating installation directory...";
                prgProgress.Value = 10;
                Directory.CreateDirectory(targetDir);

                // Copy files
                lblStatus.Text = "Copying core application files...";
                prgProgress.Value = 25;
                string[] files = new string[] { "LangVoi_Studio.exe", "LangVoi_Studio.bat", "run.py", "main.py", "requirements.txt", "README.md", "LICENSE.txt" };
                foreach (string f in files)
                {
                    string src = Path.Combine(sourceDir, f);
                    if (File.Exists(src))
                    {
                        File.Copy(src, Path.Combine(targetDir, f), true);
                    }
                }

                // Copy directories
                lblStatus.Text = "Copying modules and high-res assets...";
                prgProgress.Value = 50;
                string[] dirs = new string[] { "app", "core", "samples", "assets" };
                foreach (string d in dirs)
                {
                    string sDir = Path.Combine(sourceDir, d);
                    string tDir = Path.Combine(targetDir, d);
                    if (Directory.Exists(sDir))
                    {
                        CopyDirectory(sDir, tDir);
                    }
                }

                // Create Uninstaller
                lblStatus.Text = "Registering Windows uninstaller...";
                prgProgress.Value = 70;
                string uninstBat = Path.Combine(targetDir, "Uninstall.bat");
                string uninstScript = string.Format(
                    "@echo off\r\ntitle Uninstalling LangVoi Voice Studio Pro...\r\npowershell -NoProfile -ExecutionPolicy Bypass -Command \"Remove-Item -Force -ErrorAction SilentlyContinue '$env:USERPROFILE\\Desktop\\LangVoi Voice Studio Pro.lnk'; Remove-Item -Force -ErrorAction SilentlyContinue '$env:OneDrive\\Desktop\\LangVoi Voice Studio Pro.lnk'; Remove-Item -Recurse -Force -ErrorAction SilentlyContinue '$env:APPDATA\\Microsoft\\Windows\\Start Menu\\Programs\\LangVoi'; Remove-Item -Recurse -Force -ErrorAction SilentlyContinue '{0}'; Remove-ItemProperty -Path 'HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\LangVoi' -ErrorAction SilentlyContinue\"\r\necho LangVoi Studio has been completely uninstalled.\r\npause\r\n",
                    targetDir
                );
                File.WriteAllText(uninstBat, uninstScript);

                // Shortcuts
                lblStatus.Text = "Configuring shortcuts...";
                prgProgress.Value = 85;

                string exePath = Path.Combine(targetDir, "LangVoi_Studio.exe");
                string icoPath = Path.Combine(targetDir, "assets", "app_icon.ico");

                if (chkDesktopShortcut.Checked)
                {
                    string desktopDir = GetSafeDesktopDirectory();
                    if (!string.IsNullOrEmpty(desktopDir))
                    {
                        string lnkPath = Path.Combine(desktopDir, "LangVoi Voice Studio Pro.lnk");
                        CreateWindowsShortcut(lnkPath, exePath, targetDir, "LangVoi Voice Studio Pro - HD Audio Engineering & Neural Whisper Language Identification", icoPath);
                    }
                }

                if (chkStartMenuShortcut.Checked)
                {
                    string startMenu = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData), @"Microsoft\Windows\Start Menu\Programs\LangVoi");
                    Directory.CreateDirectory(startMenu);
                    string lnkPath = Path.Combine(startMenu, "LangVoi Voice Studio Pro.lnk");
                    CreateWindowsShortcut(lnkPath, exePath, targetDir, "LangVoi Voice Studio Pro", icoPath);
                }

                // Registry entry in Windows Add/Remove Programs
                try
                {
                    using (RegistryKey key = Registry.CurrentUser.CreateSubKey(@"Software\Microsoft\Windows\CurrentVersion\Uninstall\LangVoi"))
                    {
                        if (key != null)
                        {
                            key.SetValue("DisplayName", "LangVoi Voice Studio Pro");
                            key.SetValue("DisplayVersion", "2.2");
                            key.SetValue("Publisher", "Prince Sanchela");
                            key.SetValue("InstallLocation", targetDir);
                            key.SetValue("UninstallString", "\"" + uninstBat + "\"");
                            key.SetValue("DisplayIcon", icoPath);
                        }
                    }
                }
                catch { }

                prgProgress.Value = 100;
                lblStatus.Text = "Installation completed successfully!";
                lblStatus.ForeColor = Color.FromArgb(74, 222, 128); // Green

                MessageBox.Show(
                    "LangVoi Voice Studio Pro has been successfully installed!\n\nPublisher: Prince Sanchela\nLocation: " + targetDir,
                    "Setup Complete — Prince Sanchela",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Information
                );

                if (chkLaunchApp.Checked && File.Exists(exePath))
                {
                    Process.Start(new ProcessStartInfo
                    {
                        FileName = exePath,
                        WorkingDirectory = targetDir
                    });
                }

                this.Close();
            }
            catch (Exception ex)
            {
                prgProgress.Value = 0;
                lblStatus.Text = "Error during setup: " + ex.Message;
                lblStatus.ForeColor = Color.FromArgb(248, 113, 113); // Red
                MessageBox.Show("Installation failed:\n" + ex.Message, "Setup Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                btnInstall.Enabled = true;
                btnCancel.Enabled = true;
            }
        }

        private static string GetSafeDesktopDirectory()
        {
            // 1. Try DesktopDirectory
            try
            {
                string d = Environment.GetFolderPath(Environment.SpecialFolder.DesktopDirectory);
                if (Directory.Exists(d)) return d;
            }
            catch { }

            // 2. Try Registry User Shell Folders
            try
            {
                using (RegistryKey key = Registry.CurrentUser.OpenSubKey(@"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders"))
                {
                    if (key != null)
                    {
                        object val = key.GetValue("Desktop");
                        if (val != null)
                        {
                            string exp = Environment.ExpandEnvironmentVariables(val.ToString());
                            if (Directory.Exists(exp)) return exp;
                        }
                    }
                }
            }
            catch { }

            // 3. Try OneDrive Desktop
            string oneDrive = Environment.GetEnvironmentVariable("OneDrive");
            if (!string.IsNullOrEmpty(oneDrive))
            {
                string odd = Path.Combine(oneDrive, "Desktop");
                if (Directory.Exists(odd)) return odd;
            }

            // 4. Default fallback
            string userProfile = Environment.GetEnvironmentVariable("USERPROFILE");
            string std = Path.Combine(userProfile ?? @"C:\", "Desktop");
            Directory.CreateDirectory(std);
            return std;
        }

        private static void CreateWindowsShortcut(string shortcutPath, string targetPath, string workingDir, string description, string iconPath)
        {
            try
            {
                Type shellType = Type.GetTypeFromProgID("WScript.Shell");
                if (shellType == null) return;
                dynamic shell = Activator.CreateInstance(shellType);
                dynamic shortcut = shell.CreateShortcut(shortcutPath);
                shortcut.TargetPath = targetPath;
                shortcut.WorkingDirectory = workingDir;
                shortcut.Description = description;
                if (!string.IsNullOrEmpty(iconPath) && File.Exists(iconPath))
                {
                    shortcut.IconLocation = iconPath + ",0";
                }
                shortcut.Save();
            }
            catch { }
        }

        private static void CopyDirectory(string sourceDir, string destinationDir)
        {
            Directory.CreateDirectory(destinationDir);
            foreach (string file in Directory.GetFiles(sourceDir))
            {
                if (file.EndsWith(".pyc")) continue;
                string targetFilePath = Path.Combine(destinationDir, Path.GetFileName(file));
                File.Copy(file, targetFilePath, true);
            }
            foreach (string subDir in Directory.GetDirectories(sourceDir))
            {
                if (subDir.Contains("__pycache__")) continue;
                string targetSubDirPath = Path.Combine(destinationDir, Path.GetFileName(subDir));
                CopyDirectory(subDir, targetSubDirPath);
            }
        }
    }
}
