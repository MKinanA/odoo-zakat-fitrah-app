from odoo import http # pyright: ignore[reportMissingImports, reportAttributeAccessIssue] (ignore any import warnings here)
from json import dumps as json
from mimetypes import guess_type as guess_mimetype
from pathlib import Path
from ..helpers.get_odoo_module_path import get_odoo_module_path
from ..helpers.raise_exception import raise_exception
from ..helpers.key_error_safe_dict import KeyErrorSafeDict
from ..helpers.simple_log import simple_log as print

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
    print('ZakatFitrahController controller loaded')

    # Regular routes
    @http.route(ROUTE_PREFIX)
    def root(self, **kw) -> str:
        return open(STATIC_PATH/'dashboard.html').read().format_map(KeyErrorSafeDict({
            **self._recap(),
            'judul': 'Rekap',
            'static_route': STATIC_ROUTE_PREFIX,
        }, to_return_on_missing_key=lambda key: f'{{{key}}}'))

    # API routes
    @http.route(f'{API_ROUTE_PREFIX}/recap')
    def recap(self, **kw) -> str: return json(self._recap())

    # Static resources route
    @http.route(f'{STATIC_ROUTE_PREFIX}/<path:subpath>')
    def static(self, subpath: str, **kw) -> str: return (
        raise_exception(HTTP_ACCESS_DENIED) if not str((STATIC_PATH/subpath).resolve()).startswith(str(STATIC_PATH))
        else (lambda path: http.Response(self._open_and_format_file_if_text(path), content_type=guess_mimetype(path)[0] or 'application/octet-stream'))(
            STATIC_PATH/subpath/'index.html' if (STATIC_PATH/subpath).is_dir() and (STATIC_PATH/subpath/'index.html').is_file()
            else STATIC_PATH/subpath if (STATIC_PATH/subpath).is_file()
            else raise_exception(HTTP_NOT_FOUND)
        )
    )

    # Non-route functions
    @staticmethod
    def _recap() -> dict:
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
            'total_kg_beras': round(total_kg_beras) if round(total_kg_beras) == total_kg_beras else round(total_kg_beras, 2),
            'total_liter_beras': round(total_liter_beras) if round(total_liter_beras) == total_liter_beras else round(total_liter_beras, 2),
            'total_kg_beras_disetor': round(total_kg_beras_disetor) if round(total_kg_beras_disetor) == total_kg_beras_disetor else round(total_kg_beras_disetor, 2),
            'total_liter_beras_disetor': round(total_liter_beras_disetor) if round(total_liter_beras_disetor) == total_liter_beras_disetor else round(total_liter_beras_disetor, 2),
            'total_kg_beras_disalurkan': round(total_kg_beras_disalurkan) if round(total_kg_beras_disalurkan) == total_kg_beras_disalurkan else round(total_kg_beras_disalurkan, 2),
            'total_liter_beras_disalurkan': round(total_liter_beras_disalurkan) if round(total_liter_beras_disalurkan) == total_liter_beras_disalurkan else round(total_liter_beras_disalurkan, 2),
            'persentase_progres_penyaluran': f'{round(((((total_kg_beras_disalurkan / total_kg_beras_disetor) if total_kg_beras_disalurkan != 0 else 0) * 100) + (((total_liter_beras_disalurkan / total_liter_beras_disetor) if total_liter_beras_disalurkan != 0 else 0) * 100)) / 2)}%',
        }

    @staticmethod
    def _open_and_format_file_if_text(path: Path | str):
        try: return open(path, 'rt').read().format_map(KeyErrorSafeDict(get_safe_globals(globals()), to_return_on_missing_key=lambda key: key)) if 'noformat' not in Path(path).parts[-1] else open(path, 'rt').read()
        except UnicodeDecodeError: return open(path, 'rb').read()