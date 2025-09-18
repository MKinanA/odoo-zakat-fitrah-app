from datetime import datetime
from colorama import Fore
from get_odoo_module_path import get_odoo_module_path

try: ODOO_MODULE_PATH = get_odoo_module_path(__file__)
except: ODOO_MODULE_PATH = None
ODOO_MODULE_NAME = ODOO_MODULE_PATH.parts[-1] if ODOO_MODULE_PATH != None else None

simple_log = lambda *args, **kwargs: print(f'{Fore.RESET}{datetime.now().strftime(f'%Y-%m-%d{kwargs['sep'] if 'sep' in kwargs else ' '}%H:%M:%S:%f')}{f'{kwargs['sep'] if 'sep' in kwargs else ' '}[{Fore.BLUE}{kwargs['name'] if 'name' in kwargs else ODOO_MODULE_NAME}{Fore.RESET}]' if (ODOO_MODULE_NAME != None or 'name' in kwargs) and not ('name' in kwargs and kwargs['name'] == None) else ''}{kwargs['sep'] if 'sep' in kwargs else ' '}[{kwargs['level'] if 'level' in kwargs else f'{Fore.GREEN}INFO{Fore.RESET}'}]', *args, **{key: kwargs[key] for key in kwargs if key not in ['name', 'level']})