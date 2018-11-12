import concurrent.futures


class PepperTabletDialogHandler(object):
    """
    Helper-Class for handling Tablet Dialog Interactions between User and Pepper.
    Works only on real Robot and can therefore not be used on Choregraphe Simulation
    """
    def __init__(self, my_robot):
        self._session = my_robot.session
        self._app = my_robot.app
        self._proxyALTabletService = self._session.service("ALTabletService")
        self._result = None
        self._signal_id = None
        self._executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)

    def show_input_text_dialog_blocking(self, text_dialog,
                                        ok_button_text="OK",
                                        cancel_button_text="Cancel",
                                        timeout=None):
        # type: (str, str, str, int) -> str
        """
        Starts the Text Dialog on the Pepper Tablet with Text for Header, OK and Cancel as defined in the
        parameters. The Method is blocking, thus waits either for an Userinput or the given timeout

        Args:
        :param text_dialog: Header/Question of the Dialog-Window
        :param ok_button_text: Text shown in the OK Button
        :param cancel_button_text: Text shown in the Cancel Button
        :param timeout:

        Returns:
        :rtype: str
        :return: Userinput from Tablet as str or None if User selected "Cancel"

        Raises:
        TimeoutError: If the user makes no Input before the given timeout.
        """
        future = self.show_input_text_dialog_concurrently(text_dialog, ok_button_text, cancel_button_text)
        return future.result(timeout)

    def show_input_text_dialog_concurrently(self, text_dialog,
                                            ok_button_text="OK",
                                            cancel_button_text="Cancel"):
        # type: (str, str, str) -> concurrent.futures.Future
        """
        Starts the Text Dialog on the Pepper Tablet with Text for Header, OK and Cancel as defined in the
        parameters. The Method is blocking, thus waits either for an Userinput or the given timeout

        Args:
        :param text_dialog: Header/Question of the Dialog-Window
        :param ok_button_text: Text shown in the OK Button
        :param cancel_button_text: Text shown in the Cancel Button

        Returns:
        :rtype: concurrent.futures.Future
        :return: Futur-Object for the given Task
        """

        future = self._executor.submit(self.__callback_on_input_text, text_dialog,
                                          ok_button_text, cancel_button_text)
        return future

    def __callback_on_input_text(self, button_id, input_text):
        if button_id == 1:
            self._result(input_text)

        self._app.stop()

    def __show_input_text_dialog_logic(self, text_dialog, ok_button_text="OK", cancel_button_text="Cancel"):
        # type: (str, str, str) -> str
        """
        Private Method which registers the Callback-Method "__callback_on_input_text" on the Robot
        and waits until the User triggers an Input. Disconnects from ALTabletService-Proxy afterwards.
        :param text_dialog: Header/Question of the Dialog-Window
        :param ok_button_text: Text shown in the OK Button
        :param cancel_button_text: Text shown in the Cancel Button

        :rtype: str
        :return: Userinput from Tablet as str if User selected "OK" or None if User selected "Cancel"
        """
        try:
            self._proxyALTabletService.showInputTextDialog(text_dialog, ok_button_text, cancel_button_text)

            self._signal_id = self._proxyALTabletService.onInputText.connect(self.__callback_on_input_text)
            self._app.run()

            self._proxyALTabletService.onInputText.disconnect(self._signal_id)
        except Exception, e:
            print "Error occurred: ", e

        return self.__get_result_and_reset()

    def __get_result_and_reset(self):
        result = self._result
        self._result = None
        return result


