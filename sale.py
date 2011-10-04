# -*- encoding: utf-8 -*-
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time

from osv import fields, osv
from tools.translate import _
import decimal_precision as dp
import netsvc


class sale_order_line(osv.osv):
    _inherit = 'sale.order.line'
    #Do not touch _name it must be same as _inherit
    #_name = 'sale.order.line'' cr
    _columns = {
            'real_stock': fields.float(string='Giac.Reale A Dt Ordine'),
            'virtual_stock': fields.float(string='Giac.Virtuale A Dt Ordine'),
            
                    }
    
    def product_id_change(self, cr, uid, ids, pricelist, product, qty=0,
            uom=False, qty_uos=0, uos=False, name='', partner_id=False,
            lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False, flag=False):
        #import pdb;pdb.set_trace()
        res = super(sale_order_line, self).product_id_change(cr, uid, ids, pricelist, product, qty,
            uom, qty_uos, uos, name, partner_id,
            lang, update_tax, date_order, packaging, fiscal_position, flag)
         
        value = res['value']
        domain = res['domain']
        warning = res.get('warning', False)
        if product:
       
            product_obj = self.pool.get('product.product')
            giac_reale = product_obj.browse(cr, uid, product).qty_available
            giac_virt = product_obj.browse(cr, uid, product).virtual_available
            value['real_stock'] = giac_reale
            value['virtual_stock'] = giac_virt

        return {'value': value, 'domain': domain, 'warning': warning} 
    
sale_order_line()
