from playwright.async_api import async_playwright
import logging


logger = logging.getLogger(__name__)


class LoginPlaywright:
    def __init__(self, redis_client, usuario: str, password: str = None):
        self.redis_client = redis_client
        self.usuario = usuario
        self.password = password

    async def login(self) -> bool:
        """
        Realiza login con Playwright usando usuario y password.
        """
        try:
            async with async_playwright() as pw:
                navegador = await pw.chromium.launch(headless=True)
                pagina = await navegador.new_page()
                login_url = "https://intranet.cibertec.edu.pe/LoginIntranet/LoginCIB.aspx"
                await pagina.goto(login_url, timeout=5000)
                await pagina.wait_for_selector("#ctl00_ContentPlaceHolder1_Login1_UserName", timeout=5000)
                await pagina.fill("#ctl00_ContentPlaceHolder1_Login1_UserName", self.usuario)
                await pagina.wait_for_selector("#ctl00_ContentPlaceHolder1_Login1_Password", timeout=5000)
                await pagina.fill("#ctl00_ContentPlaceHolder1_Login1_Password", self.password)
                await pagina.click("a[href='javascript:InvocarForm();']")
                await pagina.wait_for_load_state()
                if "LoginCIB.aspx" not in pagina.url:
                    await navegador.close()
                    return True
                await navegador.close()
                return False
        except Exception as e:
            logger.error(f"Error en login playwright: {e}")
            return False
