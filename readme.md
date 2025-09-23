# TerjeExp

Tool for reading, editing and exporting `.dat` files used by [**TerjePartyMod**](https://github.com/TerjeBruoygard/TerjePartyMod) in DayZ. Allows testing and modifying party GUIDs.

---

## `.dat` File Structure

The `.dat` file used by the mod contains:

- Header (4 bytes): Total number of GUIDs (32-bit integer, little-endian).
- GUID Header (4 bytes): Length of the GUID string.
- GUID: GUID is a Steam ID that has been digested with a SHA-256 hash and then encoded with a base64 URL-safe code.

---

## Features

- Load and parse `.dat` files
- Allows you to manually add new GUIDs (Steam ID)
- Import GUIDs from another `.dat`
- Export data to `.json`

---

## Exploit

The .dat file used by TerjePartyMod is stored locally on your computer and controls who you see as a member of your party. This means that parties are non-reciprocal by default: when you add another player's GUID to your .dat file, you can see their party dot in-game, but they still can't see yours unless they also add your GUID to theirs. Therefore, for two players to see each other, they must both have each other's GUIDs in their .dat files. This logic makes the system one-way, requiring manual synchronization between files to create a complete party where everyone sees each other.
