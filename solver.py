'''''''''''''''''''''''''''''
COPYRIGHT DOTERUROD & LESTERRRY,

2021
'''''''''''''''''''''''''''''

cookie = """Cookie"""

ids = [
"194854525",
"195162710", 
"195163858", 
"195304784", 
"195378428", 
"195379409", 
"195379761", 
"195380095"
]

import requests
import base64
import json
import urllib.parse

def get_link(id):
    return f"https://online.patriotsport.moscow/pl/teach/control/lesson/view?id={id}&editMode=0"

def parse_between(string, fr, to):
    start = string.find(fr) + len(fr)
    end = string.find(to, start)
    return string[start:end]

def solve(link, cookies):
    headers = {'cookie': cookies, 'referer': link,'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'}
    r = requests.get(link, headers=headers)
    questionaryId = parse_between(r.text, "questionaryId:", ",") #регулярки? не не слышал
    object_id = parse_between(r.text, "objectId: ", ",")
    is_last_question = False

    while not is_last_question:
        r = requests.post("https://online.patriotsport.moscow/pl/teach/questionary-public/testing?id=" + questionaryId, headers=headers, data=f"questionaryId={questionaryId}") #получаем вопросы и ответы
        if "Ваш результат" in r.text:
            print("Тест уже решен")
            return #ес уже решали то пропускаем эти тесты
        try: 
            json_data = r.json()['data']
        except:
            print("Тест непроходим")
            return
        is_last_question = json_data['isLastQuestion']
        answers = json.loads(base64.b64decode(json_data['resultHash']))
        try:
            right_answer = next(item for item in answers['question']['variants'] if item['is_right'] == 1)
        except:
            right_answer = answers['question']['variants'][0] #у них в нескольких вопросах нет ни одного правильного ответа. Кто тот сайт писал?
        r = requests.post('https://online.patriotsport.moscow/pl/teach/questionary-public/do-question-answer', headers=headers, data=f"questionId={json_data['question_id']}&answerValue={urllib.parse.quote(right_answer['value'].encode('utf-8'))}&objectId={object_id}")
        print(f"Q: {answers['question']['title']}\nA: {right_answer['value']}")

def check(link, cookies):
    headers = {'cookie': cookies, 'referer': link,'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'}
    r = requests.get(link, headers=headers)
    questionaryId = parse_between(r.text, "questionaryId:", ",") #регулярки? не не слышал
    r = requests.post("https://online.patriotsport.moscow/pl/teach/questionary-public/testing?id=" + questionaryId, headers=headers, data=f"questionaryId={questionaryId}") #получаем вопросы и ответы
    if "Ваш результат" in r.text or "Ваша оценка" in r.text:
        print("РЕШЕН")
    else:
        print("ОШИБКА")

n = 0
for id in ids:
    n += 1
    print(f"Решаем #{n}")
    solve(get_link(id), cookie)
print("Цикл завершен, проверка...")
n = 0
for id in ids:
    n += 1
    print(f"Тест #{n}: ", end="", flush=True)
    check(get_link(id), cookie)
