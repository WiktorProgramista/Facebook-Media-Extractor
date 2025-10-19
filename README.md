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
2. Run the script:
```bash
python main.py
```

3. Sit back and watch the magic happen! ✨

## 🔍 Supported Data Structures

- Standard Facebook export (`facebook-*/your_facebook_activity/messages/`) 📦
- Message JSON files in current directory or subdirectories 🔎
- Multiple media file locations (automatic search) 🕵️‍♂️

## 📝 Output File Naming

Files are named using this pattern:
`[conversation_title]_[timestamp]_[uuid].[extension]`

Example: `JohnDoe_20231015143045_550e8400-e29b-41d4-a716-446655440000.jpg`

## 💡 Important Notes

- 📋 Script creates file copies, doesn't delete originals
- 🚫 Invalid characters in conversation titles are automatically removed
- 📊 Error details are logged to console for troubleshooting
- ⚡ For GIFs without timestamps, message timestamp is used as fallback
- 🎯 Handles multiple conversation formats and media locations

## 🎉 Get Started!

Ready to organize your Facebook memories? Run the script and watch your media get beautifully organized! 🎊
```
