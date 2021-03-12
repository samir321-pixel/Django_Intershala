from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

gender_choices = (
    ("Male", "Male"),
    ("Female", "Female"),
    ("Other", "Other"),
)


class Recruiter(models.Model):
    user = models.OneToOneField("user.User", on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    company = models.ForeignKey("intershala_admin.IntershalaCompany", on_delete=models.CASCADE,
                                related_name="recruiter_company")
    DOB = models.DateField()
    created_profile = models.ManyToManyField("job_profile.Profile", null=True, blank=True, related_name="my_profiles")
    gender = models.CharField(max_length=10, choices=gender_choices, default="Male")
    active = models.BooleanField(default=True)
    company_address = models.CharField(max_length=200)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=200)
    password = models.CharField(max_length=30)
    overall_rating = models.FloatField(default=0)
    pincode = models.CharField(("pin code"), max_length=7, default="00000")
    created_at = models.DateTimeField(auto_now=True)
    unseen_notification = models.IntegerField(default=0)

    def __str__(self):
        return "{} {}".format(self.user, self.first_name)

    def rating_counter(self, recruiter_id):
        count = RecruiterReview.objects.filter(id=recruiter_id).count()
        if count == 0:
            count = 1
        else:
            count
        total = 0
        for i in RecruiterReview.objects.filter(id=recruiter_id):
            total = i.rating + total
        overall_rating = total / count
        recruiter_query = Recruiter.objects.get(id=recruiter_id)
        recruiter_query.overall_rating = overall_rating
        recruiter_query.save()


class RecruiterReview(models.Model):
    recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE)
    student = models.ForeignKey("student.Student", on_delete=models.CASCADE)
    rating = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    message = models.TextField()
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.rating)
