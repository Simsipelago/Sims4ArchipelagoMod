import _thread
import json
import uuid
from typing import Dict

import websocket
import s4ap
from rel import rel
from s4ap.enums.S4APLocalization import S4APStringId
from s4ap.events.checks.send_check_event import SendCheckEvent
from s4ap.logging.s4ap_logger import S4APLogger
from s4ap.modinfo import ModInfo
from s4ap.enums import ap_cmds, S4APLocalization
from s4ap.persistance.ap_session_data_store import S4APSessionStoreUtils
from sims4communitylib.dialogs.common_input_multi_text_dialog import CommonInputMultiTextDialog
from sims4communitylib.dialogs.common_input_text_field import CommonInputTextField
from sims4communitylib.enums.common_character_restrictions import CommonCharacterRestriction
from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.notifications.common_basic_notification import CommonBasicNotification
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand, \
    CommonConsoleCommandArgument
from sims4communitylib.dialogs.common_choice_outcome import CommonChoiceOutcome
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils

logger = S4APLogger.get_log()
logger.enable()

s4apclient = None
thread = None


class S4APWebSocketApp:
    def __init__(self, host, port, slot_name, password=None):
        self.host = host
        self.port = port
        self.ws = websocket.WebSocketApp(f"wss://{host}:{port}",
                                         on_open=self.on_open,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)
        self.is_connected = False
        self.slot_name = slot_name
        self.uuid = uuid.getnode()
        self.password = password

    def on_message(self, ws, message):
        output = CommonConsoleCommandOutput
        logger.debug(message)
        decoder = json.JSONDecoder()
        parsed_message = decoder.decode(message)
        cmd = parsed_message[0]["cmd"]
        if cmd == ap_cmds.ROOMINFO:
            # Check if connection data already exists in storage for save and is the same
            seed_name = parsed_message[0]["seed_name"]
            data_store = S4APSessionStoreUtils()
            if not data_store.check_session_values(host_name=self.host, port=self.port, seed_name=seed_name,
                                                   player=self.slot_name):
                title_tokens = ""
                description_tokens = ""  # TODO show dialog

            else:
                self._send_connect(ws)

        elif cmd == ap_cmds.CONNECTED:
            logger.debug("cmd CONNECTED received")
            notification = CommonBasicNotification(
                CommonLocalizationUtils.create_localized_string(S4APStringId.CONNECTED),
                CommonLocalizationUtils.create_localized_string(S4APStringId.CONNECTED)
            )
            notification.show()
            self.is_connected = True
        elif cmd == ap_cmds.CONNECTIONREFUSED:
            logger.debug("cmd CONNECTIONREFUSED received")
            self.is_connected = False
            output(f"Connection was refused by the server. Reason: {parsed_message[0]['errors']}")
        elif cmd == ap_cmds.DATAPACKAGE:
            logger.debug("cmd DATAPACKAGE received")
            if parsed_message[0]["data"]["games"][s4ap.ap_game_name]["version"] != 0:
                output(f"Received DataPackage Version is {parsed_message[0]['version']}, current Mod version is "
                       f"{s4ap.ap_datapackage_version}")
                # TODO Show big warning sign
            else:
                output("Custom Data Package version active, ignoring")
        elif cmd == ap_cmds.PRINT or cmd == ap_cmds.PRINTJSON:
            logger.debug("Textcommand received")
            if cmd == ap_cmds.PRINT:
                logger.debug("cmd PRINT received")
                text = parsed_message[0]["text"]
            else:
                logger.debug("cmd PRINTJSON received")
                # TODO Specific handling of different PrintJSON packages
                text = str(parsed_message[0]["data"])
            output(f"Message received: {text}")
            logger.debug(f"Message received: {text}")
        elif cmd == ap_cmds.RECEIVEDITEMS:
            logger.debug("cmd RECEIVEDITEMS received")
            # [{"cmd":"ReceivedItems","index":0,"items":[{"item":80000,"location":-1,"player":0,"flags":0,"class":"NetworkItem"}]}]
            # TODO Handle Received Items
            pass
        else:
            logger.debug(f"cmd {cmd} received")
            logger.debug(f"Unhandled message received: {str(parsed_message)}")

    def on_error(self, ws, error):
        logger.error(f"Error in Websocket: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        logger.debug(f"Connection was closed with status {str(close_status_code)} and message {close_msg}")
        self.is_connected = False

    def on_open(self, ws):
        logger.debug("Opened connection, Fetching Data Package")
        gdp = f'[{{"cmd":"{ap_cmds.GETDATAPACKAGE}", "games": ["{s4ap.ap_game_name}"]}}]'
        ws.send(gdp)

    def _send_connect(self, ws):
        if self.password is None:
            self.password = "null"
        else:
            self.password = f"\"{self.password}\""

        ws.send(f'[{{"cmd": "{ap_cmds.CONNECT}", "name": "{self.slot_name}", "password": {self.password},'
                f'"version": {s4ap.ap_version},'
                '"tags": ["AP"],'
                f'"items_handling": 7, "uuid": {self.uuid}, "game": "{s4ap.ap_game_name}",'
                '"slot_data": false}]')

    def _warn_on_connect_submit(self):
        self._send_connect(self.ws)


@CommonConsoleCommand(ModInfo.get_identity(), "s4ap.connect", "Connect to a running Archipelago Server")
def _connect_to_ap(output: CommonConsoleCommandOutput):
    logger.debug("Attempt to connect to AP Server")
    global s4apclient
    if s4apclient is None or not s4apclient.is_connected:
        _login_data_input_text_dialog()
    else:
        output("Already connected to AP, if you are not try restarting the game")


@CommonConsoleCommand(ModInfo.get_identity(), 's4ap.chat', "Send Chat message to AP",
                      command_arguments=(
                              CommonConsoleCommandArgument(arg_name="message",
                                                           arg_type_name="Text",
                                                           arg_description="Chat Message to AP",
                                                           is_optional=False),
                      ))
def _send_message(output: CommonConsoleCommandOutput, message: str):
    logger.debug("Sending Message")
    if s4apclient is not None and s4apclient.is_connected:
        msg = f'[{{"cmd":"Say","text":"{message}"}}]'
        s4apclient.ws.send(msg)
    else:
        output("Couldn't send message, not connected")
        logger.debug("Cannot send message, not connected")


@CommonConsoleCommand(ModInfo.get_identity(), 's4ap.disconnect', 'Disconnect from AP Server')
def _disconnect(output: CommonConsoleCommandOutput):
    if s4apclient is not None and s4apclient.is_connected:
        logger.debug("Terminating AP Server Connection")
        s4apclient.ws.teardown()
        rel.abort()
        s4apclient.is_connected = False
        output("Connection Terminated")
    else:
        logger.debug("Not Connected")
        output("Not Connected")


@CommonConsoleCommand(ModInfo.get_identity(), 's4ap.check', 'Send Check to AP',
                      command_arguments=(CommonConsoleCommandArgument(arg_name="location_id",
                                                                      arg_type_name="Num",
                                                                      arg_description="Location ID of the Check",
                                                                      is_optional=False),
                                         ))
def _send_check(output: CommonConsoleCommandOutput, location_id: int):
    if s4apclient is not None and s4apclient.is_connected:
        logger.debug("Sending Location Check Data")
        CommonEventRegistry.get().dispatch(SendCheckEvent(location_id))
        output(f"Sending Location Check {str(location_id)}")
    else:
        logger.debug("Not Connected, Caching Location Check (NOT IMPLEMENTED YET)")
        # TODO Cache Location Check
        output("Not Connected, Caching Location Check (NOT IMPLEMENTED YET)")


@CommonEventRegistry.handle_events(ModInfo.get_identity())
def _handle_send_check(event_data: SendCheckEvent):
    if event_data.location_id == 81000:
        logger.info('Sending Check')
        location_check_msg = f'[{{"cmd":"{ap_cmds.LOCATIONCHECKS}","locations":[{event_data.location_id}]}}]'
        # TODO Caching and loading of all sent checks
        s4apclient.ws.send(location_check_msg)
        return
    pass


@CommonConsoleCommand(ModInfo.get_identity(), 's4ap.test_check_session_data', 'Test Data Store',
                      command_arguments=(CommonConsoleCommandArgument(arg_name="seed_name",
                                                                      arg_type_name="Text",
                                                                      arg_description="Seed Name to check against",
                                                                      is_optional=False),))
def _test_check_session_data(output: CommonConsoleCommandOutput, seed_name: str):
    output(f"Accessing Data Store and checking against seed {seed_name}")
    data_store = S4APSessionStoreUtils()

    if not data_store.check_session_values(host_name="localhost", port="38281", seed_name=seed_name, player="Player1"):
        output("Conflicting session values!")
    else:
        output("Data matched")
    data_store.check_datapackage_version(1)


def _run_websocket():
    output = CommonConsoleCommandOutput
    global s4apclient
    global thread
    s4apclient.ws.run_forever(dispatcher=rel, reconnect=5)
    rel.signal(2, rel.abort)
    thread = _thread.start_new_thread(rel.dispatch, ())
    output("Connected to AP")


def _login_data_input_text_dialog():
    def _on_submit(input_values: Dict[str, str], outcome: CommonChoiceOutcome):
        output = CommonConsoleCommandOutput
        if not CommonChoiceOutcome.is_error_or_cancel(outcome):
            logger.debug("Dialog confirmed")
            try:
                global s4apclient
                if input_values["password"] == '':
                    password = None
                else:
                    password = input_values["password"]
                output(f"Attempting to connect to {input_values['host']}:{input_values['port']} "
                       f"as {input_values['player_name']}")
                output(f"Password: {password}")
                logger.debug("Generating Websocket")
                s4apclient = S4APWebSocketApp(host=input_values["host"],
                                              port=input_values["port"],
                                              slot_name=input_values["player_name"],
                                              password=password)
                websocket.enableTrace(True)
                _run_websocket()
            except ConnectionRefusedError:
                output("Connection to the server was refused")
            except Exception:
                output("Generic Error happened")
        else:
            logger.debug("Cancelled or Error")
            output("Cancelled or Error")

        return

    dialog = CommonInputMultiTextDialog(
        ModInfo.get_identity(),
        S4APStringId.CONNECT_TO_SLOT,
        S4APStringId.ENTER_SLOT_DATA,
        (
            CommonInputTextField('host', 'localhost', title='Hostname'),
            CommonInputTextField('port', '38281', title='Port',
                                 character_restriction=CommonCharacterRestriction.NUMBERS_ONLY),
            CommonInputTextField('player_name', 'Player',
                                 title=CommonLocalizationUtils.create_localized_string(S4APStringId.PLAYER)),
            CommonInputTextField('password', '', title='Password (optional)')
        )
    )
    dialog.show(on_submit=_on_submit)
