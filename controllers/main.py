from odoo import http # pyright: ignore[reportMissingImports, reportAttributeAccessIssue] (ignore any import warnings here)
from .get_odoo_module_path import get_odoo_module_path

PATH_PREFIX = '/zakat-fitrah'
API_PATH_PREFIX = f'{PATH_PREFIX}/api'

class ZakatFitrahController(http.Controller):
    print('\nSUCCESS: ZakatFitrahController controller loaded\n')

    @http.route(PATH_PREFIX)
    def root(self, **kw):
        odoo_module_path = get_odoo_module_path()
        if odoo_module_path == None: raise Exception('Not an Odoo module')
        odoo_module_name = odoo_module_path.parts[-1]
        return odoo_module_name

    @http.route(f'{API_PATH_PREFIX}/summary')
    def summary(self, **kw):
        return {
            'total_muzakki': 1,
            'total_mustahiq': 2,
            'total_kg_beras': 3,
            'total_liter_beras': 4,
            'total_kg_beras_disetor': 5,
            'total_liter_beras_disetor': 6,
            'total_kg_beras_disalurkan': 7,
            'total_liter_beras_disalurkan': 8,
        }