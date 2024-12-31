class RequestStates:
    """
    All possible states could be existed.

    All states except -1 and 0 can be set only by server side.
    """

    state_error = -1  # If something went wrong.

    state_initialised = 0  # Internal side.

    state_serverAccepted = 1  # Server handler accepted request and waits for connection.
    state_serverDeclined = 2  # Server handler declined request and will delete it soon.
    state_clientAccepted = 3  # Client handler accepted request (Only works where client is a receiver).
    state_clientDeclined = 4  # Client handler declined request, so request will be deleted soon.

    state_sending = 5  # Updates each time for each file.

    state_completed = 6  # Everything went successfully.
    state_cancelled = 7  # Client or server cancelled file transferring.

    state_timed_out_client_response = 8  # Client didn't answer request.

    states_dict_int_to_str = {
        -1: "state_error",
        0: "state_initialised",
        1: "state_serverAccepted",
        2: "state_serverDeclined",
        3: "state_clientAccepted",
        4: "state_clientDeclined",
        5: "state_sending",
        6: "state_completed",
        7: "state_cancelled",
        8: "state_timed_out_client_response",
    }

    states_dict_str_to_int = {
        "state_error": -1,
        "state_initialised": 0,
        "state_serverAccepted": 1,
        "state_serverDeclined": 2,
        "state_clientAccepted": 3,
        "state_clientDeclined": 4,
        "state_sending": 5,
        "state_completed": 6,
        "state_cancelled": 7,
        "state_timed_out_client_response": 8,
    }
