from odoo import models, fields # pyright: ignore[reportMissingImports, reportAttributeAccessIssue] (ignore any import warnings here)
from ..helpers.get_odoo_module_path import get_odoo_module_path
from ..helpers.simple_log import simple_log as print

ODOO_MODULE_PATH = get_odoo_module_path(__file__)
ODOO_MODULE_NAME = ODOO_MODULE_PATH.parts[-1]

class Muzakki(models.Model):
    print('Muzakki model loaded')
    _name = 'zf.muzakki'
    _description = 'Pembayar'
    _rec_name = 'nama'

    nama = fields.Char(required=True)
    petugas_id = fields.Many2one('zf.petugas', required=True)
    jumlah_jiwa_zakat_fitrah = fields.Integer()
    zakat_fitrah_kilogram_beras = fields.Float() # Total seluruhnya atau sebagian yang dalam kg, bukan perjiwa
    zakat_fitrah_liter_beras = fields.Float() # Total seluruhnya atau sebagian yang dalam liter, bukan perjiwa
    fidyah_kilogram_beras = fields.Float()
    fidyah_liter_beras = fields.Float()