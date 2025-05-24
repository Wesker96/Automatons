import os
from typing import Optional


__NAME_ENV_AUTOMATONS__ = 'AUTOMATONS'
__PATTERN_OF_SUBL_FOLDER__ = "Sublime Text"


def get_path_to_subl() -> Optional[str]:
    automations_path = os.getenv(__NAME_ENV_AUTOMATONS__)

    if automations_path:
        paths = automations_path.split(os.pathsep)

        for path in paths:
            if __PATTERN_OF_SUBL_FOLDER__ in path:
                return path
    return None


def install():
    path2subl = get_path_to_subl()

    if path2subl:
        print(path2subl)
    else:
        print("Not found path to Sublime Text.")


if __name__ == "__main__":
    # C:\Users\user\AppData\Roaming\Sublime Text\Packages
    # path = "C:/Users/user/AppData/Roaming/Sublime Text/Packages"

    install()
