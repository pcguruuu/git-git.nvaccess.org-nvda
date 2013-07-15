; Copyright 2010 Steve Gray aka 'Lexikos'
; Modified by Michael Curran <mick@kulgan.net>
;   Permission is granted to use and/or redistribute this code without restriction.
;
; Visual C++ 2010 ordinarily creates a dependency on EncodePointer and DecodePointer,
; which means XP SP2 or later is required to run the executable.  Assembling this file
; and linking the result into the application prevents this dependency at the expense
; of any added security those two functions might've provided.
;
; Note that there are two alternative approaches:
;
;  1) Compile a lib containing the two functions and link that ahead of kernel32.lib.
;     This requires the use of the /FORCE:MULTIPLE linker option, which is not ideal.
;
;  2) Compile a dll containing the two functions and use that.  This doesn't seem to
;     have the same 'multiply defined symbols' problem as #1, but means that the exe
;     won't run on *any* OS without a copy of the dll.
;

.686p
.model flat

.code
extrn _fakeEncodePointer@4 : PROC
extrn _fakeDecodePointer@4 : PROC
; Override dll import symbols:
__imp__EncodePointer@4 DWORD _fakeEncodePointer@4
__imp__DecodePointer@4 DWORD _fakeDecodePointer@4
public __imp__EncodePointer@4
public __imp__DecodePointer@4
end