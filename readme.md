# TerjeExp

Tool for reading, editing and exporting `.dat` files used by [**TerjePartyMod**](https://github.com/TerjeBruoygard/TerjePartyMod) in DayZ. Allows testing and modifying party UIDs.

---

## `.dat` File Structure

The `.dat` file used by the mod contains:

- Header (4 bytes): Total number of UIDs (32-bit integer, little-endian).
- UID: Each starts with an integer (4 bytes) below the length of the string.
- Then the bytes of the UTF-8 string.

---

## Features

- Load and parse `.dat` files
- Allows you to manually add new UIDs
- Import UIDs from another `.dat`
- Export data to `.json`

---

## Exploit

The .dat file used by TerjePartyMod is stored locally on your computer and controls who you see as a member of your party. This means that parties are non-reciprocal by default: when you add another player's UID to your .dat, you can see them in-game, but they can't see you unless they also add your UID to their own file. Therefore, in order for two players to see each other, they must both have each other's UIDs in their .dat files. This logic makes the system one-way, requiring manual synchronization between files to create a full party where everyone sees each other.
