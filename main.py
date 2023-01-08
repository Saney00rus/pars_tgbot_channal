import time
import telebot
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from botset import token

driver = webdriver.Chrome()


def parsbot():
    bot.send_message(chat_me, '✅Успешный запуск бота на канале!')
    history = []
    options = Options()
    options.add_extension("extension_5_3_2_0.crx")
    s = Service('chromedriver.exe')
    global driver
    driver = webdriver.Chrome(service=s, options=options)
    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "eager"

    driver.get('https://www.google.ru/')
    driver.switch_to.window(driver.window_handles[1])
    driver.close()
    driver.switch_to.window(driver.window_handles[0])


    def avito():
        cont = True
        avito_link = 'https://www.avito.ru/moskva/avtomobili?f=ASgCAgECAUXGmgwWeyJmcm9tIjowLCJ0byI6MjMwMDAwfQ&radius' \
                     '=300&s=104 '
        x = 1
        while cont == True:
            y = str(x)
            href = f"/html/body/div[1]/div/div[3]/div[2]/div[3]/div[3]/div[3]/div[2]/div[{y}]/div/div[2]/div[2]/a"
            try:
                time.sleep(3)
                driver.get(avito_link)
            except Exception:
                print('Ошибка... (avito_link)')
                print('Restart bot...')
                parsbot()

            try:
                link = driver.find_element(By.XPATH, href).get_attribute("href")
            except Exception:
                print('Ошибка...(link)')
                avito()
            else:
                time.sleep(3)
                driver.get(link)
                if link not in history:
                    cont = True
                else:
                    print("Повторное объявление, обновляю поиск...")
                    avito()
                try:
                    price = driver.find_element(By.XPATH,
                                                '/html/body/div[1]/div/div[2]/div/div[3]/div[3]/div[1]/div[2]/div['
                                                '2]/div/div/div[1]/span').text
                except Exception:
                    price = " - Рынок не определен"
                    print(link, price)
                    driver.back()
                else:
                    if "цена ниже рыночной" in price:
                        try:
                            mid_price = driver.find_element(By.XPATH,
                                                            '/html/body/div[1]/div/div[2]/div/div[3]/div[3]/div[1]/div['
                                                            '2]/div[2]/div/div/div[1]/div[1]/div/div[2]/span[2]').text
                        except Exception:
                            print("Ошибка... (mid_price)")
                            avito()
                        try:
                            title = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/div[3]/div[3]/div['
                                                                  '1]/div[1]/div/div[1]/h1/span').text
                        except Exception:
                            print("Ошибка... (title)")
                            avito()
                        try:
                            car_price = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/div[3]/div['
                                                                      '3]/div[2]/div[1]/div/div/div[1]/div/div[1]/div['
                                                                      '1]/div/span/span/span[1]').text
                        except Exception:
                            print("Ошибка... (car_price)")
                            avito()
                        try:
                            city = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/div[3]/div[3]/div['
                                                                 '1]/div[2]/div[4]/div/div[2]/div[1]/div/span').text
                        except Exception:
                            print("Ошибка... (sity)")
                            avito()
                        try:
                            gen = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/div[3]/div[3]/div['
                                                                '1]/div[2]/div[1]/div[3]/div/ul/li[2]/a').text
                        except Exception:
                            gen = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/div[3]/div[3]/div['
                                                                '1]/div[2]/div[1]/div[2]/div/ul/li[2]/a').text
                        print("!!! ", link, " - ", price)
                        good_price = "🚗 " + title + " 🚗 \n" + "🚘 Поколение: " + gen + " 🚘 \n" + "💰 Цена: " + car_price + " ₽ " + " 💰 \n" + "📊 Рынок: " + mid_price + " 📊 \n" + "📌 Город: " + city + " 📌 \n" + "🔗 " + link
                        send_gp = good_price
                        bot.send_message(chat_id, send_gp)
                        driver.back()
                    else:
                        print(link, " - ", price)
                        driver.back()
                history.append(link)
            x += 1
        a = 0
        if a < 5:
            a += 1
        else:
            avito()
    avito()


if __name__ == '__main__':
    bot = telebot.TeleBot(token)
    chat_me = '167749311'  # Мой
    # chat_id = '-1001857902932' # Тестовый
    chat_id = '-1001807362385' # Канал
    bot.send_message(chat_id, 'Бот запущен!')
    print("_____Bot is running_____")
    while True:
        try:
            parsbot()
        except Exception as e:
            print('Fatal error... restart bot...')
            print(e)
            bot.send_message(chat_me, f'⚠При работе бота произошла ошибка: \n {e}')
            driver.quit()
            continue