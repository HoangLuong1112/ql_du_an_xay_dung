from odoo import models, fields, api 
from odoo.exceptions import ValidationError
class Risk(models.Model):
    _name = "cpm_odoo.risk_mgmt_issue"
    _description = "Model"
    
    title = fields.Char(
        string = 'Title',
        required=True,
        size = 256
    )
    
    description = fields.Text(
        string = 'Description'
    )
    
    category_id = fields.Many2one(
        comodel_name = 'cpm_odoo.risk_mgmt_issue_category', 
        string='Category',
        required=True
    )
    
class RiskCategory(models.Model):
    _name = "cpm_odoo.risk_mgmt_issue_category"
    _description = "Model"
    
    name = fields.Char(
        string = 'name',
        size=128,
        required=True
    )


class Issue(models.Model):
    _name = "cpm_odoo.risk_mgmt_issue"
    _description = "Model"
    
    title = fields.Char(
        string = 'Title',
        required=True,
        size = 256
    )
    
    description = fields.Text(
        string = 'Description'
    )
    
    category_id = fields.Many2one(
        comodel_name = 'cpm_odoo.risk_mgmt_issue_category', 
        string='Category',
        required=True
    )

    level = fields.Selection(
        [
            ("minor", "Minor"),
            ("moderate", "Moderate"),
            ("major", "Major"),
            ("critical", "Critical")
        ],
        string = "Level",
        store = True
    )
    
    status = fields.Selection(
        [
            ("not_resolved", "Not Resolved"),
            ("in_progress", "In Progress"),
            ("resolved", "Resolved")
        ],
        string = "Status",
        store = True,
        default = "not_resolved"
    )

    created_at = fields.Datetime(
        string='Created At',
        store=True,
        default=fields.Datetime.now
    )

    staff_id = fields.Many2one(
        comodel_name ='cpm_odoo.human_res_staff', 
        string='Staff',
        default=lambda self: self._default_staff_id(),
    )

    @api.model
    def _default_staff_id(self):
        current_user = self.env.user

        staff = self.env['cpm_odoo.human_res_staff'].sudo().search([
            ('user_id', '=', current_user.id)
        ], limit=1)

        return staff.id if staff else False
    
    def action_view(self):
        self.ensure_one()
        
        view_id = self.env.ref("cpm_odoo.issue_select_view_form").id

        return {
            'type': 'ir.actions.act_window',
            'name': 'Issue',
            'res_model': 'cpm_odoo.risk_mgmt_issue',
            'view_mode': 'form',
            'view_id': view_id,
            'target': 'current',
            'res_id': self.id
        }

    def action_in_progress(self):
        for record in self:
            record.status = "in_progress"

    def action_resolved(self):
        for record in self:
            record.status = "resolved"

    def unlink(self):
        if self.status != "not_resolved":
            raise ValidationError("You cannot delete issue with resolved or in progress status")
        return super(Issue, self).unlink()
    
    def write(self, vals):
        for record in self:
            if record.status != 'not_resolved':
                raise ValidationError("You cannot edit issue with resolved or in progress status.")
        return super().write(vals)


class IssueCategory(models.Model):
    _name = "cpm_odoo.risk_mgmt_issue_category"
    _description = "Model"
    
    name = fields.Char(
        string = 'name',
        size=128,
        required=True
    )