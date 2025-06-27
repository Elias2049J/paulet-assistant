from playwright.async_api import async_playwright
from app.infrastructure.consultas.scrapers.base_web_scraper_impl import BaseWebScraperImpl
from app.domain.entities.horarios.mappers import dict_to_horario_diario
import logging

logger = logging.getLogger(__name__)


class HorariosWebScraperImpl(BaseWebScraperImpl):
    async def scrap(self) -> dict:
        logger.info("Iniciando scraping de horarios")

        async with async_playwright() as pw:
            logger.info("Lanzando navegador Chromium")
            navegador = await pw.chromium.launch(headless=True)
            pagina = await navegador.new_page()

            # Navegar a login
            login_url = "https://intranet.cibertec.edu.pe/LoginIntranet/LoginCIB.aspx"
            logger.info(f"Navegando a página de login: {login_url}")
            await pagina.goto(login_url, timeout=5000)

            # Login con logging detallado
            logger.info("Iniciando proceso de login detallado")

            logger.info("Esperando selector de campo de usuario")
            await pagina.wait_for_selector("#ctl00_ContentPlaceHolder1_Login1_UserName", timeout=5000)
            logger.info("Campo de usuario detectado correctamente")

            logger.info(f"Completando campo de usuario: {self.usuario}")
            await pagina.fill("#ctl00_ContentPlaceHolder1_Login1_UserName", self.usuario)
            logger.info("Campo de usuario completado exitosamente")

            logger.info("Esperando selector de campo de contraseña")
            await pagina.wait_for_selector("#ctl00_ContentPlaceHolder1_Login1_Password", timeout=5000)
            logger.info("Campo de contraseña detectado correctamente")

            logger.info("Completando campo de contraseña")
            await pagina.fill("#ctl00_ContentPlaceHolder1_Login1_Password", self.clave)
            logger.info("Campo de contraseña completado exitosamente")

            logger.info("Haciendo clic en botón de login")
            await pagina.click("a[href='javascript:InvocarForm();']")
            logger.info("Botón de login presionado correctamente")

            logger.info("Esperando carga completa de página después del login")
            await pagina.wait_for_load_state()
            logger.info("Login completado correctamente, página cargada")

            # Navegar a la página de horarios
            horarios_url = "https://intranet.cibertec.edu.pe/Redirecciona.asp?iTipo=1&inum=3&nomasp=SesionNet.asp?WPAG1=gestudiante/GESEST000.aspx?Destino=GESEST003.aspx"
            logger.info(f"Navegando a página de horarios: {horarios_url}")
            await pagina.goto(horarios_url, timeout=30000)
            logger.info(f"URL actual después de navegación: {pagina.url}")

            logger.info("Esperando carga completa de página de horarios")
            await pagina.wait_for_load_state()
            logger.info(f"Página de horarios cargada completamente. URL actual: {pagina.url}")

            # Extraer datos de horarios por día
            logger.info("Iniciando extracción de datos de horarios por día")
            horarios_por_dia = {}
            dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
            logger.info(f"Días a procesar: {dias}")

            try:
                # Buscar las tarjetas para cada día
                logger.info("Buscando tarjetas con horarios por día")
                cards = await pagina.query_selector_all("div.card")
                logger.info(f"Encontradas {len(cards)} tarjetas de horarios")

                for card in cards:
                    # Extraer el día del encabezado de la tarjeta
                    header = await card.query_selector("div.card-header h6")
                    if not header:
                        continue

                    dia = await header.inner_text()
                    dia = dia.strip()

                    logger.info(f"Procesando tarjeta para el día: {dia}")

                    # Inicializar lista para este día si no existe
                    if dia not in horarios_por_dia:
                        horarios_por_dia[dia] = []

                    # Buscar la tabla de horarios dentro de la tarjeta
                    tabla = await card.query_selector("table.tbDatos")
                    if not tabla:
                        logger.warning(f"No se encontró tabla de horarios para {dia}")
                        continue

                    # Extraer encabezados de la tabla
                    logger.info(f"Extrayendo encabezados para {dia}")
                    encabezados_elementos = await tabla.query_selector_all("thead th")

                    # Crear lista de encabezados, manejando las columnas combinadas
                    encabezados = []
                    for elemento in encabezados_elementos:
                        texto = await elemento.inner_text()
                        texto = texto.strip()

                        # Ignorar elementos vacíos y encabezados de columnas combinadas
                        if texto and not texto.startswith("Hora de Clase"):
                            encabezados.append(texto)

                    # Añadir encabezados específicos para columnas de hora
                    encabezados_hora_encontrados = False
                    for elemento in encabezados_elementos:
                        texto = await elemento.inner_text()
                        if texto.strip() == "Desde" or texto.strip() == "Hasta":
                            encabezados_hora_encontrados = True

                    if not encabezados_hora_encontrados:
                        # Si no se encontraron encabezados específicos, añadirlos
                        if "Hora de Clase" in [await e.inner_text() for e in encabezados_elementos]:
                            if "Desde" not in encabezados:
                                encabezados.append("Desde")
                            if "Hasta" not in encabezados:
                                encabezados.append("Hasta")

                    logger.info(f"Encabezados encontrados para {dia}: {encabezados}")

                    # Extraer filas de la tabla
                    filas = await tabla.query_selector_all("tbody tr")
                    logger.info(f"Encontradas {len(filas)} filas para {dia}")

                    for fila in filas:
                        celdas = await fila.query_selector_all("td")
                        if len(celdas) < 6:  # Verificar mínimo de columnas
                            continue

                        # Mapear valores a las claves correctas
                        curso_data = {}
                        valores = []

                        # Extraer valores de las celdas
                        for celda in celdas:
                            texto = await celda.inner_text()
                            valores.append(texto.strip())

                        # Construir el diccionario de curso con los nombres correctos de campo
                        curso_data = {
                            "curso": valores[0] if len(valores) > 0 else "",
                            "clase": valores[1] if len(valores) > 1 else "",
                            "tipo_clase": valores[2] if len(valores) > 2 else "",
                            "aula": valores[3] if len(valores) > 3 else "",
                            "desde": valores[4] if len(valores) > 4 else "",
                            "hasta": valores[5] if len(valores) > 5 else "",
                            "sede": valores[6] if len(valores) > 6 else ""
                        }

                        horarios_por_dia[dia].append(curso_data)
                        logger.info(f"Datos extraídos para {dia}: {curso_data['curso']}")

                # Si no se encontraron datos, intentar con otra estructura
                if not any(horarios_por_dia.values()):
                    logger.warning("No se encontraron datos en las tarjetas, intentando con estructura alternativa")

                    # Buscar todas las tablas tbDatos directamente
                    tablas = await pagina.query_selector_all("table.tbDatos")
                    for tabla in tablas:
                        # Intentar encontrar el día de la tabla
                        parent_card = await tabla.evaluate("el => el.closest('.card')")
                        if parent_card:
                            dia_header = await pagina.evaluate("""card => {
                                const header = card.querySelector('.card-header h6');
                                return header ? header.textContent.trim() : null;
                            }""", parent_card)

                            if dia_header in dias:
                                dia = dia_header
                                logger.info(f"Encontrada tabla para día: {dia}")

                                if dia not in horarios_por_dia:
                                    horarios_por_dia[dia] = []

                                # Extraer filas
                                filas = await tabla.query_selector_all("tbody tr")
                                for fila in filas:
                                    celdas = await fila.query_selector_all("td")
                                    valores = [await celda.inner_text() for celda in celdas]

                                    if len(valores) >= 6:
                                        curso_data = {
                                            "curso": valores[0].strip(),
                                            "clase": valores[1].strip(),
                                            "tipo_clase": valores[2].strip(),
                                            "aula": valores[3].strip(),
                                            "desde": valores[4].strip(),
                                            "hasta": valores[5].strip(),
                                            "sede": valores[6].strip() if len(valores) > 6 else ""
                                        }

                                        horarios_por_dia[dia].append(curso_data)
                                        logger.info(f"Datos extraídos alternativos para {dia}: {curso_data['curso']}")

                # Asegurar que todos los días posibles tengan una entrada
                for dia in dias:
                    if dia not in horarios_por_dia:
                        horarios_por_dia[dia] = []
                        logger.info(f"Inicializado día sin datos: {dia}")

            except Exception as e:
                logger.error(f"Error durante la extracción de datos: {e}", exc_info=True)
                # En caso de error, crear estructura vacía
                horarios_por_dia = {}
                for dia in dias:
                    horarios_por_dia[dia] = []

            # Convertir a objetos de dominio
            logger.info("Convirtiendo datos extraídos a objetos de dominio")
            horarios_diarios = {}
            for dia, cursos_data in horarios_por_dia.items():
                horarios_diarios[dia] = dict_to_horario_diario(dia, cursos_data)
                logger.info(f"Horario diario para {dia} convertido exitosamente con {len(cursos_data)} cursos")

            await navegador.close()
            logger.info("Navegador cerrado")
            logger.info("Scraping de horarios finalizado")
            return horarios_diarios
