import requests
from bs4 import BeautifulSoup
from typing import List
from loguru import logger

from .models import LessonParseResult


class SgugitWebParser:

    def parse_teachers(self) -> List[str]:
        logger.debug('Запрос страницы с преподавателями')
        url = 'https://sgugit.ru/raspisanie/teacher/'
        response = requests.get(url)
        page = BeautifulSoup(response.text, "html.parser")

        logger.debug('Парсинг страницы с преподавателями')
        return list(
            teacher.text.strip()
            for teacher in page.find('div', 'card_teachers').find_all('a')
        )


    def parse_lessons(self, url: str) -> List[LessonParseResult]:
        logger.debug(f'Запрос на {url}')
        response = requests.get(url)
        page = BeautifulSoup(response.text, "html.parser")

        logger.debug(f'Парсинг страницы {url}')
        result = list()
        for date_info, day in zip(page.find_all('div', 'date_info'), page.find_all('div', 'day')):
            for index, day_hours in enumerate(day.find_all('div', 'day_hours')):
                lesson = day_hours.find('div', 'lesson_info')
                if lesson is None:
                    continue
                
                result.append(
                    LessonParseResult(
                        hour        = index,
                        lesson_type = lesson.find('p', 'lesson_type').text.strip().capitalize(),
                        audience    = lesson.find('a', 'aud_num').text.strip(),
                        group       = page.find('div', 'container_title').find('h1').text.strip(),
                        teacher     = lesson.find('a', 'teach_name').text.strip(),
                        lesson_name = lesson.find('div', 'lesson_name').text.strip(),
                        date        = date_info.find('div', 'date').text.strip(),
                    )
                )
        
        logger.debug(f'Парсинг страницы {url} завершен')
        return result
