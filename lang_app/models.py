from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.contrib.auth.models import BaseUserManager
# from moviepy.editor import VideoFileClip, AudioFileClip

DIFFICULTY_CHOICES = [
    (1, 'Beginner'),
    (2, 'Intermediate'),
    (3, 'Advanced'),
]
LEVEL_CHOICES = [
    ('beginner', 'Beginner'),
    ('intermediate', 'Intermediate'),
    ('advanced', 'Advanced'),
]
class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a valid username")

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, username, password, **extra_fields)


class MyUser(AbstractUser):
    email = models.EmailField(unique=True)
    country=models.CharField(max_length=30)
    city = models.CharField(max_length=30, null=True, blank=True)
    device_info = models.CharField(max_length=30,null=True, blank=True)
    display_name=CharField(unique=True, max_length=255, blank=True, null=True)
    phone_number = models.CharField(unique=True, max_length=255, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures', blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

#To store the blog post data: each blog can only have one image
class Blog(models.Model):
    blog_image=models.ImageField(upload_to='blog-images', blank=True, null=True)
    blog_title = models.CharField(max_length=255)
    blog_content = models.TextField()
    blog_author = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.blog_title

#To store the post data: each blog can have multiple images and is to be uploaded by a specific author
class Post(models.Model):
    post_author=models.ForeignKey(MyUser,on_delete=models.CASCADE, related_name='post_author')
    post_content = models.TextField()
    post_images = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.post_content


#To store the all the courses available
class Course(models.Model):
    course_name=models.CharField(max_length=255)
    course_level=models.CharField(choices=LEVEL_CHOICES, max_length=255, default='beginner')
    # course_thumbnail=models.ImageField(upload_to='course-thumbnails', blank=True, null=True)
    instructor_name=models.CharField(max_length=255)
    difficulty = models.IntegerField(choices=DIFFICULTY_CHOICES, default=1)

    # def __str__(self):
    #     return self.course_name
    def __str__(self):
        return f"{self.course_name} - {self.course_level}"

    class Meta:
        ordering = ['course_name','difficulty']

#To store the enrolment details for the courses
class EnrolledCourses(models.Model):
    course_name=models.ForeignKey(Course,on_delete=models.CASCADE, related_name='courses')
    course_level =models.CharField(choices=LEVEL_CHOICES, max_length=255, default='beginner')
    student=models.ForeignKey(MyUser,on_delete=models.CASCADE, related_name='students')
    enrolment_date=models.DateTimeField(auto_now_add=True)
    progress=models.FloatField(default=0.0, blank=True, null=True)
    is_completed=models.BooleanField(default=False)
    completion_date=models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = ('student', 'course_name', 'course_level')

    def __str__(self):
        return self.course_name.course_name


class CourseModule(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_modules')
    module_title = models.CharField(max_length=255)
    module_description = models.TextField()
    module_order = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.module_title} - {self.course}"
        # return self.module_title


# To do: add a quiz table that stores questions that will be shown at the end of each module

class CourseLesson(models.Model):
    LESSON_CHOICES = [
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('read', 'Read'),
        ('quiz', 'Quiz'),
    ]
    module_name = models.ForeignKey(CourseModule, on_delete=models.CASCADE, related_name='module_lessons')
    lesson_title = models.CharField(max_length=255)
    lesson_description = models.TextField()
    lesson_number = models.IntegerField()
    lesson_type = models.CharField(max_length=255, choices=LESSON_CHOICES, default='read')
    lesson_file = models.FileField(upload_to='course-lessons', blank=True, null=True)
    lesson_transcript = models.TextField(blank=True, null=True)
    lesson_content = models.TextField(blank=True, null=True)
    lesson_duration = models.FloatField(blank=True, null=True, help_text="Duration of the lesson in seconds")

    # use moviepy to extract the video and audio lengths nly if the content type is either  video or audio but for the read content you add the estimated duration it would take the user to complete the lesson

    def __str__(self):
        return self.lesson_title
