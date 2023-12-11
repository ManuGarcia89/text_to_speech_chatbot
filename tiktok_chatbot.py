import os
import pygame
from openai import OpenAI

class tiktok_chatbot:
    def __init__(self):
        self.client = OpenAI(api_key='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')
        self.on_play = False
        self.regalo_barato = 50
        self.chat_context = [
            {"role": "system", "content": "asume el rol de una mujer coqueta que responde en español, te llamas Anakin, eres de Bogotá, Colombia, te dedicas a crear contenido en TikTok y quieres empezar a entablar una conversación"}
        ]
        pygame.init()
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.chat_context
        )
        print(response.choices[0].message.content)
        #self.reproducir_y_eliminar_mp3(response.choices[0].message.content)

    def chatbot_response(self, prompt, user):
        content = f"{user} dice: {prompt}"
        self.chat_context.append({"role": "user", "content": content})
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.chat_context
        )
        ruta = "output.mp3"
        content = response.choices[0].message.content
        self.crear_audio_y_guardarlo(content, ruta)
        self.reproducir_mp3(ruta)
        #os.remove(ruta)

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

    def reproducir_mp3(self, ruta):
        pygame.mixer.music.load(ruta)
        pygame.mixer.music.play()
        self.on_play = True
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        self.on_play = False
        pygame.mixer.music.stop()
        

    def crear_audio_y_guardarlo(self, texto, ruta) :
        response = self.client.audio.speech.create(
            model="tts-1",
            voice="nova",
            input=texto
        )
        response.stream_to_file(ruta)
        response.close()

    def crear_audio_temporal_con_texto(self, texto):
        ruta = "output.mp3"
        self.crear_audio_y_guardarlo(texto, ruta)
        self.reproducir_mp3(ruta)
        os.remove(ruta)

    def recibir_regalo_y_dar_feednback(self, gift_name, gift_type, gift_price, gift_quantity, tiktok_user):

        if gift_type == 1 :
            ammount = gift_price * gift_quantity
            if ammount <= self.regalo_barato: 
                ruta = "audio_gift/" + gift_name + "_" + str(gift_quantity) + ".mp3"
                if os.path.exists(ruta):
                    print(f"El archivo en la ruta {ruta} existe.")
                    self.reproducir_mp3(ruta)
                else:
                    print(f"El archivo en la ruta {ruta} no existe.")
                    prompt, tokens  = self.dar_una_respuesta_sencilla_para_un_regalo_barato(gift_name, gift_price, gift_quantity) 
                    respuesta = self.generar_respuesta(tokens, prompt)
                    self.crear_audio_y_guardarlo(respuesta, ruta)
                    self.reproducir_mp3(ruta)
            else :
                ruta = "output.mp3"
                prompt, tokens  = self.traer_prompt_para_dar_una_nueva_respuesta_para_regalo_tipo_1_a_usuario(gift_name, gift_price, gift_quantity, tiktok_user) 
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
                    prompt, tokens = self.dar_una_respuesta_sencilla_para_un_regalo_barato(gift_name, gift_price, gift_quantity) 
                    respuesta = self.generar_respuesta(tokens, prompt)
                    self.crear_audio_y_guardarlo(respuesta, ruta)
                    self.reproducir_mp3(ruta)

            else :
                ruta = "output.mp3"
                prompt, tokens = self.dar_una_nueva_respuesta_para_regalo_tipo_x_a_usuario(gift_name, gift_price, tiktok_user)
                respuesta = self.generar_respuesta(tokens, prompt)
                self.crear_audio_y_guardarlo(respuesta, ruta)
                self.reproducir_mp3(ruta)
                os.remove(ruta)


        
    def generar_respuesta(self, tokens, content) :
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-instruct",
            max_tokens=tokens,
            messages=[
                {
                    "role": "system", 
                    "content": content
                }
            ]
        )
        print(response.choices[0].message.content)
        return response.choices[0].message.content

    def traer_prompt_para_dar_una_nueva_respuesta_para_regalo_tipo_1_a_usuario(self, gift_name, gift_price, gift_quantity, tiktok_user):
        content = f"Escribe una respuesta asumiendo el rol de una mujer coqueta agradecida con {tiktok_user} por enviarte {gift_quantity} en {gift_name} en un live de tiktok. Tener en cuenta para la respuesta que en un rango de 1 a 35000 diamantes el regalo es de {gift_price} diamantes, con base a la anterior proporcion la respuesta debe tener un tono desagradable para 1 diamante a un tono coqueto para 100 diamantes para arriba."
        tokens = int(gift_price * gift_quantity)
        return content, tokens
        
    
    def dar_una_nueva_respuesta_para_regalo_tipo_x_a_usuario(self, gift_name, gift_price, tiktok_user):
        content = f"Escribe una respuesta asumiendo el rol de una mujer coqueta agradecida con {tiktok_user} por enviarte un regalo llamado '{gift_name}', este regalo lo envio por medio de un live de tiktok. Tener en cuenta para la respuesta que en un rango de 1 a 35000 diamantes el regalo es de {gift_price} diamantes, con base a la anterior proporcion la respuesta debe tener un tono desagradable para 1 diamante a un tono coqueto para 100 diamantes para arriba."
        tokens = gift_price
        return content, tokens
    
    def dar_una_respuesta_sencilla_para_un_regalo_barato(self, gift_name, gift_price, gift_quantity):
        content = f"Escribe una respuesta asumiendo el rol de una mujer coqueta, agradecida por recibir {gift_quantity} regalo llamado '{gift_name}', este regalo lo recibiste por un live de tiktok. Tener en cuenta para la respuesta que en un rango de 1 a 35000 diamantes el regalo es de {gift_price} diamantes, con base a la anterior proporcion la respuesta debe tener un tono desagradable para 1 diamante a un tono coqueto para 100 diamantes para arriba."
        tokens = 200
        return content, tokens
    
    def hablar_de(tema):
        content = f"hablame de {tema} en un tono coqueto"
        tokens = 500
        return content, tokens
    
    def crear_un_nuevo_tema_de_conversacion():
        content = "hablame de cualquier tema de comun en tiktok en un tono coqueto"
        tokens = 500
        return content, tokens