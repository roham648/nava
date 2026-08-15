# Nava

Nava is a lightweight Voice-to-Text application designed for simple and fast speech recognition.

## Features

* 🎙️ Voice-to-Text
* 🧠 Vosk speech recognition
* 🐍 Self-contained Python runtime
* 📦 Automatic dependency installation
* 🔄 Automatic application update checking
* 🌐 GitHub-based update system
* 💻 Windows support

## Project Structure

```text
Nava/
│
├── main.py
├── installer.py
├── ui.py
├── stt.py
│
├── version.json
├── files.json
│
├── models/
├── packages/
└── runtime/
```

## Launcher

`main.py` is the Nava launcher.

When Nava starts, it:

1. Checks whether Nava is installed.
2. Runs the installer if required.
3. Reads the local version.
4. Checks the GitHub repository for a newer version.
5. Checks for code updates.
6. Downloads updated files when available.
7. Replaces the old files.
8. Starts Nava.

## Version System

Nava uses three version numbers:

```json
{
    "version": "1.0.0",
    "code_version": "1.0.0",
    "model_version": "1.0.0"
}
```

### `version`

The public Nava version.

### `code_version`

The version of the application code.

For example, if `ui.py` or `stt.py` changes:

```text
1.0.0 → 1.0.1
```

### `model_version`

The version of the speech recognition model.

This is currently reserved for the future model updater.

## files.json

`files.json` tells Nava which files can be updated.

Example:

```json
{
    "files": [
        {
            "path": "ui.py",
            "type": "code"
        },
        {
            "path": "stt.py",
            "type": "code"
        }
    ]
}
```

When the code version changes, Nava downloads these files from GitHub and replaces the local versions.

## Updating Nava

To publish a code update:

### 1. Modify the source code

For example:

```text
ui.py
```

### 2. Test the application

Run:

```bash
python ui.py
```

or run the launcher:

```bash
python main.py
```

### 3. Update `version.json`

Example:

```json
{
    "version": "1.0.1",
    "code_version": "1.0.1",
    "model_version": "1.0.0"
}
```

### 4. Push the changes to GitHub

The repository must contain:

```text
version.json
files.json
ui.py
stt.py
```

After the files are pushed, existing Nava installations will detect the new code version when they start.

## Model Updates

Model updates are planned for a future version.

The intended system is:

```text
Nava
 ↓
Check model_version
 ↓
New model available?
 ↓
Ask user
 ↓
Download new model
 ↓
Replace old model
```

The model itself should not be stored directly inside the normal Git repository.

## Development

Nava is currently developed with Python.

Main technologies include:

* Python
* Tkinter
* Vosk
* PyInstaller
* GitHub

## Repository

Nava is developed and distributed through GitHub.

## License

This project is currently under development.
