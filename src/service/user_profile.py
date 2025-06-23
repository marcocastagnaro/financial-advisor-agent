def generar_prompt_usuario(usuario, activos):
    prompt = f"""
Sos un asesor financiero experto.

Perfil del usuario:
- Edad: {usuario['edad']}
- Ingresos mensuales: {usuario['ingresos']}
- Ocupación: {usuario.get('ocupacion', 'No especificado')}
- Descripción personal: {usuario.get('descripcion_personal', 'No especificado')}
- Tolerancia al riesgo: {usuario['riesgo']}
- Objetivo de inversión: {usuario.get('objetivo', 'No especificado')}
- Horizonte de inversión: {usuario.get('horizonte_inversion', 'No especificado')}
- Experiencia en inversiones: {usuario.get('experiencia_inversion', 'No especificado')}
- Intereses personales: {', '.join(usuario.get('intereses', []))}

Activos disponibles (con información financiera clave):
"""

    for ticker, v in activos.items():
        prompt += (
            f"\n- {ticker}: Sector: {v.get('sector', 'N/A')}, Industria: {v.get('industria', 'N/A')}, "
            f"País: {v.get('pais', 'N/A')}, Riesgo: {v['riesgo']}, "
            f"Retorno estimado a 5 años: {v['retorno_5a']}, "
            f"Capitalización bursátil: {v.get('market_cap', 'N/D')}, "
            f"Ratio P/E: {v.get('pe_ratio', 'N/D')}, "
            f"Dividend yield: {v.get('dividendo', 'N/D')}. "
            f"{v['descripcion']}"
        )

    prompt += """

Tarea:
Recomendá una cartera de inversión de entre 3 y 5 activos, cuidadosamente seleccionados para este usuario. Considerá todos los factores relevantes:

- Edad y horizonte de inversión implícito
- Ingresos mensuales como indicador de capacidad de inversión
- Tolerancia al riesgo como guía principal para la asignación
- Sector, industria, país, riesgo y retorno estimado de cada activo
- Capitalización bursátil (para saber si es una empresa sólida o pequeña)
- Ratio P/E y dividend yield (para entender valuación y rendimiento pasivo)
- Diversificación sectorial y geográfica para mitigar riesgos
- Equilibrio entre activos de alto crecimiento y de estabilidad relativa

Formato de salida esperado (sin asteriscos, sin bullets, sin advertencias legales):

[Porcentaje] [Ticker] - [Breve descripción del activo: qué es y en qué invierte]. [Justificación clara y específica basada en el perfil del usuario y los datos disponibles].

Ejemplo:
30% NVDA - NVIDIA es una empresa de chips líder en inteligencia artificial con alta capitalización y retorno estimado del 12%. Fue seleccionada por su crecimiento agresivo, alineado con el perfil del usuario y su interés en tecnología.

Devolvé únicamente un JSON con el siguiente formato:

{
  "introduccion": "Texto introductorio que contextualiza la recomendación.",
  "activos": [
    {
      "ticker": "AAPL",
      "porcentaje": 30,
      "justificacion": "Apple es una empresa tecnológica sólida, con crecimiento sostenido..."
    },
    {
      "ticker": "ARKK",
      "porcentaje": 25,
      "justificacion": "ETF de innovación con alto potencial, adecuado para perfiles de riesgo alto..."
    }
  ],
  "conclusion": "Resumen final que refuerza la lógica de la selección y posibles ajustes futuros."
}

No escribas nada fuera del JSON. Asegurate de que el JSON sea válido y pueda ser parseado sin errores.

"""

    return prompt
