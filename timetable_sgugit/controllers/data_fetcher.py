import requests
from typing import List
from loguru import logger

from . import GroupDBController
from . import LessonDBController
from . import TeacherDBController
from . import LessonNameDBController
from ..parser import SgugitWebParser
from ..models import LessonAddRequest
from ..models import LessonParseResult
from ..models import GroupCreateRequest
from ..constants import REVERS_LESSON_TYPE
from ..constants import EDUCATION_FORMS
from ..constants import INSTITUTS
from ..constants import COURSES


class DataFetcher:

    def __init__(
        self,
        parser: SgugitWebParser,
        group_controller: GroupDBController,
        lesson_controller: LessonDBController,
        teacher_controller: TeacherDBController,
        lesson_name_controller: LessonNameDBController,
    ):
        self._parser = parser
        self._group_controller = group_controller
        self._lesson_controller = lesson_controller
        self._teacher_controller = teacher_controller
        self._lesson_name_controller = lesson_name_controller

    
    def fetch_teachers(self):
        logger.info('Фетчим преподавателей')
        data = self._parser.parse_teachers()
        logger.info('Данные по предователям получены, загружаем в БД')
        self._teacher_controller.fill_for_iter(data)
        logger.success('Данные по предователям загружены в БД')


    def fetch_groups(self):
        logger.info('Фетчим группы')
        add_list: List[GroupCreateRequest] = list()
        for inst_k, inst_v in INSTITUTS.items():
            for course in COURSES[inst_k]:
                logger.debug(f'Фетчим данные для института {inst_v}, курса {course}')
                try:
                    resp = requests.get(
                        'https://sgugit.ru/bitrix/services/main/ajax.php?mode=class&c=sgugit:rasp&action=getGroupsInfo',
                        params = { 'instituteId': inst_k, 'course': course },
                        headers = { 'Content-Type': 'application/x-www-form-urlencoded' }
                    )
                except Exception as e:
                    logger.error(f'Ошибка запроса списка групп для института {inst_v}, курса {course}: {e}')
                else:
                    logger.debug(f'Данные для института {inst_v}, курса {course} получены')
                    add_list.extend(
                        GroupCreateRequest(
                            sgugit_id      = group.get('id'),
                            name           = group.get('name'),
                            course         = course,
                            institute      = inst_k,
                            education_form = EDUCATION_FORMS[group.get('form').capitalize()]

                        )
                        for group in resp.json().get('data')
                    )
        
        logger.info('Все данные по группам получены, загружаем в БД')
        self._group_controller.fill_for_iter(add_list)
        logger.success('Данные по группам успешно загружены в БД')


    def fetch_lessons(self):
        logger.info('Фетчим занятия')
        add_list: List[LessonParseResult] = list()
        for group_db in self._group_controller.get():
            logger.debug(f'Фетчим занятия для группы {group_db.name}')
            try:
                add_list.extend(
                    LessonAddRequest(
                        hour_id        = lesson.hour ,
                        lesson_type_id = REVERS_LESSON_TYPE[lesson.lesson_type],
                        audience       = lesson.audience,
                        group_id       = group_db.id,
                        teacher_id     = self._teacher_controller.create_if_not_exists(lesson.teacher).id,
                        lesson_name_id = self._lesson_name_controller.create_if_not_exists(lesson.lesson_name).id,
                        date           = lesson.date,
                    )
                    for lesson in 
                        self._parser.parse_lessons(
                            f'https://sgugit.ru/raspisanie/group/{group_db.sgugit_id}/'
                        )
                )
                logger.debug(f'Занятия для группы {group_db.name} успешно получены')
            except Exception as e:
                logger.error(f'Ошибка фетчинга занятий для группы {group_db.name}: {e}')
        
        logger.info('Все данные по занятиям получены, загружаем в БД')
        self._lesson_controller.fill_table(add_list)
        logger.success('Данные по занятиям успешно загружены в БД')
