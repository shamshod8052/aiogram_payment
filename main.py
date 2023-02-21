import config
import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ContentType

# log
logging.basicConfig(level=logging.INFO)

#init
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)

#prices
PRICE = types.LabeledPrice(label='Subscribe', amount=1000 * 100) # amont need be in cents!

# buy
@dp.message_handler(commands=["buy"])
async def buy(message: types.Message):
  if config.PAYMENTS_TOKEN.split(':')[1] == 'TEST':
    await bot.send_message(message.chat.id, "Test payment!")

    await bot.send_invoice(
      message.chat.id,
      title="Subscribe",
      description="Simple description",
      provider_token=config.PAYMENTS_TOKEN,
      currency="uzs", # Yiu can use USD (dollars),
      photo_url="https://www.aroged.com/wp-content/uploads/2022/06/Telegram-has-a-premium-subscription.jpg",
      photo_width=416,
      photo_height=234,
      photo_size=416,
      is_flexible=False,
      prices=[PRICE],
      start_parameter="one-month-subcription" ,
      payload="test-invoice-payload"
    )

# pre checkout (must be answered in 10 seconds)
@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
  await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)

#successful payment
@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
  print("SUCCESSFUL PAYMENT:")
  payment_info = message.successful_payment.to_python()
  for key, value in payment_info.items():
    print(f"{key} = {value}")

  await bot.send_message(message.chat.id, f"Payment for the amount {message.successful_payment.total_amount // 100} {message.successful_payment.currency} passed successfuly!!!")

# run long-polling
if __name__ == "__main__":
  executor.start_polling(dp, skip_updates=False)