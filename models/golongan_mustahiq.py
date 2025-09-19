from odoo import models, fields # pyright: ignore[reportMissingImports, reportAttributeAccessIssue] (ignore any import warnings here)
from ..helpers.get_odoo_module_path import get_odoo_module_path
from ..helpers.simple_log import simple_log as print

ODOO_MODULE_PATH = get_odoo_module_path(__file__)
ODOO_MODULE_NAME = ODOO_MODULE_PATH.parts[-1]

class GolonganMustahiq(models.Model):
    print('GolonganMustahiq model loaded')
    _name = 'zf.mustahiq.golongan'
    _description = 'Golongan penerima'
    _rec_name = 'nama'

    nama = fields.Char(required=True)