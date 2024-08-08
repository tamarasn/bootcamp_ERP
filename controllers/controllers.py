from odoo import http
from odoo.http import request
import base64
import json
import requests
import csv
import io


class TrainingController(http.Controller):

    # download data csv
    @http.route('/download/data', type='http', auth='public', methods=['GET'], csrf=False)
    def download_data(self, **kwargs):
        records = request.env['training.course'].search([])
        output = io.StringIO()
        writer = csv.writer(output)
        
        writer.writerow(['Name', 'Description'])
        for record in records:
            writer.writerow([record.name, record.description])
        
        output.seek(0)
        data = output.read()
        output.close()
        return request.make_response(
            data,
            headers = [
                ('Content-Type', 'text/csv'),
                ('Content-Disposition', 'attachment; filename="data_training_course.csv"')
            ]
        )
    
    # get list data
    @http.route('/api/training/course/list', type='http', auth='public')
    def training_course_list(self, **kw):
        try:
            course = request.env['training.course'].search([])
        except:
            return "<h3>Can't Access Training Course List</h3>"
        
        json_data = []
        for dt in course:
            json_record = {
                'name': dt.name,
                'description': dt.description
            }
            json_data.append(json_record)
        return json.dumps(json_data)
    
    # controller api create data
    @http.route('/api/training/course/create', type='http', auth='public', methods=['POST'], csrf=False)
    def training_course_create(self, **kw):
        try:
            data = json.loads(request.httprequest.data)
            name = data.get('name')
            description = data.get('description')
            Record = request.env['training.course']
            new_record = Record.create({
                'name': name,
                'description': description,
            })
            return json.dumps({'message': 'Success Create', 'id': new_record.id})
        except Exception as e:
            return json.dumps({'message': 'Failed Create', 'error': str(e)})
    
    # controller api update data
    @http.route('/api/training/course/update', type='http', auth='public', methods=['POST'], csrf=False)
    def training_course_update(self, **kw):
        try:
            data = json.loads(request.httprequest.data)
            id = data.get('id')
            name = data.get('name')
            description = data.get('description')
            Record = request.env['training.course'].search([('id', '=', id)])
            if Record:
                Record.write({
                    'name': name,
                    'description': description,
                })
                return json.dumps({'message': 'Success Update'})
            else:
                return json.dumps({'message': 'Failed Update'})
        except Exception as e:
            return json.dumps({'message': False, 'error': str(e)})
    
    # controller api delete data
    @http.route('/api/training/course/delete', type='http', auth='public', methods=['POST'], csrf=False)
    def training_course_delete(self, **kw):
        try:
            data = json.loads(request.httprequest.data)
            id = data.get('id')
            Record = request.env['training.course'].search([('id', '=', id)])
            if Record:
                Record.unlink()
                return json.dumps({'message': 'Success Delete'})
            else:
                return json.dumps({'message': 'Failed Delete'})
        except Exception as e:
            return json.dumps({'message': False, 'error': str(e)})