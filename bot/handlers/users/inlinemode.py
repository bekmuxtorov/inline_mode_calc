from aiogram import types
from loader import dp, db


def get_result(word: str) -> int:
    hints: list = ['+', '-', '*', "/"]
    result: int = 0
    if word:
        if word[-1] not in hints:
            result = eval(word)
    return result


@dp.inline_handler()
async def calc(query: types.InlineQuery):
    input: str = query['query']
    result = get_result(input)
    await db.create_user(query['from'])

    solution_answer: str = f"<b>📌Javob:</b>\n\n"
    solution_answer += f"{input} = {result}"
    solution_answer += f"\n\n{'➖'*10}"
    solution_answer += "\n💡Author: @Asadbek_Muxtorov"
    await query.answer(
        results=[
            types.InlineQueryResultArticle(
                id='id001',
                title=f"Natija: {result}",
                input_message_content=types.InputTextMessageContent(
                    message_text=solution_answer
                ),
            )
        ]
    )
