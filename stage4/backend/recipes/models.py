from django.db import models
from django.conf import settings
import uuid


class Tag(models.Model):
    name = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    UNITS_CHOICES = [
        ('u', 'units'),
        ('dash', 'dash'),
        ('ml', 'ml'),
        ('l', 'l'),
        ('g', 'g'),
        ('kg', 'kg'),
        ('tsp', 'tsp'),
        ('Tbsp', 'Tbsp')
    ]

    name = models.CharField(max_length=100, unique=True)
    amount = models.CharField(max_length=50, blank=True)
    units = models.CharField(choices=UNITS_CHOICES)

    def __str__(self):
        return f"{self.amount} {self.name}" if self.amount else self.name


class Step(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          editable=False)
    description = models.TextField(max_length=300, blank=False, null=False)
    order = models.PositiveIntegerField()

    def __str__(self):
        return f"Step {self.order}: {self.description[:30]}..."


class Recipe(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    DIETARY_CHOICES = [
        ('none', 'None'),
        ('vegan', 'Vegan'),
        ('vegetarian', 'Vegetarian'),
        ('gluten_free', 'Gluten-Free'),
        ('dairy_free', 'Dairy-Free'),
        ('nut_free', 'Nut-Free'),
        ('low_carb', 'Low-Carb'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          editable=False)
    title = models.CharField(max_length=200, blank=True, null=True,
                             unique=True)
    description = models.TextField(max_length=400, blank=True, null=True)
    image = models.ImageField(
        upload_to='recipes/',
        default='recipes/default_recipe.png',
        blank=True, null=True)
    rating = models.FloatField(default=0)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name='recipes')
    ingredients = models.ManyToManyField(Ingredient,
                                         related_name='recipes')
    steps = models.ManyToManyField(Step, related_name='recipes')
    anime = models.CharField(max_length=100, blank=True, null=True)
    difficulty = models.CharField(max_length=10,
                                  choices=DIFFICULTY_CHOICES)
    preparation_time = models.PositiveIntegerField(
        help_text='Aproximate preparation time in minutes',
        blank=True, null=True)
    dietary_class = models.CharField(max_length=20,
                                     choices=DIETARY_CHOICES,
                                     default='none')
    servings = models.PositiveIntegerField(default=1)
    tags = models.ManyToManyField(Tag, blank=True, null=True,
                                  related_name='recipes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.title:
            unnamed_recipes = Recipe.objects.filter(
                author=self.author,
                title__startswith=f"{self.author}'s recipe number "
                )
            numbers = []
            for recipe in unnamed_recipes:
                numbers.append(recipe.title.split(" ")[-1])
            last_num = max(numbers) if numbers != [] else 0
            self.title = f"{self.author}'s recipe number {last_num + 1}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
