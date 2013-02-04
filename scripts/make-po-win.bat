@echo off
echo Generating file list..
dir ..\capsnavigator\*.py /L /B /S > %TEMP%\listfile.txt
echo Generating .POT file...
xgettext --from-code utf-8  -o messages.po -L Python --no-wrap --no-location -D ..\capsnavigator -f %TEMP%\listfile.txt
echo Done.
del %TEMP%\listfile.txt