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
        self.tenant_id = None
        self.results = dict(changed=False)
        self.state = None
        self.url = None
        self.status_code = [200, 201, 202]
        self.to_do = Actions.NoAction
        self.module_arg_spec=dict()

        super(AzureRMServicePrincipal, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                            supports_check_mode=False,
                                                            supports_tags=False)
                                            
    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        resource_group = self.get_resource_group(self.resource_group)
        if not self.location:
            self.location = resource_group.location

        to_be_update = False
        response = self.get_resource()

        if response:
            if self.state == 'present':
                to_be_update = self.check_update(response)
                if to_be_update:
                    self.action = Actions.CreateOrUpdate
            elif self.state == 'absent':
                # delete
                self.action = Actions.Delete
        else:
            if self.state == 'present':
                self.action = Actions.CreateOrUpdate
            elif self.state == 'absent':
                # delete when no exists
                self.fail("Traffic Manager endpoint {0} not exists.".format(self.name))

        if self.action == Actions.CreateOrUpdate:
            self.results['changed'] = True
            if self.check_mode:
                return self.results

            response = self.create_or_update()
        
        if self.action == Actions.Delete:
            self.results['changed'] = True
            if self.check_mode:
                return self.results
            response = self.delete_traffic_manager_endpoint()

        return self.results

    def create_resource(self):
        try:
            client = self.get_graphrbac_client(self.tenant)
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