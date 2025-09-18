from odoo import http # pyright: ignore[reportMissingImports, reportAttributeAccessIssue] (ignore any import warnings here)
from json import dumps as json
from mimetypes import guess_type as guess_mimetype
from ..helpers.get_odoo_module_path import get_odoo_module_path
from ..helpers.raise_exception import raise_exception

ROUTE_PREFIX = '/zakat-fitrah'
API_ROUTE_PREFIX = f'{ROUTE_PREFIX}/api'
STATIC_FOLDER = 'static'
STATIC_ROUTE_PREFIX = f'{ROUTE_PREFIX}/{STATIC_FOLDER}'
ODOO_MODULE_PATH = get_odoo_module_path(__file__)
ODOO_MODULE_NAME = ODOO_MODULE_PATH.parts[-1]
STATIC_PATH = (ODOO_MODULE_PATH/STATIC_FOLDER).resolve()

HTTP_NOT_FOUND = http.NotFound('Requested resource is not found on the server')
HTTP_ACCESS_DENIED = http.AccessDenied('Access to requested resource denied')

class ZakatFitrahController(http.Controller):
    print(f'\n{ODOO_MODULE_NAME}: [SUCCESS] ZakatFitrahController controller loaded\n')

    # Regular routes
    @http.route(ROUTE_PREFIX)
    def root(self, **kw) -> str:
        return open(STATIC_PATH/'dashboard.html').read().format(**self._summary())

    # API routes
    @http.route(f'{API_ROUTE_PREFIX}/summary')
    def summary(self, **kw) -> str: return json(self._summary())

    # Static resources route
    @http.route(f'{STATIC_ROUTE_PREFIX}/<path:subpath>')
    def static(self, subpath: str, **kw) -> str: return (
        raise_exception(HTTP_ACCESS_DENIED) if not str((STATIC_PATH/subpath).resolve()).startswith(str(STATIC_PATH))
        else (lambda path: http.Response(open(path, 'rb').read(), content_type=guess_mimetype(path)[0] or 'application/octet-stream'))(
            STATIC_PATH/subpath/'index.html' if (STATIC_PATH/subpath).is_dir() and (STATIC_PATH/subpath/'index.html').is_file()
            else STATIC_PATH/subpath if (STATIC_PATH/subpath).is_file()
            else raise_exception(HTTP_NOT_FOUND)
        )
    )

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