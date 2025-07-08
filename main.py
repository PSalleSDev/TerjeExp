import json
import struct
from typing import BinaryIO, List, Dict, Any

int32: int = 4

class Uid:
    def __init__(self, value: str):
        self.value: str = value

    @staticmethod
    def deserialize(file: BinaryIO) -> 'Uid':
        """Deserialize a UID from binary file"""
        size_bytes = file.read(int32)
        if len(size_bytes) < int32:
            raise ValueError("Invalid UID format - missing size")
        
        size = struct.unpack('<i', size_bytes)[0]
        
        uid_bytes = file.read(size)
        if len(uid_bytes) < size:
            raise ValueError("Invalid UID format - data too short")
        
        return Uid(uid_bytes.decode('utf-8'))

class Dat:
    def __init__(self, path: str):
        self.path = path
        self.file: BinaryIO = None
        self.uid_count: int = 0
        self.uids: List[Uid] = []
        
        try:
            self.file = open(self.path, 'r+b')
        except Exception as e:
            raise RuntimeError(f"Failed to open file: {str(e)}")
        
        try:
            self.__deserialize()
        except Exception as e:
            raise RuntimeError(f"Failed to deserialize file: {str(e)}")
        
    def __enter__(self):
        return self

    def _read_header(self) -> bytes:
        """Read and return the header (count bytes)"""
        self.file.seek(0)
        return self.file.read(int32)

    def __deserialize(self):
        """Load all UIDs from file"""
        count_bytes = self._read_header()
        if len(count_bytes) < int32:
            raise ValueError("Invalid .dat file - missing UID count")
        
        self.uid_count = struct.unpack('<i', count_bytes)[0]
        self.uids = []
        
        for _ in range(self.uid_count):
            self.uids.append(Uid.deserialize(self.file))

    def dump(self) -> Dict[str, Any]:
        """Return data as dictionary"""
        return {
            "uid_count": self.uid_count,
            "uids": [uid.value for uid in self.uids]
        }

    def append(self, new_uid: str) -> bool:
        """Append a new UID to the file"""

        if new_uid in [uid.value for uid in self.uids]:
            return False

        self.file.seek(0)
        count_bytes = self.file.read(int32)
        count = struct.unpack('<i', count_bytes)[0]
        
        self.file.seek(0, 2)
        
        uid_bytes = new_uid.encode('utf-8')
        self.file.write(struct.pack('<i', len(uid_bytes)))
        self.file.write(uid_bytes)
        
        self.file.seek(0)
        self.file.write(struct.pack('<i', count + 1))
        
        self.__deserialize()

        return True

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close the file"""
        if self.file and not self.file.closed:
            self.file.close()

def header():
        print("\033[H\033[J")
        print(r"""
___________            __       ___________
\__    ___/__________ |__| ____ \_   _____/__  _________
  |    |_/ __ \_  __ \|  |/ __ \ |    __)_\  \/  /\____ \
  |    |\  ___/|  | \/|  \  ___/ |        \>    < |  |_> >
  |____| \___  >__/\__|  |\___  >_______  /__/\_ \|   __/
             \/   \______|    \/        \/      \/|__|
            """)

def main():
    header()
    path = input("TerjePartyMod .dat file path: ")
    output_path = "PartyData.json"
    
    try:
        with Dat(path) as dat:
            while True:
                header()

                print("\033[1;31mChanges to parties are made automatically, but the game must be restarted to load them. Don't forget to turn off TerjeExp after making changes. If it is open, this will prevent DayZ from opening your .dat, since it is being used in another process.\n\033[0m")

                print(f"You have in your .dat {dat.uid_count} parties\n")
                
                print("1: Dump party data to JSON")
                print("2: Add UID to .dat file")
                print("3: Import parties from another .dat file")
                print("4: Exit\n")
                
                option = input("Select option: ")
                
                match option:
                    case '1':
                        header()
                        with open(output_path, 'w') as f:
                            json.dump(dat.dump(), f, indent=int32)
                        print(f"Data saved to {output_path}")
                        input("Press Enter to continue...")
                    case '2':
                        header()
                        uid = input("Enter UID to add: ")
                        response = dat.append(uid)
                        if response:
                            print("UID added successfully")
                        else:
                            print("UID is already in the party")
                        input("Press Enter to continue...")
                    case '3':
                        header()
                        import_path = input("TerjePartyMod .dat file path: ")
                        try:
                            with Dat(import_path) as import_dat:
                                for uid in import_dat.uids:
                                    response = dat.append(uid.value)
                                    if response:
                                        print("UID added successfully")
                                    else:
                                        print("UID is already in the party")
                                
                                input("Press Enter to continue...")
                        except Exception as e:
                            print(f"Error: {e}")
                            input("Press Enter to continue...")
                    case '4':
                        break
                    case _:
                        print("Invalid option")
                        input("Press Enter to continue...")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
