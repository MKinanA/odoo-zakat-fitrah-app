from odoo import http # pyright: ignore[reportMissingImports, reportAttributeAccessIssue] (ignore any import warnings here)
from json import dumps as json
from ..helpers.get_odoo_module_path import get_odoo_module_path

PATH_PREFIX = '/zakat-fitrah'
API_PATH_PREFIX = f'{PATH_PREFIX}/api'
ODOO_MODULE_PATH = get_odoo_module_path(__file__)
ODOO_MODULE_NAME = ODOO_MODULE_PATH.parts[-1]

class ZakatFitrahController(http.Controller):
    print(f'\n{ODOO_MODULE_NAME}: [SUCCESS] ZakatFitrahController controller loaded\n')

    # Regular routes
    @http.route(PATH_PREFIX)
    def root(self, **kw) -> str:
        return open(ODOO_MODULE_PATH/'pages/dashboard.html').read().format(**self._summary())

    # API routes
    @http.route(f'{API_PATH_PREFIX}/summary')
    def summary(self, **kw) -> str: return json(self._summary())

    # Non-route functions
    @staticmethod
    def _summary() -> dict:
        muzakkis = http.request.env['zf.muzakki'].search([])
        mustahiqs = http.request.env['zf.mustahiq'].search([])

        total_muzakki = sum(muzakki.jumlah_jiwa_zakat_fitrah for muzakki in muzakkis)
        total_mustahiq = len(mustahiqs)
        total_kg_beras = sum(muzakki.zakat_fitrah_kilogram_beras for muzakki in muzakkis) - sum(mustahiq.kilogram_beras_dari_zakat_fitrah for mustahiq in mustahiqs)
        total_liter_beras = sum(muzakki.zakat_fitrah_liter_beras for muzakki in muzakkis) - sum(mustahiq.liter_beras_dari_zakat_fitrah for mustahiq in mustahiqs)
        total_kg_beras_disetor = sum(muzakki.zakat_fitrah_kilogram_beras for muzakki in muzakkis)
        total_liter_beras_disetor = sum(muzakki.zakat_fitrah_liter_beras for muzakki in muzakkis)
        total_kg_beras_disalurkan = sum(mustahiq.kilogram_beras_dari_zakat_fitrah for mustahiq in mustahiqs)
        total_liter_beras_disalurkan = sum(mustahiq.liter_beras_dari_zakat_fitrah for mustahiq in mustahiqs)

        return {
            'total_muzakki': total_muzakki,
            'total_mustahiq': total_mustahiq,
            'total_kg_beras': round(total_kg_beras) if round(total_kg_beras) == total_kg_beras else total_kg_beras,
            'total_liter_beras': round(total_liter_beras) if round(total_liter_beras) == total_liter_beras else total_liter_beras,
            'total_kg_beras_disetor': round(total_kg_beras_disetor) if round(total_kg_beras_disetor) == total_kg_beras_disetor else total_kg_beras_disetor,
            'total_liter_beras_disetor': round(total_liter_beras_disetor) if round(total_liter_beras_disetor) == total_liter_beras_disetor else total_liter_beras_disetor,
            'total_kg_beras_disalurkan': round(total_kg_beras_disalurkan) if round(total_kg_beras_disalurkan) == total_kg_beras_disalurkan else total_kg_beras_disalurkan,
            'total_liter_beras_disalurkan': round(total_liter_beras_disalurkan) if round(total_liter_beras_disalurkan) == total_liter_beras_disalurkan else total_liter_beras_disalurkan,
        }