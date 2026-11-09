using System;
using System.IO;
using System.Drawing;
using System.Diagnostics;
using System.Windows.Forms;
using Microsoft.Win32;
using System.Runtime.InteropServices;

[assembly: System.Reflection.AssemblyTitle("Setup - LangVoi Voice Studio Pro")]
[assembly: System.Reflection.AssemblyDescription("LangVoi Voice Studio Pro Setup Wizard")]
[assembly: System.Reflection.AssemblyCompany("Prince Sanchela")]
[assembly: System.Reflection.AssemblyProduct("LangVoi Voice Studio Pro")]
[assembly: System.Reflection.AssemblyCopyright("Copyright (C) 2026 Prince Sanchela. All Rights Reserved.")]
[assembly: System.Reflection.AssemblyVersion("2.2.0.0")]
[assembly: System.Reflection.AssemblyFileVersion("2.2.0.0")]

namespace LangVoi.Installer
{
    public class SetupWizardForm : Form
    {
        private int currentStep = 0;
        private const int TOTAL_STEPS = 7;

        // Top Header Controls
        private Panel pnlHeader;
        private Label lblHeaderTitle;
        private Label lblHeaderSub;
        private PictureBox picHeaderIcon;

        // Step Panels
        private Panel[] stepPanels;

        // Step 1: License Controls
        private RadioButton radAccept;
        private RadioButton radReject;
        private RichTextBox rtbLicense;

        // Step 2: Destination Controls
        private TextBox txtInstallDir;

        // Step 3: Tasks Controls
        private CheckBox chkDesktopShortcut;
        private CheckBox chkStartMenuShortcut;

        // Step 4: Ready Summary Controls
        private TextBox txtSummary;

        // Step 5: Progress Controls
        private ProgressBar prgProgress;
        private Label lblStatus;

        // Step 6: Finish Controls
        private CheckBox chkLaunchApp;

        // Bottom Navigation Buttons
        private Button btnBack;
        private Button btnNext;
        private Button btnCancel;

        private string sourceDir;

        [STAThread]
        public static void Main()
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            Application.Run(new SetupWizardForm());
        }

        public SetupWizardForm()
        {
            this.sourceDir = AppDomain.CurrentDomain.BaseDirectory;

            // Form Properties - Classic Inno Setup Dimensions
            this.Text = "Setup - LangVoi Voice Studio Pro";
            this.Size = new Size(520, 395);
            this.MinimumSize = new Size(520, 395);
            this.MaximumSize = new Size(520, 395);
            this.StartPosition = FormStartPosition.CenterScreen;
            this.FormBorderStyle = FormBorderStyle.FixedDialog;
            this.MaximizeBox = false;
            this.BackColor = SystemColors.Control;
            this.Font = new Font("Segoe UI", 9f, FontStyle.Regular);

            // Set Form Icon
            string icoPath = Path.Combine(sourceDir, "assets", "app_icon.ico");
            if (File.Exists(icoPath))
            {
                try { this.Icon = new Icon(icoPath); } catch { }
            }

            BuildUI();
            ShowStep(0);
        }

        private void BuildUI()
        {
            // -------------------------------------------------------------
            // 1. TOP HEADER (Classic Inno White Header)
            // -------------------------------------------------------------
            pnlHeader = new Panel
            {
                Dock = DockStyle.Top,
                Height = 60,
                BackColor = Color.White
            };

            lblHeaderTitle = new Label
            {
                Location = new Point(18, 9),
                Size = new Size(420, 18),
                Font = new Font("Segoe UI", 9.25f, FontStyle.Bold),
                ForeColor = Color.Black,
                Text = "License Agreement"
            };

            lblHeaderSub = new Label
            {
                Location = new Point(32, 28),
                Size = new Size(410, 28),
                Font = new Font("Segoe UI", 8.25f, FontStyle.Regular),
                ForeColor = Color.FromArgb(70, 70, 70),
                Text = "Please read the following important information before continuing."
            };

            picHeaderIcon = new PictureBox
            {
                Location = new Point(455, 6),
                Size = new Size(46, 46),
                SizeMode = PictureBoxSizeMode.Zoom
            };
            string pngIcon = Path.Combine(sourceDir, "assets", "app_icon_256.png");
            if (File.Exists(pngIcon))
            {
                try { picHeaderIcon.Image = Image.FromFile(pngIcon); } catch { }
            }

            Panel pnlHeaderLine = new Panel
            {
                Dock = DockStyle.Bottom,
                Height = 1,
                BackColor = SystemColors.ControlDark
            };

            pnlHeader.Controls.Add(lblHeaderTitle);
            pnlHeader.Controls.Add(lblHeaderSub);
            pnlHeader.Controls.Add(picHeaderIcon);
            pnlHeader.Controls.Add(pnlHeaderLine);
            this.Controls.Add(pnlHeader);

            // -------------------------------------------------------------
            // 2. BOTTOM NAVIGATION BAR
            // -------------------------------------------------------------
            Panel pnlBottom = new Panel
            {
                Dock = DockStyle.Bottom,
                Height = 48,
                BackColor = SystemColors.Control
            };

            Panel pnlBottomLine = new Panel
            {
                Dock = DockStyle.Top,
                Height = 1,
                BackColor = SystemColors.ControlDark
            };
            pnlBottom.Controls.Add(pnlBottomLine);

            btnBack = new Button
            {
                Text = "< Back",
                Size = new Size(75, 24),
                Location = new Point(260, 12),
                UseVisualStyleBackColor = true
            };
            btnBack.Click += (s, e) => { if (currentStep > 0) ShowStep(currentStep - 1); };

            btnNext = new Button
            {
                Text = "Next >",
                Size = new Size(75, 24),
                Location = new Point(340, 12),
                UseVisualStyleBackColor = true
            };
            btnNext.Click += OnNextClicked;

            btnCancel = new Button
            {
                Text = "Cancel",
                Size = new Size(75, 24),
                Location = new Point(425, 12),
                UseVisualStyleBackColor = true
            };
            btnCancel.Click += (s, e) => {
                if (currentStep == 5) return;
                if (currentStep == 6 || MessageBox.Show("Setup is not complete. Are you sure you want to exit?", "Exit Setup", MessageBoxButtons.YesNo, MessageBoxIcon.Question) == DialogResult.Yes)
                {
                    this.Close();
                }
            };

            pnlBottom.Controls.Add(btnBack);
            pnlBottom.Controls.Add(btnNext);
            pnlBottom.Controls.Add(btnCancel);
            this.Controls.Add(pnlBottom);

            // -------------------------------------------------------------
            // 3. STEP PANELS CONTAINER
            // -------------------------------------------------------------
            stepPanels = new Panel[TOTAL_STEPS];
            for (int i = 0; i < TOTAL_STEPS; i++)
            {
                stepPanels[i] = new Panel
                {
                    Location = new Point(0, 60),
                    Size = new Size(504, 247),
                    Visible = false
                };
                this.Controls.Add(stepPanels[i]);
            }

            BuildStep0_Welcome();
            BuildStep1_License();
            BuildStep2_Destination();
            BuildStep3_Tasks();
            BuildStep4_Ready();
            BuildStep5_Installing();
            BuildStep6_Finish();
        }

        // STEP 0: WELCOME
        private void BuildStep0_Welcome()
        {
            Panel p = stepPanels[0];

            Label lblTitle = new Label
            {
                Location = new Point(20, 18),
                Size = new Size(465, 48),
                Font = new Font("Segoe UI", 12f, FontStyle.Bold),
                Text = "Welcome to the LangVoi Voice Studio Pro\nSetup Wizard"
            };

            Label lblBody = new Label
            {
                Location = new Point(22, 75),
                Size = new Size(465, 150),
                Font = new Font("Segoe UI", 9f),
                Text = "This will install LangVoi Voice Studio Pro v2.2.0 on your computer.\n\n" +
                       "LangVoi Voice Studio Pro is a high-performance audio workstation\n" +
                       "featuring real-time 64-band spectrum visualization, high-precision dual\n" +
                       "VU meters, and an offline neural spoken-language identification engine.\n\n" +
                       "Architect & Creator: Prince Sanchela\n\n" +
                       "Click Next to continue, or Cancel to exit Setup."
            };

            p.Controls.Add(lblTitle);
            p.Controls.Add(lblBody);
        }

        // STEP 1: LICENSE AGREEMENT
        private void BuildStep1_License()
        {
            Panel p = stepPanels[1];

            Label lblPrompt = new Label
            {
                Location = new Point(15, 6),
                Size = new Size(475, 26),
                Font = new Font("Segoe UI", 8.5f),
                Text = "Please read the following License Agreement. You must accept the terms of this agreement before continuing with the installation."
            };

            rtbLicense = new RichTextBox
            {
                Location = new Point(15, 34),
                Size = new Size(474, 140),
                ReadOnly = true,
                BackColor = Color.White,
                Font = new Font("Consolas", 8f),
                ScrollBars = RichTextBoxScrollBars.Vertical,
                BorderStyle = BorderStyle.FixedSingle
            };

            string licPath = Path.Combine(sourceDir, "LICENSE.txt");
            if (File.Exists(licPath))
            {
                try { rtbLicense.Text = File.ReadAllText(licPath); }
                catch { rtbLicense.Text = GetDefaultLicense(); }
            }
            else
            {
                rtbLicense.Text = GetDefaultLicense();
            }

            radAccept = new RadioButton
            {
                Location = new Point(20, 182),
                Size = new Size(350, 20),
                Text = "I accept the agreement",
                Font = new Font("Segoe UI", 9f)
            };
            radAccept.CheckedChanged += (s, e) => { btnNext.Enabled = radAccept.Checked; };

            radReject = new RadioButton
            {
                Location = new Point(20, 204),
                Size = new Size(350, 20),
                Text = "I do not accept the agreement",
                Checked = true,
                Font = new Font("Segoe UI", 9f)
            };
            radReject.CheckedChanged += (s, e) => { btnNext.Enabled = radAccept.Checked; };

            p.Controls.Add(lblPrompt);
            p.Controls.Add(rtbLicense);
            p.Controls.Add(radAccept);
            p.Controls.Add(radReject);
        }

        // STEP 2: SELECT DESTINATION
        private void BuildStep2_Destination()
        {
            Panel p = stepPanels[2];

            Label lblPrompt = new Label
            {
                Location = new Point(15, 12),
                Size = new Size(475, 32),
                Font = new Font("Segoe UI", 8.5f),
                Text = "Setup will install LangVoi Voice Studio Pro into the following folder.\n" +
                       "To continue, click Next. If you would like to select a different folder, click Browse."
            };

            string defaultDir = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData), "Programs", "LangVoi Voice Studio Pro");

            txtInstallDir = new TextBox
            {
                Location = new Point(18, 55),
                Size = new Size(385, 23),
                Text = defaultDir
            };

            Button btnBrowse = new Button
            {
                Location = new Point(410, 54),
                Size = new Size(78, 25),
                Text = "Browse...",
                UseVisualStyleBackColor = true
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

            Label lblSpace = new Label
            {
                Location = new Point(18, 105),
                Size = new Size(400, 20),
                ForeColor = SystemColors.ControlDarkDark,
                Text = "At least 25.0 MB of free disk space is required."
            };

            p.Controls.Add(lblPrompt);
            p.Controls.Add(txtInstallDir);
            p.Controls.Add(btnBrowse);
            p.Controls.Add(lblSpace);
        }

        // STEP 3: ADDITIONAL TASKS
        private void BuildStep3_Tasks()
        {
            Panel p = stepPanels[3];

            Label lblPrompt = new Label
            {
                Location = new Point(15, 12),
                Size = new Size(475, 32),
                Font = new Font("Segoe UI", 8.5f),
                Text = "Select the additional tasks you would like Setup to perform while installing\n" +
                       "LangVoi Voice Studio Pro, then click Next."
            };

            Label lblGroup = new Label
            {
                Location = new Point(15, 55),
                Size = new Size(200, 18),
                Font = new Font("Segoe UI", 8.5f, FontStyle.Bold),
                Text = "Additional shortcuts:"
            };

            chkDesktopShortcut = new CheckBox
            {
                Location = new Point(25, 80),
                Size = new Size(350, 22),
                Text = "Create a &desktop shortcut",
                Checked = true
            };

            chkStartMenuShortcut = new CheckBox
            {
                Location = new Point(25, 106),
                Size = new Size(350, 22),
                Text = "Create a &Start Menu shortcut",
                Checked = true
            };

            p.Controls.Add(lblPrompt);
            p.Controls.Add(lblGroup);
            p.Controls.Add(chkDesktopShortcut);
            p.Controls.Add(chkStartMenuShortcut);
        }

        // STEP 4: READY TO INSTALL
        private void BuildStep4_Ready()
        {
            Panel p = stepPanels[4];

            Label lblPrompt = new Label
            {
                Location = new Point(15, 10),
                Size = new Size(475, 28),
                Font = new Font("Segoe UI", 8.5f),
                Text = "Click Install to continue with the installation, or click Back if you want to review or change any settings."
            };

            txtSummary = new TextBox
            {
                Location = new Point(15, 42),
                Size = new Size(474, 185),
                Multiline = true,
                ReadOnly = true,
                BackColor = Color.White,
                ScrollBars = ScrollBars.Vertical,
                Font = new Font("Segoe UI", 8.5f)
            };

            p.Controls.Add(lblPrompt);
            p.Controls.Add(txtSummary);
        }

        // STEP 5: INSTALLING PROGRESS
        private void BuildStep5_Installing()
        {
            Panel p = stepPanels[5];

            Label lblPrompt = new Label
            {
                Location = new Point(15, 20),
                Size = new Size(475, 20),
                Font = new Font("Segoe UI", 8.5f),
                Text = "Please wait while Setup installs LangVoi Voice Studio Pro on your computer."
            };

            lblStatus = new Label
            {
                Location = new Point(15, 55),
                Size = new Size(475, 18),
                ForeColor = Color.Black,
                Font = new Font("Segoe UI", 8.25f),
                Text = "Extracting files..."
            };

            prgProgress = new ProgressBar
            {
                Location = new Point(15, 78),
                Size = new Size(474, 20),
                Minimum = 0,
                Maximum = 100,
                Value = 0
            };

            p.Controls.Add(lblPrompt);
            p.Controls.Add(lblStatus);
            p.Controls.Add(prgProgress);
        }

        // STEP 6: FINISH
        private void BuildStep6_Finish()
        {
            Panel p = stepPanels[6];

            Label lblTitle = new Label
            {
                Location = new Point(20, 18),
                Size = new Size(465, 48),
                Font = new Font("Segoe UI", 12f, FontStyle.Bold),
                Text = "Completing the LangVoi Voice Studio Pro\nSetup Wizard"
            };

            Label lblBody = new Label
            {
                Location = new Point(22, 75),
                Size = new Size(465, 80),
                Font = new Font("Segoe UI", 9f),
                Text = "Setup has finished installing LangVoi Voice Studio Pro on your computer.\n" +
                       "The application may be launched by selecting the installed shortcuts.\n\n" +
                       "Click Finish to exit Setup."
            };

            chkLaunchApp = new CheckBox
            {
                Location = new Point(25, 175),
                Size = new Size(400, 22),
                Text = "&Launch LangVoi Voice Studio Pro",
                Checked = true,
                Font = new Font("Segoe UI", 9f)
            };

            p.Controls.Add(lblTitle);
            p.Controls.Add(lblBody);
            p.Controls.Add(chkLaunchApp);
        }

        private void ShowStep(int step)
        {
            currentStep = step;

            for (int i = 0; i < TOTAL_STEPS; i++)
            {
                stepPanels[i].Visible = (i == step);
            }

            pnlHeader.Visible = (step != 0 && step != 6);

            switch (step)
            {
                case 0:
                    btnBack.Enabled = false;
                    btnNext.Text = "Next >";
                    btnNext.Enabled = true;
                    break;
                case 1:
                    lblHeaderTitle.Text = "License Agreement";
                    lblHeaderSub.Text = "Please read the following important information before continuing.";
                    btnBack.Enabled = true;
                    btnNext.Text = "Next >";
                    btnNext.Enabled = radAccept.Checked;
                    break;
                case 2:
                    lblHeaderTitle.Text = "Select Destination Location";
                    lblHeaderSub.Text = "Where should LangVoi Voice Studio Pro be installed?";
                    btnBack.Enabled = true;
                    btnNext.Text = "Next >";
                    btnNext.Enabled = true;
                    break;
                case 3:
                    lblHeaderTitle.Text = "Select Additional Tasks";
                    lblHeaderSub.Text = "Which additional tasks should be performed?";
                    btnBack.Enabled = true;
                    btnNext.Text = "Next >";
                    btnNext.Enabled = true;
                    break;
                case 4:
                    lblHeaderTitle.Text = "Ready to Install";
                    lblHeaderSub.Text = "Setup is now ready to begin installing LangVoi Voice Studio Pro on your computer.";
                    btnBack.Enabled = true;
                    btnNext.Text = "Install";
                    btnNext.Enabled = true;
                    txtSummary.Text = "Destination location:\r\n   " + txtInstallDir.Text + "\r\n\r\n" +
                                      "Additional tasks:\r\n" +
                                      (chkDesktopShortcut.Checked ? "   Create a desktop shortcut\r\n" : "") +
                                      (chkStartMenuShortcut.Checked ? "   Create a Start Menu shortcut\r\n" : "");
                    break;
                case 5:
                    lblHeaderTitle.Text = "Installing";
                    lblHeaderSub.Text = "Please wait while Setup installs LangVoi Voice Studio Pro on your computer.";
                    btnBack.Enabled = false;
                    btnNext.Enabled = false;
                    btnCancel.Enabled = false;
                    DoInstall();
                    break;
                case 6:
                    btnBack.Visible = false;
                    btnCancel.Visible = false;
                    btnNext.Text = "Finish";
                    btnNext.Enabled = true;
                    break;
            }
        }

        private void OnNextClicked(object sender, EventArgs e)
        {
            if (currentStep == 4)
            {
                ShowStep(5);
            }
            else if (currentStep == 6)
            {
                if (chkLaunchApp.Checked)
                {
                    string exePath = Path.Combine(txtInstallDir.Text, "LangVoi_Studio.exe");
                    if (File.Exists(exePath))
                    {
                        try { Process.Start(exePath); } catch { }
                    }
                }
                this.Close();
            }
            else
            {
                ShowStep(currentStep + 1);
            }
        }

        private void DoInstall()
        {
            Timer t = new Timer();
            t.Interval = 35;
            int step = 0;

            t.Tick += (s, e) =>
            {
                step += 3;
                if (step <= 100) prgProgress.Value = step;

                if (step == 15)
                {
                    lblStatus.Text = "Creating installation directory...";
                    try { Directory.CreateDirectory(txtInstallDir.Text); } catch { }
                }
                else if (step == 45)
                {
                    lblStatus.Text = "Extracting and installing application files...";
                    CopyPayloadFiles();
                }
                else if (step == 75)
                {
                    lblStatus.Text = "Copying neural models and acoustic biometrics...";
                    CopyPayloadDirs();
                }
                else if (step == 90)
                {
                    lblStatus.Text = "Creating shortcuts and registering uninstaller...";
                    CreateShortcuts();
                    RegisterUninstaller();
                }
                else if (step >= 100)
                {
                    t.Stop();
                    t.Dispose();
                    ShowStep(6);
                }
            };

            t.Start();
        }

        private void CopyPayloadFiles()
        {
            string targetDir = txtInstallDir.Text;
            string[] files = new string[] {
                "LangVoi_Studio.exe", "LangVoi_Studio.bat", "run.py", "main.py",
                "requirements.txt", "README.md", "LICENSE.txt"
            };

            foreach (string f in files)
            {
                string src = Path.Combine(sourceDir, f);
                if (File.Exists(src))
                {
                    try { File.Copy(src, Path.Combine(targetDir, f), true); } catch { }
                }
            }
        }

        private void CopyPayloadDirs()
        {
            string targetDir = txtInstallDir.Text;
            string[] dirs = new string[] { "app", "core", "samples", "assets" };

            foreach (string d in dirs)
            {
                string sDir = Path.Combine(sourceDir, d);
                string tDir = Path.Combine(targetDir, d);
                if (Directory.Exists(sDir))
                {
                    try { CopyDirectory(sDir, tDir); } catch { }
                }
            }
        }

        private static void CopyDirectory(string sourceDir, string destinationDir)
        {
            Directory.CreateDirectory(destinationDir);
            foreach (string file in Directory.GetFiles(sourceDir))
            {
                if (file.EndsWith(".pyc")) continue;
                string targetFilePath = Path.Combine(destinationDir, Path.GetFileName(file));
                try { File.Copy(file, targetFilePath, true); } catch { }
            }
            foreach (string subDir in Directory.GetDirectories(sourceDir))
            {
                if (subDir.Contains("__pycache__")) continue;
                string targetSubDirPath = Path.Combine(destinationDir, Path.GetFileName(subDir));
                CopyDirectory(subDir, targetSubDirPath);
            }
        }

        private void CreateShortcuts()
        {
            string targetDir = txtInstallDir.Text;
            string targetExe = Path.Combine(targetDir, "LangVoi_Studio.exe");
            string icoPath = Path.Combine(targetDir, "assets", "app_icon.ico");

            try
            {
                Type shellType = Type.GetTypeFromProgID("WScript.Shell");
                if (shellType == null) return;
                object shell = Activator.CreateInstance(shellType);
                System.Reflection.MethodInfo createSc = shellType.GetMethod("CreateShortcut");

                if (chkDesktopShortcut.Checked)
                {
                    string desktop = Environment.GetFolderPath(Environment.SpecialFolder.DesktopDirectory);
                    string lnk = Path.Combine(desktop, "LangVoi Voice Studio Pro.lnk");
                    object sc = createSc.Invoke(shell, new object[] { lnk });
                    SetProperty(sc, "TargetPath", targetExe);
                    SetProperty(sc, "WorkingDirectory", targetDir);
                    SetProperty(sc, "Description", "LangVoi Voice Studio Pro - Prince Sanchela");
                    if (File.Exists(icoPath)) SetProperty(sc, "IconLocation", icoPath + ",0");
                    sc.GetType().InvokeMember("Save", System.Reflection.BindingFlags.InvokeMethod, null, sc, null);
                }

                if (chkStartMenuShortcut.Checked)
                {
                    string startMenu = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.StartMenu), "Programs", "LangVoi");
                    Directory.CreateDirectory(startMenu);
                    string lnk = Path.Combine(startMenu, "LangVoi Voice Studio Pro.lnk");
                    object sc = createSc.Invoke(shell, new object[] { lnk });
                    SetProperty(sc, "TargetPath", targetExe);
                    SetProperty(sc, "WorkingDirectory", targetDir);
                    SetProperty(sc, "Description", "LangVoi Voice Studio Pro");
                    if (File.Exists(icoPath)) SetProperty(sc, "IconLocation", icoPath + ",0");
                    sc.GetType().InvokeMember("Save", System.Reflection.BindingFlags.InvokeMethod, null, sc, null);
                }
            }
            catch { }
        }

        private static void SetProperty(object target, string name, object val)
        {
            try
            {
                target.GetType().InvokeMember(name, System.Reflection.BindingFlags.SetProperty, null, target, new object[] { val });
            }
            catch { }
        }

        private void RegisterUninstaller()
        {
            try
            {
                string targetDir = txtInstallDir.Text;
                string uninstBat = Path.Combine(targetDir, "Uninstall.bat");
                string uninstContent = "@echo off\r\n" +
                                       "title Uninstalling LangVoi Voice Studio Pro...\r\n" +
                                       "powershell -Command \"Remove-Item -Force -ErrorAction SilentlyContinue '$([Environment]::GetFolderPath([Environment+SpecialFolder]::DesktopDirectory))\\LangVoi Voice Studio Pro.lnk'; Remove-Item -Recurse -Force -ErrorAction SilentlyContinue '$([Environment]::GetFolderPath([Environment+SpecialFolder]::StartMenu))\\Programs\\LangVoi'; Remove-Item -Recurse -Force -ErrorAction SilentlyContinue '" + targetDir + "'; Remove-ItemProperty -Path 'HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\LangVoi' -ErrorAction SilentlyContinue\"\r\n" +
                                       "echo LangVoi has been uninstalled successfully.\r\n" +
                                       "pause\r\n";
                File.WriteAllText(uninstBat, uninstContent);

                using (RegistryKey key = Registry.CurrentUser.CreateSubKey(@"Software\Microsoft\Windows\CurrentVersion\Uninstall\LangVoi"))
                {
                    if (key != null)
                    {
                        key.SetValue("DisplayName", "LangVoi Voice Studio Pro");
                        key.SetValue("DisplayVersion", "2.2.0");
                        key.SetValue("Publisher", "Prince Sanchela");
                        key.SetValue("InstallLocation", targetDir);
                        key.SetValue("UninstallString", "\"" + uninstBat + "\"");
                        key.SetValue("DisplayIcon", Path.Combine(targetDir, "assets", "app_icon.ico"));
                    }
                }
            }
            catch { }
        }

        private string GetDefaultLicense()
        {
            return "LANGVOI VOICE STUDIO PRO - SOFTWARE LICENSE AGREEMENT\r\n" +
                   "Copyright (C) 2026 Prince Sanchela. All Rights Reserved.\r\n\r\n" +
                   "1. GRANT OF LICENSE\r\n" +
                   "Prince Sanchela grants you a personal, non-exclusive license to use LangVoi Voice Studio Pro on compatible Windows workstations.\r\n\r\n" +
                   "2. PROPRIETARY RIGHTS\r\n" +
                   "All algorithms, architecture, user interface, and neural models remain the intellectual property of Prince Sanchela.\r\n\r\n" +
                   "3. DISCLAIMER\r\n" +
                   "THE SOFTWARE IS PROVIDED 'AS IS' WITHOUT WARRANTY OF ANY KIND.\r\n\r\n" +
                   "Lead Architect: Prince Sanchela\r\n" +
                   "Contact: contact.princesanchela@gmail.com";
        }
    }
}
