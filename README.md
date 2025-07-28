# 🎞️ Video Splitter & Renamer (FFmpeg + Python)

A powerful Python utility to **automatically split videos into 2-minute segments**, remove clips shorter than 50 seconds, and **rename files safely and sequentially** to avoid conflicts — all powered by FFmpeg.

## 📌 Features

- 🔪 **Split videos into 2-minute segments** using FFmpeg
- 🧹 **Auto-remove clips shorter than 50 seconds**
- ♻️ **Deletes original videos after processing**
- 🧠 **Smart renaming logic** to handle name conflicts
- 📂 Saves all processed clips to a dedicated `output_videos` folder
- ⚡ Supports common video formats like `.mp4`, `.avi`, `.mov`, `.mkv`, `.flv`, `.webm`, `.wmv`

## 📸 Example Workflow

1. Drop your video files (`.mp4`, `.avi`, etc.) in the same directory as the script.
2. Run the Python script.
3. Get clean, renamed, 2-minute video chunks in the `output_videos/` folder.

---

## 📁 Folder Structure

```

project/
├── main.py
├── output\_videos/
│   ├── sample\_part000.mp4
│   ├── sample\_part001.mp4
│   └── ...

````

---

## ⚙️ Requirements

- Python 3.x
- [FFmpeg](https://ffmpeg.org/) (including `ffmpeg` and `ffprobe`) installed and added to your system's `PATH`

### 🔧 Install FFmpeg

- **Windows:** Download from [FFmpeg.org](https://ffmpeg.org/download.html), extract, and add to system PATH
- **Linux/macOS:**  
  ```bash
  sudo apt install ffmpeg   # or brew install ffmpeg
````

---

## 🚀 How to Run

```bash
python main.py
```

The script will:

* Split all video files in the current directory
* Remove clips shorter than 50 seconds
* Delete original input files
* Rename all output files uniquely in the `output_videos/` folder

---

## 🔍 Customization

You can customize:

* Segment duration (currently 120 seconds)
* Minimum allowed clip duration (currently 50 seconds)
* File formats to support

Modify these in `main.py` as needed.

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---

## 🤝 Contributing

Contributions are welcome! If you find a bug or want to suggest a new feature, feel free to open an issue or submit a pull request.

---

## 🙌 Credits

Built with ❤️ using Python and FFmpeg.
