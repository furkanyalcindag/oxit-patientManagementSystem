from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group, User

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from career.models import Language, Gender, ForeignLanguage, JobType
from career.models.ForeignLanguageDescription import ForeignLanguageDescription
from career.models.GenderDescription import GenderDescription


class InitDataApi(APIView):

    def get(self, request, format=None):
        group_admin = Group()
        group_admin.name = 'Admin'
        group_admin.save()

        group = Group()
        group.name = 'Student'
        group.save()

        group = Group()
        group.name = 'Company'
        group.save()

        group = Group()
        group.name = 'Consultant'
        group.save()

        group = Group()
        group.name = 'ContentManager'
        group.save()

        superuser = User()
        superuser.username = 'admin'
        superuser.is_superuser = True
        superuser.password = make_password('oxit2016')
        superuser.save()
        superuser.groups.add(Group.objects.get(name='Admin'))
        superuser.save()

        language_tr = Language()
        language_tr.name = 'Turkish'
        language_tr.code = 'tr'
        language_tr.flag = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAVCAIAAACor3u9AAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAyZpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDUuNi1jMTExIDc5LjE1ODMyNSwgMjAxNS8wOS8xMC0wMToxMDoyMCAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RSZWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIENDIDIwMTUgKFdpbmRvd3MpIiB4bXBNTTpJbnN0YW5jZUlEPSJ4bXAuaWlkOkY1RTE3MzY4MEQyODExRTY5MTgyOEFBNEZENDlFMUVBIiB4bXBNTTpEb2N1bWVudElEPSJ4bXAuZGlkOkY1RTE3MzY5MEQyODExRTY5MTgyOEFBNEZENDlFMUVBIj4gPHhtcE1NOkRlcml2ZWRGcm9tIHN0UmVmOmluc3RhbmNlSUQ9InhtcC5paWQ6RjVFMTczNjYwRDI4MTFFNjkxODI4QUE0RkQ0OUUxRUEiIHN0UmVmOmRvY3VtZW50SUQ9InhtcC5kaWQ6RjVFMTczNjcwRDI4MTFFNjkxODI4QUE0RkQ0OUUxRUEiLz4gPC9yZGY6RGVzY3JpcHRpb24+IDwvcmRmOlJERj4gPC94OnhtcG1ldGE+IDw/eHBhY2tldCBlbmQ9InIiPz7T8qTbAAACSElEQVR42uRVz2sTQRSe92Y32d0mzebnRjCCvxAVRMSTiogg6KHiD0TwKIhQ8aCgF/GuePAP8CRFKdY2YtQieBRB8CYqUkmxEW0rjUlqdpPd2RknENQQalxr8OAwA8vs7vvmfe/73kDJsEg/B5I+j38OIOQUywFQlnzDGHcdkCcASgQjABA2CMLfARC2jVZ68MQpbf8+zKT94rRTmHTuPeR1G1QlEAA9r0Y6d0DY9fCuHelH48bxoxAOOxMF9/kLTCTUTRv8mZKo2wTxzzMQzaayfl3yzk26IuvkH5RPDvuVOSAqIRzjKTBjhFLBmCSsDQMQsMi+Gz13RkZn0+/Lp8/yahWNOBgRMAZFo8k/zhLPM44chIhOBAdd7ymBTgDfx1hc27tHPjoT9/3Pn1ohfpDXOrVA1A8PpcZumdevwoAhfwlAkRACBwxMxlsiKs10w0uKzEsX9KEDoGuNp89YqYiGGQBAMiv1w8tfMJWkuZzkvVMQVNQWKxcvY9aimTS1MkpuDZ+bJ4ry2yqSDCzW1M0bQ9u30axl374rI4Kqfk9Q8k58Lj+rXbnWKEy2bCgp+mWdu2TKCXs7ZRw7pORWKmtXNx8/4V8XiOcTr4mRKKZSotHwXr8hrrQeSjP2VBF0d1Nu17XdOxMjN5RVOb/0oT4yyqaKGDeF6zr5Al8oS66WYzQCaoi9K9qj43x2Hs1YaOsWaqW9l6+csTyvVEEJ5mRY8j7wGPd+6kWSC00P5OFezU5VUI22yigXaH3opu0M2+s/vtG+CTAAgljgQ5Eee/gAAAAASUVORK5CYIIxNDk2'
        language_tr.save()

        language_en = Language()
        language_en.name = 'English'
        language_en.code = 'en'
        language_en.flag = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAQCAYAAAB3AH1ZAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAyZpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDUuNi1jMTExIDc5LjE1ODMyNSwgMjAxNS8wOS8xMC0wMToxMDoyMCAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RSZWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIENDIDIwMTUgKFdpbmRvd3MpIiB4bXBNTTpJbnN0YW5jZUlEPSJ4bXAuaWlkOjFFODhFQjJFMEQyRDExRTZBMjM0Rjc1Q0QzODFGMTY3IiB4bXBNTTpEb2N1bWVudElEPSJ4bXAuZGlkOjFFODhFQjJGMEQyRDExRTZBMjM0Rjc1Q0QzODFGMTY3Ij4gPHhtcE1NOkRlcml2ZWRGcm9tIHN0UmVmOmluc3RhbmNlSUQ9InhtcC5paWQ6MUU4OEVCMkMwRDJEMTFFNkEyMzRGNzVDRDM4MUYxNjciIHN0UmVmOmRvY3VtZW50SUQ9InhtcC5kaWQ6MUU4OEVCMkQwRDJEMTFFNkEyMzRGNzVDRDM4MUYxNjciLz4gPC9yZGY6RGVzY3JpcHRpb24+IDwvcmRmOlJERj4gPC94OnhtcG1ldGE+IDw/eHBhY2tldCBlbmQ9InIiPz5XLj5qAAAEj0lEQVR42sRVfUxVZRj/nXPPuZ9A4BZbW5SlAi1GWHDBIIHL5QLNcnWRGeIK1uzCAlfSHK2t9Y/ipmuZE9QtsWmkAhMXeLkffOi88mXMlRGIUdOyeSkj5HK/b885B0zwOl3/9Nzd7d15n/f9/Z7f8/EyN8pME6qS12Ki1hlgH/kNO/eY0X32ChAIAWoeYBgsMpcXLV+/A73tOCZ2NQLktrKuEhZdCUreOEBn5Iv9Q+Qw5wMi1DDkJKA6WYnkkV74/5zG8u1VU5wjRReb0WGN9Jw8hezNG6A/VgHz4DXs3muDvW/8/kQeZAvAGgJel4TKZzhoxwfADdxG9CYj5AV5sAxdY1jjoVFfBVLhSMmFs7UDU+XvIn/mKmxHy9HZUgVdbgLgCQCzXunShwEmlcDyBLwabVXP4jD3LTJH7IhdX4DYL/ejZ1kC8jc3ocDY4Ofg86Hr9Ai6IgWJ0mBKYpF+sgP80RbklxWj6Fg5zAOkyOfzihCRcDzEbwJJjWo+Yl6MmB+ZQUypERxFbB68jt1lh+eVDYrp4uAmmQR1Z1ywnBiAhXKVmZOMykQZ0praID/UDP2WUhR+sQkd5ydR/1mPkPZFJBbWWaTW+9mPImNiEOzFaSiNrxKwHu1CSo0H0b8ArJJLKaUUMSf6fvqDzi67c1kwBBdtqKI0yM18HNGjV+Ca+BnReVnEWCXVIf1vfbgDv+85IBbhY7UmxOyog7g7OIxZXxCaTK3oe8MVRK/jKjy+ANQUMbO4lpzMXx/XLyKwYEEiMufxI8TzYGQyBN1uhIi9jJUumD4/BPflMZGAMikRj2SmilGFFARCP9Gf7uBkDJQKHiwbtoidzLDiybAEHmSsUgFGLrVcyOslQA/+gzlZ/M/GrdxuuvcrSSmkwO3xwU9zgCH5GKVS2vJ4hEKhFAzfmwIINUb+MpYUUlLKAmCpy5QKTkpBmPbhbPqNS9qJcj/nhZyTIfvFFYhTSbmbdQxBw9M6LRVzgh8VoWv4kkggKjvj3yIU9lwuTPc4oIl/CrdWrYDVcR0e6jKVil9ahOCKNzZKLREUJhf1MbFPXxuPD2r0iIQf0+12uFtPIxARAcsqLT7deRE17xmg59g701HDs/imbxL79lpQV6ND4ZonoJGz+PWjXfAq1fDEp6Nh1I8LvaTYrEtqw3lFWBAr0puAGeheTkJnx1b0t23Bet8vcJm2YtZsR//zeagIvoDXGy7jXLck+92BCGtB3LP2MRTRoDG83YzemHgsP34QT5e+gsKxc2iJ+h4t21ZDX6wVh5UYMGFzoFbT6RJRW61HUXocAtZuON+qh1+twUBKHhrH/OgiYNx2iQcotLDPgviN9qCQwWr7EdbeceTnxKOWlDTQ+PV32bG2uRVr1BHorxIU8cFGinDm1iq+QBsHn60HN98UgNUYei4XDWMBdDXeBbz0lbufCUwEIiSv1TYqEcklItX5MDTth++MFVlftSE9MgoXTFqOM7DOm5MbPvFxUZG4lKbHvu+8BPyDOJrFV/BhgcMSUUhErESkR1KkblsBco7o8Xf7Gbx0qnPqHwEGAMUZ6nw0OFRDAAAAAElFTkSuQmCCMjA3OQ=='
        language_en.save()

        gender = Gender()
        gender.keyword = 'male'
        gender.save()

        gender_description = GenderDescription()
        gender_description.name = 'Erkek'
        gender_description.gender = gender
        gender_description.language = language_tr
        gender_description.save()

        gender_description2 = GenderDescription()
        gender_description2.name = 'Male'
        gender_description2.gender = gender
        gender_description2.language = language_en
        gender_description2.save()

        gender = Gender()
        gender.keyword = 'female'
        gender.save()

        gender_description = GenderDescription()
        gender_description.name = 'Kadın'
        gender_description.gender = gender
        gender_description.language = language_tr
        gender_description.save()

        gender_description2 = GenderDescription()
        gender_description2.name = 'Female'
        gender_description2.gender = gender
        gender_description2.language = language_en
        gender_description2.save()

        foreign_language = ForeignLanguage()
        foreign_language.keyword = 'english'
        foreign_language.save()

        foreign_language_description = ForeignLanguageDescription()
        foreign_language_description.name = 'English'
        foreign_language_description.foreignLanguage = foreign_language
        foreign_language_description.language = language_en
        foreign_language_description.save()

        foreign_language_description = ForeignLanguageDescription()
        foreign_language_description.name = 'İngilizce'
        foreign_language_description.language = language_tr
        foreign_language_description.foreignLanguage = foreign_language
        foreign_language_description.save()

        foreign_language = ForeignLanguage()
        foreign_language.keyword = 'french'
        foreign_language.save()

        foreign_language_description = ForeignLanguageDescription()
        foreign_language_description.name = 'French'
        foreign_language_description.foreignLanguage = foreign_language
        foreign_language_description.language = language_en
        foreign_language_description.save()

        foreign_language_description = ForeignLanguageDescription()
        foreign_language_description.name = 'Fransızca'
        foreign_language_description.foreignLanguage = foreign_language
        foreign_language_description.language = language_tr
        foreign_language_description.save()

        foreign_language = ForeignLanguage()
        foreign_language.keyword = 'italian'
        foreign_language.save()

        foreign_language_description = ForeignLanguageDescription()
        foreign_language_description.name = 'Italian'
        foreign_language_description.foreignLanguage = foreign_language
        foreign_language_description.language = language_en
        foreign_language_description.save()

        foreign_language_description = ForeignLanguageDescription()
        foreign_language_description.name = 'İtalyanca'
        foreign_language_description.foreignLanguage = foreign_language
        foreign_language_description.language = language_tr
        foreign_language_description.save()

        foreign_language = ForeignLanguage()
        foreign_language.keyword = 'german'
        foreign_language.save()

        foreign_language_description = ForeignLanguageDescription()
        foreign_language_description.name = 'German'
        foreign_language_description.foreignLanguage = foreign_language
        foreign_language_description.language = language_en
        foreign_language_description.save()

        foreign_language_description = ForeignLanguageDescription()
        foreign_language_description.foreignLanguage = foreign_language
        foreign_language_description.name = 'Almanca'
        foreign_language_description.language = language_tr
        foreign_language_description.save()

        job_type = JobType()
        job_type.name = 'Part Time'
        job_type.save()

        job_type = JobType()
        job_type.name = 'Full Time'
        job_type.save()

        job_type = JobType()
        job_type.name = 'Remote'
        job_type.save()

        return Response({"message": "initial datas added"}, status=status.HTTP_200_OK)
