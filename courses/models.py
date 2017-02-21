'''
Models for Courses
'''
from django.db import models
from redactor.fields import RedactorField

GENRE_CHOICES = (("Academics", "Academics"), ("Arts", "Arts"), ("Sports", "Sports"),
                 ("Programming Languages", "Programming Languages"))
class Genre(models.Model):
    '''
    Genre Object - Specifies Genre of the Courses
    Has to be from one of the Genre Choices
    '''
    name = models.CharField(max_length=40, unique=True, choices=GENRE_CHOICES)
    def __str__(self):
        return self.name

CLASS_CHOICES = ((5, "Class 1-5"), (10, "Class 6-10"), (12, "Class 11-12"), (16, "Graduation"),
                 (100, "All"))
class Class(models.Model):
    '''
    This is the standard in which the user studies
    It is categorized into 3 groups of Class Choices
    '''
    name = models.IntegerField(choices=CLASS_CHOICES, unique=True)
    def __str__(self):
        return self.get_name_display()

COURSE_TYPE_CHOICES = (("Monthly Course", "Monthly Course"),
                       ("Half Year Course", "Half Year Course"),
                       ("One Year Course", "One Year Course"),
                       ("Two Year Course", "Two Year Course"),
                       ("Crash Course", "Crash Course"))
class CourseType(models.Model):
    '''
    This is the type of the course from one of the given choices
    '''
    name = models.CharField(max_length=50, choices=COURSE_TYPE_CHOICES, unique=True)

    def __str__(self):
        return self.name


class GraduationDepartment(models.Model):
    '''
    Graduation Department - Eg CSE/Chemical for Engineering, similar for arts and commerce
    '''
    name = models.CharField(max_length=200, unique=True)
    def __str__(self):
        return self.name

class Course(models.Model):
    '''
    Course that an coaching institute can teach
    '''
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE, db_column='class_id')
    name = models.CharField(max_length=100)
    description = RedactorField(verbose_name=u'Description')
    course_type = models.ForeignKey(CourseType, on_delete=models.CASCADE)
    graduation_department = models.ForeignKey(GraduationDepartment, blank=True, null=True,
                                              on_delete=models.SET_NULL)
    active = models.BooleanField(default=True)
    def __str__(self):
        display_string = self.name + " " + self.course_type.name
        display_string += " for " + self.class_id.get_name_display()
        if (self.class_id.name == 16) and self.graduation_department != None:
            display_string += " : " + self.graduation_department.name
        return display_string

    def display(self):
        '''
        Function to print Course as string
        '''
        return self.__str__()

class Subject(models.Model):
    '''
    Subjects taught within a course
    '''
    name = models.CharField(max_length=100)
    description = RedactorField(verbose_name=u'Description')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + " - " + self.course.display()

    def display(self):
        '''
        Display subject as string
        '''
        return self.__str__()

    class Meta:
        '''
        Meta information of Subject. Used to declare unique key
        '''
        unique_together = ("name", "course")

class CourseMenu(object):
    '''
    Class to generate menu_items
    '''
    def __init__(self, name="", url_name=None, child_nodes=None):
        self.name = name
        self.url_name = url_name
        self.child_nodes = child_nodes

    def toDict(self):
        '''
        parse class course menu to dictionary
        '''
        dict_value = dict(name=self.name, url_name=self.url_name, child_nodes=[])
        if self.child_nodes is None:
            return dict_value
        for node in self.child_nodes:
            dict_value["child_nodes"].append(self.child_nodes[node].toDict())
        return dict_value

    def add_course_for_course_type(self, course):
        '''
        add a course in the menu for a course type
        '''
        if self.child_nodes is None:
            self.child_nodes = {}
        self.child_nodes[course.id] = CourseMenu(name=course.name, url_name=course.id)

    def add_course_for_class(self, course):
        '''
        add a course in the menu for a class
        '''
        if self.child_nodes is None:
            self.child_nodes = {}

        if course.course_type.id not in self.child_nodes:
            self.child_nodes[course.course_type.id] = CourseMenu(name=course.course_type.name)
        next_node = self.child_nodes[course.course_type.id]
        next_node.add_course_for_course_type(course)

    def add_course_for_genre(self, course):
        '''
        Add a course in the menu for a genre
        '''
        if self.child_nodes is None:
            self.child_nodes = {}
        if course.class_id.id not in self.child_nodes:
            self.child_nodes[course.class_id.id] = CourseMenu(name=course.class_id.get_name_display())
        next_node = self.child_nodes[course.class_id.id]

        next_node.add_course_for_class(course)

    def add_all_courses(self):
        '''
        Add all courses to menu
        '''
        courses = Course.objects.all()
        for course in courses:
            if self.child_nodes is None:
                self.child_nodes = {}
            if course.genre.id not in self.child_nodes:
                self.child_nodes[course.genre.id] = CourseMenu(name=course.genre.name)
            next_node = self.child_nodes[course.genre.id]
            next_node.add_course_for_genre(course)
