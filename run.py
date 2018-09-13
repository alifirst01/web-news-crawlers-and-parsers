import os
import time
import threading
import datetime
from Scripts import send_dawn, send_tribune, send_thenews, send_nation, send_pakistantoday, send_dailytimes, \
    send_businessrecorder, send_pakistanobserver, send_newsweek, send_frontier, send_fridaytimes, send_herald

def main():

    MINUTES = 30

    if not os.path.exists('Htmls'):
        os.mkdir('Htmls')
    if not os.path.exists('Jsons'):
        os.mkdir('Jsons')

    while True:
        print('\n\n\nCurrent Time:', datetime.datetime.now(), '\n')
        dawn_thread = threading.Thread(target=send_dawn.worker)
        tribune_thread = threading.Thread(target=send_tribune.worker)
        thenews_thread = threading.Thread(target=send_thenews.worker)
        nation_thread = threading.Thread(target=send_nation.worker)
        pktoday_thread = threading.Thread(target=send_pakistantoday.worker)
        dailytimes = threading.Thread(target=send_dailytimes.worker)
        brecorder_thread = threading.Thread(target=send_businessrecorder.worker)
        pkoberver_thread = threading.Thread(target=send_pakistanobserver.worker)
        newsweek_thread = threading.Thread(target=send_newsweek.worker)
        frontierpost_thread = threading.Thread(target=send_frontier.worker)
        fridaytimes_thread = threading.Thread(target=send_fridaytimes.worker)
        herald_thread = threading.Thread(target=send_herald.worker)

        dawn_thread.start()
        tribune_thread.start()
        thenews_thread.start()
        nation_thread.start()
        pktoday_thread.start()
        dailytimes.start()
        brecorder_thread.start()
        pkoberver_thread.start()
        newsweek_thread.start()
        frontierpost_thread.start()
        fridaytimes_thread.start()
        herald_thread.start()

        time.sleep(MINUTES * 60)


if __name__ == '__main__':
    exit(main())