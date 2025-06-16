from typing import Any

from playwright.async_api import async_playwright
from app.infrastructure.consultas.scrapers.base_web_scraper_impl import BaseWebScraperImpl


class NotasPlaywrightScraperImpl(BaseWebScraperImpl):
    async def scrap(self) -> list[dict[Any, Any]]:
        async with async_playwright() as pw:
            navegador = await pw.chromium.launch(headless=True)
            pagina = await navegador.new_page()
            await pagina.goto("https://intranet.cibertec.edu.pe/LoginIntranet/LoginCIB.aspx")

            await pagina.wait_for_selector("#ctl00_ContentPlaceHolder1_Login1_UserName")
            print("se detectó el campo de usr")
            await pagina.fill("#ctl00_ContentPlaceHolder1_Login1_UserName", self.usuario)
            print("se lleno el campo de usr")
            await pagina.wait_for_selector("#ctl00_ContentPlaceHolder1_Login1_Password")
            print("se detectó el campo de psw")
            await pagina.fill("#ctl00_ContentPlaceHolder1_Login1_Password", self.clave)
            print("se lleno el campo de psw")
            await pagina.click("a[href='javascript:InvocarForm();']")
            print("click en el boton login")

            await pagina.wait_for_load_state()
            await pagina.goto("https://intranet.cibertec.edu.pe/Redirecciona.asp?iTipo=1&inum=1&nomasp=SesionNet.asp?WPAG1=gestudiante/GESEST000.aspx?Destino=GESEST001.aspx")
            print(pagina.url)

            await pagina.wait_for_load_state()
            print(pagina.url)

            # Espera la tabla por clase
            await pagina.wait_for_selector("table.tbDatos")
            tabla = await pagina.query_selector("table.tbDatos")

            # extrae encabezados
            encabezado_fila = await tabla.query_selector("thead tr")
            encabezado_celdas = await encabezado_fila.query_selector_all("th")
            encabezado = [await celda.inner_text() for celda in encabezado_celdas]

            # extrae las filas
            filas = await tabla.query_selector_all("tbody tr")
            datos = []
            for fila in filas:
                celdas = await fila.query_selector_all("td")
                valores = [await celda.inner_text() for celda in celdas]
                if len(valores) == len(encabezado):
                    datos.append(dict(zip(encabezado, valores)))

            await navegador.close()
            return datos