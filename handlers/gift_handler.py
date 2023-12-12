import queue
import threading
import os

from tools.audio import TextToSpeech


class GifHandler:
    def __init__(self, *args, **kwargs):
        super(GifHandler, self).__init__(*args, **kwargs)
        # Parametros de configuracion
        self.regalo_barato = 50

        # Cola de tareas
        self.thread_queue = queue.Queue()
        self.thread_semaphore = threading.Semaphore(1)

        # Servicios
        self.speech_service = TextToSpeech()

    def gift_received(self, json_data: dict):
        pass

    def process_queue(self):
        while not self.thread_queue.empty():
            task = self.thread_queue.get()
            try:
                task()
            finally:
                self.thread_queue.task_done()

        self.thread_semaphore.release()

    def traer_prompt_para_dar_una_nueva_respuesta_para_regalo_tipo_1_a_usuario(
        self, gift_name, gift_price, gift_quantity, tiktok_user
    ):
        content = f"Escribe una respuesta asumiendo el rol de una mujer coqueta agradecida con {tiktok_user} por enviarte {gift_quantity} en {gift_name} en un live de tiktok. Tener en cuenta para la respuesta que en un rango de 1 a 35000 diamantes el regalo es de {gift_price} diamantes, con base a la anterior proporcion la respuesta debe tener un tono desagradable para 1 diamante a un tono coqueto para 100 diamantes para arriba."
        tokens = int(gift_price * gift_quantity)
        return content, tokens

    def dar_una_nueva_respuesta_para_regalo_tipo_x_a_usuario(
        self, gift_name, gift_price, tiktok_user
    ):
        content = f"Escribe una respuesta asumiendo el rol de una mujer coqueta agradecida con {tiktok_user} por enviarte un regalo llamado '{gift_name}', este regalo lo envio por medio de un live de tiktok. Tener en cuenta para la respuesta que en un rango de 1 a 35000 diamantes el regalo es de {gift_price} diamantes, con base a la anterior proporcion la respuesta debe tener un tono desagradable para 1 diamante a un tono coqueto para 100 diamantes para arriba."
        tokens = gift_price
        return content, tokens

    def dar_una_respuesta_sencilla_para_un_regalo_barato(
        self, gift_name, gift_price, gift_quantity
    ):
        content = f"Escribe una respuesta asumiendo el rol de una mujer coqueta, agradecida por recibir {gift_quantity} regalo llamado '{gift_name}', este regalo lo recibiste por un live de tiktok. Tener en cuenta para la respuesta que en un rango de 1 a 35000 diamantes el regalo es de {gift_price} diamantes, con base a la anterior proporcion la respuesta debe tener un tono desagradable para 1 diamante a un tono coqueto para 100 diamantes para arriba."
        tokens = 200
        return content, tokens

    def recibir_regalo_y_dar_feedback(
        self, gift_name, gift_type, gift_price, gift_quantity, tiktok_user
    ):

        if gift_type == 1:
            amount = gift_price * gift_quantity
            if amount <= self.regalo_barato:

                prompt = f"Gracias por el regalo {gift_name}"
                tokens = 100
                # respuesta = self.generar_respuesta(tokens, prompt)
                self.speech_service.text_to_speech(prompt)

            else:
                ruta = "output.mp3"
                (
                    prompt,
                    tokens,
                ) = self.traer_prompt_para_dar_una_nueva_respuesta_para_regalo_tipo_1_a_usuario(
                    gift_name, gift_price, gift_quantity, tiktok_user
                )
                respuesta = self.generar_respuesta(tokens, prompt)
                self.crear_audio_y_guardarlo(respuesta, ruta)
                self.reproducir_mp3(ruta)
                os.remove(ruta)

        else:
            if gift_price <= self.regalo_barato:
                ruta = "audio_gift/" + gift_name + ".mp3"
                if os.path.exists(ruta):
                    print(f"El archivo en la ruta {ruta} existe.")
                    self.reproducir_mp3(ruta)
                else:
                    print(f"El archivo en la ruta {ruta} no existe.")
                    (
                        prompt,
                        tokens,
                    ) = self.dar_una_respuesta_sencilla_para_un_regalo_barato(
                        gift_name, gift_price, gift_quantity
                    )
                    respuesta = self.generar_respuesta(tokens, prompt)
                    self.crear_audio_y_guardarlo(respuesta, ruta)
                    self.reproducir_mp3(ruta)

            else:
                ruta = "output.mp3"
                (
                    prompt,
                    tokens,
                ) = self.dar_una_nueva_respuesta_para_regalo_tipo_x_a_usuario(
                    gift_name, gift_price, tiktok_user
                )
                respuesta = self.generar_respuesta(tokens, prompt)
                self.crear_audio_y_guardarlo(respuesta, ruta)
                self.reproducir_mp3(ruta)
                os.remove(ruta)

    def add_gift(
        self,
        gift_name: str,
        gift_type: int,
        gift_price: int,
        gift_quantity: int,
        tiktok_user: str,
    ):
        print("Agregando regalo a la cola de tareas...")
        self.thread_queue.put(
            lambda: self.recibir_regalo_y_dar_feedback(
                gift_name, gift_type, gift_price, gift_quantity, tiktok_user
            )
        )

        # Iniciar el procesamiento de la cola si no hay otros hilos activos
        if not self.thread_semaphore.acquire(blocking=False):
            return

        threading.Thread(target=self.process_queue).start()

    def stop(self):
        self.speech_service.stop()
