#!/usr/bin/env python3

from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from datetime import datetime, time
from time import sleep
from playsound import playsound
from gtts import gTTS
import notify2 as notify
import schedule
import os

anime_episodes = set()

def anime_notifier():
	req = Request("https://otakustream.tv/api/feed.php", headers={"User-Agent":"Mozilla/5.0"})
	html = urlopen(req)
	soup = BeautifulSoup(html, "xml")

	global anime_episodes

	if datetime.now().time() > time(23, 00):
		anime_episodes.clear()

	try:
		items = soup.find_all("item")
		notify.init("Anime Updates")
		ICON_PATH = os.path.join(os.getcwd(), "sabergohan.jpg")

		if os.path.exists(ICON_PATH):
			notice = notify.Notification(None, icon=ICON_PATH)
		else:
			ICON_PATH = os.path.join(os.getcwd(), "Desktop", "otaku_stream_rss_reader", "sabergohan.jpg")
			notice = notify.Notification(None, icon=ICON_PATH)

		notice.set_urgency(notify.URGENCY_NORMAL)

		for item in items:

			try:
				message = item.find("description").get_text()

				if message not in anime_episodes:
					anime_episodes.add(message)
				else:
					continue

				link = item.find("link").get_text()
				notice.update(f"New episode available at OtakuStream", f"{message}\nLink: {link}")
				notice.show()
				notice.set_timeout(10000)
				print(os.getcwd())

				try:
					playsound("notificationaudio.mp3")
				except:
					AUDIO_PATH = os.path.join(os.getcwd(), "Desktop", "otaku_stream_rss_reader","notificationaudio.mp3")
					playsound(AUDIO_PATH)

				current_time = datetime.now().time()

				if time(7, 30) < current_time:
					speech = gTTS(text=f"{message} is now available at OtakuStream", lang="en")
					SPEECH_PATH = os.path.join(os.getcwd(), "Desktop", "otaku_stream_rss_reader", "voice.mp3")

					if os.path.exists(SPEECH_PATH):
						speech.save(SPEECH_PATH)
						playsound(SPEECH_PATH)
						os.unlink(SPEECH_PATH)

					else:
						speech.save("voice.mp3")
						playsound("voice.mp3")
						os.unlink("voice.mp3")

				sleep(15)

			except Exception  as e:

				print(e)

	except Exception as e:

		print(e)

	finally:
		notice.update(f"Time elapsed", f"{datetime.now()}")
		notice.close()



notify.init("Anime Notifier")
notice = notify.Notification("Initializing Anime Notifier")
notice.set_urgency(notify.URGENCY_NORMAL)
notice.set_timeout(10000)
notice.show()
sleep(3)
notice.close()

schedule.every(2).hours.do(anime_notifier)

while True:
	schedule.run_pending()
	sleep(1)

