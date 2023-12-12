import os
from openai import OpenAI


class tiktok_chatbot:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPEN_AI_KEY"))
        self.on_play = False

        self.chat_context = [
            {
                "role": "system",
                "content": "asume el rol de una mujer coqueta que responde en español, te llamas Anakin, eres de Bogotá, Colombia. te dedicas a crear contenido en TikTok y quieres empezar a entablar una conversación, motivas a las personas a que te envien regalos",
            }
        ]
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo", messages=self.chat_context
        )
        print(response.choices[0].message.content)
        # self.reproducir_y_eliminar_mp3(response.choices[0].message.content)

    def chatbot_response(self, prompt, user):
        content = f"{user} dice: {prompt}"
        self.chat_context.append({"role": "user", "content": content})
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo", messages=self.chat_context
        )
        ruta = "output.mp3"
        content = response.choices[0].message.content
        self.crear_audio_y_guardarlo(content, ruta)
        self.reproducir_mp3(ruta)
        # os.remove(ruta)

    def generar_charla_aleatoria(self, tema):
        nuevo_tema = ""
        ruta = "output.mp3"
        if tema == None or str(tema) == "":
            prompt, tokens = self.crear_un_nuevo_tema_de_conversacion()
            nuevo_tema = self.generar_respuesta(tokens, prompt)
        else:
            prompt, tokens = self.hablar_de(tema)
            nuevo_tema = self.generar_respuesta(tokens, prompt)

        self.crear_audio_y_guardarlo(nuevo_tema, ruta)
        self.reproducir_mp3(ruta)
        os.remove(ruta)

    def crear_audio_y_guardarlo(self, texto, ruta):
        response = self.client.audio.speech.create(
            model="tts-1", voice="nova", input=texto
        )
        response.stream_to_file(ruta)
        response.close()

    def generar_respuesta(self, tokens, content):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-instruct",
            max_tokens=tokens,
            messages=[{"role": "system", "content": content}],
        )
        content = response.choices[0].message.content
        print(content)
        return content

    def hablar_de(tema):
        content = f"hablame de {tema} en un tono coqueto"
        tokens = 500
        return content, tokens

    def crear_un_nuevo_tema_de_conversacion(self):
        content = "hablame de cualquier tema de comun en tiktok en un tono coqueto"
        tokens = 500
        return content, tokens
