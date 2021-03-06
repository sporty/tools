@echo off

rem 引数チェック
if "%1"=="" goto input_error
if "%2"=="" goto input_error
if not "%3"=="" goto input_error
if "%1"=="%2" goto input_error

set filename="C:\diff_view_result.diff"
set diff_program="C:\msys\1.0\bin\diff.exe"
set editor_program="C:\Program Files\vim\gvim.exe"

rem perforceカスタムツール対応
rem （ディレクトリ名が...付きで渡される）
set target_a=%1
if "%target_a:~-3%"=="..." (
	set target_a=%target_a:~0,-3%
)
set target_b=%2
if "%target_b:~-3%"=="..." (
	set target_b=%target_b:~0,-3%
)

rem 実行
echo 以下の差分をサブディレクトリごととり、エディタで表示します
echo ----------
echo %target_a%
echo %target_b%
echo ----------

%diff_program% -r %target_a% %target_b% > %filename%
if %ERRORLEVEL%==2 goto error
%editor_program% %filename%
if not %ERRORLEVEL%==0 goto error

goto end

:error
echo エラーが発生しました
pause
goto end

:input_error
echo 入力エラー
echo %0 ディレクトリA ディレクトリB
echo と実行してください
pause
goto end

:end
