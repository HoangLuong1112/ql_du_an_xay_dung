from odoo import models, fields, api 
from odoo.exceptions import ValidationError

class Risk(models.Model):
    _name = "cpm_odoo.risk_mgmt"
    _description = "Model"
    
    name = fields.Char(
        string = 'Name',
        required=True,
        size = 256
    )
    
    description = fields.Text(
        string = 'Description'
    )
    
    category_id = fields.Many2one(
        comodel_name = 'cpm_odoo.risk_mgmt_category', 
        string='Category',
        required=True
    )

    priority = fields.Selection(
        [
            ("0", "Normal"),
            ("1", "Low"),
            ("2", "Medium"),
            ("3", "High")
        ],
        string = "Priority",
        store = True
    )
    
    project_id = fields.Many2one(
        comodel_name = "cpm_odoo.root_project",
        string = "Project",
        required = True
    )

    def action_view_solutions(self):
        self.ensure_one()
        
        view_id = self.env.ref("cpm_odoo.risk_mgmt_solution_create_form").id

        return {
            'type': 'ir.actions.act_window',
            'name': 'Solutions',
            'res_model': 'cpm_odoo.risk_mgmt_solution',
            'view_mode': 'tree,form',
            'views': [
                [False, 'tree'],
                [view_id, 'form'],
            ],
            'domain': [('risk_id', '=', self.id)],
            'context': {
                'default_risk_id': self.id 
            },
            'target': 'current',
        }

    
class RiskCategory(models.Model):
    _name = "cpm_odoo.risk_mgmt_category"
    _description = "Model"
    
    name = fields.Char(
        string = 'name',
        size=128,
        required=True
    )
    
class Solution(models.Model):
    _name = "cpm_odoo.risk_mgmt_solution"
    _description = "Model"

    name = fields.Char(
        string = 'Name',
        size = 128,
        required = True
    )

    description = fields.Text(
        string = "Description"
    )

    risk_id = fields.Many2one(
        comodel_name = "cpm_odoo.risk_mgmt",
        string = "Risk",
        required = True
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

    is_editable = fields.Boolean(
        compute="_compute_is_editable", string="Is Editable", store=False)

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
            if record.status != 'not_resolved' and self.env.user.has_group('cpm_gr.user_issues'):
                raise ValidationError("You cannot edit issue with resolved or in progress status.")
        return super().write(vals)
    
    @api.depends('status')
    def _compute_is_editable(self):
        for record in self:
            record.is_editable = self.env.user.has_group('cpm_gr.user_issues')


class IssueCategory(models.Model):
    _name = "cpm_odoo.risk_mgmt_issue_category"
    _description = "Model"
    
    name = fields.Char(
        string = 'name',
        size=128,
        required=True
    )
