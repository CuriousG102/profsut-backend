from django.contrib import admin
from nested_inline.admin import NestedStackedInline, NestedModelAdmin
from dataCollections.models import *

from alpha_upload import tableToDatabase

# Register your models here.

admin.site.register(Question)

class CourseTimeInline(NestedStackedInline):
	model = CourseTime
	extra = 1
	fk_name = 'course'

class CourseInline(NestedStackedInline):
	model = Course
	extra = 1
	fk_name = 'instructor'
	inlines = [
		CourseTimeInline,
	]

class ResponseInline(NestedStackedInline):
	model = Response
	extra = 1
	fk_name = 'instructor'

class InstructorAdmin(NestedModelAdmin):
	fieldsets = [
		(None, {'fields': ['last', 'first', 'profile_photo']})
	]
	inlines = [
		CourseInline,
		ResponseInline,
	]

admin.site.register(Instructor, InstructorAdmin)

class CourseAdmin(admin.ModelAdmin):
	inlines = [
		CourseTimeInline,
	]

class CourseTimeInline(admin.TabularInline):
	model = CourseTime

admin.site.register(Course, CourseAdmin)

class RawDataAdmin(admin.ModelAdmin):
	actions = ['db_upload']

	def db_upload(self, request, queryset):
		for table in queryset:
			tableToDatabase(table.spreadsheet.url)