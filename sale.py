# -*- encoding: utf-8 -*-
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time

from osv import fields, osv
from tools.translate import _
import decimal_precision as dp
import netsvc


class stock_location_qty(osv.osv_memory):
    _name='stock.location.qty'
    _columns={
              'sale_order_line':fields.many2one('sale.order.line', 'Order Reference line', required=False, ondelete='cascade', select=True, readonly=True),
              'location_id':fields.many2one('stock.location', 'Magazzino', required=True),
              'real_stock': fields.float(string='Giac.Reale A Dt Ordine'),
              'virtual_stock': fields.float(string='Giac.Virtuale A Dt Ordine'),
              }
    
    def _read_flat(self,cr, user, ids2,fields_to_read,context=None, load='_classic_write'):
    # def   _read_flat(self,cr, user, ids2, [self._fields_id], context=context, load='_classic_write'):
        res=[]
        return res
    
stock_location_qty()


class sale_order_line(osv.osv):
    _inherit = 'sale.order.line'
    #Do not touch _name it must be same as _inherit
    #_name = 'sale.order.line'' cr
    _columns = {
            #'real_stock': fields.float(string='Giac.Reale A Dt Ordine'),
            #'virtual_stock': fields.float(string='Giac.Virtuale A Dt Ordine'),
            'location_qtys':fields.one2many('stock.location.qty', 'sale_order_line', 'Order Lines', readonly=True, require=False),           
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
            #product_obj = self.pool.get('product.product')
            #giac_reale = product_obj.browse(cr, uid, product).qty_available
            #giac_virt = product_obj.browse(cr, uid, product).virtual_available
            #value['real_stock'] = giac_reale
            #value['virtual_stock'] = giac_virt
            context={'product_id':product}            
            ids_location = self.pool.get('stock.location').search(cr,uid,[('usage', '=', 'internal')])
            if ids_location:
                elenco_location=[]
                for stock_l in self.pool.get('stock.location').browse(cr,uid,ids_location,context):
                    #import pdb;pdb.set_trace()
                    elenco_location.append({'location_id':stock_l.id,'real_stock':stock_l.stock_real,'virtual_stock':stock_l.stock_virtual})
                value['location_qtys'] = elenco_location

        return {'value': value, 'domain': domain, 'warning': warning} 
    
sale_order_line()


class FiscalDocRighe(osv.osv):
   _inherit = "fiscaldoc.righe"

   _columns = {
            #'real_stock': fields.float(string='Giac.Reale A Dt Ordine'),
            #'virtual_stock': fields.float(string='Giac.Virtuale A Dt Ordine'),
            'location_qtys':fields.one2many('stock.location.qty', 'sale_order_line', 'Order Lines', readonly=True, require=False),           
             }
   def onchange_articolo(self, cr, uid, ids, product_id, listino_id, qty, partner_id, data_doc, uom,context):
                res = super(FiscalDocRighe, self).onchange_articolo(cr, uid, ids, product_id, listino_id, qty, partner_id, data_doc, uom,context)
                v = res.get('value', False)
                warning = res.get('warning', False)
                domain = res.get('domain', False)
                if product_id:
                    context={'product_id':product_id}            
                    ids_location = self.pool.get('stock.location').search(cr,uid,[('usage', '=', 'internal')])
                    if ids_location:
                        elenco_location=[]
                        for stock_l in self.pool.get('stock.location').browse(cr,uid,ids_location,context):
                            #import pdb;pdb.set_trace()
                            elenco_location.append({'location_id':stock_l.id,'real_stock':stock_l.stock_real,'virtual_stock':stock_l.stock_virtual})
                        v['location_qtys'] = elenco_location
                return {'value': v, 'domain': domain, 'warning': warning}
   

FiscalDocRighe()

