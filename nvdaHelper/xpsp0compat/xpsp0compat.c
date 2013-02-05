/*
This file is a part of the NVDA project.
URL: http://www.nvda-project.org/
Copyright 2006-2013 NVDA contributers.
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License version 2.0, as published by
    the Free Software Foundation.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
This license can be found at:
http://www.gnu.org/licenses/old-licenses/gpl-2.0.html
*/

#include <windows.h>

typedef void*(__stdcall *EncodePointer_funcType)(void*);
EncodePointer_funcType realEncodePointer=NULL;
void* __stdcall fakeEncodePointer(void* ptr) {
	if(!realEncodePointer) {
		HANDLE h=GetModuleHandle(L"KERNEL32.DLL");
		if(h) {
			realEncodePointer=(EncodePointer_funcType)GetProcAddress((HMODULE)h,"EncodePointer");
		}
	}
	if(realEncodePointer) {
		return realEncodePointer(ptr);
	}
	return ptr;
}

typedef void*(__stdcall *DecodePointer_funcType)(void*);
DecodePointer_funcType realDecodePointer=NULL;
void* __stdcall fakeDecodePointer(void* ptr) {
	if(!realDecodePointer) {
		HANDLE h=GetModuleHandle(L"KERNEL32.DLL");
		if(h) {
			realDecodePointer=(DecodePointer_funcType)GetProcAddress((HMODULE)h,"DecodePointer");
		}
	}
	if(realDecodePointer) {
		return realDecodePointer(ptr);
	}
	return ptr;
}
