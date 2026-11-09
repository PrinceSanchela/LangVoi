"""
Export & Reporting Dialog Module.
Generates Printable Laboratory Reports (PDF/HTML), JSON Datasets, and CSV Spreadsheets.
"""

import time
import json
import csv
from tkinter import filedialog, messagebox


def show_export_dialog(parent, current_filename: str, metrics: dict, lang_results: dict):
    if not metrics or not lang_results:
        messagebox.showinfo("Export", "No voice analysis data available to export. Please open or record audio first.")
        return

    primary = lang_results.get("primary", {})
    candidates = lang_results.get("candidates", [])

    path = filedialog.asksaveasfilename(
        title="Export Laboratory Acoustic & Linguistic Report",
        defaultextension=".html",
        filetypes=[("Printable HTML / PDF Report", "*.html"), ("JSON Telemetry Dataset", "*.json"), ("CSV Spreadsheet", "*.csv")]
    )
    if not path:
        return

    ext = path.lower().split(".")[-1]

    if ext == "json":
        data = {"source_file": current_filename, "voice_analysis": metrics, "language_detection": lang_results}
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        messagebox.showinfo("Export Success", f"JSON telemetry data saved:\n{path}")

    elif ext == "csv":
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Parameter", "Value"])
            writer.writerow(["Source File", current_filename])
            writer.writerow(["Detected Language", primary.get("name", "Unknown")])
            writer.writerow(["ISO Code", primary.get("code", "")])
            writer.writerow(["Confidence Match", f"{primary.get('probability_pct', 0)}%"])
            writer.writerow(["Language Family", primary.get("family", "")])
            writer.writerow(["Script", primary.get("script", "")])
            for k, v in metrics.items():
                if not isinstance(v, (list, dict)):
                    writer.writerow([k, v])
        messagebox.showinfo("Export Success", f"CSV spreadsheet saved:\n{path}")

    else:
        # Formal Printable HTML / PDF Laboratory Document
        rows_html = "".join([f"<tr><td>#{i+1}</td><td>{c['flag']} <strong>{c['name']}</strong></td><td>{c.get('native_name','-')}</td><td>{c.get('family','-')}</td><td><strong>{c.get('probability_pct',0)}%</strong></td></tr>" for i, c in enumerate(candidates)])

        html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>LangVoi Voice Studio Pro - Laboratory Report</title>
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; color: #1e293b; margin: 30px; font-size: 13px; line-height: 1.5; }}
  .hdr {{ border-bottom: 2px solid #0284c7; padding-bottom: 15px; margin-bottom: 20px; }}
  h1 {{ margin: 0; font-size: 24px; color: #0f172a; }}
  .box {{ background: #f0fdf4; border: 1px solid #86efac; border-radius: 8px; padding: 18px; margin: 20px 0; }}
  table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
  th, td {{ border-bottom: 1px solid #e2e8f0; padding: 8px; text-align: left; }}
  th {{ background: #f8fafc; font-size: 11px; text-transform: uppercase; color: #475569; }}
</style>
</head>
<body>
  <div class="hdr">
    <h1>LangVoi Voice Studio Pro - Acoustic Laboratory Report</h1>
    <p>Source Audio: <strong>{current_filename}</strong> | Generated: {time.ctime()} | Detection Engine: {lang_results.get('method','Acoustic Prosody')}</p>
  </div>
  <div class="box">
    <h2>Primary Detected Language: {primary.get('flag')} {primary.get('name')} ({primary.get('probability_pct')}% Confidence)</h2>
    <p>Native Script: {primary.get('native_name')} | Family: {primary.get('family')} | Region: {primary.get('region')}</p>
  </div>
  <h3>Top Candidate Languages Across the World:</h3>
  <table>
    <tr><th>Rank</th><th>Language</th><th>Native Script</th><th>Linguistic Family</th><th>Acoustic Probability</th></tr>
    {rows_html}
  </table>
  <h3>Acoustic Biometrics & Voice Telemetry:</h3>
  <table>
    <tr><td>Fundamental Pitch (F0)</td><td><strong>{metrics.get('avg_pitch_hz')} Hz ({metrics.get('musical_note')})</strong></td></tr>
    <tr><td>Vocal Register Classification</td><td>{metrics.get('vocal_register')}</td></tr>
    <tr><td>Signal-to-Noise Ratio (SNR)</td><td>{metrics.get('snr_db')} dB ({metrics.get('snr_quality')})</td></tr>
    <tr><td>Speaking Tempo</td><td>{metrics.get('tempo_wpm')} WPM ({metrics.get('tempo_category')})</td></tr>
    <tr><td>Voice Activity Ratio (VAD)</td><td>{metrics.get('speech_ratio_pct')}% active</td></tr>
    <tr><td>Dynamic Range</td><td>{metrics.get('dynamic_range_db')} dB</td></tr>
    <tr><td>Spectral Timbre (Centroid)</td><td>{metrics.get('spectral_centroid_hz')} Hz ({metrics.get('timbre_profile')})</td></tr>
  </table>
</body>
</html>"""
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        messagebox.showinfo("Export Success", f"Laboratory report saved:\n{path}\nYou can open this file in any web browser and print directly to PDF!")
