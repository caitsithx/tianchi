import glob
import logging
import shutil
import zipfile
from os import path

from settings import *

logging.basicConfig(filename=path.join(BASE_DIR, 'unzipping.log'),
                    level=logging.INFO)


def unzip_files(zip_files, tgt_folder):
    if not os.path.exists(tgt_folder):
        os.mkdir(tgt_folder)
        logging.info("mkdir %s" % tgt_folder)

    for zip_file in zip_files:
        path_parts = zip_file.split("/")
        file_name = path_parts[len(path_parts) - 1]
        new_zip_file = path.join(tgt_folder, file_name)
        logging.info('copy %s to %s' % (zip_file, new_zip_file))
        shutil.copyfile(zip_file, new_zip_file)
        with zipfile.ZipFile(new_zip_file, "r") as zip_ref:
            zip_ref.extractall(tgt_folder)

        unzipped_path = path.join(tgt_folder, file_name.split(".")[0])
        for unzipped_file in glob.glob(path.join(unzipped_path, "*")):
            shutil.move(unzipped_file, tgt_folder)

        shutil.rmtree(unzipped_path)

        logging.info('%s is unzipped.' % new_zip_file)
        os.remove(new_zip_file)
        logging.info('%s is deleted.' % new_zip_file)
        break


def unzip():
    train_zip_files = glob.glob(path.join(DL_DIR, "train*.zip"))
    unzip_files(train_zip_files, BASE_DIR)

    val_zip_files = glob(path.join(DL_DIR, "val*.zip"))
    unzip_files(val_zip_files, path.join(BASE_DIR, "val"))

    test_zip_files = glob(path.join(DL_DIR, "test*.zip"))
    unzip_files(test_zip_files, path.join(BASE_DIR, "test"))

    test2_zip_files = glob(path.join(DL_DIR, "test2*.zip"))
    unzip_files(test2_zip_files, path.join(BASE_DIR, "test2"))


def unzip_1(zip_file):
    correct_images_zip = path.join(BASE_DIR, zip_file)
    shutil.copyfile(path.join(DL_DIR, zip_file),
                    correct_images_zip)
    logging.info('copy %s to %s' % (path.join(DL_DIR, zip_file),
                                    correct_images_zip))

    with zipfile.ZipFile(correct_images_zip, "r") as zip_ref:
        zip_ref.extractall(BASE_DIR)

    logging.info('unzipped %s' % correct_images_zip)
    os.remove(correct_images_zip)
    logging.info('removed %s' % correct_images_zip)


if __name__ == '__main__':
    unzip()
    unzip_1('correct_images.zip')
