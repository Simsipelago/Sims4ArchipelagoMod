import _thread
import json
import uuid
import websocket
import s4ap
from rel import rel
from s4ap.events.checks.send_check_event import SendCheckEvent
from s4ap.logging.s4ap_logger import S4APLogger
from s4ap.modinfo import ModInfo
from s4ap.enums import ap_cmds
from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand, \
    CommonConsoleCommandArgument


logger = S4APLogger.get_log()
logger.enable()

s4apclient = None


class S4APWebSocketApp:
    def __init__(self, host, port, slot_name, password=None):
        self.ws = websocket.WebSocketApp(f"ws://{host}:{port}",
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
            if self.password is None:
                self.password = "null"
            else:
                self.password = f"\"{self.password}\""
            ws.send(f'[{{"cmd": "{ap_cmds.CONNECT}", "name": "{self.slot_name}", "password": {self.password},'
                    f'"version": {s4ap.ap_version},'
                    '"tags": ["AP", "TextOnly"],'
                    f'"items_handling": 7, "uuid": {self.uuid}, "game": "",'
                    '"slot_data": false}]')
        elif cmd == ap_cmds.CONNECTED:
            self.is_connected = True
        elif cmd == ap_cmds.CONNECTIONREFUSED:
            self.is_connected = False
            output(f"Connection was refused by the server. Reason: {parsed_message[0]['errors']}")
        elif cmd == ap_cmds.DATAPACKAGE:
            # TODO handle DataPackage
            pass
            # if parsed_message[0]["version"] != 0:
            #    pass
            # else:
            #    output("Datapackage version is 0")
        elif cmd == ap_cmds.PRINT or cmd == ap_cmds.PRINTJSON:
            if cmd == ap_cmds.PRINT:
                text = parsed_message[0]["text"]
            else:
                # TODO Specific handling of different PrintJSON packages
                text = parsed_message[0]["data"]
            output(f"Message received: {text}")
        elif cmd == ap_cmds.RECEIVEDITEMS:
            # [{"cmd":"ReceivedItems","index":0,"items":[{"item":80000,"location":-1,"player":0,"flags":0,"class":"NetworkItem"}]}]
            # TODO Handle Received Items
            pass

    def on_error(self, ws, error):
        logger.error(error)

    def on_close(self, ws, close_status_code, close_msg):
        logger.debug("### closed ###")
        self.is_connected = False

    def on_open(self, ws):
        logger.debug("Opened connection, Fetching Data Package")
        gdp = f'[{{"cmd":"{ap_cmds.GETDATAPACKAGE}"}}]'
        ws.send(gdp)


@CommonConsoleCommand(ModInfo.get_identity(), "s4ap.connect", "Connect to AP Server",
                      # TODO: Remove Player and Password altogether and use dialog instead
                      command_arguments=(
                              CommonConsoleCommandArgument(arg_name="host",
                                                           arg_type_name="Text",
                                                           arg_description="Host name of the game you want to connect to",
                                                           is_optional=True,
                                                           default_value="archipelago.gg"),
                              CommonConsoleCommandArgument(arg_name="port",
                                                           arg_type_name="Num",
                                                           arg_description="The Port of the game you want to connect to",
                                                           is_optional=False),
                              # TODO: Once we're safe set default to Async Port
                              CommonConsoleCommandArgument(arg_name="player",
                                                           arg_type_name="Text",
                                                           arg_description="Name of the slot to connect to",
                                                           is_optional=True,
                                                           default_value="MrSummer"),
                              CommonConsoleCommandArgument(arg_name="password",
                                                           arg_type_name="Text",
                                                           arg_description="Password for the game",
                                                           is_optional=True,
                                                           default_value=None)
                      ))
def _connect_to_ap(output: CommonConsoleCommandOutput, host: str, port: int, player: str, password: str):
    logger.debug("Attempt to connect to AP Server")
    global s4apclient
    if s4apclient is None or not s4apclient.is_connected:
        s4apclient = S4APWebSocketApp(host, port, player, password)
        websocket.enableTrace(True)

        s4apclient.ws.run_forever(dispatcher=rel,
                                  reconnect=5)
        rel.signal(2, rel.abort)  # Keyboard Interrupt
        _thread.start_new_thread(rel.dispatch, ())
        output("Connected!")
    else:
        output("Connection already established")


@CommonConsoleCommand(ModInfo.get_identity(), 's4ap.chat', 'Send Text Message to AP Server',
                      command_arguments=(CommonConsoleCommandArgument(arg_name="message",
                                                                      arg_type_name="Text",
                                                                      arg_description="Chat Message",
                                                                      is_optional=False),
                                         ))
def _send_message(output: CommonConsoleCommandOutput, message: str):
    logger.debug("Sending Message")
    if s4apclient is not None and s4apclient.is_connected:
        msg = f'[{{"cmd":"Say","text":"{message}"}}]'
        s4apclient.ws.send(msg)
    else:
        output("Cannot send message, not connected")
        logger.debug("Cannot send message, not connected")


@CommonConsoleCommand(ModInfo.get_identity(), 's4ap.disconnect', 'Disconnect from AP Server')
def _disconnect(output: CommonConsoleCommandOutput):
    if s4apclient is not None and s4apclient.is_connected:
        logger.debug("Terminating AP Server Connection")
        s4apclient.ws.close()
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
