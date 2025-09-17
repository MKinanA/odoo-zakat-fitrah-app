from odoo import models, fields # pyright: ignore[reportMissingImports, reportAttributeAccessIssue] (ignore any import warnings here)
from ..helpers.get_odoo_module_path import get_odoo_module_path

ODOO_MODULE_PATH = get_odoo_module_path(__file__)
ODOO_MODULE_NAME = ODOO_MODULE_PATH.parts[-1]

class Mustahiq(models.Model):
    print(f'\n{ODOO_MODULE_NAME}: [SUCCESS] Mustahiq model loaded\n')
    _name = 'zf.mustahiq'
    _description = 'Penerima'
    _rec_name = 'nama'

    nama = fields.Char(required=True)
    kilogram_beras_dari_zakat_fitrah = fields.Float()
    liter_beras_dari_zakat_fitrah = fields.Float()
    kilogram_beras_dari_fidyah = fields.Float()
    liter_beras_dari_fidyah = fields.Float()