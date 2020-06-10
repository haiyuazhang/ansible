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

        self.module_arge_spec = dict(

        )

        self.resource_group = None
        self.state = None
        self.tenant_id = None
        self.app_id = None

        self.results = dict(changed=False)
        self.action = Actions.NoAction

        super(AzureRMServicePrincipal, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                      supports_check_mode=False,
                                                      supports_tags=False)
                                            
    def exec_module(self, **kwargs):

        for key in list(self.module_arge_spec.keys()):
            setattr(self, key, kwargs[key])

        resource_group = self.get_resource_group(self.resource_group)

        to_be_update = False
        response = self.get()

        if response:
            if self.state == 'present':
                to_be_update = self.check_update(response)
                if to_be_update:
                    self.action = Actions.CreateOrUpdate
            elif self.state == 'absent':
                self.action = Actions.Delete
        else:
            if self.state == 'present':
                self.action = Actions.CreateOrUpdate
            elif self.state == 'absent':
                # delete when no exists
                self.fail("resource {0} not exists.".format(self.app_id))

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

    def create_or_update(self):
        from azure.graphrbac.models import ServicePrincipalCreateParameters
        try:
            client = self.get_graphrbac_client(self.tenant_id)
            response = client.service_principals.create(ServicePrincipalCreateParameters(app_id=self.app_id, account_enabled=True))

            return response
        except CloudError as ce:
            self.fail("Error creating service principle, app id {0} - {1}".format(self.app_id), str(ce))

    def delete_resource(self):
        try:
            client = self.get_graphrbac_client(self.tenant_id)
            client.applications.delete(self.app_id)
            return True
        except CloudError as ce:
            self.fail("Error deleting service principal app_id {0} - {1}".format(self.app_id, str(ce)))
            return False

    def get_resource(self):
        try:
            client = self.get_graphrbac_client(self.tenant_id)
            result = list(client.list(filter="servicePrincipalNames/any(c:c eq '{}')".format(self.app_id)))
            return result
        except CloudError as e:
            self.log('Did not find the instance.')
            return False


def main():
    AzureRMServicePrincipal()

if __name__ == '__main__':
    main()