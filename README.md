# 🌊 Subnautica Nitrox Savegame Cleaner

A powerful Python tool for cleaning and optimizing [Subnautica Nitrox](https://github.com/SubnauticaNitrox/Nitrox) multiplayer savegames.

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)

## 🚀 Features

### 🔍 **Specific Search**

- Remove specific creatures (Mesmer, Rockgrub, etc.)
- Custom search terms
- Flexible text recognition in all entity data

### 🐟 **Performance Cleanup**

- Remove **77,970+ 'None' Entities** for instant performance improvement
- Remove all fish (30,000+ entities)
- Clean up plants and resources
- Optimize large quantity objects

### 📍 **Position-based Filters**

- Remove entities below certain depths
- Delete distant objects
- Spawn area optimized cleanup

### 📊 **Analysis Tools**

- Detailed savegame statistics
- Top 20 most common entity types
- File size before/after comparison
- Performance metrics

## 📦 Installation

### Prerequisites

- Python 3.7 or higher
- Subnautica with [Nitrox Mod](https://github.com/SubnauticaNitrox/Nitrox)

### Setup

```bash
# Clone repository
git clone https://github.com/yourusername/nitrox-savegame-cleaner.git
cd nitrox-savegame-cleaner

# Run script
python script.py
```

## 🎮 Usage

1. **Locate savegame**: Find your `EntityData.json` file in the Nitrox server folder
2. **Copy file**: Copy the `EntityData.json` to the script folder
3. **Run script**: `python script.py`
4. **Choose option**: Select from 15 different cleanup options
5. **Use backup**: The cleaned savegame is saved as `EntityData_cleaned.json`

### 📂 Nitrox Savegame Paths

```
Windows: %APPDATA%/Nitrox/Server/
macOS: ~/Library/Application Support/Nitrox/Server/
Linux: ~/.config/Nitrox/Server/
```

## 🛠️ Available Options

| Category           | Option           | Description                    |
| ------------------ | ---------------- | ------------------------------ |
| 🔍 **Specific**    | Remove Mesmer    | Removes all Mesmer creatures   |
|                    | Remove Rockgrub  | Removes all Rockgrub creatures |
|                    | Custom search    | Enter your own search terms    |
| 🐟 **Performance** | All fish         | Removes all fish entities      |
|                    | 'None' types     | Removes all empty entities     |
|                    | Plants/Resources | Cleans up flora objects        |
| 📍 **Position**    | Depth filter     | Entities below certain depth   |
|                    | Distance filter  | Far away objects               |
|                    | Spawn area       | Optimized for spawn proximity  |
| 📊 **Analysis**    | Statistics       | Detailed savegame analysis     |
|                    | Top TechTypes    | Most common entity types       |

## 📈 Performance Improvements

### Typical Results:

- **Before**: 300,000+ entities, 50+ MB file size
- **After**: 150,000 entities, 25 MB file size
- **Improvement**: 50% fewer entities, 50% smaller file

## ⚠️ Important Notes

### 🔒 **Safety**

- **ALWAYS** create a backup of your savegame
- The script automatically creates a new file (`EntityData_cleaned.json`)
- The original file remains unchanged

### 🎮 **Multiplayer Compatibility**

- All players should use the same cleaned savegame
- Restart server after cleanup
- Clients must reconnect

### 📁 **Supported Files**

- `EntityData.json` (Nitrox entity data)
- Automatic compression for optimal performance
- JSON integrity is ensured

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- [Subnautica Nitrox Team](https://github.com/SubnauticaNitrox/Nitrox) for the fantastic multiplayer mod

---

⭐ **Like the project? Give it a star!** ⭐
