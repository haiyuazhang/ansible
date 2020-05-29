#!/usr/bin/python
#
# Copyright (c) 2020 Haiyuan Zhang, <haiyzhan@microsoft.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''

'''

EXAMPLES = '''

'''

RETURN = '''

'''

import time
import json
from ansible.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt
from ansible.module_utils.azure_rm_common_rest import GenericRestClient

try:
    from msrestazure.azure_exceptions import CloudError
except ImportError:
    # This is handled in azure_rm_common
    pass

class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMServicePrincipal(AzureRMModuleBaseExt):
    def __init__(self):

        self.recourse_group = None
        self.results = dict(changed=False)
        self.state = None
        self.url = None
        self.status_code = [200, 201, 202]
        self.to_do = Actions.NoAction
        self.mgmt_client = None

        self.body = {}
        self.query_parameters = {}
        self.query_parameters['api-version'] = '2019-07-01'
        self.head_parameters = {}
        self.header_parameters['Content-Type'] = 'application/json; charset=utf-8'
        self.module_arg_spec=dict()

        super(AzureRMServicePrincipal, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                            supports_check_mode=True,
                                                            supports_tags=False)
                                            
    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()):
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                self.body[key] = kwargs[key]

        self.inflate_paramters(self.module_arg_spec, self.body, 0)

        old_response = None
        response = None

        self.mgmt_client = self.get_mgmt_svc_client(GenericRestClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)
        
        resource_group = self.get_resource_group(self.resource_group)

        if 'location' not in self.body:
            self.body['location'] = resource_group.location

        old_response = self.get_resource()

        if not old_response:
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("Instance already exist")
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.can_update(old_response):
                self.to_do = Actions.Update

        if self.to_do == Actions.NoAction:
            self.results['changed'] = False
            response = old_response
        elif self.to_do == Actions.Delete:
            self.results['changed'] = True
            
            self.delete_resource()
            while self.get_resource():
                    time.sleep(20)
        elif self.to_do == Actions.Create:
            response = self.create_resource()
            self.results['changed'] = True
        else:
            response = self.update_resource()
            self.results['changed'] = True

        return self.results

    def create_resource(self):
        self._gen_body()
        self._gen_url()
    
        try:
            response = self.mgmt_client.query(self.url,
                                              'PUT',
                                              self.query_parameters,
                                              self.header_parameters,
                                              self.body,
                                              self.status_code,
                                              600,
                                              30)
        except CloudError as exc:
            self.log('Error attempting to create the GalleryImage instance.')
            self.fail('Error creating the GalleryImage instance: {0}'.format(str(exc)))

        try:
            response = json.loads(response.text)
        except Exception:
            response = {'text': response.text}

        return response


    def update_resource(self):
        pass

    def delete_resource(self):
        pass

    def get_resource(self):
        found = False
        try:
            response = self.mgmt_client.query(self.url,
                                              'GET',
                                              self.query_parameters,
                                              self.header_parameters,
                                              None,
                                              self.status_code,
                                              600,
                                              30)
            response = json.loads(response.text)
            found = True
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Did not find the instance.')
        if found is True:
            return response

        return False

    def can_update(self, old_response):
        return True

    def _gen_body(self):
        self.inflate_parameters(self.module_arg_spec, self.body, 0)

    def _gen_url(self):
        self.url = ('/subscriptions' +
                    '/{{ subscription_id }}' +
                    '/resourceGroups' +
                    '/{{ resource_group }}' +
                    '/providers' +
                    '/Microsoft.Compute' +
                    '/galleries' +
                    '/{{ gallery_name }}' +
                    '/images' +
                    '/{{ image_name }}')
        self.url = self.url.replace('{{ subscription_id }}', self.subscription_id)
        self.url = self.url.replace('{{ resource_group }}', self.resource_group)
        self.url = self.url.replace('{{ gallery_name }}', self.gallery_name)
        self.url = self.url.replace('{{ image_name }}', self.name)

    def _upsert(self):
        try:
            response = self.mgmt_client.query(self.url,
                                              'PUT',
                                              self.query_parameters,
                                              self.header_parameters,
                                              self.body,
                                              self.status_code,
                                              600,
                                              30)
        except CloudError as exc:
            self.log('Error attempting to create the GalleryImage instance.')
            self.fail('Error creating the GalleryImage instance: {0}'.format(str(exc)))

        try:
            response = json.loads(response.text)
        except Exception:
            response = {'text': response.text}

        return response

def main():
    AzureRMServicePrincipal()

if __name__ == '__main__':
    main()