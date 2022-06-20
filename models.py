# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import api, fields, models
from odoo.fields import first


class StockProductionLot(models.Model):
    _inherit = "stock.production.lot"

    def _compute_reservation(self):
        for rec in self:
            query = """
                SELECT id,move_id
                FROM stock_move_line
                WHERE lot_id = %s
                and state not in ('cancel','done')
                LIMIT 1
                """
            self.env.cr.execute(query, (rec.id,))
            result = self.env.cr.dictfetchall()
            if result != [] and result[0].get('move_id'):
                rec.is_reserved = True
                rec.reservation_move = result[0].get('move_id')
            else:
                rec.is_reserved = False
                rec.reservation_move = None

    is_reserved = fields.Boolean('is reserved',compute=_compute_reservation)
    reservation_move = fields.Many2one('stock.move','Reservation move',compute=_compute_reservation)
