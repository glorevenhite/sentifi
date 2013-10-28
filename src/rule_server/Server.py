import SocketServer
import simplejson
from Ruler import Ruler


class RuleTCPServer(SocketServer.ThreadingTCPServer):
    allow_reuse_address = True


class RuleTCPServerHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        try:
            data = simplejson.loads(self.request.recv(1024).strip())
            print "DATA RECEIVED:", data
            type = data['type']

            returned_data = ""
            if type == 'categories_name':
                phase = data['phase']
                returned_data = Ruler().get_list_category_ids_by_phase(phase)
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

            self.request.sendall(simplejson.dumps(returned_data))

        except Exception, e:
            print "Exception while receiving messsage:", e

server = RuleTCPServer(('127.0.0.1', 13373), RuleTCPServerHandler)
server.serve_forever()
