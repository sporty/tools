@echo off

rem �����`�F�b�N
if "%1"=="" goto input_error
if "%2"=="" goto input_error
if not "%3"=="" goto input_error
if "%1"=="%2" goto input_error

set filename="C:\diff_view_result.diff"
set diff_program="C:\msys\1.0\bin\diff.exe"
set editor_program="C:\Program Files\vim\gvim.exe"

rem perforce�J�X�^���c�[���Ή�
rem �i�f�B���N�g������...�t���œn�����j
set target_a=%1
if "%target_a:~-3%"=="..." (
	set target_a=%target_a:~0,-3%
)
set target_b=%2
if "%target_b:~-3%"=="..." (
	set target_b=%target_b:~0,-3%
)

rem ���s
echo %target_a%��%target_b%�̍������T�u�f�B���N�g�����ƂƂ�A�G�f�B�^�ŕ\�����܂�

%diff_program% -r %target_a% %target_b% > %filename%
%editor_program% %filename%

if not %ERRORLEVEL%==0 goto error
goto end

:error
echo �G���[���������܂���
pause
goto end

:input_error
echo ���̓G���[
echo %0 �f�B���N�g��A �f�B���N�g��B
echo �Ǝ��s���Ă�������
pause
goto end

:end