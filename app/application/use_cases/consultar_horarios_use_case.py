# caso de uso concreto de consultar horarios
# hereda de BaseConsultar
from app.application.use_cases.base_consultar import BaseConsultar
import json


class ConsultarHorariosUseCase(BaseConsultar):
    async def ejecutar_consulta(self):
        datos = await self.obtener_de_cache()
        desde_cache = False
        if datos:
            horarios = json.loads(datos)
            desde_cache = True
        else:
            horarios = await self.obtener_de_fuente()
            await self.guardar_en_cache(json.dumps(horarios))
        return horarios, self.ciclo, desde_cache
