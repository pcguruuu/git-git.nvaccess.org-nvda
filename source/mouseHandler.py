#mouseHandler.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import time
import tones
import ctypes
import winUser
import queueHandler
import api
import screenBitmap
import speech
import globalVars
import eventHandler
from logHandler import log
import config
import winInputHook
import core
import screenExplorer

WM_MOUSEMOVE=0x0200
WM_LBUTTONDOWN=0x0201
WM_LBUTTONUP=0x0202
WM_LBUTTONDBLCLK=0x0203
WM_RBUTTONDOWN=0x0204
WM_RBUTTONUP=0x0205
WM_RBUTTONDBLCLK=0x0206

curMousePos=(0,0)
mouseMoved=False
curMouseShape=""
mouseShapeChanged=0
scrBmpObj=None
#: The time (in seconds) at which the last mouse event occurred.
#: @type: float
lastMouseEventTime=0

def updateMouseShape(name):
	global curMouseShape, mouseShapeChanged
	if not name or name==curMouseShape:
		return
	curMouseShape=name
	mouseShapeChanged=1

#Internal mouse event

def internal_mouseEvent(msg,x,y,injected):
	global mouseMoved, curMousePos, lastMouseEventTime
	lastMouseEventTime=time.time()
	if injected:
		return True
	if not config.conf['mouse']['enableMouseTracking']:
		return True
	try:
		curMousePos=(x,y)
		if msg==WM_MOUSEMOVE: 
			mouseMoved=True
			core.requestPump()
		elif msg in (WM_LBUTTONDOWN,WM_RBUTTONDOWN):
			queueHandler.queueFunction(queueHandler.eventQueue,speech.cancelSpeech)
	except:
		log.error("", exc_info=True)
	return True

def executeMouseMoveEvent(x,y):
	global currentMouseWindow
	desktopObject=api.getDesktopObject()
	screenLeft,screenTop,screenWidth,screenHeight=desktopObject.location
	x=min(max(screenLeft,x),(screenLeft+screenWidth)-1)
	y=min(max(screenTop,y),(screenTop+screenHeight)-1)
	if config.conf["mouse"]["audioCoordinatesOnMouseMove"]:
		screenExplorer.playLocationCoordinates(x,y,screenWidth,screenHeight,config.conf['mouse']['audioCoordinates_detectBrightness'],config.conf['mouse']['audioCoordinates_blurFactor'])
	oldMouseObject=api.getMouseObject()
	mouseObject=desktopObject.objectFromPoint(x,y)
	while mouseObject and mouseObject.beTransparentToMouse:
		mouseObject=mouseObject.parent
	if not mouseObject:
		return
	if oldMouseObject==mouseObject:
		mouseObject=oldMouseObject
	else:
		api.setMouseObject(mouseObject)
	try:
		eventHandler.executeEvent("mouseMove",mouseObject,x=x,y=y)
		oldMouseObject=mouseObject
	except:
		log.error("api.notifyMouseMoved", exc_info=True)

#Register internal mouse event

def initialize():
	global curMousePos, scrBmpObj
	scrBmpObj=screenBitmap.ScreenBitmap(1,1)
	(x,y)=winUser.getCursorPos()
	desktopObject=api.getDesktopObject()
	try:
		mouseObject=desktopObject.objectFromPoint(x,y)
	except:
		log.exception("Error retrieving initial mouse object")
		mouseObject=None
	if not mouseObject:
		mouseObject=api.getDesktopObject()
	api.setMouseObject(mouseObject)
	curMousePos=(x,y)
	winInputHook.initialize()
	winInputHook.setCallbacks(mouse=internal_mouseEvent)

def pumpAll():
	global mouseMoved, curMousePos, mouseShapeChanged, curMouseShape
	if mouseMoved:
		mouseMoved=False
		(x,y)=curMousePos
		executeMouseMoveEvent(x,y)
	if config.conf["mouse"]["reportMouseShapeChanges"] and mouseShapeChanged>0:
		if mouseShapeChanged==10:
			mouseShapeChanged=0
			# Translators: Reported when mouse cursor shape changes (example output: edit cursor).
			speech.speakMessage(_("%s cursor")%curMouseShape)
		else:
			mouseShapeChanged+=1

def terminate():
	global scrBmpObj
	scrBmpObj=None
	winInputHook.terminate()
