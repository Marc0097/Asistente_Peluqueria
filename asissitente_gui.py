import tkinter as tk
from tkinter import scrolledtext, messagebox
import google.generativeai as genai
from dotenv import load_dotenv
import os


load_dotenv()
API_KEY = os.getenv("API_KEY")

if not API_KEY:
    messagebox.showerror("Error", "No se encontró la API_KEY en el archivo .env")
    exit()

genai.configure(api_key=API_KEY)


try:
    model = genai.GenerativeModel("gemini-2.5-flash")
except Exception:
    messagebox.showerror("Error", "No se pudo cargar el modelo gemini‑2.5‑flash. Verifica que tu cuenta tenga acceso.")
    exit()


def cargar_contexto():
    try:
        with open("servicios.txt", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "No se encontró el archivo servicios.txt."


def obtener_respuesta(pregunta, contexto):
    pregunta_lower = pregunta.lower()

    # Saludos
    if any(p in pregunta_lower for p in ["hola", "buenas", "hey", "holaa", "buenos días", "buenas tardes"]):
        return "¡Hola! Soy tu asistente de peluquería. ¿En qué puedo ayudarte hoy?"

    
    temas_peluqueria = [
        "corte", "tinte", "mechas", "peinado", "horario", "precio", "peluquer",
        "tratamiento", "color", "depilación", "servicios"
    ]
    if not any(p in pregunta_lower for p in temas_peluqueria):
        return "Lo siento, no puedo ayudarte con eso."

    
    prompt = f"""
Eres el asistente virtual de una peluquería.
Responde de manera amable, breve y clara usando la información de contexto.

Contexto:
{contexto}

Pregunta del cliente:
{pregunta}
"""

    try:
        respuesta = model.generate_content(prompt)
        return respuesta.text.strip()
    except Exception as e:
        return f"Ocurrio un error al generar la respuesta: {e}"


def main():
    root = tk.Tk()
    root.title("Asistente de Peluquería - IA")
    root.geometry("700x450")

    contexto = cargar_contexto()

    # Etiqueta y campo de texto
    tk.Label(root, text="Pregunta:").pack(anchor="w", padx=10, pady=(10, 0))
    entrada = tk.Entry(root, width=90)
    entrada.pack(padx=10, pady=5)

    # Área de salida
    salida = scrolledtext.ScrolledText(root, wrap="word", height=18)
    salida.pack(padx=10, pady=10, fill="both", expand=True)

    # Función al enviar
    def enviar():
        pregunta = entrada.get().strip()
        if not pregunta:
            return
        salida.insert(tk.END, f"Tú: {pregunta}\n")
        respuesta = obtener_respuesta(pregunta, contexto)
        salida.insert(tk.END, f"Asistente: {respuesta}\n\n")
        salida.see(tk.END)
        entrada.delete(0, tk.END)

    # Botón enviar
    tk.Button(root, text="Enviar", command=enviar).pack(pady=5)

    # Mensaje inicial
    salida.insert(tk.END, "Asistente de Peluquería listo.\n---\n")
    salida.insert(tk.END, "Escribe 'hola' para saludar o pregunta sobre cortes, tintes, precios, servicios, horarios, etc.\n\n")

    root.mainloop()

if __name__ == "__main__":
    main()