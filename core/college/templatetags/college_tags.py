from django import template

from core.college.models import TeacherMatterDet

register = template.Library()


@register.filter
def get_matters_prof(course_id, doc_id):
    return TeacherMatterDet.objects.filter(teacher_mat__teacher_id=doc_id, course_mat__course_id=course_id)
