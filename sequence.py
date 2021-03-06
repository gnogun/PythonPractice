import pyautogui
import time
import win32clipboard
import webbrowser
import eventManager
from collections import deque

import os.path
from bs4 import BeautifulSoup

class sequence:
    def __init__(self, startXy, eventType, endXy, text, _url, command, delayTime, actionType, pinList):
        # print(eventType)

        self.eventType = eventType
        self.startXy = startXy
        self.endXy = endXy
        self.text = text
        self._url = _url
        self.command = command
        self.delayTime = delayTime
        self.actionType = actionType
        self.pinList = pinList

        # if eventType == 'click':
        #     self.mouseDown(startXy)
        # elif eventType == 'drag':
        #     self.mouseDrag(startXy, endXy)
        # elif eventType == 'text':
        #     self.textTypo(text)
        # elif eventType == 'hotkey':
        #     if command == 'copy':
        #         self.commandCopy()
        #     elif command == 'paste':
        #         self.commandPaste()
        #     else:
        #         print('{} 는 단축 명령이 아님'.format(command))
        # else:
        #     print('{} 는 이벤트 타입이 아님'.format(eventType))

    def mouseDown(self, startXy):
        # print(startXy)

        data = startXy.split(',')

        pyautogui.click(x=int(data[0]), y=int(data[1]))
        

    def mouseDrag(self, startXy, endXy):
        # print(startXy)
        # print(endXy)

        data = startXy.split(',')
        data2 = endXy.split(',')

        pyautogui.click(x=int(data[0]), y=int(data[1]))
        pyautogui.dragTo(x=int(data2[0]), y=int(data2[1]), duration=1, button='left')
    
    def textTypo(self, text):
        # print(text)
        # win32clipboard.OpenClipboard()
        # win32clipboard.EmptyClipboard()
        # win32clipboard.SetClipboardText(text, win32clipboard.CF_TEXT)
        # win32clipboard.CloseClipboard()

        # pyautogui.hotkey('ctrl', 'v')

        pyautogui.write(text, interval=0.1)

    def commandCopy(self):
        pyautogui.hotkey('ctrl', 'c')

    def commandPaste(self):
        pyautogui.hotkey('ctrl', 'v')

    def commandClose(self):
        pyautogui.hotkey('alt', 'f4')

    def mouseMove(self, startXy):
        data = startXy.split(',')
        pyautogui.moveTo(x=int(data[0]), y=int(data[1]), duration=1)

    def cultureLoggingResult(self):
        # win32clipboard.OpenClipboard()
        # resultString = win32clipboard.GetClipboardData()
        # win32clipboard.EmptyClipboard()
        # win32clipboard.CloseClipboard()

        # resultString = resultString.replace('null')
        # resultString = resultString.replace('추가 충전하기다 쓴 문상이벤트 바로가기')

        # print(resultString)

        fileExist = os.path.isfile('C:/Users/gnogu/OneDrive/Documents/culture.htm')

        pyautogui.hotkey('ctrl', 's')

        time.sleep(1)

        pyautogui.write('culture.htm', interval=0.1)

        time.sleep(1)

        pyautogui.press('tab')

        time.sleep(1)

        pyautogui.press('down')

        time.sleep(1)

        pyautogui.press('down')

        time.sleep(1)

        pyautogui.press('down')

        time.sleep(1)

        pyautogui.press('enter')

        time.sleep(1)

        pyautogui.press('enter')

        if fileExist:
            time.sleep(1)
            pyautogui.press('left')
            time.sleep(1)
            pyautogui.press('enter')

        time.sleep(5)

        f = open("C:/Users/gnogu/OneDrive/Documents/culture.htm", 'r', encoding='UTF8')
        data = f.read()

        soup = BeautifulSoup(data, 'html.parser')

        name = soup.select('#contents > div.contents > div.section.sec-form > div > div.article > table > tbody')

        resultString = name[0].text

        print(resultString)

        logFile = open('log.txt', 'a', encoding='utf-8')
        logFile.write(resultString)
        logFile.close

    def happyLoggingResult(self):
        win32clipboard.OpenClipboard()
        resultString = win32clipboard.GetClipboardData()
        win32clipboard.EmptyClipboard()
        win32clipboard.CloseClipboard()

        resultString = resultString.replace('null')

        print(resultString)        

    def launch(self, evManager):

        if self.eventType == '클릭':
            self.mouseDown(self.startXy)
        elif self.eventType == '드래그':
            self.mouseDrag(self.startXy, self.endXy)
        elif self.eventType == '텍스트':
            self.textTypo(self.text)
        elif self.eventType == '핫키':
            
            if self.command == 'copy':
                self.commandCopy()
            elif self.command == 'paste':
                self.commandPaste()
            elif self.command == 'close':
                self.commandClose()
        elif self.eventType == '브라우저':
            # webbrowser.open(self._url, new=2)
            iexplore = os.path.join(os.environ.get("PROGRAMFILES", "C:/Program Files"),"Internet Explorer/IEXPLORE.EXE")
            ie = webbrowser.BackgroundBrowser(iexplore)
            ie.open(self._url, new=2)
        elif self.eventType == '이동' or self.eventType == '마우스이동':
            self.mouseMove(self.startXy)
        elif self.eventType == '핀입력':
            self.inputPinCount = 0

            if len(self.pinList) == 0:
                print('out of PIN List')
                evManager.isRun = False

            while len(self.pinList):
                self.inputPinCount += 1

                self.textTypo(self.pinList.popleft())

                if self.inputPinCount == 5:
                    break
        elif self.eventType == '컬쳐결과확인':
            # self.commandCopy()
            self.cultureLoggingResult()
            

            # if len(self.pinList) == 0 and self.inputPinCount != 5:
            #     for i in range(5 - self.inputPinCount):
            #         self.textTypo('000000000000000000')
        elif self.eventType == '해피결과확인':

            self.happyLoggingResult()

        time.sleep(int(self.delayTime))