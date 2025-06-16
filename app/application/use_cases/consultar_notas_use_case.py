# caso de uso concreto para consultar notas
# hereda de BaseConsultar
from app.application.use_cases.base_consultar import BaseConsultar
import json


class ConsultarNotasUseCase(BaseConsultar):
    async def ejecutar_consulta(self):
        # primero intenta obtener de caché
        datos = await self.obtener_de_cache()
        desde_cache = False
        if datos:
            # si hay datos en caché, deserializa
            notas = json.loads(datos)
            desde_cache = True
        else:
            # si no hay datos en caché, obtiene de fuente y guarda
            notas = await self.obtener_de_fuente()
            await self.guardar_en_cache(json.dumps(notas))
        return notas, self.ciclo, desde_cache
