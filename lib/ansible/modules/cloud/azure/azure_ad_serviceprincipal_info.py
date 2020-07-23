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

from ansible.module_utils.azure_rm_common_ext import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from azure.graphrbac.models import GraphErrorException
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMServicePrincipalInfo(AzureRMModuleBase):
    def __init__(self):

        self.module_arg_spec = dict(
            app_id=dict(type='str'),
            object_id=dict(type='str'),
            tenant=dict(type='str', required=True),
        )

        self.tenant = None
        self.app_id = None
        self.object_id = None
        self.results = dict(changed=False)

        super(AzureRMServicePrincipalInfo, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                          supports_check_mode=False,
                                                          supports_tags=False,
                                                          is_ad_resource=True)
                                            
    def exec_module(self, **kwargs):

        for key in list(self.module_arg_spec.keys()):
            setattr(self, key, kwargs[key])

        service_principals = []

        try:
            client = self.get_graphrbac_client(self.tenant)
            if self.object_id is None:
                service_principals = list(client.service_principals.list(filter="servicePrincipalNames/any(c:c eq '{}')".format(self.app_id)))
            else:
                service_principals = [client.service_principals.get(self.object_id)]

            self.results['service_principals'] = [self.to_dict(sp) for sp in service_principals]
        except GraphErrorException as ge:
            self.fail("failed to get service principal info {0}".format(str(ge)))

        return  self.results

    def to_dict(self, object):
        return dict(
            app_id = object.app_id,
            object_id = object.object_id,
            app_display_name = object.display_name,
            app_role_assignment_required= object.app_role_assignment_required
        )


def main():
    AzureRMServicePrincipalInfo()

if __name__ == '__main__':
    main()