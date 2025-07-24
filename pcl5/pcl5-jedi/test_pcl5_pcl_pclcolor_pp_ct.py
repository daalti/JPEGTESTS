import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using pp_ct.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:720
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:pp_ct.obj=d2740a6eaf3e4d7957dcf95f4046682865eb021ec99f5273cae73b63d769c395
    +test_classification:System
    +name: test_pcl5_pcl_pclcolor_pp_ct
    +test:
        +title: test_pcl5_pcl_pclcolor_pp_ct
        +guid:a3a2d89a-f814-4a7f-b129-436d46ddf93a
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_pclcolor_pp_ct(setup_teardown, printjob, outputsaver):
    printjob.print_verify('d2740a6eaf3e4d7957dcf95f4046682865eb021ec99f5273cae73b63d769c395', timeout=600)
    outputsaver.save_output()
