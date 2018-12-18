from django.db import models

# Create your models here.
class Img(models.Model):

    CLASSIFICATION_TYPES = (
        ('ASSESSED','assessed FFPA'),
        ('PARTIAL','partial FFPA'),
        ('NOT_ASSESSED', 'not assessed FFPA'),
        ('UNKNOWN', 'unknown'),
    )

    image = models.ImageField(upload_to='pics_to_classify/')
    image_classification = models.CharField(max_length=12, choices=CLASSIFICATION_TYPES, blank=True)
    updated_by_user = models.CharField(max_length=50, blank=True)

    # for django shell, upload files:
    # for i in glob.glob(p + "\\*.jpg"):
    # ...     pic = Img(image=i)
    # ...     pic.image.save(os.path.basename(i), open(i, 'rb'))

    @property
    def pictures_to_classify(self):
        return [i for i in Img.objects.all() if not i.image_classification]

    def __str__(self):
        if self.image_classification:
            return "Classified Image - {}".format(self.image_classification)
        if not self.image_classification:
            return "Not Classified Image"
