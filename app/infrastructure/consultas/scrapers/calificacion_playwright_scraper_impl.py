from typing import Any, Dict, List, Tuple
from playwright.async_api import async_playwright
from app.infrastructure.consultas.scrapers.base_web_scraper_impl import BaseWebScraperImpl
from app.domain.entities.calificaciones.mappers import crear_calificaciones_por_periodo
import logging
from app.infrastructure.config.redis_client import redis_client
from cryptography.fernet import Fernet
import os
from app.infrastructure.config.auth_loader import AuthLoader

logger = logging.getLogger(__name__)


class CalificacionPlaywrightScraperImpl(BaseWebScraperImpl):
    def __init__(self, usuario, clave, redis=None):
        super().__init__(usuario, clave)
        self.redis = redis or redis_client()
        FERNET_KEY = os.getenv("FERNET_KEY")
        if not FERNET_KEY:
            raise RuntimeError("FERNET_KEY debe estar definida en el entorno para encriptar credenciales.")
        self.fernet = Fernet(FERNET_KEY)

    async def scrap(self) -> Dict[str, Any]:
        """Extrae tanto períodos como calificaciones de la misma página en una sola operación"""
        logger.info("Iniciando scraping de notas y períodos")

        # Recuperar usuario y contraseña descifrados desde Redis usando AuthLoader
        try:
            self.usuario, self.clave = AuthLoader.get_credentials(self.redis)
        except Exception as e:
            logger.error(f"No se pudieron obtener credenciales: {e}")
            return {"periodos": [], "calificaciones": {}}

        try:
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

                # Navegar a notas
                notas_url = "https://intranet.cibertec.edu.pe/Redirecciona.asp?iTipo=1&inum=1&nomasp=SesionNet.asp?WPAG1=gestudiante/GESEST000.aspx?Destino=GESEST001.aspx"
                logger.info(f"Navegando a página de notas: {notas_url}")
                await pagina.goto(notas_url, timeout=30000)
                logger.info(f"URL actual después de navegación: {pagina.url}")

                logger.info("Esperando carga completa de página de notas")
                await pagina.wait_for_load_state()
                logger.info(f"Página de notas cargada completamente. URL actual: {pagina.url}")

                # Verificar si hay que hacer clic en el botón Buscar
                logger.info("Verificando si existe botón de búsqueda")
                buscar_btn = await pagina.query_selector("#MainContent_btnBuscar")
                if buscar_btn:
                    logger.info("Botón de búsqueda encontrado, haciendo clic para mostrar resultados")
                    await buscar_btn.click()
                    await pagina.wait_for_load_state()
                    # Esperar a que aparezcan los resultados de la búsqueda
                    logger.info("Esperando aparición de resultados (.card)")
                    await pagina.wait_for_selector(".card", timeout=8000)
                    logger.info("Resultados de búsqueda cargados")
                else:
                    logger.info("No se encontró botón de búsqueda, continuando")

                # Extraer períodos y calificaciones en una sola operación
                logger.info("Iniciando extracción de datos completos")
                periodos_calificaciones, lista_periodos = await self._extraer_datos_completos(pagina)

                logger.info(f"Scraping completado: {len(lista_periodos)} períodos, {len(periodos_calificaciones)} con calificaciones")
                await navegador.close()

                return {
                    "periodos": lista_periodos,
                    "calificaciones": periodos_calificaciones
                }

        except Exception as e:
            logger.error(f"Error durante el scraping: {e}")
            # Devolver estructura vacía pero válida para evitar crashes
            return {
                "periodos": [],
                "calificaciones": {}
            }

    async def _extraer_datos_completos(self, pagina) -> Tuple[Dict[str, Any], List[str]]:
        """Extrae tanto los períodos como las calificaciones de la página usando la estructura HTML real"""
        logger.info("Iniciando extracción de datos completos")
        periodos_calificaciones = {}
        lista_periodos = []

        try:
            # Extraer períodos desde el select primero (método más confiable)
            logger.info("Buscando selector de períodos: select[name='ctl00$MainContent$Periodo']")
            select_periodos = await pagina.query_selector("select[name='ctl00$MainContent$Periodo']")
            if select_periodos:
                logger.info("Selector de períodos encontrado, extrayendo opciones")
                options = await select_periodos.query_selector_all("option")
                logger.info(f"Encontradas {len(options)} opciones en el selector")

                for i, option in enumerate(options):
                    option_text = await option.inner_text()
                    option_value = await option.get_attribute("value")

                    # Ignorar la opción "--Todos--"
                    if option_text != "--Todos--" and option_value and option_value.strip() != "":
                        # Extraer el código del período (ej: "202543 - Campus Virtual" -> "202543")
                        codigo_periodo = option_text.split(" - ")[0].strip()
                        if codigo_periodo and codigo_periodo not in lista_periodos:
                            lista_periodos.append(codigo_periodo)
                            logger.info(f"Período encontrado en selector: {codigo_periodo}")

                logger.info(f"Períodos extraídos del selector: {lista_periodos}")
            else:
                logger.warning("No se encontró selector de períodos")

            # Esperar a que aparezca el contenido de resultados
            logger.info("Esperando contenido de resultados (.card)")
            await pagina.wait_for_selector(".card", timeout=8000)

            # Buscar todas las tarjetas de períodos (.card)
            logger.info("Buscando tarjetas de períodos (.card)")
            cards = await pagina.query_selector_all(".card")
            logger.info(f"Encontradas {len(cards)} tarjetas de períodos")

            for i, card in enumerate(cards):
                logger.info(f"Procesando tarjeta {i+1}/{len(cards)}")

                # Extraer período del header (h6 con id="hTituloAsistencia")
                header = await card.query_selector("h6[id='hTituloAsistencia']")
                if not header:
                    logger.warning(f"Tarjeta {i+1} sin header h6[id='hTituloAsistencia']")
                    continue

                periodo_text = await header.inner_text()
                logger.info(f"Texto del header: '{periodo_text}'")

                # Extraer el número del período (ej: "Periodo 202543" -> "202543")
                if "Periodo" in periodo_text:
                    periodo = periodo_text.replace("Periodo", "").strip()
                    logger.info(f"Período extraído de tarjeta: {periodo}")

                    # Añadir a la lista de períodos si no existe
                    if periodo and periodo not in lista_periodos:
                        lista_periodos.append(periodo)
                        logger.info(f"Período {periodo} agregado a la lista")

                    # Extraer tabla de notas del período actual
                    logger.info(f"Buscando tabla de notas para período {periodo}")
                    tabla = await card.query_selector("table.tbDatos")
                    if not tabla:
                        logger.warning(f"Período {periodo} sin tabla de datos")
                        # Si no hay tabla, crear período vacío pero válido
                        if periodo:
                            periodo_obj = crear_calificaciones_por_periodo(periodo, [])
                            periodos_calificaciones[periodo] = periodo_obj
                            logger.info(f"Período {periodo} creado con datos vacíos")
                        continue

                    logger.info(f"Tabla encontrada para período {periodo}")

                    # Extraer encabezados de la tabla
                    encabezado_fila = await tabla.query_selector("thead tr")
                    if not encabezado_fila:
                        logger.warning(f"Tabla del período {periodo} sin encabezados")
                        continue

                    encabezado_celdas = await encabezado_fila.query_selector_all("th")
                    encabezados = []
                    for celda in encabezado_celdas:
                        texto = await celda.inner_text()
                        encabezados.append(texto.strip())

                    logger.info(f"Encabezados extraídos para {periodo}: {encabezados}")

                    # Extraer todas las filas de datos del tbody
                    filas = await tabla.query_selector_all("tbody tr")
                    logger.info(f"Encontradas {len(filas)} filas de datos para período {periodo}")
                    datos_periodo = []

                    for j, fila in enumerate(filas):
                        celdas = await fila.query_selector_all("td")
                        valores = []
                        for celda in celdas:
                            texto = await celda.inner_text()
                            valores.append(texto.strip())

                        # Crear diccionario con los datos de cada curso
                        if len(valores) >= len(encabezados):
                            # Tomar solo los valores necesarios según los encabezados
                            valores_curso = valores[:len(encabezados)]
                            datos_curso = dict(zip(encabezados, valores_curso))
                            datos_periodo.append(datos_curso)

                            # Log del primer curso como ejemplo
                            if j == 0:
                                logger.info(f"Ejemplo de curso extraído: {datos_curso.get('Curso', 'N/A')}")

                    # Convertir a objeto de dominio
                    periodo_obj = crear_calificaciones_por_periodo(periodo, datos_periodo)
                    periodos_calificaciones[periodo] = periodo_obj
                    logger.info(f"Período {periodo} procesado con {len(datos_periodo)} cursos")

            # Asegurar que todos los períodos tengan un objeto de calificaciones, aunque sea vacío
            for periodo in lista_periodos:
                if periodo not in periodos_calificaciones:
                    periodo_obj = crear_calificaciones_por_periodo(periodo, [])
                    periodos_calificaciones[periodo] = periodo_obj
                    logger.info(f"Período {periodo} completado con datos vacíos")

            # Ordenar períodos de más reciente a más antiguo (asumiendo formato YYYYPP)
            lista_periodos.sort(reverse=True)
            logger.info(f"Períodos ordenados: {lista_periodos}")

            logger.info(f"Extracción completada exitosamente: {len(lista_periodos)} períodos, {len(periodos_calificaciones)} con datos")

        except Exception as e:
            logger.error(f"Error extrayendo datos completos: {e}")
            logger.error(f"Activando modo de recuperación - devolviendo datos vacíos")
            # En caso de error, devolver datos mínimos para evitar crashes
            lista_periodos = []
            periodos_calificaciones = {}
            logger.warning("Devolviendo listas vacías debido al error")

        return periodos_calificaciones, lista_periodos

    async def _extraer_periodos_desde_select(self, pagina) -> List[str]:
        """Método alternativo para extraer períodos desde el select si el principal falla"""
        periodos = []

        try:
            # Buscar el select de períodos
            select_element = await pagina.query_selector("select[name='ctl00$MainContent$Periodo']")
            if select_element:
                options = await select_element.query_selector_all("option[value]")
                for option in options:
                    option_text = await option.inner_text()
                    option_value = await option.get_attribute("value")

                    if option_value and option_value.strip() != "":
                        periodo = option_text.split(" - ")[0].strip()
                        if periodo and periodo not in periodos and periodo != "--Todos--":
                            periodos.append(periodo)
        except Exception as e:
            print(f"Error extrayendo períodos desde select: {e}")

        return periodos
