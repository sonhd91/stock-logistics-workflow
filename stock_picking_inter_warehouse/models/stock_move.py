from odoo import fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    inter_warehouse_picking_id = fields.Many2one(
        "stock.picking",
        "Inter-Warehouse Picking",
    )

    def _search_picking_for_assignation(self):
        # We do not want to merge pickings made in a transfer
        # between warehouses
        res = super()._search_picking_for_assignation()
        if res and any(
            self.move_orig_ids.mapped("picking_type_id").mapped(
                "disable_merge_picking_moves"
            )
        ):
            domain = self._search_picking_for_assignation_domain()
            picking = (
                self.env["stock.picking"]
                .search(domain)
                .filtered(
                    lambda x: x.move_lines.inter_warehouse_picking_id
                    == self.inter_warehouse_picking_id
                )
            )
            return picking or False
        return res
