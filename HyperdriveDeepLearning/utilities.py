from azureml.core.authentication import ServicePrincipalAuthentication, AzureCliAuthentication, InteractiveLoginAuthentication, AuthenticationException

import os
from dotenv import set_key, get_key
import logging
import urllib
from zipfile import ZipFile


def get_auth(env_path):
    logger = logging.getLogger(__name__)
    if os.environ.get("AML_SP_PASSWORD", None):
        logger.debug("Trying to create Workspace with Service Principal")
        aml_sp_password = os.environ.get("AML_SP_PASSWORD")
        aml_sp_tennant_id = os.environ.get("AML_SP_TENNANT_ID")
        aml_sp_username = os.environ.get("AML_SP_USERNAME")
        auth = ServicePrincipalAuthentication(
            tenant_id=aml_sp_tennant_id,
            username=aml_sp_username,
            password=aml_sp_password
        )
    else:
        logger.debug("Trying to create Workspace with CLI Authentication")
        try:
            auth = AzureCliAuthentication()
            auth.get_authentication_header()
        except AuthenticationException:
            logger.debug("Trying to create Workspace with Interactive login")
            auth = InteractiveLoginAuthentication()
    return auth


def download_data(data_file, download_url):
    urllib.request.urlretrieve(download_url, filename=data_file)
    # extract files
    with ZipFile(data_file, 'r') as zip:
        print('Extracting files...')
        zip.extractall('scripts')
        print('Finished extracting.')
        data_dir = zip.namelist()
    # delete zip file
    os.remove(data_file)
    return