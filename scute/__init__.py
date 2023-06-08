from scute.commands import command_stack
from os.path import join
import os, json, shutil


class pack:
    meta = {"pack": {"pack_format": 1, "description": "My first pack"}}
    name = ""
    path = ""

    @staticmethod
    def build():
        if pack.name != "":
            if pack.path != "":
                bp = join(os.path.expandvars(pack.path), pack.name)
                shutil.rmtree(bp)
                os.makedirs(bp)
                try:
                    with open(join(bp, "pack.mcmeta"), "w") as mcmeta:
                        json.dump(pack.meta, mcmeta, indent=4)
                except Exception as e:
                    print("Build path is not valid, or folder does not exist. Error:")
                    print(e)
                    return

                os.makedirs(os.path.join(bp, "data"))

            else:
                print("Please set a path to compile to with scute.pack.setBuildPath()")
                return
        else:
            print("Please set a pack name with scute.pack.setName()")
            return

    @staticmethod
    def setName(name):
        pack.name = name

    @staticmethod
    def setDescription(desc: str):
        pack.meta["pack"]["description"] = desc

    @staticmethod
    def setVersion(version: str | int):
        """
        :param version: Can be a major release like "1.19.4" (goes back to 1.16) or a pack_format number like 11
        """
        if isinstance(version, str):
            pack.meta["pack"]["pack_format"] = versions[version]
        else:
            pack.meta["pack"]["pack_format"] = version

    @staticmethod
    def setBuildPath(path: str):
        """
        Sets the folder which your datapack will be built into - for example, "%appdata%/.minecraft/saves/world/datapacks. Should be a full path."
        """
        pack.path = path


versions = {
    "1.16": 5,
    "1.16.1": 5,
    "1.16.2": 6,
    "1.16.3": 6,
    "1.16.4": 6,
    "1.16.5": 6,
    "1.17": 7,
    "1.17.1": 7,
    "1.18": 8,
    "1.18.1": 8,
    "1.18.2": 9,
    "1.19": 10,
    "1.19.1": 10,
    "1.19.2": 10,
    "1.19.3": 10,
    "1.19.4": 12,
}
