import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from flask import Flask, request

TOKEN = '6241086649:AAGYrmGqayufsZ5R-xGuXPRnbjWya0RhYL0'
ADMIN_CHAT_ID = '5039206995'  # Replace with the admin chat ID
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Create Flask app
app = Flask(__name__)

# Bot logic: Define command handlers and callback handlers here
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user = message.from_user
    await message.answer(f"Hi {user.username}! Here is where you can make payments for Legendary Predict VIP/PREMIUM SUBSCRIPTION.")
    await message.answer("Please select your country of origin.")
    options = [
        'Europe',
        'North America',
        'Australia',
        'South America',
        'Asia',
        'Russia/Ukraine',
        'Africa'
    ]
    await message.answer_poll("Which country do you come from?", options=options, is_anonymous=False)

# Define your callback handler for processing poll updates
@dp.poll_answer_handler()
async def process_poll(poll_answer: types.PollAnswer):
    selected_option = poll_answer.option_ids[0]
    if selected_option in (0, 1, 2, 3, 4):  # Europe, North America, Australia, South America, Asia
        payment_info = '''
        40 euros one month.
        43 USD one month.

        Pay with PayPal or
        Pay with Bitcoin/Binance

        PayPal:
        zoebeaney22@gmail.com

        Friends and Family ONLY
        Send an exact amount of 40 Euros.
        A screenshot with the name zoebeaney22@gmail.com is needed.

        Bitcoin/Binance:

        Binance/Bitcoin ID: 186630865

        Binance/Bitcoin Address: 1D4N7h55M1NMSy9wM63NMzJHEtEB1EZSgw

        Bitcoin/Binance TRC20 Address: TNqvvZyUXZNHgyBDNXeiwCr5xoSSewXF4e

        Send a screenshot when the payment is made.
        '''
    elif selected_option == 5:  # Russia/Ukraine
        payment_info = '''
        Russia/Ukraine

        Contact https://t.me/L_predicttbot
        And make payments there.
        '''
    elif selected_option == 6:  # Africa
        await bot.send_message(chat_id=poll_answer.user.id, text="🌍 Africa 🌍\nWhat country are you from?")
        options = [
            '🇰🇪 🇺🇬 🇹🇿 🇿🇲 🇷🇼',
            '🇳🇬 🇬🇭 🇿🇦',
            '🇧🇯 🇧🇫 🇨🇮 🇲🇱 🇳🇪 🇹🇬',
            '🇨🇲'
        ]
        await bot.send_poll(chat_id=poll_answer.user.id, question="Select your country", options=options, is_anonymous=False)
        return

    await bot.send_message(chat_id=poll_answer.user.id, text=payment_info)

@dp.poll_answer_handler()
async def process_sub_poll(poll_answer: types.PollAnswer):
    selected_sub_option = poll_answer.option_ids[0]
    if selected_sub_option == 1:  # User selected the first option in the sub-poll
        payment_info = '''
        🇰🇪: 4,500 Kenyan shillings one month
            🇺🇬: 120,000 Ugandan Shillings one month
            🇹🇿: 105,180.27 Tanzanian Shilling one month
            🇿🇲: 615 Zambian Kwacha one month
            🇷🇼: 50,118.81 Rwandan Franc

            +254731357381-ELVIS
            +254112549205-ELVIS

            Any can be used, send a screenshot after payment
        '''
        await bot.send_message(chat_id=poll_answer.user.id, text=payment_info)
    elif selected_sub_option == 2:  # User selected the second option in the sub-poll
        payment_info = '''
        🇳🇬: 15,000 Naira one month
            🇬🇭: 365 Cedis one month
            🇿🇦: 816.83 South African Rand one month

            🇳🇬 Payment:
            8137946750
            Opay
            Dada

            Any amount less than 15,000 Naira will not be accepted, send a screenshot of FRANCA Ifeyinwa DADA name showing

            🇬🇭 Payments
            MTN GHANA
            NUMBER: 0257131767
            NAME: JUSTICE MANFUL

            Any amount less than 365 cedis will not be accepted, send a screenshot for confirmation
        '''
        await bot.send_message(chat_id=poll_answer.user.id, text=payment_info)
    elif selected_sub_option == 4:  # User selected the fourth option in the sub-poll
        payment_info = '''
        🇨🇲 Payments:

            UPDATED ✅ ✅ ✅ ✅

            MTN CAMEROON

            ✨ Mobile Money Transfers For 👇

            👉 Nchad
            👉 Gabon
            👉 Cameroon
            👉 Congo brazzaville
            👉 Equitorial guinea
            👉 International Ria money

            Mtn No. +237 676403589

            Name Of Receiver: Eva Harris

            Send a screenshot after payment
        '''
        await bot.send_message(chat_id=poll_answer.user.id, text=payment_info)


@dp.message_handler(content_types=['photo'])
async def process_screenshot(message: types.Message):
    # Send screenshot to admin Telegram account
    user = message.from_user
    screenshot = message.photo[-1]  # Retrieve the last photo sent by the user
    caption = f"New screenshot from user: {user.username}"
    await bot.send_photo(chat_id=ADMIN_CHAT_ID, photo=screenshot.file_id, caption=caption)



# Flask route for handling incoming messages from Telegram
@app.route('/your-bot-endpoint', methods=['POST'])
async def handle_bot_request():
    # Retrieve the incoming message data from Telegram
    update_data = await request.get_json()

    # Process the update
    await dp.process_update(update_data)

    # Return a response (optional)
    return {'status': 'success'}

# Start the Flask app
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(dp.start_polling())
    app.run()
