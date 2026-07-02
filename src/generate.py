import os
import shutil


def generate(public_dir: str, static_dir: str):
    public_dir_abs: str = os.path.abspath(public_dir)
    if os.path.exists(public_dir_abs):
        shutil.rmtree(public_dir_abs)

    static_dir_abs: str = os.path.abspath(static_dir)
    if not os.path.exists(static_dir_abs):
        raise ValueError("static dir does not exists")

    os.mkdir(public_dir_abs)

    cp_static_to_public(public_dir_abs, static_dir_abs)


def cp_static_to_public(public_dir_abs: str, static_dir_abs: str):
    entries: list[str] = os.listdir(static_dir_abs)
    for entry in entries:
        entry_abs: str = os.path.join(static_dir_abs, entry)
        if os.path.isfile(entry_abs):
            shutil.copy(entry_abs, public_dir_abs)
        else:
            public_subdir_abs: str = os.path.join(public_dir_abs, entry)
            os.mkdir(public_subdir_abs)
            cp_static_to_public(public_subdir_abs, entry_abs)
