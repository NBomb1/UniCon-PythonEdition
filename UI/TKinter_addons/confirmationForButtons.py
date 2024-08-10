import tkinter as tk
from functools import partial

funcDict = {}


def functionConfirmation(button: tk.Button, func: callable, wait_time: int, confirmation_time: int):
    """
    :param button: the button that will activate the function
    :param func: what function will we call if called
    :param wait_time: in seconds
    :param confirmation_time: in seconds
    :return: None
    """

    if funcDict.get(func) is None:
        stateBeforeConfirmation = button.cget('state')
        textBeforeConfirmation = button.cget('text')

        funcDict[func] = {'text': textBeforeConfirmation, 'state': stateBeforeConfirmation, 'after': []}
        for i in range(wait_time):
            funcDict[func]['after'].append(
                button.after(
                    i * 1000,
                    partial(button.configure, text=f'Are you sure? {wait_time - i}', state=tk.DISABLED)
                )
            )
        for i in range(confirmation_time):
            funcDict[func]['after'].append(
                button.after(
                    (i + wait_time) * 1000,
                    partial(button.configure, text=f'Confirm {confirmation_time - i}', state=tk.NORMAL)
                )
            )
        # for i in range(wait_time // 1000 + 1):
        #     funcDict[func]['after'].append(
        #         button.after(
        #             i * 1000 + wait_time,
        #             partial(button.configure, text=f'Confirm {(wait_time//1000) - i}', state=tk.NORMAL)
        #         )
        #     )
        funcDict[func]['after'].append(
            button.after((wait_time + confirmation_time) * 1000,
                         lambda: None if funcDict.get(func) is None else button.configure(
                             text=textBeforeConfirmation,
                             state=stateBeforeConfirmation
                            )
                         )

        )
        funcDict[func]['after'].append(
            button.after((wait_time + confirmation_time) * 1000,
                         lambda: None if funcDict.get(func) is None else funcDict.pop(func))
        )
    else:
        for i in funcDict.get(func).get('after'):
            button.after_cancel(i)
        button.configure(state=funcDict.get(func)['state'], text=funcDict.get(func)['text'])
        funcDict.pop(func)
        func()
