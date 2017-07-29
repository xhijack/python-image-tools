import os

from PIL import Image


class DirectorySameException(Exception):
    pass


class PicMassResizer(object):

    def __init__(self, source_directory, target_directory, file_types='jpg|png|JPG|PNG', image_processor=Image):
        """
            Picture Mass Resizer
        :param `str` source_directory: source images
        :param `str` target_directory: target directory after resizing images
        :param `str` file_types: extensions of images eg: jpg|png. You can change it
        :param `class` image_processor: default is PIL.Image
        """

        self._source_directory = source_directory
        self._target_directory = target_directory
        self._file_types = file_types
        self._image_processor = image_processor

    def _preprocessing(self):
        if self._source_directory == self._target_directory:
            raise DirectorySameException("Source Directory and Target Directory must be different")

        if not os.path.exists(self._target_directory):
            os.makedirs(self._target_directory)

    def choose_source_directory(self, directory):
        self._source_directory = directory

    def choose_target_directory(self, directory):
        self._target_directory = directory

    def _get_images(self):
        """
            get all images from source directory
        :return: returning all images
        :rtype: `list`
        """
        files = os.listdir(self._source_directory)
        file_types = self._file_types.split("|")
        return [i for i in files if i.endswith(tuple(file_types))]

    def _get_new_sized(self, width, height, percentage_reduced):
        """

        :param `int` width: original width
        :param `int` height: original height
        :param `float` percentage_reduced: percentage reduced
        :return: returning new width and new height
        :rtype: `tuple`
        """
        return int(width - (width * percentage_reduced)), int(height - (height * percentage_reduced))

    def process(self, percentage_reduced):
        """
           resize all images
        :param `float` percentage_reduced: percentage you want to resize eg: 0.1 (10%) reduce 10%. Be careful to set it.
        :return:
        """
        self._preprocessing()

        for image_path in self._get_images():
            img = self._image_processor.open(self._source_directory + "/" + image_path)

            new_width, new_height = self._get_new_sized(img.size[0], img.size[1], percentage_reduced)

            new_image = img.resize((new_width, new_height))

            print(img.filename)
            new_image.save(self._target_directory + '/' + image_path)


if __name__ == '__main__':
    app = PicMassResizer(SOURCE_PATH, TARGET_PATH)
    app.process(0.5)
