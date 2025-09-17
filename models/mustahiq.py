from odoo import models, fields # pyright: ignore[reportMissingImports, reportAttributeAccessIssue] (ignore any import warnings here)

class Mustahiq(models.Model):
    print('\nSUCCESS: Mustahiq model loaded\n')
    _name = 'zf.mustahiq'
    _description = 'Penerima'
    _rec_name = 'nama'

    nama = fields.Char(required=True)
    kilogram_beras_dari_zakat_fitrah = fields.Float()
    liter_beras_dari_zakat_fitrah = fields.Float()
    kilogram_beras_dari_fidyah = fields.Float()
    liter_beras_dari_fidyah = fields.Float()