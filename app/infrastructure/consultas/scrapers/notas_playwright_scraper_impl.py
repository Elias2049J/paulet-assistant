from typing import List, Dict, Any

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
            await pagina.goto("https://intranet.cibertec.edu.pe/Redirecciona.asp?iTipo=1&inum=1&nomasp=SesionNet.asp"
                              "?WPAG1=gestiante/GESEST000.aspx?Destino=GESEST001.aspx")
            print(pagina.url)
            await pagina.wait_for_load_state()

            cuerpo = await pagina.query_selector("body")
            cuerpohtml = await cuerpo.inner_html()
            print(cuerpohtml)

            print(pagina.url)
            await pagina.wait_for_selector("#DataTables_Table_0")
            print("se detectó la 1ra tabla")

            # selecciona la tabla y todas las filas dentro
            tabla = await pagina.query_selector("#DataTables_Table_0")
            print("se guardo la tabla")
            filas = await tabla.query_selector_all("#DataTables_Table_0 tr")
            print("se guardo las filas")

            # extrae primero el encabezado de la tabla
            encabezado_celdas = await filas[0].query_selector_all("th,td")
            encabezado = [await celda.inner_text() for celda in encabezado_celdas]
            print(f"Encabezado: {encabezado}")

            datos = []
            for fila in filas[1:]:
                celdas = await fila.query_selector_all("td")
                if not celdas:
                    continue
                valores = [await celda.inner_text() for celda in celdas]
                # empareja el encabezado con los valores
                fila_dict = dict(zip(encabezado, valores))
                datos.append(fila_dict)

            await navegador.close()
            return datos
