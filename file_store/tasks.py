"""Tasks for file management."""

def image_auto_crop_task(original_image, sizes=None):
    """Crop and/or resize an Image according to an applications config.

    Images are expected to be cropped async to the Django application,
    management of the crop is managed through Celery and external apps.

    @:param original_image: Image model detailing the image to crop.
    @:param sizes: tuple of pair of integers as ((width, height, ), )
    """
    pass
