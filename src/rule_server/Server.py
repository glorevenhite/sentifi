import SocketServer
import simplejson
from Ruler import Ruler
from Constant import *


class RuleTCPServer(SocketServer.ThreadingTCPServer):
    allow_reuse_address = True


class RuleTCPServerHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        try:
            data = simplejson.loads(self.request.recv(10000).strip(), encoding="utf-8")
            print "DATA RECEIVED:", data
            type = data['type']
            returned_data = ""
            if type == 'categories_name':
                phase = data['phase']
                returned_data = Ruler().get_list_category_ids_by_phase(phase)
                print "DATA SENT:", returned_data

            elif type == 'classes':
                phase = data['phase']
                parent_class = data['parent_class']
                returned_data = Ruler().get_classes_by_phase_name(phase, parent_class)
                print returned_data
                print "DATA SENT:", returned_data

            elif type == 'rules':
                cat_id = data['category_id']
                field_id = data['field_id']
                returned_data = Ruler().get_list_rules_by_category_id(cat_id, field_id)
            elif type == 'keywords':
                rule_id = data['rule_id']
                returned_data = Ruler().get_rules(rule_id)

            elif type == 'ruleset':
                phase = data['phase']
                field_id = data['field_id']
                returned_data = Ruler().get_ruleset_in_json2(phase, field_id)

            elif type == 'parent':
                category_name = data['category_name']
                returned_data = Ruler().get_parent_phase(category_name)
                print "DATA SENT:", returned_data

            elif type == 'subset':
                phase = data['phase']
                field_id = data['field_id']
                if ['parent_id'] not in data.keys():
                    returned_data = Ruler().get_rule_subset_by_phase_and_field(phase, field_id)    # IMPORTANT
                else:
                    parent_id = data['parent_id']
                    returned_data = Ruler().get_rule_subset_by_phase_field_parent(phase, field_id, parent_id)    # IMPORTANT

            returned_message = {}
            if returned_data != {}:
                returned_message.update({'status': SERVER_STATUS_OK})
                returned_message.update({'data': returned_data})
            else:
                returned_message.update({'status': SERVER_STATUS_ERROR})
                returned_message.update({'code': '0'})

            #print returned_message
            self.request.sendall(simplejson.dumps(returned_message, encoding='utf-8'))

        except Exception, e:
            print "Exception while sending message:", e
            returned_message = {}
            returned_message.update({'status': SERVER_STATUS_ERROR})
            returned_message.update({'code': '0'})
            self.request.sendall(simplejson.dumps(returned_message, encoding="utf-8"))

server = RuleTCPServer(('127.0.0.1', 13373), RuleTCPServerHandler)
server.serve_forever()
