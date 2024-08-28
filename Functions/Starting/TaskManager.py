import getpass
import traceback
from os import getcwd
from threading import Thread

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
import pythoncom


TASK_NAME = "Unicon auto-starting. Task scheduler"


def __create_task(showException=True, status=True, applyForThisUser=False) -> bool:
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
        # logon_trigger = scheduler.Create(win32com.client.constants.TaskEventTrigger_Logon)
        logon_trigger = triggers.Create(11)
        # print(logon_trigger)
        # print(logon_trigger.__dict__)
        # # logon_trigger = scheduler.CreateTrigger(1)
        logon_trigger.StartBoundary = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        logon_trigger.UserId = getpass.getuser() if applyForThisUser else ''

        # logon_trigger2 = triggers.Create(11)
        # logon_trigger2.StartBoundary = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        # logon_trigger2.UserId = ''
        # logon_trigger2.UserId = getpass.getuser()

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
        print(traceback.format_exc())
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
        pythoncom.CoInitialize()
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
        pythoncom.CoInitialize()
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


def get_task_user_applied() -> str | None:
    try:
        pythoncom.CoInitialize()
        scheduler = win32com.client.Dispatch("Schedule.Service")
        scheduler.Connect()
        root_folder = scheduler.GetFolder("\\")
        try:
            task = root_folder.GetTask(TASK_NAME)
            triggers = task.Definition.Triggers
            logon_trigger = triggers.Item(1)  # Индексация начинается с 1
            return logon_trigger.UserId
        except Exception:
            return None
    except Exception as e:
        messagebox.showerror('Error', f"Could not check task trigger settings. Exception:{e}")
        raise e


def set_task_user_applied(state: bool):
    try:
        pythoncom.CoInitialize()
        scheduler = win32com.client.Dispatch("Schedule.Service")
        scheduler.Connect()
        root_folder = scheduler.GetFolder("\\")
        task = root_folder.GetTask(TASK_NAME)
        triggers = task.Definition.Triggers

        # logon_trigger = triggers.Remove(1)  # Индексация начинается с 1
        logon_trigger = triggers.Item(1)  # Индексация начинается с 1
        # print(logon_trigger.UserId, 123)
        logon_trigger.UserId = ''
        # # logon_trigger.Enabled = state
        # print('logon\n', dir(logon_trigger))
        # print('triggers', dir(triggers))
        # print('task', dir(task))

        # logon_trigger = triggers.Create(11)
        # logon_trigger.StartBoundary = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        # logon_trigger.UserId = getpass.getuser() if state else ''
        removeTask()
        root_folder.RegisterTaskDefinition(
            TASK_NAME,
            task.Definition,
            6,  # TASK_CREATE_OR_UPDATE
            None,
            None,
            3,  # LOGON_INTERACTIVE_TOKEN
            None
        )
    except Exception as e:
        messagebox.showerror('Error', f"Couldn't change the task status. Exception:\n{e}")
        raise e


def saveTaskSettings(applyForThisUser: CheckButton, checkWidget: CheckButton):
    def thread():

        if disable:
            if checkWidget.v.get():
                checkWidget.v.set(False)
                messagebox.showerror('Error', "You cannot use this option because pywin32 is not installed.")
                return
        # print(get_task_user_applied())
        # print(
        #     is_task_exist() and applyForThisUser.v.get() != bool(get_task_user_applied()),
        #     is_task_exist(),
        #     applyForThisUser.v.get() != bool(get_task_user_applied()),
        #     applyForThisUser.v.get(), bool(get_task_user_applied()), get_task_user_applied()
        # )
        # if is_task_exist() and applyForThisUser.v.get() != bool(get_task_user_applied()):
        #     set_task_user_applied(applyForThisUser.v.get())
        # TODO: remove this peace of misunderstanding code after next update
        state = checkWidget.v.get()  # check this code again 1
        checkWidget.v.set(True)  # check this code again 1
        if is_task_exist() and applyForThisUser.v.get() != bool(get_task_user_applied()):
            removeTask()

        # if checkWidget.v.get():
        try:
            if not is_task_exist():
                try:
                    __create_task(applyForThisUser=applyForThisUser.v.get())
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
        # else:
        checkWidget.v.set(state)  # check this code again 1
        if not state:
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
    a = Thread(target=thread, daemon=True)
    a.start()


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
    def thread():
        if not isAdmin:
            return
        if is_task_exist():
            status = is_task_enabled()
            username = bool(get_task_user_applied())
            removeTask()
            __create_task(applyForThisUser=username)
            setTaskStatus(status)
    Thread(target=thread, daemon=True).start()
