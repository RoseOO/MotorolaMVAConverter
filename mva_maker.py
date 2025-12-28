#!/usr/bin/env python3
import os
import shutil
import subprocess
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

APP_TITLE = "Motorola Voice File Converter (WAV → MVA / CPS-ready WAV)"

PROFILES = {
    # For APX CPS VA Converter Utility input
    "APX CPS-ready WAV (8 kHz, 16-bit PCM, mono)": {
        "ext": ".wav",
        "ffmpeg_args": ["-c:a", "pcm_s16le", "-ar", "8000", "-ac", "1"],
        "note": "Use this for APX: import/convert inside CPS via Tools → VA Converter Utility.",
    },
    # For MOTOTRBO CPS .mva format (commonly described as 8kHz 8-bit μ-law)
    "MOTOTRBO MVA (legacy CPS safe)": {
        "ext": ".mva",
        "ffmpeg_args": [
            "-ar", "8000",
            "-ac", "1",
            "-c:a", "pcm_mulaw",
            "-map_metadata", "-1",
            "-fflags", "+bitexact",
            "-flags:a", "+bitexact",
            "-f", "wav"
        ],
        "note": "Legacy MOTOTRBO CPS-safe μ-law MVA (no metadata, no filters)."
}

}

def which_ffmpeg() -> str | None:
    return shutil.which("ffmpeg")

def run_ffmpeg(in_path: str, out_path: str, extra: list[str]) -> tuple[bool, str]:
    ffmpeg = which_ffmpeg()
    if not ffmpeg:
        return False, "FFmpeg not found in PATH. Install FFmpeg and restart."

    cmd = [
        ffmpeg,
        "-y",                 # overwrite
        "-hide_banner",
        "-loglevel", "error",
        "-i", in_path,
        *extra,
        out_path
    ]

    try:
        p = subprocess.run(cmd, capture_output=True, text=True, check=False)
        if p.returncode != 0:
            err = p.stderr.strip() or "Unknown FFmpeg error."
            return False, err
        return True, "OK"
    except Exception as e:
        return False, str(e)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.minsize(720, 360)
        self.columnconfigure(1, weight=1)

        self.in_var = tk.StringVar()
        self.out_dir_var = tk.StringVar(value=os.getcwd())
        self.profile_var = tk.StringVar(value=list(PROFILES.keys())[0])
        self.base_name_var = tk.StringVar(value="voice_announcement")

        # --- UI ---
        pad = {"padx": 10, "pady": 6}

        ttk.Label(self, text="Input WAV (or any audio FFmpeg can read):").grid(row=0, column=0, sticky="w", **pad)
        in_entry = ttk.Entry(self, textvariable=self.in_var)
        in_entry.grid(row=0, column=1, sticky="ew", **pad)
        ttk.Button(self, text="Browse…", command=self.pick_input).grid(row=0, column=2, **pad)

        ttk.Label(self, text="Output folder:").grid(row=1, column=0, sticky="w", **pad)
        out_entry = ttk.Entry(self, textvariable=self.out_dir_var)
        out_entry.grid(row=1, column=1, sticky="ew", **pad)
        ttk.Button(self, text="Browse…", command=self.pick_out_dir).grid(row=1, column=2, **pad)

        ttk.Label(self, text="Output filename (no extension):").grid(row=2, column=0, sticky="w", **pad)
        name_entry = ttk.Entry(self, textvariable=self.base_name_var)
        name_entry.grid(row=2, column=1, sticky="ew", **pad)

        ttk.Label(self, text="Profile:").grid(row=3, column=0, sticky="w", **pad)
        profile = ttk.Combobox(self, textvariable=self.profile_var, values=list(PROFILES.keys()), state="readonly")
        profile.grid(row=3, column=1, sticky="ew", **pad)
        profile.bind("<<ComboboxSelected>>", lambda _e: self.update_note())

        self.note_lbl = ttk.Label(self, text="", wraplength=680, justify="left")
        self.note_lbl.grid(row=4, column=0, columnspan=3, sticky="w", **pad)

        ttk.Separator(self).grid(row=5, column=0, columnspan=3, sticky="ew", padx=10, pady=10)

        ttk.Button(self, text="Convert", command=self.convert).grid(row=6, column=0, **pad)
        ttk.Button(self, text="Open output folder", command=self.open_out_dir).grid(row=6, column=1, sticky="w", **pad)

        self.status = ttk.Label(self, text="Ready.")
        self.status.grid(row=7, column=0, columnspan=3, sticky="w", padx=10, pady=10)

        self.update_note()

    def pick_input(self):
        path = filedialog.askopenfilename(
            title="Select input audio",
            filetypes=[("Audio files", "*.wav *.mp3 *.m4a *.flac *.aiff *.ogg *.aac *.wma"), ("All files", "*.*")]
        )
        if path:
            self.in_var.set(path)
            # default output name from file
            base = os.path.splitext(os.path.basename(path))[0]
            self.base_name_var.set(base)

    def pick_out_dir(self):
        path = filedialog.askdirectory(title="Select output folder")
        if path:
            self.out_dir_var.set(path)

    def update_note(self):
        prof = PROFILES[self.profile_var.get()]
        self.note_lbl.config(text=f"Note: {prof['note']}")

    def convert(self):
        in_path = self.in_var.get().strip()
        out_dir = self.out_dir_var.get().strip()
        base = self.base_name_var.get().strip()

        if not in_path or not os.path.isfile(in_path):
            messagebox.showerror("Missing input", "Please choose a valid input file.")
            return

        if not out_dir or not os.path.isdir(out_dir):
            messagebox.showerror("Missing output folder", "Please choose a valid output folder.")
            return

        if not base:
            messagebox.showerror("Missing filename", "Please enter an output filename (no extension).")
            return

        prof = PROFILES[self.profile_var.get()]
        ext = prof["ext"]
        out_path = os.path.join(out_dir, base + ext)

        # Make audio level sensible for voice prompts:
        # - loudness normalization to a reasonable target (works well for spoken prompts)
        # You can remove this filter if you prefer.
        audio_filter = ["-af", "loudnorm=I=-16:TP=-4:LRA=11"]

        extra = [*audio_filter, *prof["ffmpeg_args"]]

        self.status.config(text="Converting…")
        self.update_idletasks()

        ok, msg = run_ffmpeg(in_path, out_path, extra)
        if ok:
            self.status.config(text=f"Done: {out_path}")
            messagebox.showinfo("Converted", f"Created:\n{out_path}")
        else:
            self.status.config(text="Failed.")
            messagebox.showerror("FFmpeg error", msg)

    def open_out_dir(self):
        out_dir = self.out_dir_var.get().strip()
        if not out_dir or not os.path.isdir(out_dir):
            return
        # Windows / macOS / Linux
        try:
            if os.name == "nt":
                os.startfile(out_dir)  # type: ignore[attr-defined]
            elif sys.platform == "darwin":
                subprocess.run(["open", out_dir], check=False)
            else:
                subprocess.run(["xdg-open", out_dir], check=False)
        except Exception:
            pass

if __name__ == "__main__":
    import sys
    app = App()
    app.mainloop()
