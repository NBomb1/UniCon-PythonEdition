from os import getcwd

from UI.TKinter_addons.Tools.DataSettings.Widgets.checkWidget import CheckButton

disable = False
isAdmin = False
try:
    import win32com.client
    import pyuac

    isAdmin = pyuac.isUserAdmin()
except ImportError:
    disable = True
import sys
from datetime import datetime
from tkinter import messagebox

TASK_NAME = "Unicon auto-starting. Task scheduler"


def __create_task(showException=True, status=True) -> bool:
    try:
        if not isAdmin:
            return False
        mainScript = '\\main.py'
        task_description = "Runs Python script."
        script_path = f""""{getcwd() + mainScript}" """  # Полный путь к вашему скрипту

        # Создаем объект COM
        scheduler = win32com.client.Dispatch("Schedule.Service")
        scheduler.Connect()

        root_folder = scheduler.GetFolder("\\")

        # Удаляем задачу, если она уже существует
        # try:
        #     root_folder.DeleteTask(TASK_NAME, 0)
        # except Exception as e:
        #     if showException:
        #         print(f"Failed to delete existing task: {e}")

        # Создаем новую задачу
        task_def = scheduler.NewTask(0)

        # Настраиваем параметры задачи
        task_def.RegistrationInfo.Description = task_description
        task_def.RegistrationInfo.Author = "ArT"

        # Настраиваем триггеры задачи
        triggers = task_def.Triggers

        # # Пример триггера для запуска при входе в систему
        # logon_trigger = triggers.Create(1)  # 1 = TASK_TRIGGER_LOGON
        # logon_trigger.StartBoundary = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        #
        # # Пример триггера для запуска при входе в систему
        # logon_trigger = triggers.Create(11)  # 1 = TASK_TRIGGER_LOGON
        # logon_trigger.StartBoundary = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

        # Пример триггера для запуска при запуске компьютера
        boot_trigger = triggers.Create(8)  # 8 = TASK_TRIGGER_BOOT
        boot_trigger.StartBoundary = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        #
        # # Пример триггера для запуска в определенное время
        # time_trigger = triggers.Create(1)  # 1 = TASK_TRIGGER_TIME
        # time_trigger.StartBoundary = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        #
        # # Пример триггера для периодического запуска
        # daily_trigger = triggers.Create(2)  # 2 = TASK_TRIGGER_DAILY
        # daily_trigger.DaysInterval = 1  # Каждый день
        # daily_trigger.StartBoundary = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

        # Настраиваем действия задачи
        actions = task_def.Actions
        exec_action = actions.Create(0)  # 0 = TASK_ACTION_EXEC
        exec_action.Path = sys.executable  # Путь к интерпретатору Python
        exec_action.Arguments = f'{script_path}'  # Путь к вашему скрипту

        # Настраиваем параметры задачи
        settings = task_def.Settings
        settings.Enabled = True
        settings.StartWhenAvailable = True
        settings.Hidden = False
        settings.AllowDemandStart = True
        settings.RunOnlyIfIdle = False
        settings.DisallowStartIfOnBatteries = False
        settings.StopIfGoingOnBatteries = False
        settings.ExecutionTimeLimit = "PT0S"  # Без ограничения по времени
        settings.MultipleInstances = 1  # 1 = Запускать новый экземпляр (TASK_INSTANCES_PARALLEL)

        # Включаем журналирование
        task_def.Principal.LogonType = 3  # 3 = LOGON_INTERACTIVE_TOKEN
        task_def.Settings.Enabled = status
        task_def.Settings.AllowHardTerminate = True

        # Настраиваем запуск от имени администратора
        task_def.Principal.RunLevel = 1  # 1 = TASK_RUNLEVEL_HIGHEST

        # Регистрация задачи
        root_folder.RegisterTaskDefinition(
            TASK_NAME,
            task_def,
            6,  # 6 = TASK_CREATE_OR_UPDATE
            None,
            None,
            3,  # 3 = LOGON_INTERACTIVE_TOKEN
            None,
        )
        return True
    except Exception as e:
        if showException:
            messagebox.showerror('Error', f'Error creating task: \n{e}\n'
                                          f'Try installing pywin32.')
        return False


def removeTask():
    try:
        scheduler = win32com.client.Dispatch("Schedule.Service")
        scheduler.Connect()

        root_folder = scheduler.GetFolder("\\")
        root_folder.DeleteTask(TASK_NAME, 0)
    except Exception as e:
        messagebox.showerror('Error', f"Could not remove the task. Exception:\n{e}")
        raise e


def is_task_exist():
    try:
        scheduler = win32com.client.Dispatch("Schedule.Service")
        scheduler.Connect()
        root_folder = scheduler.GetFolder("\\")
        try:
            root_folder.GetTask(TASK_NAME)
            return True
        except Exception:
            return False
    except Exception as e:
        messagebox.showerror('Error', f"Could not check task existence. Exception:\n{e}")
        raise e


def is_task_enabled():
    try:
        scheduler = win32com.client.Dispatch("Schedule.Service")
        scheduler.Connect()
        root_folder = scheduler.GetFolder("\\")
        try:
            task = root_folder.GetTask(TASK_NAME)
            return task.Enabled
        except Exception:
            return False
    except Exception as e:
        messagebox.showerror('Error', f"Could not check task status. Exception:{e}")
        raise e


def saveTaskSettings(checkWidget: CheckButton):
    if disable:
        if checkWidget.savedData:
            checkWidget.v.set(False)
            messagebox.showerror('Error', "You cannot use this option because pywin32 is not installed.")
            return

    if checkWidget.savedData:
        try:
            if not is_task_exist():
                try:
                    __create_task()
                except Exception as e:
                    checkWidget.v.set(False)
                    messagebox.showerror('Error', f"Couldn't create the task. Exception:\n{e}")
            else:
                if not is_task_enabled():
                    try:
                        setTaskStatus(True)
                    except Exception as e:
                        messagebox.showerror('Error', f"Couldn't change the task status. Exception:\n{e}")
        except Exception as e:
            messagebox.showerror('Error', f"Couldn't check the task. Exception:\n{e}")
            checkWidget.v.set(False)
    else:
        try:
            if is_task_exist():
                try:
                    setTaskStatus(False)
                except Exception as e:
                    messagebox.showerror('Error', f"Couldn't change the task status. Exception:\n{e}")
                    checkWidget.v.set(True)
        except Exception as e:
            messagebox.showerror('Error', f"Couldn't check the task. Exception:\n{e}")
            checkWidget.v.set(True)


def checkImport(showMessage=True, message=None) -> bool:
    if disable:
        if showMessage:
            assert message is not None, 'CheckImport message is required'
            messagebox.showerror('Error', message)
        return False
    return True


def setTaskStatus(state: bool):
    try:
        scheduler = win32com.client.Dispatch("Schedule.Service")
        scheduler.Connect()
        root_folder = scheduler.GetFolder("\\")
        task = root_folder.GetTask(TASK_NAME)
        task.Enabled = state
    except Exception as e:
        messagebox.showerror('Error', f"Couldn't change the task status. Exception:\n{e}")
        raise e


def afterUpdate():
    if not isAdmin:
        return
    status = is_task_enabled()
    removeTask()
    __create_task()
    setTaskStatus(status)

# if __name__ == '__main__':
#     if
