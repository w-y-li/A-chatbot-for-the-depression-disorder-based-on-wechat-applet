# -*- coding: utf-8 -*-
import os
import openai


# 进入情景
def enter_conversation(response_time, length, match_time, chatgpt, label):
    # response_time用户回复时长（需要提供）
    # length用户回复句子长度（需要提供）
    # match_time匹配sds量表问题的时间间隔（对话轮数）（需要提供）
    if length <= 10 and match_time >= 10:#response_time >= 10 and
        conversation(chatgpt, label)


# 情景对话函数
def conversation(chatgpt, label, re, usersname):
    if len(label) == 20:
        return chatgpt
    r = re
    record_file = open(os.path.join(r"D:\sdsQA\chatbot\txt", "situ_" + usersname + ".txt"),
                       "r", encoding='utf-8-sig')
    rfile = record_file.read().split()
    rfile = list(set(rfile + label))
    if len(rfile) == 20:
        record_file.close()
        clear_file = open(os.path.join(r"D:\sdsQA\chatbot\txt", "situ_" + usersname + ".txt"),
                          "w", encoding='utf-8-sig')
        clear_file.truncate(0)
        clear_file.close()
        record_file = open(os.path.join(r"D:\sdsQA\chatbot\txt", "situ_" + usersname + ".txt"),
                           "r", encoding='utf-8-sig')
        rfile = record_file.read().split()
    with open('conversation.txt', encoding='utf-8-sig') as f:
        conversation_responses = f.read()
        conversation_responses_list = conversation_responses.split('\n')
        # print(conversation_responses_list)
        # m = len(conversation_responses_list)
        # print(conversation_responses_list)
        flag = 1
        # 抛出情景对应的行号
        while flag == 1:
            if conversation_responses_list[r].split('，', 1)[0] not in label:
                if conversation_responses_list[r].split('，', 1)[0] not in rfile:
                    # print(conversation_responses_list[r].split('，', 1)[0])
                    response = conversation_responses_list[r]
                    r = r + 1
                    flag = 0
                else:
                    r = r + 1
            else:
                r = r + 1
        record_file_write = open(
            os.path.join(r"D:\sdsQA\chatbot\txt", "situ_" + usersname + ".txt"),
            "a+", encoding='utf-8-sig')
        record_file_write.write(response.split('，', 1)[0] + '\n')
        record_file_write.close()
        response = response.split('，', 1)[1]
        response = chatgpt + response
        # print(response)
    # response传给gpt

    return response, r


# enter_conversation(20, 1, 20)
# def check_ans(texts, sdstext):
#     openai.api_key = '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'
#     completion = openai.ChatCompletion.create(  # Change the function Completion to ChatCompletion
#         model='gpt-3.5-turbo',
#         messages=[
#             {'role': 'user',
#              'content': f'在接下来我说完“开始”之后，我说话的格式将会是“user：a”，“a”将会是具体的随意的一句话，如果你判断“a”是在回答“{sdstext}”这个SDS量表的问题，那么请你以下列格式进行回复："1,b",其中“b”是句子“a”中你用来判断“a”是在回答SDS量表问题“{sdstext}”的部分，所以字符串“b”应当是“a”的一部分，同时也是“a”中最能看出来是在回复这个SDS量表问题的部分，要求“b”的长度应当尽可能的短；如果你判断“a”并不是在回答“{sdstext}”这个SDS量表的问题，那么请你以下列格式进行回复："0,0"；开始 user:{texts}'}
#         ],
#         temperature=0.7
#     )
#     return completion['choices'][0]['message']['content']
#
#
# print(check_ans("我觉得是的。我曾经一直就很自卑，尤其是有一次去菜市场买菜，我要买一个红薯，但是那人竟然不给我，我问他为什么，他竟然说他看不起我！我的猫没有死", '你觉得如果你死了，别人是不是会生活得更好？'))
# print(conversation('chatgpt', ['6'], 0, 'test'))

