import pyttsx3
import copy
from random import shuffle

from settings import FILE_NAME, SPEED


class WordsTrainer:
    """Класс-тренер, предназначенный для зазубривания слов на различных языках, путём механического заучивания"""
    def __init__(self):
        """Инициализация всех необходимых для работы атрибутов экзэмпляра"""

        self._file_name = FILE_NAME
        self._speed = SPEED
        self._exit_word = 'выход'

        self._words = self._get_words()

        self._words_to_speak = copy.copy(self._words)
        shuffle(self._words_to_speak)

        self._used_words = []
        self._wrong_answers = []
        self._correct = 0
        self._wrong = 0

    def _get_words(self) -> list[str]:
        """Получение слов из файла"""
        with open(self._file_name, 'r', encoding='utf-8') as file:
            return [line.strip() for line in file.readlines() if line.strip()]

    @staticmethod
    def _replace_word(user_word: str) -> str:
        """Приведение строки в нижний регистр и удаление всех пробелов"""
        user_word = user_word.lower()
        user_word = user_word.replace(' ', '')
        return user_word

    def _check_word(self, current_word: str, user_word: str) -> bool:
        """Проверка введённого слова на правильность и увеличение в последствии счёткика
        верных или неверных ответов"""
        if user_word == current_word:
            self._correct += 1
            return True

        self._wrong += 1
        self._wrong_answers.append((current_word, user_word))
        return False

    def _print_results(self) -> None:
        """Вывод резельтатов тренировки"""
        print('\n\n\n-----------------------------')
        print(f'Всего праильных ответов:\t{self._correct}')
        print(f'Всего непраильных ответов:\t{self._wrong}')

        if self._wrong > 0:
            print(f'Слова с ошибками')
            print('Вы написали\t|Правильно')
            for word, user_word in self._wrong_answers:
                print(f'{word}\t|{user_word}')

    def _say(self, word: str) -> bool:
        """Произношение слова и обработка ошибок"""
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', self._speed)
            engine.say(word)
            engine.runAndWait()
            engine.stop()
            del engine
            return True
        except Exception as e:
            print(f"Ошибка произношения: {e}")
            return False

    def run(self) -> None:
        """Основной метод, в котором произносятся и проверяются все слова до остановки."""
        for i, word in enumerate(self._words_to_speak):
            print(f'\nСлово {i + 1}/{len(self._words_to_speak)}')

            if not self._say(word):
                continue

            user_word = input(f'Введите слово ("{self._exit_word}", чтобы закончить): ')
            user_word = self._replace_word(user_word)

            if user_word == self._exit_word:
                break

            self._check_word(word, user_word)

        self._print_results()
