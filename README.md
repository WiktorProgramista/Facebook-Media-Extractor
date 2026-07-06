```markdown
# 📸 Facebook Messages Media Extractor 💬

This Python script extracts media files (photos 📷, videos 🎥, GIFs 🎞️) from Facebook message JSON exports and organizes them with proper metadata! 🚀

## ✨ Features

- 🔍 **Automatic Detection** - Finds Facebook directories (`facebook-*`) or processes from current directory
- 📁 **Media Extraction** - Extracts photos, videos, and GIFs from messages
- ⏰ **Metadata Restoration** - Updates file creation/modified/accessed dates based on Facebook timestamps
- 🗂️ **Smart Organization** - Output files organized in folders:
  - `output/photos` 📸 - for images
  - `output/videos` 🎥 - for videos  
  - `output/gifs` 🎞️ - for animated GIFs
- 📦 **Automatic Cleanup** - Moves processed conversations to `done` ✅ and errored ones to `error` ❌
- 👤 **Flexible Naming** - Choose between conversation title or sender name for file naming

## 📋 Requirements

- Python 3.x 🐍
- Required library: `filedate`

Install dependencies:
```bash
pip install filedate
```

## 📁 Folder Structure

```
.
├── facebook-XXXXXXXXX/          # Facebook export directory (optional)
├── output/                      # ✨ Extracted media
│   ├── photos/ 📸
│   ├── videos/ 🎥
│   └── gifs/ 🎞️
├── done/ ✅                     # Processed conversations
├── error/ ❌                   # Conversations with errors
└── main.py 🐍                  # Main script
```

## 🚀 How to Use

1. Place `main.py` in the root directory with your Facebook data
2. Run the script with your preferred option:

### Default mode (uses conversation title for file naming):
```bash
python main.py
```

### Sender name mode (uses sender_name for file naming):
```bash
python main.py -s
```

### Help:
```bash
python main.py -h
```

3. Sit back and watch the magic happen! ✨

## 🎯 Command Line Options

| Option | Description |
|--------|-------------|
| `-s` | Use sender_name from each message for file naming instead of conversation title |
| `-h` | Show help message with all available options |

## 📝 Output File Naming

Files are named using one of these patterns:

### Default mode (without `-s`):
`[conversation_title]_[timestamp]_[uuid].[extension]`

Example: `JohnDoe_20231015143045_550e8400-e29b-41d4-a716-446655440000.jpg`

### Sender name mode (with `-s`):
`[sender_name]_[timestamp]_[uuid].[extension]`

Example: `AliceSmith_20231015143045_550e8400-e29b-41d4-a716-446655440000.jpg`

## 🔍 Supported Data Structures

- Standard Facebook export (`facebook-*/your_facebook_activity/messages/`) 📦
- Message JSON files in current directory or subdirectories 🔎
- Multiple media file locations (automatic search) 🕵️‍♂️
- Messages with `sender_name` field (required for `-s` mode) 👤

## 💡 Important Notes

- 📋 Script creates file copies, doesn't delete originals
- 🚫 Invalid characters in conversation titles and sender names are automatically removed
- 📊 Error details are logged to console for troubleshooting
- ⚡ For GIFs without timestamps, message timestamp is used as fallback
- 🎯 Handles multiple conversation formats and media locations
- 👤 In `-s` mode, if `sender_name` is missing, the script uses `"unknown"` as fallback
- 🔄 In default mode, the script uses conversation title (`title` field) from the JSON

## 📊 Example

### Input JSON:
```json
{
  "title": "Family Group Chat",
  "messages": [
    {
      "sender_name": "Alice Smith",
      "timestamp_ms": 1697459445000,
      "photos": [
        {"uri": "./media/photo123.jpg", "creation_timestamp": 1697459445}
      ]
    }
  ]
}
```

### Default mode output:
```
output/photos/Family Group Chat_20231016033045_550e8400-e29b-41d4-a716-446655440000.jpg
```

### Sender name mode (`-s`) output:
```
output/photos/Alice Smith_20231016033045_550e8400-e29b-41d4-a716-446655440000.jpg
```

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: No module named 'filedate'` | Install: `pip install filedate` |
| Media files not found | Check that `uri` paths in JSON match actual file locations |
| Metadata changes fail on macOS/Linux | Try running with `sudo` (rarely needed) |
| `sender_name` not found in `-s` mode | Script will use `"unknown"` as fallback |

## 🎉 Get Started!

Ready to organize your Facebook memories? Run the script and watch your media get beautifully organized! 🎊

## 📄 License

This script is provided without any warranty. You are free to modify and use it as you wish.
```

## Główne zmiany w README:

1. **Dodano informację o nowej funkcjonalności** – "Flexible Naming" w sekcji Features
2. **Zaktualizowano sekcję "How to Use"** – dodano informację o parametrze `-s` i jego użyciu
3. **Dodano sekcję "Command Line Options"** – opis dostępnych opcji
4. **Zaktualizowano sekcję "Output File Naming"** – pokazano oba tryby nazewnictwa
5. **Dodano informację o `sender_name`** – w sekcji "Supported Data Structures"
6. **Dodano nowe uwagi** – dotyczące trybu `-s` i fallbacka
7. **Dodano przykłady** – pokazujące różnicę między trybami
8. **Rozszerzono sekcję "Troubleshooting"** – o problemy związane z `-s`
9. **Dodano sekcję "License"** – dla kompletności

Plik README jest teraz w pełni zgodny z nową funkcjonalnością skryptu.
