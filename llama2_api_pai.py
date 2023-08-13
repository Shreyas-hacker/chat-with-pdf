import websocket
import json
import struct


class pai_llama:
    def __init__(self, api_key):
        self.api_key = api_key
        self.input_message = ""
        self.temperature = 0.0
        self.round = 1
        self.received_message = None
        host = "ws://5568953365102451.ap-southeast-1.pai-eas.aliyuncs.com/api/predict/llama_api"
        self.host = host

    def on_message(self, ws, message):
        assert self.input_message in message, "request not in response."
        self.received_message = message

    def on_error(self, ws, error):
        print('error happened .. ')
        print(str(error))

    def on_close(self, ws, a, b):
        print("### closed ###", a, b)

    def on_pong(self, ws, pong):
        print('pong:', pong)

    def on_open(self, ws):
        print('Opening WebSocket connection to the server ... ')
        params_dict = {}
        params_dict['input_ids'] = self.input_message
        params_dict['temperature'] = self.temperature
        params_dict['repetition_penalty'] = self.repetition_penalty
        params_dict['top_p'] = self.top_p
        params_dict['max_length'] = 2048
        params_dict['num_beams'] = 1
        raw_req = json.dumps(params_dict)
        ws.send(raw_req)

        # for i in range(self.round):
        # ws.send(self.input_message)

        ws.send(struct.pack('!H', 1000), websocket.ABNF.OPCODE_CLOSE)

    def generate(self, message, temperature=0.95, repetition_penalty=1, top_p=0.01, max_length=2048, num_beams=1):
        self.input_message = message
        self.temperature = temperature
        self.repetition_penalty = repetition_penalty
        self.top_p = top_p
        self.max_length = max_length
        self.num_beams = num_beams

        ws = websocket.WebSocketApp(
            self.host,
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_pong=self.on_pong,
            on_close=self.on_close,
            header=[
                f'Authorization: {self.api_key}'],
        )
        # setup ping interval to keep long connection.
        ws.run_forever(ping_interval=2)
        return self.received_message.split('<br/>')[1:]

llama2_pai_client = pai_llama(api_key="")
res = llama2_pai_client.generate(
    message="tell me about alibaba cloud PAI", 
    temperature=0.95
)
print(f"Final: {res}")
print(" ")